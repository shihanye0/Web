# G1 XR 正式连续性采集脚本说明

> 当前入口：`g1-dex3-care-vla/scripts/g1_official_xr_continuity_qualification_run.sh`  
> 实时控制 owner：官方 `xr_teleoperate/teleop/teleop_hand_and_arm.py`  
> 适用场景：正式采集 XR 遥操训练 source，并验证 Quest 输入短暂不新鲜时的“保持—平滑恢复”行为。  
> 最后按源码核对：2026-08-26

## 先说结论

这个脚本现在是项目使用的**正式 XR 采集入口**。它没有另写一套 G1 控制器：真正的 XR → IK → G1 双臂/Dex3 控制仍由官方 `teleop_hand_and_arm.py` 完成。

项目脚本做的是一层很薄但很关键的封装：把固定的机器人 profile、任务语义、运行环境、版本、原始证据和连续性检查锁定下来。它解决的不是“让机器人换一种控制方式”，而是让一次正式采集能回答：**这次到底用的是哪份官方代码、输入短暂卡顿时实际下发的命令有没有保持、恢复时是否仍受限，以及原始数据在哪里。**

这里的 `continuity` 是“连续性资格检查”，不是“临时实验脚本”的意思。它仍应如实保留资格边界：`analysis.json` 的 `pass` 只说明该次会话的连续性检查通过；训练还要走 EpisodeV2/source/release 校验，实机任务成功仍要靠现场观察，策略部署更是另一条链路。

## 当前粉色药盒倒药命令

```bash
cd /home/user/github-product/g1-dex3-care-vla && bash scripts/g1_official_xr_continuity_qualification_run.sh --confirm-official-xr-continuity-qualification --task-version grasp-pink-medicine-box-and-pour-into-medicine-cup-v1 --task-goal '抓取粉色药盒并把药倒入药杯中' --task-steps 'grasp-pink-medicine-box,pour-medicine-into-medicine-cup'
```

这是一条会启动官方遥操并可能让机器人运动的命令；每次运行前仍应确认现场范围、吊装/限位、相机、机器人模式和监督人员。异常响声、可见跳变、意外运动或失去监督时，立即按终端 `q` 停止，并按现场恢复流程处理。

只想检查环境、**不启动 DDS/controller** 时，可执行：

```bash
cd /home/user/github-product/g1-dex3-care-vla && bash scripts/g1_official_xr_continuity_qualification_run.sh --preflight-only
```

## 实际运行的链路

```text
Quest 手势 / 官方 XR
    -> 官方 IK、官方 G1_23 双臂控制、官方 Dex3 retargeting
    -> 官方 native data.json + JPEG
    -> 项目 trace（动作、writer/after-observation 事实）
    -> 独立 xr-input.jsonl（输入与实际 guard telemetry）
    -> analysis.json（pass / inconclusive / fail）
    -> 后续独立的 EpisodeV2 / release 校验
```

运行 profile 固定为 `G1_23 + dex3 + hand + ego + 30 Hz + --motion + --record + --affinity`，使用官方 Motion Mode。`r` 让 `s` 可分段操作；`s` 开始或保存一个段；`a/f/o` 标记成功、失败、碰倒物体；`q` 正常退出。每个段最多 180 秒。

V3 是经过批准的监督锁存语义：不使用终端 Space deadman，也不会伪造 `deadman_held=true`。这并不是“放松安全”的通用替代品，而是以现场人工持续监督、180 秒段上界、明确 `q` 停止和完整运行证据为前提的已记录取舍。

## 相比官方原始脚本，主要加了什么

官方脚本已经拥有真正的实时控制：参数解析、Quest 输入、IK、手臂/Dex3 写入、相机和 native 录制。项目 wrapper 不替代这些能力，而是在官方入口外增加以下固定边界。

