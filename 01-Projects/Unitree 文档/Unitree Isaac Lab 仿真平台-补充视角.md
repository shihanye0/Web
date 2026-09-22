# Unitree Isaac Lab 仿真平台 — 补充视角

> 补充笔记，覆盖架构深度解析中未充分展开的角度。
> 对应主笔记：[[Unitree Isaac Lab 仿真平台代码架构深度解析]]
> 整理日期：2026-07-01

---

## 1. 项目定位与全局视角

### 1.1 一句话定位

**仿真数据工厂**——本质是一个能跑多种任务的机器人数据回环系统，核心价值在于**数据**而非仿真本身。

### 1.2 项目的四层价值

```
原始价值：Isaac Sim 物理仿真（NVIDIA 提供）
         ↓
工具价值：宇树机器人仿真配置 + DDS 通信封装
         ↓
应用价值：多种操作任务的场景/观测/奖励等配置
         ↓
数据价值：采集 → 增强 → 回放 → 验证的数据闭环  ← 核心
```

### 1.3 为什么是"数据工厂"

| 环节 | 说明 | 对应模块 |
|------|------|---------|
| **采集** | 遥操作录制关节轨迹和图像 | `sim_main.py` + `xr_teleoperate` |
| **存储** | JSON 格式保存每帧状态 | `tools/episode_writer.py` |
| **回放** | 重新执行录制数据，验证可复现性 | `action_provider_replay.py` |
| **增强** | 回放时变换光照/相机参数生成变体 | 主循环中的 `modify_light` / `modify_camera` |
| **迁移** | DDS 协议与实机一致，数据可直接部署 | DDS 所有模块 |
| **验证** | 加载 ONNX 模型在仿真中测试策略 | `DDSRLActionProvider` + `policy.onnx` |

### 1.4 与 xr_teleoperate 的关系

> 仓库：[xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate)

```
xr_teleoperate (遥操作系统)
    │
    ├── 通过 XR 设备采集人体动作
    ├── 映射到机器人关节空间
    ├── 通过 DDS 发布控制命令 → unitree_sim_isaaclab 接收
    └── 可以录制数据集到文件
                                                    │
                                                    ↓
                                        unitree_sim_isaaclab (仿真平台)
                                            │
                                            ├── 接收 DDS 命令 → 控制仿真机器人
                                            ├── 渲染摄像头图像 → 通过共享内存返回
                                            ├── 发布仿真状态 → 用于监控/记录
                                            └── 回放录制数据 → 生成增强数据

两个项目配合形成完整链路：
  XR 遥操作 → DDS 指令 → 仿真执行 → 数据录制 → 回放增强 → 模型训练 → 部署到真机
```

---

## 2. 依赖生态全景图

### 2.1 依赖层级结构

```
     ┌──────────────────────────────────────────┐
     │           Python 标准库                   │
     │  os, sys, json, time, threading,          │
     │  multiprocessing, signal, pathlib,        │
     │  contextlib, argparse, abc                │
     └────────────────┬─────────────────────────┘
                      │
     ┌────────────────▼─────────────────────────┐
     │            PyTorch 生态                    │
     │  torch (GPU 张量计算)                      │
     │  torchvision (图像处理)                    │
     │  onnxruntime (策略模型推理)                │
     └────────────────┬─────────────────────────┘
                      │
     ┌────────────────▼─────────────────────────┐
     │         Isaac 生态（核心）                  │
     │  isaacsim (NVIDIA 仿真引擎)               │
     │  isaaclab (RL 框架 + Gymnasium 接口)      │
     │  ├── ManagerBasedRLEnvCfg                 │
     │  ├── InteractiveSceneCfg                  │
     │  ├── Articulation / RigidObject           │
     │  ├── ObsGroup / ObsTerm                  │
     │  └── Camera / EventManager               │
     └────────────────┬─────────────────────────┘
                      │
     ┌────────────────▼─────────────────────────┐
     │          通信生态                           │
     │  cyclonedds (DDS 底层, Eclipse 项目)       │
     │  unitree_sdk2_python (宇树 DDS 封装)       │
     │  pyzmq (图像传输)                          │
     │  aiortc + aiohttp (WebRTC 视频流)          │
     └────────────────┬─────────────────────────┘
                      │
     ┌────────────────▼─────────────────────────┐
     │          工具生态                           │
     │  rerun-sdk (可视化日志)                     │
     │  opencv-python (图像处理)                  │
     │  gymnasium (RL 环境接口)                   │
     │  pynput (键盘监听)                         │
     └──────────────────────────────────────────┘
```

