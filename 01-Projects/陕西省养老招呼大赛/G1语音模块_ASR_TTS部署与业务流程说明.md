# G1 服药辅助机器人语音模块：ASR/TTS 部署与业务流程说明

更新日期：2026-08-06

## 1. 文档目的

本文记录 G1 服药辅助机器人语音模块在 PC2 上的部署位置、运行环境、ASR/TTS 交互流程、已部署脚本、测试命令和当前实机验证结果。

当前语音模块分为两种验证入口：

1. **TTS 全文案试听**：依次播放完整业务中的 12 段固定播报，用于检查音量、音色、断句和官方 TTS 稳定性。
2. **ASR/TTS 交互预览**：机器人询问姓名，等待用户回答；Qwen ASR 识别后，机器人请求确认，再等待用户回答“是的”；确认成功后继续播放药物说明。

这两个入口都不会写入 SQLite，不会调用 VLA、视觉模块或机器人运动控制。它们只验证语音模块本身。

## 2. PC2 环境

| 项目             | 当前值                                                                               |
| -------------- | --------------------------------------------------------------------------------- |
| PC2 地址         | `192.168.123.164`                                                                 |
| SSH 用户         | `unitree`                                                                         |
| 项目目录           | `/home/unitree/medication_robot`                                                  |
| Conda 环境       | `/home/unitree/miniconda3/envs/qwen_asr_robot`                                    |
| Python         | `3.10.20`                                                                         |
| PyTorch        | `2.7.0+cpu`                                                                       |
| PyTorch 模块路径   | `/home/unitree/miniconda3/envs/qwen_asr_robot/lib/python3.10/site-packages/torch` |
| Qwen ASR 模型    | `/home/unitree/medication_robot/models/Qwen3-ASR-0.6B`                            |
| G1 麦克风组播       | `239.168.123.161:5555`                                                            |
| PC2 麦克风接口 IP   | `192.168.123.164`                                                                 |
| G1 官方 TTS 网络接口 | `eth0`                                                                            |
| 当前音量           | `60`                                                                              |
|                |                                                                                   |

当前 CUDA 不可用，Qwen ASR 使用 CPU。实机已观察到模型加载约 2.6 秒；身份交互完成后会主动释放 Qwen 模型，避免后续与 VLA、视觉模型同时驻留。

### 2.1 比赛时没有外部主机如何启动

语音模块是离线部署。Python、Qwen 模型、业务脚本和宇树 TTS 程序都在 PC2，运行时不需要互联网、训练服务器、SSH tunnel 或外部 HTTP 服务。SSH 只是开发阶段从笔记本启动和查看日志的手段，不是比赛运行依赖。

当前最小可用启动方式是在 PC2 本地终端执行：

```bash
cd /home/unitree/medication_robot && ./start_robot.sh
```

`start_robot.sh` 负责激活独立 Conda 环境、设置离线模式和 CPU 线程数，最后启动 `run_robot.py`。如果只验证已部署的 ASR/TTS 交互预览，在 PC2 本地终端执行：

```bash
cd /home/unitree/medication_robot && timeout 300s /home/unitree/miniconda3/envs/qwen_asr_robot/bin/python -u g1_audio_interactive_preview.py --initial-timeout 12 --max-speech-duration 20 --interface-ip 192.168.123.164 --model-path /home/unitree/medication_robot/models/Qwen3-ASR-0.6B
```

完整 VLA/视觉 adapter 接入并通过实机闭环后，再把同一个 `start_robot.sh` 包装为 `systemd` 服务，实现 PC2 开机自动启动和失败日志留存。当前不启用开机自启，避免半成品流程在 G1 上误播报或误占用资源。

### 2.2 音量由哪个脚本负责

Python 侧唯一 owner 是：

```text
/home/unitree/medication_robot/speech/unitree_speech.py
```

默认值来自：

```python
TTS_VOLUME = int(os.getenv("UNITREE_TTS_VOLUME", "60"))
```

`speak()` 将音量限制在 `0..100`，再作为参数传给 `/home/unitree/medication_robot/bin/g1_speak`。调大音量时优先使用环境变量，不要先改源码：

```bash
cd /home/unitree/medication_robot && UNITREE_TTS_VOLUME=70 ./start_robot.sh
```

