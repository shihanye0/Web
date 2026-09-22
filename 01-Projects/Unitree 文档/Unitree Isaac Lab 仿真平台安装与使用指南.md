# Unitree Isaac Lab 仿真平台安装与使用指南

> 仓库：[unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)
> 整理日期：2026-06-01（2026-06-12 根据源码校正）

---

## 1. 平台简介

`unitree_sim_isaaclab` 是宇树官方基于 **NVIDIA Isaac Lab**（Isaac Sim）的仿真平台，支持 G1 人形机器人配合 Dex3-1 灵巧手进行抓取、堆叠等任务的仿真训练。

### 核心能力

- 基于 Isaac Sim 的高保真物理仿真
- 支持 DDS 通信（与实机一致的控制接口）
- 内置多种 Dex3 灵巧手操作任务
- 支持策略训练（RL）和遥操作数据采集
- 支持摄像头图像流式传输

### 系统要求

| 要求 | 最低配置 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Ubuntu 20.04/22.04 | Ubuntu 22.04 |
| GPU | NVIDIA RTX 3060（8GB） | RTX 4090（24GB） |
| 显存 | 8GB | 16GB+ |
| 内存 | 16GB | 32GB+ |
| CUDA | 12.1+ | 12.6 |
| 磁盘 | 50GB 可用空间 | 100GB SSD |

> **注意**：Isaac Sim 仅支持 NVIDIA GPU，不支持 AMD 或集成显卡。RTX 50 系列需要 Isaac Sim 5.0.0+。

---

## 2. 安装步骤

### 2.1 一键安装脚本

官方提供了自动安装脚本 `auto_setup_env.sh`，流程如下：

```
克隆仓库 → 安装系统依赖 → 克隆 IsaacLab/CycloneDDS/unitree_sdk2_python
→ 创建 Conda 环境 → 安装 PyTorch → 安装 Isaac Sim → 安装 Isaac Lab
→ 安装 SDK → 安装剩余依赖
```

**运行方式：**

```bash
# 1. 克隆仓库
git clone https://github.com/unitreerobotics/unitree_sim_isaaclab.git
cd unitree_sim_isaaclab

# 2. 运行安装脚本（参数：Isaac版本 环境名 CUDA版本）
# 支持的 Isaac 版本：4.5 / 5.0 / 5.1
bash auto_setup_env.sh 5.1 unitree_sim cu126
```

脚本参数说明：

| 参数 | 可选值 | 说明 |
|------|--------|------|
| 第1个参数 | `4.5` / `5.0` / `5.1` | Isaac Sim 版本 |
| 第2个参数 | 自定义名称 | Conda 环境名 |
| 第3个参数 | `cu121` / `cu126` | CUDA 版本（可选，默认根据 Isaac 版本自动选择） |

### 2.2 各版本对应的依赖

| Isaac 版本 | Python | PyTorch | CUDA 默认 |
|:----------:|:------:|:-------:|:---------:|
| 4.5 | 3.10 | 2.5.1 | cu121 |
| 5.0 | 3.11 | 2.7.0 | cu126 |
| 5.1 | 3.11 | 2.7.0 | cu126 |

### 2.3 手动安装（如果一键脚本失败）

```bash
# Step 1: 系统依赖
sudo apt-get update && sudo apt-get install -y cmake build-essential openssl git-lfs unzip

# Step 2: 克隆依赖仓库（放在 unitree_sim_isaaclab 的同级目录）
cd ..
git clone https://github.com/isaac-sim/IsaacLab.git
git clone https://github.com/eclipse-cyclonedds/cyclonedds -b releases/0.10.x
git clone https://github.com/unitreerobotics/unitree_sdk2_python

# Step 3: 编译 CycloneDDS
cd cyclonedds
mkdir -p build install && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=../install
cmake --build . --target install
export CYCLONEDDS_HOME="$(pwd)/install"
cd ../..

# Step 4: 创建 Conda 环境
conda create -n unitree_sim python=3.11
conda activate unitree_sim

# Step 5: 安装 PyTorch
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu126

# Step 6: 安装 Isaac Sim
pip install "isaacsim[all,extscache]==5.1.0" --extra-index-url https://pypi.nvidia.com

# Step 7: 安装 Isaac Lab
cd ../IsaacLab
./isaaclab.sh --install

# Step 8: 安装 unitree_sdk2_python
cd ../unitree_sdk2_python
pip install -e .

# Step 9: 安装仿真平台自身依赖
cd ../unitree_sim_isaaclab
pip install -r requirements.txt
cd teleimager && pip install -e . && cd ..

# Step 10: 生成证书（用于图像流传输）
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout key.pem -out cert.pem
mkdir -p ~/.config/xr_teleoperate/
cp key.pem cert.pem ~/.config/xr_teleoperate/
rm key.pem cert.pem

# Step 11: 下载仿真资源
bash fetch_assets.sh

# Step 12: 初始化子模块
git submodule update --init --depth 1

# Step 13: libstdc++ 补丁（Isaac 5.0/5.1 需要）
conda install -c conda-forge libstdcxx-ng
```

---

## 3. 运行仿真

### 3.1 基本启动命令