### 2.2 各依赖的核心作用

| 依赖 | 版本 | 作用 | 能否替换 |
|------|------|------|---------|
| **isaacsim** | 4.5/5.x | GPU 物理仿真 + 渲染引擎 | ❌ 不可替代，项目基础 |
| **isaaclab** | 跟随版本 | RL 框架、场景管理、观测系统 | ❌ 不可替代 |
| **cyclonedds** | 0.10.x | DDS 实时通信中间件 | ⚠️ 可换 FastDDS，但宇树 sdk 依赖它 |
| **unitree_sdk2_python** | 最新 | 宇树 DDS 消息类型定义 | ❌ 必须用宇树的 |
| **torch** | 2.5/2.7 | GPU 张量 + 关节控制 + 策略推理 | ⚠️ 可换，但 Isaac Lab 需要 |
| **pyzmq** | 27 | 图像传输通道 | ✅ 可换，当前设计 |
| **onnxruntime** | 1.22 | 策略模型推理 | ✅ 可换 PyTorch 原生 |
| **rerun-sdk** | 0.20 | 可视化日志数据 | ✅ 可选的，当前非核心 |

### 2.3 版本兼容表

| Isaac Sim | Python | PyTorch | CUDA | Ubuntu |
|:---------:|:------:|:-------:|:----:|:------:|
| 4.5 | 3.10 | 2.5.1 | 12.1 | 20.04/22.04 |
| 5.0 | 3.11 | 2.7.0 | 12.6 | 22.04 |
| 5.1 | 3.11 | 2.7.0 | 12.6 | 22.04 |

**RTX 50 系列必须用 Isaac Sim 5.0.0+。**

---

## 3. 端到端工作流

### 3.1 完整用户流程

```
┌─────────────────────────────────────────────────────────────────┐
│                    第一阶段：环境搭建                             │
│                                                                 │
│  1. Ubuntu 22.04 + NVIDIA GPU + CUDA 12.6 前置条件               │
│  2. git clone 项目                                               │
│  3. bash auto_setup_env.sh 5.1 unitree_sim_env                   │
│     （自动装：系统依赖 → IsaacLab → CycloneDDS → sdk2 → 项目依赖） │
│  4. bash fetch_assets.sh（下载机器人 USD 资产，需要 git-lfs）      │
│  5. conda activate E:/conda_envs/unitree_sim_env（激活环境）      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    第二阶段：遥操作采集数据                        │
│                                                                 │
│  # 终端 1：启动仿真（带 Dex3 灵巧手的圆柱体抓取任务）              │
│  python sim_main.py --task Isaac-PickPlace-Cylinder-G129-Dex3-Joint │
│                     --enable_dex3_dds --robot_type g129          │
│                                                                 │
│  # 终端 2：启动 xr_teleoperate 遥操作（采集数据集）                │
│  操作者通过 XR 设备控制机器人，数据自动录制到文件                   │
│                                                                 │
│  # 或者：用键盘控制机器人移动                                     │
│  python send_commands_keyboard.py                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    第三阶段：数据回放验证                          │
│                                                                 │
│  python sim_main.py --task Isaac-PickPlace-Cylinder-G129-Dex3-Joint │
│                     --replay --file_path /path/to/data            │
│                                                                 │
│  仿真环境重放录制的关节轨迹，验证：                               │
│  - 动作是否可以复现                                              │
│  - 物体是否到达目标位置                                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    第四阶段：数据增强                              │
│                                                                 │
│  python sim_main.py --task ... --replay --file_path ./data       │
│                     --generate_data --generate_data_dir ./data2   │
│                     --modify_light --modify_camera               │
│                                                                 │
│  回放时自动随机调整光照和相机参数，生成多样化视觉数据：              │
│  同一个动作轨迹 × 10 种光照 × 5 种相机位姿 = 50× 数据量           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    第五阶段：策略模型验证                          │
│                                                                 │
│  python sim_main.py --task Isaac-Move-Cylinder-G129-Dex3-Wholebody │
│                     --action_source dds_wholebody                │
│                     --model_path assets/model/policy.onnx        │
│                                                                 │
│  RL 策略控制行走 + DDS 遥控手臂 = 全身协同操作                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 路径约定

| 路径 | 说明 |
|------|------|
| `assets/robots/` | 机器人 USD 模型文件（git-lfs） |
| `assets/model/policy.onnx` | 默认 RL 策略模型路径 |
| `./data/` | 默认数据录制目录 |
| `./data2/` | 增强数据输出目录 |

### 3.3 多终端协作架构（重要）

项目需要**同时运行多个进程**：

```
终端 1: sim_main.py（主仿真进程）
  ├── 物理仿真 + 渲染
  ├── DDS 发布：rt/lowstate, rt/sim_state, rt/rewards_state
  ├── DDS 订阅：rt/lowcmd, rt/reset_pose/cmd
  └── 共享内存：摄像头图像