只测交互预览时：

```bash
cd /home/unitree/medication_robot && UNITREE_TTS_VOLUME=70 timeout 300s /home/unitree/miniconda3/envs/qwen_asr_robot/bin/python -u g1_audio_interactive_preview.py --initial-timeout 12 --max-speech-duration 20 --interface-ip 192.168.123.164 --model-path /home/unitree/medication_robot/models/Qwen3-ASR-0.6B
```

修改环境变量或 Python 中的默认值都不需要重新编译，只需重启当前 Python 进程。只有修改 `g1_speak` 的 C++ 源码时才需要重新编译并部署二进制。Git 提交与运行生效无关：现场试验可先用环境变量，数值稳定且决定作为比赛默认值后，再由用户明确要求提交。

实机曾出现 `SetVolume返回码：100`，同时 TTS RPC 返回 `0` 并正常播放。因此从 `60` 改为 `70` 后必须以下一次 `GetVolume` 和现场听感共同验证，不能只看 Python 参数判定已生效。

### 2.3 GPU PyTorch 隔离环境

现有 CPU 环境必须保留：

```text
/home/unitree/miniconda3/envs/qwen_asr_robot
```

GPU 尝试只能新建：

```text
/home/unitree/miniconda3/envs/qwen_asr_gpu
```

不允许在 VLA 或视觉环境中安装、卸载或升级 PyTorch，也不允许覆盖 `qwen_asr_robot`。切换生产启动脚本前，GPU 环境必须独立通过：

1. `torch.cuda.is_available() == True`；
2. 能输出 Jetson GPU 名称；
3. 同一短 WAV 在 GPU 环境中识别成功；
4. 记录模型加载、ASR 推理耗时和峰值内存；
5. 一次真实 G1 麦克风 ASR/TTS 交互成功；
6. 失败时能立即回到 `qwen_asr_robot` CPU 启动。

当前已固定的官方兼容性事实：PC2 是 JetPack 5.1.1 / Jetson Linux R35.3.1 / CUDA 11.4；NVIDIA 在 JetPack 5.1.1 目录提供的 GPU PyTorch 2.0 wheel 是 `cp38`，只能用于 Python 3.8；当前 `qwen-asr 0.0.6` 和 `transformers 4.57.6` 都声明需要 Python 3.9 以上。因此不能把官方 `cp38` wheel 强行安装到现有 Python 3.10 环境。

2026-08-06 已对 PC2 完成只读盘点：Conda 中只有 `qwen_asr_robot`、`teleimager` 和 `vla`；后两个环境均未安装 PyTorch；系统 Python 也未安装 PyTorch；本地唯一 wheel 是 CPU 版 `torch-2.7.0-cp310-cp310-manylinux_2_28_aarch64.whl`。未找到可用的 Python 3.9/3.10 Jetson GPU PyTorch 产物。

最终决策是回到已验证的 CPU 基线：未创建 `qwen_asr_gpu`，未安装或卸载任何包，未修改 `qwen_asr_robot`、VLA 或视觉环境。不为当前语音提速升级 JetPack 6，因为这会改变 G1 的 CUDA、驱动和其他模型运行基线。只有将来获得经验证的 JetPack 5.1.1 + Python 3.10 GPU wheel 时，才在新的隔离环境中重新评估。

## 3. 正常语音业务流程

完整语音交互不是连续播放 TTS，而是 ASR 和 TTS 交替工作：

```text
预加载 Qwen ASR
  -> TTS：您好，我是服药辅助机器人
  -> TTS：请说出您的姓名
  -> G1 麦克风录音
  -> Qwen ASR 识别姓名
  -> 姓名不是张建国/张爷爷/老张：TTS 提示失败并停止
  -> TTS：请确认，您是张爷爷吗
  -> G1 麦克风录音
  -> Qwen ASR 识别“是/否”
  -> 否认、未知或超时：TTS 提示失败并停止
  -> 确认成功
  -> 释放 Qwen ASR 模型
  -> TTS 播报身份确认、药物、餐后要求和注意事项
  -> TTS：我现在为您准备药物和水，请稍等
  -> 交给 VLA 模块
```

接入 VLA 和视觉模块后的完整比赛流程为：

