---
title: VLABench单任务复现与桌面纹理对照
date: 2026-11-10
type: experiment
status: in-progress
tags: [VLABench, SmolVLA, reproduction, visual-robustness]
---

# VLABench 单任务复现与桌面纹理对照

本地已完成独立环境配置、原始入口运行及相机适配后的单任务诊断，保存了一个满足官方任务判据的成功样本。论文 PS 与当前公开代码存在口径差异：代码的意图分只检查目标水果，缺少论文要求的目标容器选择分项。因此本阶段保留 `paper_ps = null`，分开记录官方成功判据、意图分和步骤进度。10 对桌面纹理实验尚未运行。

本文用于课程汇报中的复现记录与后续实验衔接；论文内容见 [[02-Papers/VLABench - A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks.md|VLABench 论文阅读笔记]]。这里仅将保存了运行收据的结果列为已完成。

## 1. 复现范围与固定环境

目标是先完成 `SmolVLA + select_fruit` 的正常单次运行，再用 10 个初始场景做正常桌面/变化纹理的配对探索。只测试单任务，不训练模型，也不运行完整任务集。

Linux 实验目录为 `/home/user/paper/vlabench-repro`；这些路径属于 Linux 复现环境，不是 Windows 知识库的运行入口。

| 项目 | 实际配置 |
| --- | --- |
| 硬件 | NVIDIA GeForce RTX 4070，显存 12282 MiB；驱动 535.309.01 |
| 环境 | 项目 `.venv`，Python 3.12.13；177 个包的依赖一致性检查通过 |
| 计算与仿真 | PyTorch 2.7.1+cu118，torchvision 0.22.1+cu118；MuJoCo 3.2.2，dm-control 1.0.22；EGL 实际渲染通过 |
| LeRobot | 0.7.1；源码 `81b8c5bfdd5591ec59e512cfc7ac6db8151c70ee` |
| VLABench | `cf588fe60c0c7282174fe979f5913170cfe69017` |
| RRT | `e51d95ee489a225220d6ae2a764c4111f6ba7d85` |
| 策略 | `lerobot/smolvla_vlabench@7ef370813eb35823caa94088b50f5389a51e4c47` |
| 视觉语言基础模型 | `HuggingFaceTB/SmolVLM2-500M-Video-Instruct@7b375e1b73b11138ff12fe22c8f2822d8fe03467` |
| 资产 | `lerobot/vlabench-assets@08d7a4479a55c8fbb89ac0fd6fcf06e53d65b4a4`；单任务清单 6501 个文件，2,581,576,390 bytes；完整性门禁通过 |

官方 Google Drive 下载脚本曾返回下载限制，随后采用 LeRobot CI 指定的 Hugging Face 资产镜像。策略及基础模型均按固定版本下载，SHA-256 已核对；严格模型加载、CUDA 推理与真实任务创建通过。`env.sh` 指定本地缓存、`HF_HUB_OFFLINE=1`、`MUJOCO_GL=egl` 和 `PYOPENGL_PLATFORM=egl`。

精确版本和权重散列保存在 [[VLABench-repro-versions-initial.json|版本收据]]，实测计算与渲染信息见 [[VLABench-repro-gpu-egl.json|CUDA/EGL 收据]]；完整依赖锁文件保留在实验目录的 `requirements.lock.txt`。

## 2. 官方入口与本地适配

运行顺序为：资源与版本门禁 → CUDA/EGL/模型加载 → 原始 `lerobot-eval` 单次运行 → 根据失败证据检查接口 → 相机适配及正常样本诊断 → PS 与配对恢复核验 → 正式视觉对照。

原始入口确实运行过，结果是 seed=1000 的 500 步失败。当前本地入口保留两个源码差异：

| 改动 | 依据与影响 | 保存的差异 |
| --- | --- | --- |
| `VLABench/configs/constant.py`：不存在的资产目录返回空列表 | 兼容单任务资产集合；任务所需资产仍由完整性门禁检查 | [[VLABench-repro-asset-discovery.patch]] |
| LeRobot 图像输入顺序由 `(0,1,2)` 改为 `(2,0,3)` | 编译相机实际为 `0=right`、`1=left`、`2=forward`、`3=franka/Franka_wrist_cam`；检查点训练视频对应前方、右侧、腕部，保留原三路 rename 键名 | [[VLABench-repro-camera-order.patch]] |

相机核验使用检查点 `train_config.json` 指定的 `lerobot/vlabench_unified`，固定到 `f61ad898199e746c20af3112f278cc86eb3ca3c4`，对照实际训练视频首帧与仿真相机画面。依据与帧散列见 [[VLABench-repro-camera-mapping.json]]。索引映射依赖当前版本和相机枚举，升级后需重新核对。