终端 2: xr_teleoperate / send_commands_*.py（控制端）
  ├── 订阅仿真状态
  ├── 发布控制指令
  └── 可选：录制数据

终端 3: rerun_visualizer.py（可视化监控）
  ├── 订阅 DDS 数据
  └── Rerun 可视化

终端 4: teleimager（图像服务，可选）
  ├── 从共享内存读取图像
  └── WebRTC 推流或保存
```

---

## 4. teleimager 图像服务模块

### 4.1 模块定位

`teleimager/` 是独立的图像发布服务，负责将仿真渲染的图像通过 WebRTC 推送到远程客户端。

**文件**：`teleimager/image_server.py`

**核心函数**：`run_isaacsim_server(public_ip, livestream_type, ...)`

### 4.2 工作流程

```
仿真主循环渲染摄像头
    ↓
图像写入共享内存 (isaac_head_image_shm / left / right)
    ↓
teleimager 后台线程读取共享内存
    ↓
aiortc WebRTC 连接
    ↓
远程客户端（浏览器/isaacsim-webrtc-streaming-client）查看

WebRTC 模式：
  livestream_type=1：公网模式（需要 public_ip 参数）
  livestream_type=2：私网模式（默认 127.0.0.1）
```

### 4.3 入口调用

```python
# sim_main.py 中启动
from teleimager.image_server import run_isaacsim_server

# 如果 livestream_type > 0，启动 WebRTC 服务器
if args.livestream_type > 0:
    threading.Thread(
        target=run_isaacsim_server,
        args=(args.public_ip, args.livestream_type),
        daemon=True
    ).start()
```

### 4.4 典型使用场景

- **Docker 运行**：容器内无 GUI，通过 WebRTC 远程查看仿真画面
- **远程数据采集**：操作者不在同一台机器
- **多人监控**：多个客户端同时查看仿真状态

---

## 5. 多场景坐标系系统分析

### 5.1 坐标系总览

```
世界坐标系（Isaac Sim 默认）：
  - Z 轴向上
  - X/Y 水平
  - 原点在 (0, 0, 0)

场景布局方向：Z 轴正方向为"上"，Y 轴正方向为"前"

桌面高度：z = 0.84（物体初始位置）
桌子位置：z = -0.2（桌面在 z≈0.85 左右）
地面：z = 0（严格说在某些场景中地面位置不同）

四元数格式：Isaac Sim 用 [w, x, y, z]（w-first）
```

### 5.2 各任务场景空间分布

| 任务 | 场景区域 | 布局特征 | 物体坐标范围 |
|------|---------|---------|-------------|
| 圆柱体（普通） | 正面桌面 | 密集 6 张桌子，机器人站中央 | X:[-0.42,1.0], Y:[0.2,0.7], z≈0.84 |
| 圆柱体（全身） | 仓库区域 | 2 张桌子，有旋转 | X 负值区, Y 负值区 |
| 红色方块 | 仓库区域 | 密集 6 张桌子 | X:[-5.4,-2.9], Y:[-5.05,-2.8] |
| 堆叠 | 仓库区域 | 同上 | 同上（3 个方块） |
| 抽屉 | 仓库侧面 | 1 个柜子 + 1 个方块 | X:[-2.7,-2.2], Y:[-4.15,-3.55], z>0.2 |

### 5.3 桌子的空间排列

```
圆柱体任务（6 张桌子，正面视角）：
          Y
          ↑
    ┌─────┼─────┐
    │ T2  │ T1  │  T1: (0.0, 0.55)   ← 机器人前方主桌
    │     │     │  T2: (-3.5, 0.55)  ← 左侧
    ├─────┼─────┤  T3: (3.5, 0.55)   ← 右侧
    │ T5  │ T6  │
    │     │     │  T4: (3.5, -5.0)   ← 右后
    └─────┴─────┘  T5: (-3.5, -5.0)  ← 左后
          ↓        T6: (0.0, -5.0)   ← 后中
          Z
    机器人 →→ (0, 0, 0.75)