```bash
conda activate unitree_sim
cd unitree_sim_isaaclab

# 运行 Dex3 抓取圆柱体任务
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-Cylinder-G129-Dex3-Joint \
  --enable_dex3_dds --robot_type g129
```

### 3.2 所有可用任务（共 18 个，全部经代码验证）

#### G1 机器人任务（15 个）

**抓取放置圆柱体（3 种灵巧手）：**

| --task 参数 | 灵巧手 | 说明 |
|------------|--------|------|
| `Isaac-PickPlace-Cylinder-G129-Dex1-Joint` | Dex1-1 夹爪 | 抓取放置圆柱体 |
| `Isaac-PickPlace-Cylinder-G129-Dex3-Joint` | Dex3-1 灵巧手 | 抓取放置圆柱体 |
| `Isaac-PickPlace-Cylinder-G129-Inspire-Joint` | Inspire 灵巧手 | 抓取放置圆柱体 |

**抓取放置红色方块（3 种灵巧手）：**

| --task 参数 | 灵巧手 | 说明 |
|------------|--------|------|
| `Isaac-PickPlace-RedBlock-G129-Dex1-Joint` | Dex1-1 夹爪 | 抓取放置红色方块 |
| `Isaac-PickPlace-RedBlock-G129-Dex3-Joint` | Dex3-1 灵巧手 | 抓取放置红色方块 |
| `Isaac-PickPlace-RedBlock-G129-Inspire-Joint` | Inspire 灵巧手 | 抓取放置红色方块 |

**堆叠红绿黄方块（3 种灵巧手）：**

| --task 参数 | 灵巧手 | 说明 |
|------------|--------|------|
| `Isaac-Stack-RgyBlock-G129-Dex1-Joint` | Dex1-1 夹爪 | 堆叠红绿黄方块 |
| `Isaac-Stack-RgyBlock-G129-Dex3-Joint` | Dex3-1 灵巧手 | 堆叠红绿黄方块 |
| `Isaac-Stack-RgyBlock-G129-Inspire-Joint` | Inspire 灵巧手 | 堆叠红绿黄方块 |

**抓取红色方块放入抽屉（2 种灵巧手）：**

| --task 参数 | 灵巧手 | 说明 |
|------------|--------|------|
| `Isaac-Pick-Redblock-Into-Drawer-G129-Dex1-Joint` | Dex1-1 夹爪 | 抓取方块放入抽屉 |
| `Isaac-Pick-Redblock-Into-Drawer-G129-Dex3-Joint` | Dex3-1 灵巧手 | 抓取方块放入抽屉 |

**全身协调移动圆柱体（3 种灵巧手）：**

| --task 参数 | 灵巧手 | 说明 |
|------------|--------|------|
| `Isaac-Move-Cylinder-G129-Dex1-Wholebody` | Dex1-1 夹爪 | 全身协调移动圆柱体 |
| `Isaac-Move-Cylinder-G129-Dex3-Wholebody` | Dex3-1 灵巧手 | 全身协调移动圆柱体 |
| `Isaac-Move-Cylinder-G129-Inspire-Wholebody` | Inspire 灵巧手 | 全身协调移动圆柱体 |

#### H1-2 机器人任务（3 个）

| --task 参数 | 灵巧手 | 说明 |
|------------|--------|------|
| `Isaac-PickPlace-Cylinder-H12-27dof-Inspire-Joint` | Inspire 灵巧手 | H1-2 抓取放置圆柱体 |
| `Isaac-PickPlace-RedBlock-H12-27dof-Inspire-Joint` | Inspire 灵巧手 | H1-2 抓取放置红色方块 |
| `Isaac-Stack-RgyBlock-H12-27dof-Inspire-Joint` | Inspire 灵巧手 | H1-2 堆叠红绿黄方块 |

> **注意**：G1 任务使用 `--robot_type g129`，H1-2 任务使用 `--robot_type h1_2`。

### 3.3 命令行参数详解

```bash
python sim_main.py \
  --task <任务名> \
  --enable_dex3_dds \
  --robot_type g129 \
  --step_hz 100
```