| 项目 wrapper 增加的能力 | 解决的问题 | 官方控制是否被改写 |
| --- | --- | --- |
| 强制显式确认、`task-version/task-goal/task-steps` 必填且 `task-version` 格式校验 | 防止无任务语义、重复/拼错参数或无确认地进入采集 | 否 |
| `--preflight-only` | 在启动 DDS 前检查依赖与导入，排除环境问题 | 否 |
| 同时锁定候选采集 checkout、正式回退 checkout、通用 runner、Televuer、Unitree Python SDK 的 clean 状态和 revision | 防止采集时误加载未审阅修改或错误版本；保留可回退基线 | 否 |
| 固定 `tv` Python、`PYTHONNOUSERSITE=1`、`PYTHONPATH`、`LD_LIBRARY_PATH`，并验证 CUDA、PyTorch、官方依赖、Dex3 和 SDK 的实际加载路径 | 避免 `~/.local`、旧 editable 安装或错误动态库悄悄混入运行 | 否 |
| 把任务文字同时传给官方 native metadata 和 project trace，并用 task version 派生会话目录 | 目录改名不能篡改任务语义；方便后续按任务复核/导出 | 否 |
| 单独保存 `native/`、`trace/`、`xr-input.jsonl`、`analysis.json` | 不把诊断结果混进官方 native source，也不以日志替代原始事实 | 否 |
| `--project-input-continuity` + 独立分析器 | 专门验证输入不新鲜时保持、恢复时限速/限加速度 | 否 |

官方原始 `teleop_hand_and_arm.py` 本身提供通用参数，例如 `--frequency`、`--arm`、`--ee`、`--motion`、`--record` 和 task metadata。当前正式入口只是把本项目验证过的一组参数固定下来，并把“能否作为本次正式采集证据”的检查补齐。

## 连续性检查具体优化了什么

这是当前脚本相对普通官方录制最重要的差量。

1. **输入短暂不新鲜时明确进入 HOLD。** 候选官方实现把输入不新鲜与 arm/Dex3 的实际 guard 状态记录为 sidecar telemetry，而不是只凭主循环猜测。
2. **恢复不是突然跳回目标。** `RECOVERING` 阶段检查实际动作的速度和加速度；arm 与 Dex3 分别使用自己的维度和限制。
3. **用 guard 真正接收命令的时间做判断。** 分析器要求 `guard_monotonic_ns` 不晚于 writer 时间，避免把排队后的日志时间错当实际恢复时刻。
4. **不从稀疏 trace 推导连续性。** trace 的 writer fact 用于 source/完成证据；连续性只以 sidecar 的实际 arm/Dex3 guard telemetry 判断。没有这份 telemetry 时结果必须是 `inconclusive`，不能“看起来没问题”就判通过。
5. **队列丢失是失败，不静默忽略。** 跨进程 telemetry queue drop、append error、writer error、HOLD 期间动作变化或恢复越界都会进入 `fail`。
6. **按采集段独立比较。** 不跨 `s` 的分段边界比较 HOLD，避免把两段独立操作错误判成一次跳变。
7. **现场观察仍是必需证据。** `analysis.json` 还明确要求确认：没有异常关节声、没有可见跳变、操作没有中断、停止/保持行为可接受。

这套检查验证的是“输入卡顿时控制链是否连续”；它没有改变官方 IK、DDS topic、控制频率、增益、关节限位或官方 Motion Mode。

## 相比项目最早期脚本，为什么换成当前入口

项目早期脚本并非错误，而是完成当时不同阶段的任务；它们不应再承担当前实时 XR 正式采集 owner。