全身任务（2 张桌子，带旋转）：
  T1: (-2.36, -3.46, -0.2), 四元数 ≈ 90° 旋转（朝机器人）
  T2: (-3.97, -4.34, -0.2), 无旋转
  ← 场景更空旷，机器人可以移动
```

### 5.4 坐标系注意点

1. **Isaac Sim 的 quat 格式**：`[w, x, y, z]`，注意与常见 ROS 格式区分（ROS 也是 w-first）
2. **Camera 的 offset**：`pos_offset` + `rot_offset`，使用 ROS 坐标系约定
3. **FrameTransformer** 的 `OffsetCfg`：用于抽屉任务，定位把手相对于柜体的偏移
4. **姿态单位**：角度为弧度，长度为米

---

## 6. 数据录制格式（episode_writer）

### 6.1 录制机制

**文件**：`tools/episode_writer.py`

数据以 JSON 格式逐帧写入，每 episode 一个文件：

```json
{
  "episode_index": 1,
  "frames": [
    {
      "step": 42,
      "timestamp": 12.345,
      "joint_pos": [0.1, -0.2, ...],     // 29 个关节位置
      "joint_vel": [0.0, 0.0, ...],       // 29 个关节速度
      "joint_torque": [0.5, -0.3, ...],   // 29 个力矩
      "root_pos": [0.0, 0.0, 0.75],       // 根位置
      "root_quat": [1.0, 0.0, 0.0, 0.0],  // 根朝向
      "object_pos": [-0.35, 0.40, 0.84],  // 物体位置（可选）
      "reward": 0.0,                       // 当前奖励
    },
    // ... 更多帧
  ],
  "metadata": {
    "task_name": "Isaac-PickPlace-Cylinder-G129-Dex3-Joint",
    "robot_type": "g129",
    "episode_length": 2000,
    "success": false,
    "max_reward": 0.5
  }
}
```

### 6.2 与 xr_teleoperate 的兼容性

录制格式与 `xr_teleoperate` 项目保持一致，所以回放时 `--file_path` 可以直接指向遥操作录制的数据目录。

### 6.3 数据生成流水线

```
原始数据（遥操作录制）
    │
    ├── sim_main.py --replay → 回放验证
    │
    ├── sim_main.py --replay --generate_data → 生成增强数据
    │       ├── 调整光照（--modify_light）
    │       ├── 调整相机（--modify_camera）
    │       ├── 启用 JPEG 压缩（--camera_jpeg）
    │       └── 每帧重新渲染 → 新图像
    │
    └── tools/data_convert.py → 格式转换
    └── tools/data_json_load.py → 数据加载工具