```text
ASR/TTS 身份确认与药物说明
  -> 释放 Qwen ASR
  -> VLA 拿药、倒药、递送药盒和水
  -> 释放 VLA
  -> 加载并预热视觉模型
  -> TTS：药盒和水已经送到，请开始服药
  -> TTS 播放结束后开启最长 180 秒视觉窗口
  -> 视觉观察橙色药杯饮用动作
  -> 视觉观察蓝色水杯饮用动作
  -> 释放视觉模型
  -> 视觉证据成功后 SQLite 才写入 completed 和服药记录
  -> TTS 播报最终结果
```

重要边界：VLA 递送成功不等于服药完成。只有视觉模块观察到“橙色药杯后蓝色水杯”的规定动作并返回真实证据，数据库才能完成任务。视觉只证明可观察动作，不证明真实吞咽。

## 4. 已部署脚本

### 4.1 TTS 全文案试听

PC2 路径：

```text
/home/unitree/medication_robot/g1_audio_flow_preview.py
```

用途：连续播放完整业务涉及的 12 段固定 TTS，不启用麦克风和 Qwen ASR。

完整脚本：

```python
#!/usr/bin/env python3

from __future__ import annotations

import json
from typing import Callable

from speech.unitree_speech import speak as unitree_speak


PHRASES = (
    "您好，我是服药辅助机器人。接下来需要核对您的身份。",
    "您好，请说出您的姓名。",
    "请确认，您是张爷爷吗？",
    "好的，张爷爷，身份确认成功。",
    "张爷爷，身份和服药任务已经核对完成。",
    "您本次需要服用测试降压药A一片、测试肠溶药B一片。",
    "请在餐后按照要求服用。",
    "请注意，测试肠溶药B：请整片吞服，不要掰开、压碎或咀嚼。",
    "这是您的餐后测试药物。",
    "我现在为您准备药物和水，请稍等。",
    "您的药盒和水已经送到。请开始服药。完成药杯饮用后，请再饮水。",
    "已经观察到您依次完成药杯和水杯的饮用动作。本次服药信息已经记录。",
)


def run_preview(
    speak: Callable[[str], None] = unitree_speak,
) -> None:
    for text in PHRASES:
        speak(text)


def main() -> int:
    try:
        run_preview()
    except Exception as exc:
        print(
            json.dumps(
                {
                    "kind": "g1_audio_flow_preview",
                    "status": "failed",
                    "message": str(exc),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        return 1

    print(
        json.dumps(
            {
                "kind": "g1_audio_flow_preview",
                "status": "completed",
                "phrase_count": len(PHRASES),
                "database_used": False,
                "vla_used": False,
                "visual_used": False,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

运行命令：

```bash
ssh unitree@192.168.123.164 'cd /home/unitree/medication_robot && timeout 180s /home/unitree/miniconda3/envs/qwen_asr_robot/bin/python -u g1_audio_flow_preview.py'
```

### 4.2 ASR/TTS 真实交互预览

PC2 路径：

```text
/home/unitree/medication_robot/g1_audio_interactive_preview.py
```

用途：执行两轮真实麦克风交互，再播放剩余业务 TTS。成功操作时依次回答：

1. `我是张建国`
2. `是的`

完整脚本：

```python
#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from typing import Callable, Optional, Sequence

from asr.intent import INTENT_CONFIRM, recognize_intent
from g1_audio_flow_preview import PHRASES
from speech.unitree_speech import speak as unitree_speak


KNOWN_IDENTITIES = {
    "张建国",
    "张爷爷",
    "老张",
}


def normalize_identity(text: str) -> str:
    normalized = re.sub(
        r"^(我是|我叫|我的名字是|本人是|姓名是)",
        "",
        str(text).strip(),
    )
    return re.sub(
        r"[\s，。！？、；：,.!?;:]",
        "",
        normalized,
    )


def run_interactive_preview(
    *,
    speak: Callable[[str], None],
    listen: Callable[[], str],
    after_identity_confirmed: Callable[[], None] = lambda: None,
) -> bool:
    speak(PHRASES[0])
    speak(PHRASES[1])

    identity_text = listen()
    if normalize_identity(identity_text) not in KNOWN_IDENTITIES:
        speak(
            "抱歉，我暂时无法确认您的身份。"
            "本次语音流程测试停止。"
        )
        return False

    speak(PHRASES[2])
    confirmation_text = listen()
    if recognize_intent(confirmation_text) != INTENT_CONFIRM:
        speak(
            "身份确认未通过。"
            "本次语音流程测试停止。"
        )
        return False

    after_identity_confirmed()

    for phrase in PHRASES[3:]:
        speak(phrase)
    return True