| 参数                        | 默认值                                                 | 说明                                                                         |
| ------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- |
| `--task`                  | `Isaac-PickPlace-G129-Head-Waist-Fix`               | 任务名称（见 §3.2）                                                               |
| `--action_source`         | `dds`                                               | 动作来源：`dds` / `file` / `trajectory` / `policy` / `replay` / `dds_wholebody` |
| `--enable_dex3_dds`       | false                                               | 启用 Dex3-1 灵巧手 DDS 通信                                                       |
| `--enable_dex1_dds`       | false                                               | 启用 Dex1-1 夹爪 DDS 通信                                                        |
| `--enable_inspire_dds`    | false                                               | 启用 Inspire 灵巧手 DDS 通信                                                      |
| `--enable_wholebody_dds`  | false                                               | 启用全身 DDS 控制                                                                |
| `--robot_type`            | `g129`                                              | 机器人类型（`g129` 或 `h1_2`）                                                     |
| `--step_hz`               | `100`                                               | 控制频率（Hz）                                                                   |
| `--model_path`            | `assets/model/policy.onnx`                          | ONNX 策略模型路径                                                                |
| `--file_path`             | -                                                   | 回放数据文件路径                                                                   |
| `--generate_data`         | false                                               | 是否采集数据                                                                     |
| `--generate_data_dir`     | `./data`                                            | 数据保存目录                                                                     |
| `--public_ip`             | `127.0.0.1`                                         | 图像流公网 IP                                                                   |
| `--livestream_type`       | `2`                                                 | 直播类型（0=关闭，1=WebRTC公网，2=WebRTC局域网）                                          |
| `--physics_dt`            | 自动                                                  | 物理仿真时间步长（如 0.005）                                                          |
| `--no_render`             | false                                               | 禁用渲染（加速仿真）                                                                 |
| `--camera_include`        | `front_camera,left_wrist_camera,right_wrist_camera` | 启用的摄像头                                                                     |
| `--camera_exclude`        | `world_camera`                                      | 禁用的摄像头                                                                     |
| `--camera_jpeg`           | true                                                | 启用 JPEG 压缩                                                                 |
| `--camera_jpeg_quality`   | `85`                                                | JPEG 质量（1-100）                                                             |
| `--seed`                  | `42`                                                | 随机种子                                                                       |
| `--reward_interval`       | `10`                                                | 奖励计算间隔（步）                                                                  |
| `--env_reward_interval`   | `5`                                                 | 环境奖励计算间隔（步）                                                                |
| `--solver_iterations`     | 自动                                                  | PhysX 求解器迭代次数                                                              |
| `--physx_substeps`        | 自动                                                  | 物理子步数                                                                      |
| `--gravity_z`             | 自动                                                  | 重力加速度                                                                      |
| `--render_interval`       | 自动                                                  | 每 N 步渲染一次                                                                  |
| `--camera_write_interval` | 自动                                                  | 每 N 步写入一次图像                                                                |
| `--headless`              | false                                               | 无头模式（无窗口，后台运行）                                                             |
| `--modify_light`          | false                                               | 修改光照参数                                                                     |
| `--modify_camera`         | false                                               | 修改摄像头参数                                                                    |
| `--replay_data`           | false                                               | 启用数据回放模式                                                                   |
| `--rerun_log`             | false                                               | 启用日志重放                                                                     |
| `--stats_interval`        | `10.0`                                              | 统计打印间隔（秒）                                                                  |
| `--profile_interval`      | `500`                                               | 性能分析报告间隔（步）                                                                |

> **注意**：`--enable_dex3_dds`、`--enable_dex1_dds`、`--enable_inspire_dds` 三者互斥，不能同时启用。

---

## 4. 项目结构

```
unitree_sim_isaaclab/
├── sim_main.py                  # 主入口
├── requirements.txt             # Python 依赖
├── auto_setup_env.sh            # 一键安装脚本
├── fetch_assets.sh              # 下载仿真资源脚本
├── robots/                      # 机器人模型配置
│   └── unitree.py               # 宇树机器人定义
├── tasks/                       # 任务定义
│   ├── config/                  # 任务配置
│   ├── common_config/           # 通用配置（机器人预设、摄像头预设）
│   ├── common_event/            # 通用事件（重置、随机化）
│   ├── common_observations/     # 通用观测函数
│   ├── common_rewards/          # 通用奖励函数
│   ├── common_scene/            # 通用场景配置
│   ├── common_termination/      # 通用终止条件
│   ├── g1_tasks/                # G1 机器人任务（15 个）
│   │   ├── pick_place_cylinder_g1_29dof_dex3/
│   │   ├── pick_place_redblock_g1_29dof_dex3/
│   │   ├── stack_rgyblock_g1_29dof_dex3/
│   │   ├── pick_redblock_into_drawer_g1_29dof_dex3/
│   │   ├── move_cylinder_g1_29dof_dex3_wholebody/
│   │   └── ...（dex1、inspire 版本）
│   ├── h1-2_tasks/              # H1-2 机器人任务（3 个）
│   └── utils/                   # 工具函数
├── dds/                         # DDS 通信模块
│   ├── dds_create.py            # DDS 对象创建
│   ├── dex3_dds.py              # Dex3 灵巧手 DDS
│   ├── gripper_dds.py           # Dex1 夹爪 DDS
│   ├── inspire_dds.py           # Inspire 灵巧手 DDS
│   ├── g1_robot_dds.py          # G1 机器人 DDS
│   ├── reset_pose_dds.py        # 重置命令 DDS
│   ├── sim_state_dds.py         # 仿真状态 DDS
│   └── rewards_dds.py           # 奖励 DDS
├── action_provider/             # 动作提供器
│   ├── action_provider_dds.py   # DDS 动作提供器
│   ├── action_provider_wh_dds.py # 全身 DDS 动作提供器
│   └── action_provider_replay.py # 回放动作提供器
├── layeredcontrol/              # 分层控制
│   └── robot_control_system.py  # 机器人控制系统
├── teleimager/                  # 图像流传输模块
├── tools/                       # 工具脚本
└── doc/                         # 文档
```

---

## 5. 任务配置文件解析

以 `pick_place_cylinder_g1_29dof_dex3` 为例，任务配置文件为：