```

---

## 7. 性能调优参数体系

### 7.1 完整参数清单

`sim_main.py` 提供了大量可调参数，覆盖从物理引擎到图像传输的各个环节：

#### 时间相关参数

| 参数 | 默认值 | 作用 | 调优方向 |
|------|--------|------|---------|
| `--step_hz` | 100 | 主循环控制频率 | 越高越流畅，但 CPU 负载越高 |
| `--physics_dt` | 0.005 (200Hz) | 物理仿真步长 | 越小越精确，但越慢 |
| `--render_interval` | 1 | 每 N 步渲染一次 | 越大渲染越少，GPU 负载越低 |
| -- | -- | decimation = physics_dt × render_interval / (1/step_hz) | 实际控制频率 |

#### 渲染与相机

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `--camera_write_interval` | 2 | 每 N 步写一次图像到共享内存 |
| `--camera_jpeg` | True | 启用 JPEG 压缩 |
| `--camera_jpeg_quality` | 85 | JPEG 质量 (1-100) |
| `--camera_include` | front,left_wrist,right_wrist | 启用的摄像头列表 |
| `--camera_exclude` | world_camera | 禁用的摄像头列表 |
| `--no_render` | False | 完全禁用渲染（Docker 模式用） |
| `--skip_cvtcolor` | False | 跳过 RGB→BGR 转换 |
| `--livestream_type` | 2 | 0=无直播, 1=公网WebRTC, 2=私网WebRTC |

#### 物理引擎

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `--solver_iterations` | 8 (position) / 4 (velocity) | PhysX 求解器迭代次数 |
| `--physx_substeps` | 4 | PhysX 子步数 |
| `--gravity_z` | -9.8 | 重力加速度 |

#### 性能统计

| 参数 | 默认值 | 作用 |
|------|--------|------|
| `--enable_profiling` | True | 启用性能分析 |
| `--profile_interval` | 500 步 | 每 N 步打印一次性能报告 |

### 7.2 常见性能调优组合

```
场景 1：最大化仿真精度
  --physics_dt 0.002 --solver_iterations 16 --physx_substeps 8
  → 代价：慢 4-8x

场景 2：最大化仿真速度（数据生成）
  --physics_dt 0.01 --render_interval 4 --camera_write_interval 4
  --camera_jpeg_quality 60 --no_render
  → 代价：精度降低，但速度快 3-5x

场景 3：平衡模式（默认）
  --physics_dt 0.005 --render_interval 1 --camera_write_interval 2
  → 默认 100Hz 控制，200Hz 物理

场景 4：Docker 无头运行
  --no_render --livestream_type 2 --public_ip 0.0.0.0
  → 通过 WebRTC 远程查看画面
```

### 7.3 性能报告解读

控制器每 2000 步（默认）打印：

```
[Performance] A:0.5ms, E:8.2ms, S:1.3ms, T:10.0ms
```

| 缩写 | 含义 | 参考值 | 优化方向 |
|------|------|--------|---------|
| A | Action 获取耗时 | < 2ms | 调小 `--step_hz` |
| E | 仿真步进耗时 | < 10ms | 减小 `--physics_dt` 或 `--render_interval` |
| S | Sleep 时间 | > 0 | 频率是否达标，S>0 说明能跑满目标频率 |
| T | 总耗时 | < 10ms | 目标：T < 1/step_hz = 10ms @ 100Hz |

如果 `S = 0ms` 说明实际频率达不到目标 `step_hz`。

---

## 8. 设计原则与决策哲学

### 8.1 核心设计理念

| 原则 | 体现 | 为什么 |
|------|------|--------|
| **仿真-真机一致** | DDS 通信与实机完全一致 | 仿真数据集可直接用于真机部署 |
| **模块化组合** | 场景/观测/奖励/终止/动作独立配置 | 可组合出 18+ 个不同任务 |
| **数据优先** | 回放/增强/录制功能完整 | 核心产出是数据集，不是仿真本身 |
| **渐进复杂度** | 简单任务不用全身控制，复杂任务可叠加 | 用户按需选择合适的复杂度 |
| **单环境默认** | `num_envs=1`，绝大多数代码假定单环境 | 简化调试和开发 |

### 8.2 刻意不做的事情

| 不做 | 原因 | 需要时怎么办 |
|------|------|-------------|
| 不处理多环境竞争 | `num_envs=1` 简化了大部分问题 | 多环境用户自己处理 batch 维度 |
| 不提供 Web UI | 聚焦仿真后端，UI 交给 xr_teleoperate | 通过 DDS 和 WebRTC 连接外部 UI |
| 不实现端到端 VLA | 项目定位是仿真数据，不是推理平台 | 提供数据导出接口，外部推理 |
| 不打包成 Docker 镜像 | 用户自己搭环境 | 提供 Dockerfile + 文档 |

### 8.3 代码中的一些设计模式

**工厂模式**（Create动作提供器）：
```python
# action_provider/create_action_provider.py
def create_action_provider(action_source: str) -> ActionProvider:
    if action_source == "dds":
        return DDSActionProvider(...)
    elif action_source == "replay":
        return FileActionProviderReplay(...)
    elif action_source == "dds_wholebody":
        return DDSRLActionProvider(...)
    # 注意：--action_source "policy" 定义了参数但未实现！