当前正常入口为实验目录下的 `bash run_baseline.sh`：单环境、同步、1 episode、CUDA、默认 seed=1000；检查点动作块为 50，采样迭代数为 10，任务上限 500 步。入口会保存实际命令、环境、源码差异、日志、评测 JSON 和视频。相机适配后的结果按本地适配方案记录。

## 3. 已保存的三次诊断运行

| 条件 | seed | 指令目标 | 步数 | 官方任务判据 | 结果收据 |
| --- | --- | --- | --- | --- | --- |
| 原始相机顺序 | 1000 | apple → plate_seen | 500 | 失败 | [[VLABench-repro-original-seed1000-eval.json]] |
| 相机适配 | 1000 | apple → plate_seen | 500 | 失败 | [[VLABench-repro-adapted-seed1000-eval.json]] |
| 相机适配，原生逐帧记录 | 1001 | banana → plate_seen | 139 | 成功 | [[VLABench-repro-adapted-seed1001-eval.json]]、[[VLABench-repro-adapted-seed1001-protocol.json]] |

三次进程均退出 0，任务结果分别为失败、失败、成功。退出码证明进程完成，任务成功由环境判据单独判断；`get_reward()` 固定返回 0，reward=0 不用作失败依据。

原始结果目录依次为：

```text
outputs/baseline-20261110T043532Z-kzxFa1
outputs/baseline-20261110T095207Z-H3kXKd
outputs/diagnostic-seed1001-20261110T095510Z-cs0Ry1
```

seed=1001 样本保存了原生 state/action 数据和三路视频，末条数据同时为 `next.success=true`、`next.done=true`。视频均为 480×480、10 fps、139 帧；此前正面视频检查可见抓起香蕉并向盘子移动。此记录方式保存动作前观测，缺少最后一步动作后的额外终态画面；`eval_info.json` 的 `video_paths=[]` 对应该次采用原生 recording，视频实际位于 `recordings/select_fruit_0/videos/`。

这三次用于入口诊断，不合并为成功率统计。seed=1000 在相机适配后仍失败；seed=1001 更换了场景，不能把两者差异归因于相机修复。正常单次样本已通过官方任务判据，正式基线分布和纹理影响仍待配对实验。

## 4. PS 论文定义与代码差异

### 4.1 论文要求同时计入目标物体与容器