```
tasks/g1_tasks/pick_place_cylinder_g1_29dof_dex3/pickplace_cylinder_g1_29dof_dex3_joint_env_cfg.py
```

### 5.1 场景配置

```python
@configclass
class ObjectTableSceneCfg(TableCylinderSceneCfg):
    robot: ArticulationCfg = G1RobotPresets.g1_29dof_dex3_base_fix()  # G1 + Dex3 机器人
    front_camera = CameraPresets.g1_front_camera()                     # 前置摄像头
    left_wrist_camera = CameraPresets.left_dex3_wrist_camera()         # 左手腕摄像头
    right_wrist_camera = CameraPresets.right_dex3_wrist_camera()       # 右手腕摄像头
```

基类 `TableCylinderSceneCfg` 包含：
- 仓库墙壁（`warehouse.usd`）
- 7 张桌子（分布在不同位置）
- 圆柱体物体（半径 0.018m，高 0.35m，质量 0.4kg，高摩擦）
- 穹顶灯（强度 3000.0）
- 世界摄像头

### 5.2 动作空间

```python
@configclass
class ActionsCfg:
    joint_pos = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=[".*"],     # 所有关节
        scale=1.0,              # 动作缩放
        use_default_offset=True # 使用默认偏移
    )
```

### 5.3 观测空间

```python
@configclass
class PolicyCfg(ObsGroup):
    robot_joint_state = ObsTerm(func=mdp.get_robot_boy_joint_states)   # 全身关节状态
    robot_gipper_state = ObsTerm(func=mdp.get_robot_dex3_joint_states) # Dex3 灵巧手状态
    camera_image = ObsTerm(func=mdp.get_camera_image)                  # 摄像头图像

    def __post_init__(self):
        self.enable_corruption = False    # 禁用观测噪声
        self.concatenate_terms = False    # 不自动拼接（返回 dict）
```

### 5.4 奖励函数

```python
@configclass
class RewardsCfg:
    reward = RewTerm(func=mdp.compute_reward, weight=1.0)
```

`compute_reward` 的实际逻辑（来自 `common_rewards/base_reward_pickplace_cylindercfg.py`）：

```python
def compute_reward(env, object_cfg, min_x, max_x, min_y, max_y, min_height,
                   post_min_x, post_max_x, post_min_y, post_max_y,
                   post_min_height, post_max_height):
    # 获取物体世界坐标
    object_pos = env.scene[object_cfg.name].data.root_pos_w

    # 判断物体是否在有效区域内
    done = (min_x < x < max_x) and (min_y < y < max_y) and (z > min_height)

    # 判断物体是否在目标位置（更严格的范围）
    done_post = (post_min_x < x < post_max_x) and (post_min_y < y < post_max_y) \
                and (post_min_height < z < post_max_height)

    # 奖励值：
    #   物体不在有效区域 → -1.0
    #   物体在有效区域但未到目标 → 0.0
    #   物体到达目标位置 → +1.0
```

**默认阈值（圆柱体任务）**：
- 有效区域：x ∈ [-0.42, 1.0]，y ∈ [0.2, 0.7]，高度 > 0.5
- 目标位置：x ∈ [0.28, 0.96]，y ∈ [0.24, 0.57]，高度 ∈ [0.81, 0.9]

**堆叠任务的层级奖励**（来自 `common_rewards/base_reward_stack_rgyblock.py`）：
- 三个方块都不在有效区域 → -1.0
- 第一个方块到位 → 0.3
- 前两个方块到位 → 0.6
- 三个方块全部到位 → 1.0

### 5.5 终止条件

```python
@configclass
class TerminationsCfg:
    success = DoneTerm(func=mdp.reset_object_estimate)
```

`reset_object_estimate` 的实际逻辑（来自 `common_termination/base_termination_pick_place_cylinder.py`）：

```python
def reset_object_estimate(env, object_cfg, min_x, max_x, min_y, max_y, min_height):
    # 当物体超出有效区域时终止（掉落出工作范围）
    # 默认有效区域：x ∈ [-0.42, 1.0]，y ∈ [0.2, 0.7]，高度 < 0.5
    return not (min_x < x < max_x and min_y < y < max_y and z > min_height)
```

### 5.6 物体随机化

```python
@configclass
class EventCfg:
    reset_object = EventTermCfg(
        func=mdp.reset_root_state_uniform,
        mode="reset",
        params={
            "pose_range": {
                "x": [-0.05, 0.05],   # X 轴随机范围 ±5cm
                "y": [-0.05, 0.05],   # Y 轴随机范围 ±5cm
            },
            "velocity_range": {},
            "asset_cfg": SceneEntityCfg("object"),
        },
    )
```

### 5.7 仿真物理参数

```python
def __post_init__(self):
    self.decimation = 2                          # 每 2 个物理步取 1 个控制步
    self.episode_length_s = 20.0                 # 每轮最长 20 秒
    self.sim.dt = 0.005                          # 物理步长 5ms
    # → 实际控制频率 = 1 / (dt × decimation) = 1 / (0.005 × 2) = 100Hz

    self.sim.render_interval = self.decimation   # 每 2 步渲染一次
    self.sim.physx.bounce_threshold_velocity = 0.01
    self.sim.physx.gpu_found_lost_aggregate_pairs_capacity = 1024 * 1024 * 4
    self.sim.physx.gpu_total_aggregate_pairs_capacity = 16 * 1024
    self.sim.physx.friction_correlation_distance = 0.00625
```