| 阶段/脚本 | 当时主要目的 | 关键边界 | 当前变化 |
| --- | --- | --- |
| 早期 raw collection：`scripts/g1_teleop_collection_session.py` | 并行留存 Quest raw、只读机器人/Dex3 状态和前视 RGB | 没有完整动作写入链，因此明确写 `training_eligible=false`、`teleop_action_chain_missing` | 保留为原始采集/审计能力，不再把它当成正式实时控制或训练标签来源 |
| 早期 Quest→G1 bounded smoke：`scripts/g1_quest_g1_bounded_teleop_smoke.py` | 用自研 24D projector 与 C++ runtime 做一次 10 秒、有 deadman 的安全 smoke | 有 arm/hand offset cap、slew、runtime pipe、release/restore 等保护，但属于验证 runtime 的单次 bounded 路线 | 保留为安全回归与异常诊断；不再与官方 XR 争夺实时控制 owner |
| 当前正式入口：`scripts/g1_official_xr_continuity_qualification_run.sh` | 用官方 XR 连续遥操采集正式 source，同时验证输入卡顿下的连续性 | 官方 controller 是唯一实时控制；项目只锁定环境、任务、证据和连续性 gate | 成为当前采集入口；后续训练导出继续由 EpisodeV2/release owner 完成 |

最关键的架构变化不是“项目自己把控制写得更复杂”，而是反过来：**停止用项目自研 smoke 充当日常遥操，回到官方 controller；项目代码只保留最小的事实记录、资格检查、回放和导出边界。**

## 运行结束后看什么

本次会话目录形如：

```text
data/qualifications/official-xr-continuity/<task-version>-continuity-<timestamp>/
├── native/           # 官方 native data.json、JPEG 等原始 source
├── trace/            # project trace：任务、动作关联、writer/after-observation 事实
├── xr-input.jsonl    # Quest 输入和实际 arm/Dex3 guard telemetry
└── analysis.json     # 连续性分析结论
```

`analysis.json` / 终端的 `continuity_qualification_verdict` 这样理解：

| 结果 | 含义 | 接下来怎么做 |
| --- | --- | --- |
| `pass` | 记录到了可判定的 HOLD 与 RECOVERING，且无 queue drop、保持跳变或恢复越界 | 可把本次连续性 evidence 归档；随后仍按 source → EpisodeV2 → release 的独立规则处理训练资格 |
| `inconclusive` | 没有触发/观察到 HOLD 或恢复，或缺少实际 writer telemetry | 不能用作“连续性已验证”；保留 artifact，按需要在受监督条件下补一次代表性验证 |
| `fail` | telemetry queue drop、append/writer error、实际 HOLD 有变化、恢复超限或 writer/trace 事实异常等 | 不升级该 runner 的连续性结论；保留 artifact，按最早失败 owner 排查 |
| `error` | artifact/参数/分析输入本身不完整或不合法 | 先修复记录或环境问题；不能把它解释成机器人控制通过/失败 |

无论哪种结果，`analysis.json` 都不会授权策略直接写 DDS，也不自动说明“粉色药盒已成功倒入药杯”。后两项必须分别由训练 release 校验与现场实机结果证明。

## 没有调整的东西（防止误解）

- 没有新增平行 DDS publisher，也没有替换官方 `teleop_hand_and_arm.py`。
- 没有修改官方 IK、Motion Mode、DDS topic、控制频率、增益或关节限位。
- 没有把 native `data.json`/JPEG 直接当训练数据；它们仍是不可变 source。
- 没有让连续性日志替代 EpisodeV2 的 raw、mapped、sent、writer result、after-observation、RGB 对齐和人工 success 标签。
- 没有把 `pass` 写成任务完成、训练 release 通过或比赛部署通过。

## 源码依据

- 当前 runner：`g1-dex3-care-vla/scripts/g1_official_xr_continuity_qualification_run.sh`
- 连续性分析：`g1-dex3-care-vla/scripts/g1_official_xr_continuity_analyze.py`
- 离线回归：`g1-dex3-care-vla/tests/g1_official_xr_continuity_qualification_test.py`
- 官方实时控制：`xr_teleoperate_input_stall_fix/teleop/teleop_hand_and_arm.py`
- 早期 raw collection：`g1-dex3-care-vla/scripts/g1_teleop_collection_session.py`
- 早期 bounded smoke：`g1-dex3-care-vla/scripts/g1_quest_g1_bounded_teleop_smoke.py`
