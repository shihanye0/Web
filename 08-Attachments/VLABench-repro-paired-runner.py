"""Run ten fixed select_fruit pairs, with a same-condition repeat before comparison."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

import cv2
import mujoco
import numpy as np
from PIL import Image
import torch

from check_assets import main as check_assets
from lerobot.envs.utils import preprocess_observation
from lerobot.policies import make_pre_post_processors
from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.sim.integrations.vlabench import VLABenchEnv
from lerobot.utils.random_utils import set_seed

ROOT = Path(__file__).resolve().parent
SEEDS = list(range(2000, 2010))
COLOR = [40, 65, 110]
THRESHOLD = 0.1
STATE_SPEC = mujoco.mjtState.mjSTATE_INTEGRATION


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def array_hash(value: np.ndarray) -> str:
    return hashlib.sha256(value.tobytes()).hexdigest()


def integration_state(physics) -> np.ndarray:
    state = np.empty(mujoco.mj_stateSize(physics.model.ptr, STATE_SPEC))
    mujoco.mj_getState(physics.model.ptr, physics.data.ptr, state, STATE_SPEC)
    return state


def model_hash(physics) -> str:
    digest = hashlib.sha256()
    for name in sorted(dir(physics.model.ptr)):
        value = getattr(physics.model.ptr, name)
        if isinstance(value, np.ndarray) and name != "tex_data":
            digest.update(f"{name}:{value.dtype}:{value.shape}".encode())
            digest.update(value.tobytes())
    digest.update(str(physics.model.opt).encode())
    return digest.hexdigest()


def set_texture(physics, texture_id: int, pixels: np.ndarray) -> None:
    start = int(physics.model.tex_adr[texture_id])
    physics.model.tex_data[start:start + pixels.size] = pixels
    with physics.contexts.gl.make_current() as context:
        context.call(mujoco.mjr_uploadTexture, physics.model.ptr, physics.contexts.mujoco.ptr, texture_id)


def scores(env) -> dict:
    physics, task = env.physics, env.task
    intention = int(task.get_intention_score(physics, threshold=THRESHOLD, discrete=True))
    progress = float(task.get_task_progress(physics))
    return {
        "official_success": bool(task.should_terminate_episode(physics)),
        "intention_score": intention,
        "progress_score": progress,
        "code_ps_proxy": 0.2 * intention + 0.8 * progress,
        "paper_ps": None,
        "target_ever_grasped": dict(task.target_is_grasped),
        "conditions_met": [bool(c.is_met(physics)) for c in task.conditions.conditions],
        "minimum_distances_m": {
            name: float(d) if np.isfinite(d) else None for name, d in task.intention_distance.items()
        },
    }


def capture(env) -> dict:
    return {
        "state": integration_state(env.physics),
        "reset_next": env._reset_next_step,
        "timestep": env.timestep,
        "episode_step_count": env._hooks._episode_step_count,
        "rng": env._random_state.get_state(),
        "intention": copy.deepcopy(env.task.intention_distance),
        "grasped": copy.deepcopy(env.task.target_is_grasped),
    }


def restore(env, snapshot: dict) -> None:
    # forward rebuilds contacts; reapply integration state to retain solver warm starts.
    mujoco.mj_setState(env.physics.model.ptr, env.physics.data.ptr, snapshot["state"], STATE_SPEC)
    env.physics.forward()
    mujoco.mj_setState(env.physics.model.ptr, env.physics.data.ptr, snapshot["state"], STATE_SPEC)
    env._reset_next_step = snapshot["reset_next"]
    env.timestep = snapshot["timestep"]
    env._hooks._episode_step_count = snapshot["episode_step_count"]
    env._random_state.set_state(snapshot["rng"])
    env.task.intention_distance = copy.deepcopy(snapshot["intention"])
    env.task.target_is_grasped = copy.deepcopy(snapshot["grasped"])
    if not np.array_equal(integration_state(env.physics), snapshot["state"]):
        raise RuntimeError("Full integration state did not restore exactly")


def frame_strip(observation: dict) -> np.ndarray:
    return np.concatenate([observation["pixels"][key] for key in ("image", "second_image", "wrist_image")], axis=1)


def rollout(wrapper, policy, preprocessor, postprocessor, output: Path, policy_seed: int) -> dict:
    output.mkdir()
    set_seed(policy_seed)
    policy.reset()
    preprocessor.reset()
    postprocessor.reset()
    observation = wrapper._get_obs()
    first_frame = frame_strip(observation)
    Image.fromarray(first_frame).save(output / "initial.png")
    video = cv2.VideoWriter(str(output / "front-right-wrist.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 10, (1440, 480))
    if not video.isOpened():
        raise RuntimeError("Cannot open video writer")
    actions, states, observation_states, image_hashes = [], [], [], []
    attempted_action, step = None, 0
    start = time.monotonic()
    try:
        with (output / "steps.jsonl").open("w") as log, torch.inference_mode():
            for step in range(1, 501):
                attempted_action = None
                frame = frame_strip(observation)
                video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                image_hashes.append(array_hash(frame))
                observation_states.append(observation["agent_pos"].copy())
                prepared = preprocess_observation(observation)
                prepared["task"] = [wrapper.task_description]
                action = postprocessor(policy.select_action(preprocessor(prepared)))[0].cpu().numpy()
                if action.shape != (7,) or not np.isfinite(action).all():
                    raise RuntimeError(f"Invalid action at step {step}")
                attempted_action = action.tolist()
                observation, _, terminated, _, info = wrapper.step(action)
                if info.get("physics_error"):
                    raise RuntimeError(f"Physics divergence at step {step}; this is an exception, not a task failure")
                states.append(integration_state(wrapper._env.physics))
                actions.append(action.copy())
                result = scores(wrapper._env)
                log.write(json.dumps({"step": step, **result}, allow_nan=False) + "\n")
                if step % 100 == 0 or terminated:
                    log.flush()
                    print(f"{output.name}: step={step}, success={result['official_success']}", flush=True)
                if terminated:
                    break
        final_frame = frame_strip(observation)
        video.write(cv2.cvtColor(final_frame, cv2.COLOR_RGB2BGR))
        Image.fromarray(final_frame).save(output / "final.png")
        result.update(steps=len(actions), elapsed_s=time.monotonic() - start,
                      policy_seed=policy_seed, final_image_sha256=array_hash(final_frame),
                      initial_image_sha256=array_hash(first_frame), status="completed")
        write_json(output / "result.json", result)
        return result
    except BaseException as exc:
        write_json(output / "error.json", {"status": "exception", "type": type(exc).__name__, "message": str(exc),
                                           "step": step, "attempted_action": attempted_action,
                                           "completed_steps": len(states), "traceback": traceback.format_exc()})
        raise
    finally:
        video.release()
        np.savez_compressed(output / "trajectory.npz", actions=actions, integration_states=states,
                            observation_states=observation_states, image_sha256=image_hashes)


def compare_repeats(first: Path, second: Path) -> dict:
    with np.load(first / "trajectory.npz") as a, np.load(second / "trajectory.npz") as b:
        equality = {key: bool(np.array_equal(a[key], b[key])) for key in a.files}
    first_result = json.loads((first / "result.json").read_text())
    second_result = json.loads((second / "result.json").read_text())
    equality["final_image"] = first_result["final_image_sha256"] == second_result["final_image_sha256"]
    equality["scores"] = (first / "steps.jsonl").read_bytes() == (second / "steps.jsonl").read_bytes()
    return {"passed": all(equality.values()), "bitwise_equal": equality}


def summarize(pairs: list[dict]) -> dict:
    counts = {"both_success": 0, "both_failure": 0, "normal_only": 0, "texture_only": 0}
    for pair in pairs:
        normal, texture = pair["normal"]["official_success"], pair["texture"]["official_success"]
        key = "both_success" if normal and texture else "normal_only" if normal else "texture_only" if texture else "both_failure"
        counts[key] += 1
    normal_successes = counts["both_success"] + counts["normal_only"]
    texture_successes = counts["both_success"] + counts["texture_only"]
    return {"completed_pairs": len(pairs), "pair_categories": counts,
            "normal_successes": normal_successes, "texture_successes": texture_successes,
            "baseline_nearly_all_failed": len(pairs) == 10 and normal_successes <= 1,
            "paper_ps": None, "pairs": pairs}


def run(output: Path) -> None:
    shutil.copy2(__file__, output / "runner.py")
    shutil.copy2(ROOT / "versions.json", output / "versions-before.json")
    write_json(output / "command.json", {"argv": sys.argv, "cwd": str(Path.cwd())})
    if check_assets():
        raise RuntimeError("Asset gate failed")
    versions = json.loads((ROOT / "versions.json").read_text())
    for repo, commit in versions["source_commits"].items():
        head = subprocess.check_output(["git", "-C", str(ROOT / "src" / repo), "rev-parse", "HEAD"], text=True).strip()
        if head != commit:
            raise RuntimeError(f"Unpinned source: {repo}={head}")
        diff = subprocess.check_output(["git", "-C", str(ROOT / "src" / repo), "diff", "HEAD"])
        (output / f"{repo}.patch").write_bytes(diff)
    policy_path = ROOT / "models/smolvla_vlabench"
    if hashlib.file_digest((policy_path / "model.safetensors").open("rb"), "sha256").hexdigest() != versions["policy"]["sha256"]:
        raise RuntimeError("Policy weight hash changed")
    policy = SmolVLAPolicy.from_pretrained(policy_path, strict=True).to("cuda").eval()
    preprocessor, postprocessor = make_pre_post_processors(policy.config, pretrained_path=policy_path)
    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    protocol = {"kind": "local_camera_adapted_paired_exploration", "scene_seeds": SEEDS,
                "policy_seeds": [4000 + i for i in range(10)], "max_steps": 500,
                "n_action_steps": policy.config.n_action_steps, "num_steps": policy.config.num_steps,
                "tf32": True, "use_amp": policy.config.use_amp,
                "camera_ids": [2, 0, 3], "texture": "table/wood", "replacement_rgb": COLOR,
                "intention_threshold_m": THRESHOLD, "paper_ps": None,
                "code_ps_proxy": "0.2 * intention_score + 0.8 * progress_score",
                "success": "fixed official contain/termination condition; no extra holding period",
                "repeat_gate": "all 500 steps or earlier success; bitwise action/state/image/score equality",
                "order": "even pair normal then texture, odd pair texture then normal",
                "low_baseline_gate": "normal successes <= 1/10: diagnose before interpreting texture effects",
                "exceptions": "stop and retain artifacts; never silently resample or count exception as failure",
                "snapshot": "mjSTATE_INTEGRATION, forward, reapply integration state; vector/config persisted",
                "scope": "ten predetermined scene seeds; repeat excluded from paired counts"}
    if (policy.config.n_action_steps, policy.config.num_steps) != (50, 10):
        raise RuntimeError("Checkpoint sampling defaults changed")
    write_json(output / "protocol.json", protocol)
    pairs = []
    for index, seed in enumerate(SEEDS):
        pair_dir = output / f"seed-{seed}"
        pair_dir.mkdir()
        set_seed(seed)
        wrapper = VLABenchEnv()
        wrapper._ENSURE_ENV_MAX_ATTEMPTS = 1
        try:
            wrapper.reset(seed=seed)
            env, physics = wrapper._env, wrapper._env.physics
            # Evaluation hooks maintain metrics without changing actions or physics parameters.
            env.task.run_mode = "eval"
            env.task.reset_intention_distance()
            env.task.reset_task_progress()
            if env.task.task_observables or env._observation_updater._enabled_list:
                raise RuntimeError("Snapshot contract needs review for tasks with temporal observables")
            snapshot = capture(env)
            np.savez_compressed(pair_dir / "initial-state.npz", integration_state=snapshot["state"])
            config = json.loads(json.dumps(env.save(), default=lambda x: np.asarray(x).tolist()))
            write_json(pair_dir / "episode-config.json", config)
            model_before = model_hash(physics)
            texture_id = physics.model.name2id("table/wood", "texture")
            start = int(physics.model.tex_adr[texture_id])
            size = int(physics.model.tex_height[texture_id] * physics.model.tex_width[texture_id] * physics.model.tex_nchannel[texture_id])
            if int(physics.model.tex_nchannel[texture_id]) != 3:
                raise RuntimeError("Expected an RGB table texture")
            original = physics.model.tex_data[start:start + size].copy()
            replacement = np.tile(np.array(COLOR, dtype=np.uint8), size // 3)
            materials = np.flatnonzero(np.any(physics.model.mat_texid == texture_id, axis=1))
            borrowers = [physics.model.id2name(int(i), "geom") for i in np.flatnonzero(np.isin(physics.model.geom_matid, materials))]
            if not borrowers or any(not name or not name.startswith("table/") for name in borrowers):
                raise RuntimeError(f"Texture is shared beyond the table: {borrowers}")
            identity = {"scene_seed": seed, "instruction": wrapper.task_description,
                        "model_arrays_except_texture_sha256": model_before,
                        "initial_state_sha256": array_hash(snapshot["state"]), "texture_geom_borrowers": borrowers,
                        "original_texture_sha256": array_hash(original), "changed_texture_sha256": array_hash(replacement),
                        "run_mode": env.task.run_mode, "start_scores": scores(env),
                        "camera_names": [physics.model.id2name(i, "camera") for i in range(physics.model.ncam)]}
            write_json(pair_dir / "identity.json", identity)
            results = {}
            order = ["normal", "texture"] if index % 2 == 0 else ["texture", "normal"]
            for condition in order:
                set_texture(physics, texture_id, original if condition == "normal" else replacement)
                restore(env, snapshot)
                if model_hash(physics) != model_before:
                    raise RuntimeError("Non-texture model parameters changed")
                print(f"scene={seed}, condition={condition}, instruction={wrapper.task_description}", flush=True)
                results[condition] = rollout(wrapper, policy, preprocessor, postprocessor, pair_dir / condition, 4000 + index)
                if index == 0 and condition == "normal":
                    restore(env, snapshot)
                    rollout(wrapper, policy, preprocessor, postprocessor, pair_dir / "repeat-normal", 4000)
                    repeat = compare_repeats(pair_dir / "normal", pair_dir / "repeat-normal")
                    write_json(output / "repeat-check.json", repeat)
                    if not repeat["passed"]:
                        raise RuntimeError(f"Same-condition repeat failed: {repeat}")
            if results["normal"]["initial_image_sha256"] == results["texture"]["initial_image_sha256"]:
                raise RuntimeError("Texture intervention did not change policy input")
            a = np.asarray(Image.open(pair_dir / "normal/initial.png"))
            b = np.asarray(Image.open(pair_dir / "texture/initial.png"))
            results["initial_changed_pixels"] = int(np.any(a != b, axis=-1).sum())
            set_texture(physics, texture_id, original)
            restore(env, snapshot)
            if array_hash(frame_strip(wrapper._get_obs())) != results["normal"]["initial_image_sha256"]:
                raise RuntimeError("Restoring the original texture failed to restore initial pixels")
            pairs.append({"scene_seed": seed, **results})
            write_json(output / "summary.json", summarize(pairs))
        finally:
            wrapper.close()
    write_json(output / "completion.json", {"status": "completed", "completed_pairs": len(pairs)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    try:
        run(output)
    except BaseException as error:
        write_json(output / "run-error.json", {"type": type(error).__name__, "message": str(error),
                                               "traceback": traceback.format_exc()})
        raise