[arXiv v1 §3.2，式 (1)](https://arxiv.org/html/2412.18194v1#S3.SS2) 定义：

$$
PS=0.2D+0.8P,
\qquad D=\frac{n_{correct}}{N},\quad P=\frac{m_{done}}{M}.
$$

其中 $N$ 是目标物体与目标容器的总数，$n_{correct}$ 是正确选择的数量；$M$ 是子步骤总数，$m_{done}$ 是完成的子步骤数。对一个水果放入一个盘子的 `select_fruit`，按论文定义自然对应两个目标：水果和盘子。论文没有在这一公式中给出把“正确选择容器”变成距离阈值的完整操作定义。

### 4.2 `intention_score` 仅查询目标水果

`PrimitiveTask.update_intention_distance()` 保存执行期间末端到各实体的最小距离，但 `get_intention_score()` 实际只将 `target_entity` 传入评分函数；本任务的 `target_entity` 是水果，并没有将 `target_container` 纳入 $N$ 和正确选择数。离散分取 `min_distance < threshold`，与“水果及容器各自正确选择后求比例”的论文 $D$ 不等价。

同一段代码中的 `target_is_grasped` 一旦变为 `True` 就保留；`get_task_progress()` 则将已抓取标记和当前条件满足数相加。对本任务的一项水果、一项 `contain` 条件，代码进度为：

$$P_{code}=\frac{\mathbf 1[\text{水果曾被抓住}]+\mathbf 1[\text{当前 contain 成立}]}{2}.$$

抓取标记是历史量，`contain` 是当前状态，因此这里也不宜直接当成通用的单调累计进度。

以下图片是**固定本地源码的浏览器渲染截图**：原样代码与真实行号生成只读 HTML，再由真实 Chromium 截屏；不是 IDE 或 GitHub 页面截图。每张图包含源路径、完整 commit 和源文件 SHA-256。取图前已逐字节核对相关文件与该 commit 的 Git blob 一致，所有图片均已检查可读性。

![[VLABench-repro-ps-primitive.png]]

### 4.3 evaluator 显式使用 0.1，而不是函数签名的 0.2

`PrimitiveTask.get_intention_score()` 的签名默认 `threshold=0.2`，但 VLABench evaluator 在第 54 行将阈值设为 `kwargs.get("intention_score_threshold", 0.1)`，并在第 169 行显式传入。复现该 evaluator 的代码意图分时应记录实际阈值 0.1；不能把函数默认值误写成实际配置，也不能据此给盘子另造一个阈值并称为论文 $D$。

此 evaluator 分别输出 `intention_score` 与 `progress_score`，该段没有将二者合成为论文 PS。当前 LeRobot 的成功 JSON 也不提供论文 PS。

![[VLABench-repro-ps-evaluator.png]]

### 4.4 评分状态仅在 `run_mode="eval"` 下维护

初始化时的 `reset_intention_distance()`、`reset_task_progress()`，以及每步后的更新，都受 `run_mode == "eval"` 控制。后续增加分项日志时必须检查实际运行模式和初始化顺序，否则可能读取未维护的状态。`get_reward()` 固定返回 0 也直接见于此段源码。

![[VLABench-repro-ps-hooks.png]]

### 4.5 `select_fruit` 继承与终止判据

`SelectFruitTask` 直接继承 `PrimitiveTask`，配置只包含将目标水果放入目标容器的 `contain` 条件，专家技能序列为 `pick → place`。因此前述基础评分实现确实作用于本次任务。

![[VLABench-repro-ps-inheritance.png]]

`should_terminate_episode()` 以当前 `conditions.is_met(physics)` 判定结束。[`ContainCondition` 第 44–69 行](https://github.com/OpenMOSS/VLABench/blob/cf588fe60c0c7282174fe979f5913170cfe69017/VLABench/tasks/condition.py#L44-L69) 检查实体位置是否被容器包含；此条件和终止函数未加入松爪、速度稳定或持续保持时长的要求。因此“官方任务判据成功”按当前包含条件解释，松爪后的稳定放置需要另设观测和额外终态记录。

![[VLABench-repro-ps-termination.png]]

### 4.6 本实验采用的报告口径

| 字段 | 含义与处理 |
| --- | --- |
| `official_success` | 当前固定实现的任务完成条件，保留为二值结果 |
| `intention_score` | 代码的水果距离意图代理量，记录实际阈值；不改称论文 $D$ |
| `progress_score` | 代码的历史抓取与当前 `contain` 组合，保留分项 |
| `code_ps_proxy` | 若计算 `0.2 × intention_score + 0.8 × progress_score`，明确称代码代理分 |
| `paper_ps` | `null`；目标容器选择的可复现操作定义尚未补齐 |

代码截图、逐字源码摘录、渲染 HTML、commit、源文件散列及图片散列统一保存于 [[VLABench-repro-evidence-manifest.json|证据来源清单]]。截图验证的是公开固定版本的实现差异；三次旧运行没有记录 PS 分项，不能由成功 JSON 反推其逐步评分。

## 5. 桌面纹理配对实验：待执行

计划为 10 组固定初始场景，每组分别运行正常桌面和变化纹理。相同 seed 只是输入之一，配对成立还需保存并恢复 `episode_config` 与物理状态，检查指令、对象实例、目标、机器人及物体状态、相机、接触和物理参数一致；变化限制在预先固定的桌面视觉纹理。

正式运行前需完成配对恢复与分项日志检查，并把实际纹理标识、场景序列、终止与异常处理写入正式 protocol。每组保存初始对照画面、逐步动作/状态、成功判据、代理分项和终态画面；同时核验视觉确实发生变化、物理设置保持一致。

配对报告按“双成功、双失败、正常成功/变化失败、正常失败/变化成功”四类统计，运行异常另列。若正常基线几乎全失败，先根据动作与视频证据排查策略/接口，避免把低基线分数直接解释为纹理效应。

| 阶段 | 本页记录时状态 |
| --- | --- |
| 依赖、完整资产、模型、CUDA/EGL | 已验证 |
| 原始入口代表性运行 | 已运行，seed=1000 失败 |
| 相机适配与正常成功样本 | 已验证，seed=1001，139 步；诊断样本 |
| 论文 PS 与代码对应 | 已确认关键差异；容器选择操作定义未解决 |
| 配对恢复及正式 protocol | 待完成 |
| 10 对纹理实验、正式成功率及纹理影响 | 待运行、待报告 |

## 来源与原始记录

- 论文：[arXiv 2412.18194v1，§3.2](https://arxiv.org/html/2412.18194v1#S3.SS2)；本地 `src/VLABench/docs/pdf/paper.pdf`，PDF 第 6 页。论文学习记录链接见开头。
- 官方入口说明：[LeRobot VLABench 文档](https://huggingface.co/docs/lerobot/vlabench)。安装与资产方案同时核对固定 LeRobot 源码中的 `docker/Dockerfile.sim`、`benchmarks/benchmarks.yaml`。
- 固定实现：[VLABench `cf588fe6`](https://github.com/OpenMOSS/VLABench/tree/cf588fe60c0c7282174fe979f5913170cfe69017)；[LeRobot `81b8c5bf`](https://github.com/huggingface/lerobot/tree/81b8c5bfdd5591ec59e512cfc7ac6db8151c70ee)。
- Linux 项目状态与版本真源：`/home/user/paper/vlabench-repro/STATUS.md`、`versions.json`；本页附带的 `versions-initial.json` 是正式配对实验前快照，后续结果以新增运行收据更新。