### 5.8 自定义事件管理器（DDS 远程重置）

每个任务配置都在 `__post_init__` 中注册了 `SimpleEventManager`，用于 DDS 远程触发重置：

```python
self.event_manager = SimpleEventManager()

# 重置物体位置
self.event_manager.register("reset_object_self", SimpleEvent(
    func=lambda env: base_mdp.reset_root_state_uniform(
        env, torch.arange(env.num_envs, device=env.device),
        pose_range={"x": [-0.05, 0.05], "y": [0.0, 0.05]},
        velocity_range={},
        asset_cfg=SceneEntityCfg("object"),
    )
))

# 重置整个场景
self.event_manager.register("reset_all_self", SimpleEvent(
    func=lambda env: base_mdp.reset_scene_to_default(
        env, torch.arange(env.num_envs, device=env.device))
))
```

---

## 6. 各任务差异对比

### 6.1 抽屉任务的特殊配置

`pick_redblock_into_drawer_g1_29dof_dex3` 与其他任务有显著差异：

| 配置项 | 圆柱体/方块任务 | 抽屉任务 |
|--------|----------------|---------|
| 奖励函数 | 有（compute_reward） | 无（`rewards = None`） |
| 物体质量 | 0.4kg / 1.0kg | 3.0kg（更重） |
| 物体随机范围 | x ±5cm, y ±5cm | x [-30cm, +25cm], y [0, +10cm] |
| 机器人初始位置 | 默认 | 自定义（-2.5, -3.7, 0.8） |
| PhysX CCD | 关闭 | 启用 |
| PhysX 子步数 | 默认 | 4 |
| 位置迭代次数 | 默认 | 16 |
| 场景物体 | 圆柱体/方块 | 方块 + 柜子（带抽屉关节） |
| 柜子关节 | 无 | drawer_top_joint, drawer_bottom_joint, door_left/right_joint |

### 6.2 全身任务的特殊配置

`move_cylinder_g1_29dof_dex3_wholebody` 的差异：

| 配置项 | 普通任务 | 全身任务 |
|--------|---------|---------|
| `decimation` | 2 | 4（控制频率降为 50Hz） |
| 机器人预设 | `g1_29dof_dex3_base_fix()` | `g1_29dof_dex3_wholebody()` |
| 接触传感器 | 无 | 有（`ContactSensorCfg`） |
| 额外摄像头 | 无 | `robot_camera`（世界视角） |
| 终止条件 | 有 | 无（空） |
| 物理材质 | 默认 | 显式设置摩擦（static=1.0, dynamic=1.0） |
| DDS 额外话题 | 无 | `RunCommandDDS`（移动命令） |
| 场景桌子数 | 7 张 | 2 张 |
| 仓库模型 | `warehouse.usd` | `small_warehouse_digital_twin.usd` |

### 6.3 不同灵巧手的观测函数

| 灵巧手 | 观测函数 | 说明 |
|--------|---------|------|
| Dex3-1 | `mdp.get_robot_dex3_joint_states` | 7 电机位置/速度/力矩 |
| Dex1-1 | `mdp.get_robot_gripper_joint_states` | 夹爪开合状态 |
| Inspire | `mdp.get_robot_inspire_joint_states` | Inspire 灵巧手状态 |

---

## 7. DDS 通信与仿真对接

仿真平台通过 DDS 与外部程序通信，话题与实机一致：

| 话题 | 方向 | 说明 |
|------|------|------|
| `rt/dex3/left/cmd` | 仿真 ← 外部 | 左手控制命令 |
| `rt/dex3/right/cmd` | 仿真 ← 外部 | 右手控制命令 |
| `rt/dex3/left/state` | 仿真 → 外部 | 左手状态反馈 |
| `rt/dex3/right/state` | 仿真 → 外部 | 右手状态反馈 |

**DDS 创建逻辑**（来自 `dds/dds_create.py`）：

```
create_dds_objects(args_cli, env)
    │
    ├── G1RobotDDS（机器人状态，始终创建）
    ├── Dex3DDS / GripperDDS / InspireDDS（三选一，根据 --enable_xxx_dds）
    ├── RunCommandDDS（仅 Wholebody 任务）
    ├── ResetPoseCmdDDS（重置命令，始终创建）
    ├── SimStateDDS（仿真状态，始终创建）
    └── RewardsDDS（奖励值，始终创建）
```

**动作提供器**（来自 `action_provider/create_action_provider.py`）：

| action_source | 提供器类 | 说明 |
|---------------|---------|------|
| `dds` | `DDSActionProvider` | 标准 DDS 遥操作 |
| `dds_wholebody` | `DDSRLActionProvider` | 全身 DDS RL 控制 |
| `replay` | `FileActionProviderReplay` | 文件回放 |

> **注意**：当任务名包含 `Wholebody` 时，`action_source` 会自动切换为 `dds_wholebody`。

这意味着你在仿真中写的控制代码，可以直接搬到实机上使用，DDS 接口完全一致。