def parse_arguments(
    argv: Optional[Sequence[str]] = None,
) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="G1 ASR与TTS完整语音业务交互预览",
    )
    parser.add_argument("--initial-timeout", type=float, default=12.0)
    parser.add_argument("--max-speech-duration", type=float, default=20.0)
    parser.add_argument("--interface-ip", default=None)
    parser.add_argument("--model-path", default=None)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    from asr.recognize import get_asr_model, release_asr_model
    from g1_mic_asr_demo import G1MicAsrDemoError, run_once

    arguments = parse_arguments(argv)
    turn = 0

    def listen() -> str:
        nonlocal turn
        turn += 1
        text = run_once(
            initial_timeout=arguments.initial_timeout,
            max_speech_duration=arguments.max_speech_duration,
            interface_ip=arguments.interface_ip,
        )
        print(
            json.dumps(
                {
                    "kind": "g1_audio_interactive_turn",
                    "turn": turn,
                    "text": text,
                    "intent": recognize_intent(text),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        return text

    try:
        get_asr_model(arguments.model_path)
        completed = run_interactive_preview(
            speak=unitree_speak,
            listen=listen,
            after_identity_confirmed=release_asr_model,
        )
    except KeyboardInterrupt:
        result = {
            "kind": "g1_audio_interactive_preview",
            "status": "interrupted",
        }
        exit_code = 130
    except G1MicAsrDemoError as exc:
        result = {
            "kind": "g1_audio_interactive_preview",
            "status": "failed",
            "error_code": str(exc),
        }
        exit_code = 2
    except Exception as exc:
        result = {
            "kind": "g1_audio_interactive_preview",
            "status": "failed",
            "error_code": "runtime_error",
            "message": str(exc),
        }
        exit_code = 1
    else:
        result = {
            "kind": "g1_audio_interactive_preview",
            "status": "completed" if completed else "stopped",
            "turn_count": turn,
            "database_used": False,
            "vla_used": False,
            "visual_used": False,
        }
        exit_code = 0 if completed else 2
    finally:
        release_asr_model()

    print(json.dumps(result, ensure_ascii=False), flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
```

运行命令：

```bash
ssh unitree@192.168.123.164 'cd /home/unitree/medication_robot && timeout 300s /home/unitree/miniconda3/envs/qwen_asr_robot/bin/python -u g1_audio_interactive_preview.py --initial-timeout 12 --max-speech-duration 20 --interface-ip 192.168.123.164 --model-path /home/unitree/medication_robot/models/Qwen3-ASR-0.6B'
```

## 5. 依赖的现有 Owner

两个顶层脚本没有重新实现 G1 音频底层能力，而是复用以下已有模块：

| 模块 | 责任 |
|---|---|
| `speech/unitree_speech.py` | 调用 PC2 上的 `bin/g1_speak`，通过宇树官方 VoiceClient 播放 TTS |
| `g1_mic_asr_demo.py` | 有界录音、临时 WAV 生命周期和单轮 Qwen 识别 |
| `asr/recorder.py` | 接收 G1 麦克风组播 PCM，进行 VAD 和最长时间限制 |
| `asr/recognize.py` | 加载、缓存、推理和释放 Qwen3-ASR-0.6B |
| `asr/intent.py` | 将“是的、不是、重复、帮助”等文本映射为受限意图 |

为控制 PC2 内存，`asr/recognize.py` 增加了以下释放函数：

```python
def release_asr_model() -> None:
    global _asr_model

    if _asr_model is None:
        return

    _asr_model = None
    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    print("Qwen3-ASR模型资源已释放。", flush=True)
```

PC2 原文件备份：

```text
/home/unitree/medication_robot/asr/recognize.py.bak_audio_interactive_20260806
```

## 6. 当前实机验证结果

### 6.1 TTS 全文案试听

- 12 段 TTS 全部执行；
- 每段 `TTS返回码：0`；
- 最终输出 `status=completed`、`phrase_count=12`；
- 实际音量保持为 `60`；
- 未使用数据库、VLA、视觉和运动控制。

### 6.2 ASR/TTS 交互预览

已经实机验证以下链路真实发生：

```text
Qwen 模型加载
  -> TTS 欢迎语
  -> TTS 姓名询问
  -> G1 麦克风录音
  -> Qwen ASR 返回原始文本
  -> 身份门禁判断
  -> TTS 失败提示
  -> 释放 Qwen 模型
```

首次运行时现场存在持续谈话，录音达到 20 秒上限，识别文本不是“我是张建国”，因此身份门禁正确停止。该结果证明 ASR/TTS 接线已生效，但尚未完成安静环境下的两轮成功交互。

下一次测试应在较安静环境进行：听到询问后只说“我是张建国”，随后只说“是的”。

## 7. 结构化输出说明

每次 ASR 结束会输出：

```json
{
  "kind": "g1_audio_interactive_turn",
  "turn": 1,
  "text": "我是张建国。",
  "intent": "unknown"
}
```

姓名轮主要读取 `text`；确认轮要求 `intent=confirm`。

完整成功时输出：

```json
{
  "kind": "g1_audio_interactive_preview",
  "status": "completed",
  "turn_count": 2,
  "database_used": false,
  "vla_used": false,
  "visual_used": false
}
```

身份不匹配、否认或识别未知时输出 `status=stopped`；等待说话超时输出 `speech_timeout`；其他错误输出 `runtime_error`。

## 8. 常见问题

### 8.1 一直录到 20 秒

原因通常是现场持续谈话、扬声器余音或环境噪声一直高于 VAD 静音阈值。先在安静环境复测，不应直接降低或提高阈值。

### 8.2 `speech_timeout`

说明 12 秒内没有检测到有效说话。检查机器人是否已开启可提供麦克风组播的唤醒/交互模式，并确认输入接口仍为 `192.168.123.164`。

### 8.3 TTS 日志出现 `SetVolume返回码：100`

当前实机 `GetVolume` 返回音量 `60`，实际 TTS 播放成功且 `TTS返回码：0`。本阶段不继续修改音量接口，以实际播放结果为准。

### 8.4 ASR 使用 CPU

当前 PyTorch 为 CPU 版本。PC2 只读盘点确认没有兼容的 Python 3.9/3.10 Jetson GPU wheel，而官方 JetPack 5.1.1 wheel 与 Qwen 当前 Python 要求存在 `cp38`/`>=3.9` ABI 冲突。本轮 GPU 升级已取消，保留 CPU 版比赛基线。

## 9. 回滚

删除两个新增预览脚本不会影响原业务：

```bash
rm /home/unitree/medication_robot/g1_audio_flow_preview.py
rm /home/unitree/medication_robot/g1_audio_interactive_preview.py
```

如需恢复原 ASR owner：

```bash
cp /home/unitree/medication_robot/asr/recognize.py.bak_audio_interactive_20260806 /home/unitree/medication_robot/asr/recognize.py
```

执行回滚前应先确认目标路径。本项目当前未修改 SQLite、VLA、视觉模块、机器人动作控制、麦克风模式或 G1 机载配置。

## 10. 当前结论

- 官方 G1 TTS 的完整 12 段播报已经实机通过。
- Qwen ASR 与官方 TTS 已形成真实交替调用链。
- 身份错误和环境干扰会安全停止，不会继续播报药物成功结果。
- 安静环境下的“我是张建国 -> 是的”两轮成功实机交互仍需补测。
- 比赛时不依赖外部主机或互联网；当前可从 PC2 本地执行 `start_robot.sh`，完整闭环后再配置开机自启。
- 音量可用 `UNITREE_TTS_VOLUME` 调整，不需重新编译；修改后需实机核对 `GetVolume` 和听感。
- GPU 升级已回档：PC2 盘点未发现兼容的 `cp39/cp310` Jetson GPU wheel，未创建新环境，未修改任何已有环境。现有 CPU 闭环仍是比赛基线。
- 数据库、VLA 和视觉模块将在完整比赛闭环阶段接入，不属于本次语音预览的完成证据。