```

**策略模式**（不同动作来源可切换）：
```python
# controller 持有 ActionProvider 接口
controller.action_provider = create_action_provider(args.action_source)
controller.action_provider.start()
# 运行时调用统一的 get_action() 接口
action = controller.action_provider.get_action(env)
```

**模板方法模式**（任务配置类层级）：
```
ManagerBasedRLEnvCfg（Isaac Lab 基类）
  └── 具体任务环境配置（如 PickPlaceCylinderG129Dex3JointEnvCfg）
        ├── 场景 = 基类场景 + 机器人预设
        ├── 观测 = 关节观测 + 灵巧手观测 + 图像
        ├── 动作 = 关节位置控制
        ├── 奖励 = 区域判定
        ├── 终止 = 出界检测
        └── 事件 = 位置随机化
```

---

## 9. 其他未覆盖细节

### 9.1 工具脚本速查

| 脚本 | 用途 | 说明 |
|------|------|------|
| `send_commands_keyboard.py` | 键盘控制机器人移动 | 在全身任务中使用 |
| `send_commands_8bit.py` | 按键遥操作 | 更精确的 8-bit 控制 |
| `reset_pose_test.py` | 测试复位功能 | 验证物体/场景复位 |
| `tools/data_convert.py` | 数据格式转换 | JSON → 其他格式 |
| `tools/data_json_load.py` | 数据加载工具 | 读取录制数据 |
| `tools/convert_urdf.py` | URDF → USD 转换 | 导入新机器人模型 |
| `tools/edit_usda.py` | USD 文件编辑 | 场景编辑器 |
| `tools/get_reward.py` | 奖励值查询工具 | 调试奖励函数 |
| `tools/get_stiffness.py` | 关节刚度查询 | 调试关节响应 |
| `tools/rerun_visualizer.py` | Rerun 可视化 | 订阅 DDS 数据实时展示 |
| `tools/shared_memory_utils.py` | 共享内存工具 | 调试共享内存 |
| `tools/augmentation_utils.py` | 数据增强工具 | 图像增强 |

### 9.2 Camera 配置系统详解

**文件**：`tasks/common_config/camera_configs.py`

```python
class CameraPresets:
    @staticmethod
    def get_front_camera_config():
        """前置摄像头 - 安装在头部"""
        return CameraBaseCfg.get_camera_config(
            prim_path="/World/envs/env_.*/Robot/d435_link/front_cam",
            pos_offset=(0.10, 0.0, 0.03),      # 相对安装位置
            rot_offset=(0.5, -0.5, 0.5, -0.5), # 四元数旋转
            focal_length=16.5,
        )
    
    @staticmethod
    def get_wrist_camera_config(side: str):
        """手腕摄像头 - 安装在灵巧手基座"""
        prim = f"/World/envs/env_.*/Robot/{side}_hand_camera_base_link/{side}_wrist_camera"
        return CameraBaseCfg.get_camera_config(
            prim_path=prim,
            data_types=["rgb"],
            width=640, height=480,
            focal_length=16.5,
        )
```

三个默认启用的摄像头：
1. **front_camera**（头部）— 主视角，看到前方桌子
2. **left_wrist_camera**（左手腕）— 看到左手的操作
3. **right_wrist_camera**（右手腕）— 看到右手的操作
4. **world_camera**（世界视角，默认禁用）— 第三人称视角

### 9.3 任务中的"head-waist-fix"配置

```python
# sim_main.py 默认任务
"--task", type=str, default="Isaac-PickPlace-G129-Head-Waist-Fix"
```

这个默认值比较特殊——`Head-Waist-Fix` 只在部分早期配置中出现，是固定头部和腰部、只控制手臂的简化配置。18 个正式任务中都没有这个。这说明项目在早期阶段曾有过更简化的任务版本，后来被标准化的关节控制取代。

---

## 索引
- 主笔记：[[Unitree Isaac Lab 仿真平台代码架构深度解析]]
- 安装指南：[[Unitree Isaac Lab 仿真平台安装与使用指南]]

#机器人 #宇树 #仿真 #IsaacLab #补充视角 #数据工厂 #性能调优 #坐标系 #工作流