---

## 8. 源码架构与关键代码详解

### 8.1 整体架构

```
sim_main.py（主入口）
│
├─ 阶段1：环境准备
│   ├── 解析命令行参数（argparse）
│   ├── 创建 Isaac Lab 仿真环境（gym.make）
│   ├── 获取机器人刚度/阻尼参数
│   └── 重置环境（env.reset）
│
├─ 阶段2：通信与控制初始化
│   ├── 创建图像流服务器（teleimager）
│   ├── 创建 DDS 通信对象（dds_create.py）
│   ├── 创建动作提供器（action_provider）
│   └── 创建机器人控制器（RobotController）
│
└─ 阶段3：主循环
    ├── 获取环境状态 → 发布到 DDS
    ├── 接收重置命令 → 重置物体/场景
    ├── 执行控制步（controller.step）
    ├── 打印频率统计
    └── 循环直到退出
```

### 8.2 主循环逻辑（简化版）

```python
def main():
    # 1. 创建环境
    env_cfg = parse_env_cfg(args.task, device=args.device, num_envs=1)
    env = gym.make(args.task, cfg=env_cfg).unwrapped
    env.reset()

    # 2. 创建 DDS 和控制器
    image_server = run_isaacsim_server()
    reset_pose_dds, sim_state_dds, dds_manager = create_dds_objects(args, env)
    action_provider = create_action_provider(env, args)
    controller = RobotController(env, control_config)
    controller.set_action_provider(action_provider)
    controller.start()

    # 3. 主循环
    while simulation_app.is_running() and controller.is_running:
        # 获取环境状态 → 发布到 DDS
        env_state = env.scene.get_state()
        sim_state_dds.write_sim_state_data(sim_state)

        # 检查重置命令
        reset_pose_cmd = reset_pose_dds.get_reset_pose_command()
        if reset_pose_cmd == '1':
            env.event_manager.trigger("reset_object_self", env)  # 只重置物体
        elif reset_pose_cmd == '2':
            env.event_manager.trigger("reset_all_self", env)     # 重置整个场景

        # 执行一步控制
        controller.step()
```

### 8.3 所有可用的运行命令（来自 sim_main.py 末尾注释）

> 通用参数说明：`--device cpu` 使用 CPU 物理仿真（无 GPU 时可用），`--enable_cameras` 启用摄像头渲染。

```bash
# ===== G1 + Dex3-1 灵巧手 =====

# G1 + Dex3：抓取放置圆柱体（手臂关节控制模式）
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-Cylinder-G129-Dex3-Joint \    # 任务：圆柱体抓取放置
  --enable_dex3_dds --robot_type g129                   # 启用 Dex3 灵巧手 DDS，机器人型号 G1-29dof

# G1 + Dex3：抓取放置红色方块（手臂关节控制模式）
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-RedBlock-G129-Dex3-Joint \     # 任务：红色方块抓取放置
  --enable_dex3_dds --robot_type g129                   # 启用 Dex3 灵巧手 DDS

# G1 + Dex3：堆叠红绿黄三个方块（手臂关节控制模式）
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-Stack-RgyBlock-G129-Dex3-Joint \         # 任务：堆叠红绿黄方块（Rgy = Red-Green-Yellow）
  --enable_dex3_dds --robot_type g129                   # 启用 Dex3 灵巧手 DDS

# G1 + Dex3：全身协调移动圆柱体（下半身+手臂联动）
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-Move-Cylinder-G129-Dex3-Wholebody \      # 任务：全身协调（Wholebody = 腿+腰+手臂联动）
  --robot_type g129 --enable_dex3_dds                   # 注意：全身任务会自动切换 action_source 为 dds_wholebody

# ===== G1 + Dex1-1 夹爪 =====

# G1 + Dex1：抓取放置圆柱体（夹爪控制模式）
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-Cylinder-G129-Dex1-Joint \     # 任务：圆柱体抓取放置
  --enable_dex1_dds --robot_type g129                   # 启用 Dex1 夹爪 DDS（不是灵巧手，是简单开合夹爪）

# ===== G1 + Inspire 灵巧手 =====

# G1 + Inspire：抓取放置圆柱体（Inspire 灵巧手控制模式）
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-Cylinder-G129-Inspire-Joint \  # 任务：圆柱体抓取放置
  --enable_inspire_dds --robot_type g129                # 启用 Inspire 灵巧手 DDS（第三方灵巧手品牌）

# ===== H1-2 机器人（人形，27 个自由度） =====

# H1-2 + Inspire：抓取放置圆柱体
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-Cylinder-H12-27dof-Inspire-Joint \  # H1-2 机型，27 自由度
  --enable_inspire_dds --robot_type h1_2                     # 注意：H1-2 用 --robot_type h1_2，不是 g129

# H1-2 + Inspire：抓取放置红色方块
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-PickPlace-RedBlock-H12-27dof-Inspire-Joint \  # H1-2 红色方块任务
  --enable_inspire_dds --robot_type h1_2

# H1-2 + Inspire：堆叠红绿黄方块
python sim_main.py --device cpu --enable_cameras \
  --task Isaac-Stack-RgyBlock-H12-27dof-Inspire-Joint \     # H1-2 堆叠任务
  --enable_inspire_dds --robot_type h1_2
```

> **命令规律总结**：
> - 任务名格式：`Isaac-{动作}-{物体}-{机器人型号}-{灵巧手类型}-{控制模式}`
> - 动作：`PickPlace`（抓取放置）、`Stack`（堆叠）、`Move`（移动）、`Pick...Into-Drawer`（放入抽屉）
> - 物体：`Cylinder`（圆柱体）、`RedBlock`（红色方块）、`RgyBlock`（红绿黄方块）
> - 控制模式：`Joint`（关节控制）、`Wholebody`（全身协调）
> - DDS 启用标志必须与灵巧手类型匹配：Dex3 → `--enable_dex3_dds`，Dex1 → `--enable_dex1_dds`，Inspire → `--enable_inspire_dds`

### 8.4 任务名称注册机制

**文件位置**：`tasks/g1_tasks/__init__.py`

所有 G1 任务在这里导入（H1-2 任务在 `tasks/h1-2_tasks/__init__.py` 中同理）：

```python
# --- 抓取放置圆柱体任务（3 种灵巧手）---
from . import pick_place_cylinder_g1_29dof_dex3        # → 注册 ID: Isaac-PickPlace-Cylinder-G129-Dex3-Joint
from . import pick_place_cylinder_g1_29dof_dex1        # → 注册 ID: Isaac-PickPlace-Cylinder-G129-Dex1-Joint
from . import pick_place_cylinder_g1_29dof_inspire     # → 注册 ID: Isaac-PickPlace-Cylinder-G129-Inspire-Joint

# --- 抓取放置红色方块任务（3 种灵巧手）---
from . import pick_place_redblock_g1_29dof_dex1        # → 注册 ID: Isaac-PickPlace-RedBlock-G129-Dex1-Joint
from . import pick_place_redblock_g1_29dof_dex3        # → 注册 ID: Isaac-PickPlace-RedBlock-G129-Dex3-Joint
from . import pick_place_redblock_g1_29dof_inspire     # → 注册 ID: Isaac-PickPlace-RedBlock-G129-Inspire-Joint

# --- 堆叠红绿黄方块任务（3 种灵巧手）---
from . import stack_rgyblock_g1_29dof_dex1             # → 注册 ID: Isaac-Stack-RgyBlock-G129-Dex1-Joint
from . import stack_rgyblock_g1_29dof_dex3             # → 注册 ID: Isaac-Stack-RgyBlock-G129-Dex3-Joint
from . import stack_rgyblock_g1_29dof_inspire          # → 注册 ID: Isaac-Stack-RgyBlock-G129-Inspire-Joint

# --- 抓取方块放入抽屉任务（2 种灵巧手）---
from . import pick_redblock_into_drawer_g1_29dof_dex1  # → 注册 ID: Isaac-Pick-Redblock-Into-Drawer-G129-Dex1-Joint
from . import pick_redblock_into_drawer_g1_29dof_dex3  # → 注册 ID: Isaac-Pick-Redblock-Into-Drawer-G129-Dex3-Joint

# --- 全身协调移动圆柱体任务（3 种灵巧手）---
from . import move_cylinder_g1_29dof_dex1_wholebody    # → 注册 ID: Isaac-Move-Cylinder-G129-Dex1-Wholebody
from . import move_cylinder_g1_29dof_dex3_wholebody    # → 注册 ID: Isaac-Move-Cylinder-G129-Dex3-Wholebody
from . import move_cylinder_g1_29dof_inspire_wholebody # → 注册 ID: Isaac-Move-Cylinder-G129-Inspire-Wholebody
```

**注册链路**：

```
tasks/g1_tasks/__init__.py 的 import 语句
    ↓ 触发每个任务目录下的 __init__.py 执行
    ↓
tasks/g1_tasks/pick_place_cylinder_g1_29dof_dex3/__init__.py 中调用 gym.register()
    ↓ 注册 gym 环境 ID（如 "Isaac-PickPlace-Cylinder-G129-Dex3-Joint"）
    ↓
sim_main.py 中 gym.make(args.task, ...) 根据 --task 参数查找已注册的 ID
    ↓ 找到对应的任务配置类并创建仿真环境
```

**每个任务目录下的 `__init__.py` 大致结构**（以 `pick_place_cylinder_g1_29dof_dex3` 为例）：

```python
import gymnasium as gym
from .pickplace_cylinder_g1_29dof_dex3_joint_env_cfg import (
    PickPlaceCylinderG129Dex3JointEnvCfg,      # 任务配置类（定义场景、动作、观测、奖励等）
    PickPlaceCylinderG129Dex3JointEnvCfg_PLAY,  # 用于推理/演示的配置（通常关闭随机化）
)

# 注册 gym 环境 ID，sim_main.py 的 --task 参数就是这个字符串
gym.register(
    id="Isaac-PickPlace-Cylinder-G129-Dex3-Joint",          # ← 这就是命令行中的 --task 值
    entry_point="isaaclab.envs:ManagerBasedRLEnv",           # 使用 Isaac Lab 的 RL 环境基类
    disable_env_checker=True,                                 # 禁用 gym 环境检查（Isaac Lab 不需要）
    kwargs={
        "env_cfg_entry_point": f"{__name__}.pickplace_cylinder_g1_29dof_dex3_joint_env_cfg:PickPlaceCylinderG129Dex3JointEnvCfg",
        "rsl_rl_cfg_entry_point": None,                       # RSL-RL 策略配置（如有）
    },
)

# 注册 PLAY 模式变体（在 --task 名称后加 `-Play` 即可切换）
gym.register(
    id="Isaac-PickPlace-Cylinder-G129-Dex3-Joint-Play",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.pickplace_cylinder_g1_29dof_dex3_joint_env_cfg:PickPlaceCylinderG129Dex3JointEnvCfg_PLAY",
    },
)
```

> **新增任务的步骤**：
> 1. 在 `tasks/g1_tasks/` 下新建目录（如 `my_new_task_g1_29dof_dex3/`）
> 2. 编写 `*_env_cfg.py` 定义场景、动作、观测、奖励、终止条件
> 3. 在目录下的 `__init__.py` 中调用 `gym.register()` 注册环境 ID
> 4. 在 `tasks/g1_tasks/__init__.py` 中添加 `from . import my_new_task_g1_29dof_dex3`
> 5. 运行时使用 `--task 你注册的ID` 即可启动新任务

---

## 9. 可修改参数速查表

| 你想改什么 | 改哪个文件 | 改哪一行 | 怎么改 |
|-----------|-----------|---------|--------|
| 物体随机范围 | `*_env_cfg.py` | `EventCfg.pose_range` | `"x": [-0.10, 0.10]` 扩大到 ±10cm |
| 控制频率 | 命令行参数 | `--step_hz` | `--step_hz 200` 提高到 200Hz |
| 仿真步长 | `*_env_cfg.py` | `self.sim.dt` | `0.002` → 更精细；`0.01` → 更快 |
| 控制降频比 | `*_env_cfg.py` | `self.decimation` | `4` → 控制频率降为 50Hz |
| 每轮时长 | `*_env_cfg.py` | `episode_length_s` | `30.0` → 给更多时间 |
| 动作幅度 | `*_env_cfg.py` | `ActionsCfg.scale` | `0.5` → 更保守；`2.0` → 更激进 |
| 奖励权重 | `*_env_cfg.py` | `RewardsCfg.weight` | `2.0` → 更注重奖励 |
| 观测内容 | `*_env_cfg.py` | `ObservationsCfg` | 注释掉 `camera_image` → 纯状态控制 |
| 渲染频率 | `*_env_cfg.py` | `render_interval` | `4` → 每 4 步渲染一次 |
| 碰撞精度 | `*_env_cfg.py` | `physx.bounce_threshold_velocity` | `0.001` → 更精确的碰撞 |
| 环境间距 | `*_env_cfg.py` | `env_spacing` | `5.0` → 多环境训练时更宽松 |
| 奖励阈值 | `common_rewards/*.py` | `compute_reward` 参数 | 调整 min_x/max_x 等边界值 |
| 终止条件 | `common_termination/*.py` | `reset_object_estimate` 参数 | 调整有效区域范围 |

---

## 10. 常见问题

### Q1: 安装时报 CUDA 版本不匹配

```bash
# 检查 CUDA 版本
nvcc --version
# 根据实际版本选择 cu121 或 cu126
```

### Q2: Isaac Sim 启动很慢

首次启动需要编译 shader 缓存，可能需要 5-10 分钟。后续启动会快很多。

### Q3: 仿真画面卡顿

```bash
# 降低渲染频率
python sim_main.py --render_interval 4

# 或完全关闭渲染（纯计算模式）
python sim_main.py --no_render
```

### Q4: 内存不足

```bash
# 减少物理仿真精度换取内存
python sim_main.py --physics_dt 0.01 --solver_iterations 2
```

### Q5: 三种灵巧手 DDS 不能同时启用

这是设计如此——`--enable_dex3_dds`、`--enable_dex1_dds`、`--enable_inspire_dds` 三者互斥，程序会检测并报错退出。

### Q6: 全身任务自动切换 action_source

当任务名包含 `Wholebody` 时，`sim_main.py` 会自动将 `action_source` 切换为 `dds_wholebody`，并启用 `enable_wholebody_dds`。无需手动指定。

---

## 11. 参考链接

| 资源 | 链接 |
|------|------|
| 仿真平台仓库 | [unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab) |
| Isaac Lab | [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) |
| unitree_sdk2_python | [unitreerobotics/unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python) |
| CycloneDDS | [eclipse-cyclonedds/cyclonedds](https://github.com/eclipse-cyclonedds/cyclonedds) |
| 遥操作数据采集 | [xr_teleoperate](https://github.com/unitreerobotics/xr_teleoperate) |
| MuJoCo 版仿真（备选） | [unitree_mujoco](https://github.com/unitreerobotics/unitree_mujoco) |
| Dex3-1 DDS 接口文档 | [[Unitree Dex3-1 灵巧手 DDS 通信接口文档]] |

---

## 12. Tag

#机器人 #宇树 #仿真 #IsaacLab #Dex3-1 #G1 #H1-2 #强化学习 #DDS
