# Unitree Isaac Lab 仿真平台代码架构深度解析

> 仓库：[unitree_sim_isaaclab](https://github.com/unitreerobotics/unitree_sim_isaaclab)
> 整理日期：2026-06-19
> 目的：详细梳理代码架构、数据流、关键 API，为后续 VLA 模型集成做准备

---

## 1. 整体架构总览

### 1.1 系统层级图

```
┌─────────────────────────────────────────────────────────┐
│                    sim_main.py（主入口）                  │
│  解析参数 → 创建环境 → 初始化 DDS → 创建控制器 → 主循环   │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
    ┌──────────▼──────────┐    ┌──────────▼──────────┐
    │   Isaac Lab 环境     │    │   DDS 通信层         │
    │   (物理仿真引擎)      │    │   (网络数据交换)      │
    │                      │    │                      │
    │  ┌────────────────┐  │    │  ┌────────────────┐  │
    │  │ 场景 Scene      │  │    │  │ G1RobotDDS     │  │
    │  │  - 机器人       │  │    │  │ Dex3DDS        │  │
    │  │  - 物体         │  │    │  │ SimStateDDS    │  │
    │  │  - 桌子/房间    │  │    │  │ RewardsDDS     │  │
    │  │  - 摄像头       │  │    │  │ ResetPoseDDS   │  │
    │  └────────────────┘  │    │  └────────────────┘  │
    │  ┌────────────────┐  │    └──────────────────────┘
    │  │ 观测 Observations│  │
    │  │  - 关节状态     │  │    ┌──────────────────────┐
    │  │  - 灵巧手状态   │  │    │   动作提供器           │
    │  │  - 摄像头图像   │  │    │   ActionProvider      │
    │  └────────────────┘  │    │                      │
    │  ┌────────────────┐  │    │  DDSActionProvider   │
    │  │ 奖励 Rewards    │  │    │  DDSRLActionProvider │
    │  │ 终止 Terminations│  │    │  FileActionReplay   │
    │  │ 事件 Events     │  │    └──────────┬───────────┘
    │  └────────────────┘  │               │
    └──────────────────────┘    ┌──────────▼──────────┐
                                │  RobotController     │
                                │  (分层控制器)         │
                                │  step() → env.step() │
                                └─────────────────────┘
```

### 1.2 主循环执行流程（sim_main.py）

主循环位于 `sim_main.py` 的 `main()` 函数，每帧执行以下步骤：

```python
# 主循环伪代码（sim_main.py 约 461-573 行）
while simulation_app.is_running() and controller.is_running:

    # ① 收集完整场景状态
    env_state = env.scene.get_state()          # 所有实体的位姿/速度
    env_state_json = sim_state_to_json(env_state)  # 序列化为 JSON
    sim_state = {"init_state": env_state_json, "task_name": args.task}
    sim_state_dds.write_sim_state_data(sim_state)  # 通过 DDS 发布

    # ② 检查远程重置命令
    reset_cmd = reset_pose_dds.get_reset_pose_command()
    if reset_cmd == '1':
        env.event_manager.trigger("reset_object_self", env)  # 只重置物体
    elif reset_cmd == '2':
        env.event_manager.trigger("reset_all_self", env)     # 重置整个场景

    # ③ 执行一步控制（内部包含：获取动作 → 物理仿真 → 计算观测）
    controller.step()
```

### 1.3 关键文件索引

| 文件路径                                     | 职责             | 重要程度  |
| ---------------------------------------- | -------------- | ----- |
| `sim_main.py`                            | 主入口，参数解析，主循环   | ⭐⭐⭐⭐⭐ |
| `tasks/common_observations/*.py`         | 观测函数（读取状态）     | ⭐⭐⭐⭐⭐ |
| `tasks/common_rewards/*.py`              | 奖励函数（读取物体位置）   | ⭐⭐⭐⭐⭐ |
| `tasks/common_scene/*.py`                | 场景定义（物体、桌子、房间） | ⭐⭐⭐⭐  |
| `tasks/common_config/robot_configs.py`   | 机器人预设配置        | ⭐⭐⭐⭐  |
| `tasks/common_config/camera_configs.py`  | 摄像头预设配置        | ⭐⭐⭐⭐  |
| `action_provider/*.py`                   | 动作提供器（控制信号来源）  | ⭐⭐⭐⭐⭐ |
| `dds/*.py`                               | DDS 通信模块       | ⭐⭐⭐⭐  |
| `layeredcontrol/robot_control_system.py` | 机器人控制器         | ⭐⭐⭐   |
| `tasks/common_event/event_manager.py`    | 事件管理（物体重置）     | ⭐⭐⭐   |
| `tasks/common_termination/*.py`          | 终止条件           | ⭐⭐⭐   |
|                                          |                |       |

---

## 2. 场景信息读取（Observations）

### 2.1 观测系统架构

Isaac Lab 的观测系统采用 **ObsGroup + ObsTerm** 模式。每个任务在 `*_env_cfg.py` 中定义一个 `ObservationsCfg`，包含一个或多个 `ObsGroup`，每个 Group 包含多个 `ObsTerm`。

以 `pick_place_cylinder_g1_29dof_dex3` 任务为例：

```python
# 文件：tasks/g1_tasks/pick_place_cylinder_g1_29dof_dex3/
#       pickplace_cylinder_g1_29dof_dex3_joint_env_cfg.py

@configclass
class ObservationsCfg:
    @configclass
    class PolicyCfg(ObsGroup):
        # 观测项 1：全身关节状态 → [batch, 87]
        robot_joint_state = ObsTerm(func=mdp.get_robot_boy_joint_states)

        # 观测项 2：灵巧手关节状态 → [batch, 14]
        robot_gipper_state = ObsTerm(func=mdp.get_robot_dex3_joint_states)

        # 观测项 3：摄像头图像 → 占位符 tensor，实际图像走共享内存
        camera_image = ObsTerm(func=mdp.get_camera_image)

        def __post_init__(self):
            self.enable_corruption = False    # 禁用观测噪声
            self.concatenate_terms = False    # 不拼接，返回 dict

    policy: PolicyCfg = PolicyCfg()
```

**关键点**：`concatenate_terms = False` 意味着观测返回的是一个字典，每个 key 对应一个 ObsTerm 的名字，value 是对应的 tensor。这很关键——后续 VLA 集成时可以分别获取图像和状态。

### 2.2 机器人全身关节状态

**文件**：`tasks/common_observations/g1_29dof_state.py`

**核心函数**：`get_robot_boy_joint_states(env, enable_dds=True) -> torch.Tensor`

**返回值**：`[batch, 87]` = 29 个关节位置 + 29 个关节速度 + 29 个关节力矩

**数据来源**：

```python
# 从 Isaac Lab 的 Articulation 数据中读取
robot = env.scene["robot"]
joint_pos = robot.data.joint_pos        # [num_envs, total_joints] 所有关节位置
joint_vel = robot.data.joint_vel        # [num_envs, total_joints] 所有关节速度
torque = robot.data.applied_torque      # [num_envs, total_joints] 施加的力矩
```

**关节索引映射**（Isaac Lab 内部顺序 → DDS/外部顺序）：

```python
# G1 29DOF 的关节重排序索引
joint_indices = [0, 3, 6, 9, 13, 17,   # 左腿 6 个关节
                 1, 4, 7, 10, 14, 18,   # 右腿 6 个关节
                 2, 5, 8, 11, 15, 19,   # 腰部 3 个 + 左臂 3 个
                 21, 23, 25, 27,        # 左臂剩余 4 个
                 12, 16, 20,            # 右臂前 3 个
                 22, 24, 26, 28]        # 右臂后 4 个
# 共 29 个关节，用 torch.gather 重排序
```

**DDS 发布**：函数内部会将关节数据通过 `g1_robot_dds.write_robot_state()` 发布到 DDS 网络，频率限制在 50Hz（20ms 间隔）。

**关节分组详解**：

| 关节组 | 数量 | 索引范围 | 说明 |
|--------|------|---------|------|
| 左腿 | 6 | 0-5 | hip_roll/pitch, knee, ankle_roll/pitch, toe |
| 右腿 | 6 | 6-11 | 同上 |
| 腰部 | 3 | 12-14 | yaw/roll/pitch |
| 左臂 | 7 | 15-21 | shoulder_pitch/roll/yaw, elbow, wrist_pitch/roll/yaw |
| 右臂 | 7 | 22-28 | 同上 |

### 2.3 IMU 数据（惯性测量单元）

**文件**：`tasks/common_observations/g1_29dof_state.py`

**核心函数**：`get_robot_imu_data(env, use_torso_imu=True) -> torch.Tensor`

**返回值**：`[batch, 13]` = 位置(3) + 四元数(4, wxyz) + 体坐标系加速度(3) + 体坐标系陀螺仪(3)

**数据来源**：

```python
# 优先从躯干 IMU 链路读取
robot = env.scene["robot"]
body_names = robot.data.body_names  # 所有 body link 名称列表

# 找到 "imu_in_torso" 对应的 body index
imu_idx = body_names.index("imu_in_torso")

# 读取该 body link 的世界坐标系位姿和速度
pose = robot.data.body_link_pose_w[:, imu_idx, :]  # [num_envs, 7] pos+quat
vel = robot.data.body_link_vel_w[:, imu_idx, :]     # [num_envs, 6] lin+ang

# 如果找不到 torso IMU，回退到 root_state_w
if imu_idx is None:
    root_state = robot.data.root_state_w  # [num_envs, 13]
```

**加速度计算**（速度微分 + 重力补偿）：

```python
# 当前速度 - 上一帧速度 = 加速度
accel = (current_vel - last_vel) / dt

# 重力补偿：在世界坐标系中减去重力加速度
accel_world[:, 2] += 9.81  # 补偿 z 轴重力

# 旋转到体坐标系：用四元数构建旋转矩阵
R = quaternion_to_rotation_matrix(quat)  # [3, 3]
accel_body = R.T @ accel_world           # 世界系 → 体坐标系
```

### 2.4 Dex3 灵巧手状态

**文件**：`tasks/common_observations/dex3_state.py`

**核心函数**：`get_robot_dex3_joint_states(env, enable_dds=True) -> torch.Tensor`

**返回值**：`[batch, 14]` = 左手 7 个关节位置 + 右手 7 个关节位置

**关节索引映射**：

```python
# Dex3-1 灵巧手的关节索引（从 Isaac Lab 全关节向量中提取）
dex3_indices = [31, 37, 41, 30, 36, 29, 35,   # 左手 7 个关节
                34, 40, 42, 33, 39, 32, 38]    # 右手 7 个关节
```

**DDS 发布**：将左手和右手数据分别发布到 `rt/dex3/left/state` 和 `rt/dex3/right/state`。

**Dex3 每个手指的关节结构**：

| 手指 | 关节数 | 说明 |
|------|--------|------|
| 拇指 | 3 | 拇指对掌 + 2 个指节弯曲 |
| 食指 | 2 | 2 个指节弯曲 |
| 中指 | 2 | 2 个指节弯曲 |
| **合计** | **7/手** | 左右共 14 个 |

### 2.5 其他灵巧手状态

**Dex1-1 夹爪**（`tasks/common_observations/gripper_state.py`）：
- 返回 `[batch, 2]`：左右夹爪各 1 个开合关节
- 索引：`[31, 29]`

**Inspire 灵巧手**（`tasks/common_observations/inspire_state.py`）：
- 返回 `[batch, 12]`：左右各 6 个关节
- 索引：`[36, 37, 35, 34, 48, 38, 31, 32, 30, 29, 43, 33]`

### 2.6 摄像头图像读取

**文件**：`tasks/common_observations/camera_state.py`

**核心函数**：`get_camera_image(env) -> torch.Tensor`

**实际图像获取**：

```python
# 从 Isaac Lab 的 Camera 数据中读取 RGB 图像
front_img = env.scene["front_camera"].data.output["rgb"][0]      # [480, 640, 3]
left_img = env.scene["left_wrist_camera"].data.output["rgb"][0]  # [480, 640, 3]
right_img = env.scene["right_wrist_camera"].data.output["rgb"][0] # [480, 640, 3]

# 注意：[0] 表示取第一个环境（num_envs=1 时）
# 返回的是 torch.Tensor，在 GPU 上，需要 .cpu().numpy() 转到 CPU
```

**图像处理流程**：

```
Isaac Lab Camera 渲染 (GPU tensor, RGB)
    ↓
numpy 转换 (CPU, RGB)
    ↓
RGB → BGR 转换 (OpenCV 格式)
    ↓
异步队列 (maxsize=1, 丢弃旧帧)
    ↓
MultiImageWriter 写入共享内存
    ↓
外部程序读取（teleimager / 数据采集）
```

**关键细节**：
- 函数返回一个占位符 `torch.zeros((1, 480, 640, 3))`，**不是实际图像**
- 实际图像通过共享内存传输给外部消费者
- 写入频率受 `write_interval_steps` 控制（默认每 2 步写一次）
- 支持 JPEG 压缩（`camera_jpeg=True`，质量 85%）

**摄像头配置**（`tasks/common_config/camera_configs.py`）：

| 摄像头 | 名称 | 安装位置 | 分辨率 |
|--------|------|---------|--------|
| 前置 | `front_camera` | `Robot/d435_link/front_cam` | 480×640 |
| 左手腕 | `left_wrist_camera` | `Robot/left_hand_camera_base_link/left_wrist_camera` | 480×640 |
| 右手腕 | `right_wrist_camera` | `Robot/right_hand_camera_base_link/right_wrist_camera` | 480×640 |
| 世界视角 | `world_camera` | `/World/PerspectiveCamera` | 480×640 |

### 2.7 完整场景状态获取

**主循环中的全场景状态**：

```python
# sim_main.py 主循环
env_state = env.scene.get_state()
```

`env_state` 是一个字典，包含场景中所有实体的状态：
- 所有 Articulation（机器人）的关节位置/速度
- 所有 RigidObject（物体）的位姿/速度
- 可以用于完整还原场景（如数据回放、场景序列化）

序列化后通过 `sim_state_dds` 发布到 DDS 话题 `rt/sim_state`。

---

## 3. 目标物体感知

### 3.1 物体位置读取 API

**所有奖励函数和终止条件都使用同一个 API 读取物体位置**：

```python
object: RigidObject = env.scene["object"]  # 按名称从场景中获取实体
pos = object.data.root_pos_w               # [num_envs, 3] 世界坐标系位置

# 分量访问
x = pos[:, 0]   # X 坐标
y = pos[:, 1]   # Y 坐标
z = pos[:, 2]   # Z 坐标（高度）
```

**可用的物体数据 API**：

| API | 形状 | 说明 |
|-----|------|------|
| `object.data.root_pos_w` | `[N, 3]` | 世界坐标系位置 |
| `object.data.root_quat_w` | `[N, 4]` | 世界坐标系四元数 |
| `object.data.root_vel_w` | `[N, 6]` | 世界坐标系速度（线速度+角速度） |
| `object.data.root_state_w` | `[N, 13]` | 完整状态：pos(3)+quat(4)+lin_vel(3)+ang_vel(3) |

**注意**：当前代码的奖励/终止只用了 `root_pos_w`，没用朝向和速度。VLA 集成时可以考虑加入。

### 3.2 场景中的物体定义（完整详解）

每个任务都有一个场景基类（`tasks/common_scene/*.py`），定义了房间、桌子、物体、灯光、摄像头。机器人不在此定义，由任务 env_cfg 中的 `G1RobotPresets` 添加。

#### 3.2.1 场景基类一览

| 文件 | 类名 | 物体 | 仓库模型 |
|------|------|------|---------|
| `base_scene_pickplace_cylindercfg.py` | `TableCylinderSceneCfg` | 1 个圆柱体 | `warehouse.usd` |
| `base_scene_pickplace_redblock.py` | `TableRedBlockSceneCfg` | 1 个红色方块 | `small_warehouse_digital_twin.usd` |
| `base_scene_stack_rgyblock.py` | `TableRedGreenYellowBlockSceneCfg` | 红+黄+绿 3 个方块 | `small_warehouse_digital_twin.usd` |
| `base_scene_pick_redblock_into_drawer.py` | `TablePickRedblockIntoDrawerSceneCfg` | 1 个红色方块 + 柜子（铰接体） | `small_warehouse_digital_twin.usd` |
| `base_scene_pickplace_cylindercfg_wholebody.py` | `TableCylinderSceneCfgWH` | 1 个圆柱体 | `small_warehouse_digital_twin.usd` |

#### 3.2.2 场景实体结构（以圆柱体任务为例）

```python
# 文件：tasks/common_scene/base_scene_pickplace_cylindercfg.py

@configclass
class TableCylinderSceneCfg(InteractiveSceneCfg):

    # ── 房间墙壁 ──
    room_walls = AssetBaseCfg(
        prim_path="/World/envs/env_.*/Room",
        pos=[0.0, 0.0, 0],
        rot=[1.0, 0.0, 0.0, 0.0],        # 四元数 [w, x, y, z]，identity = 无旋转
        spawn=UsdFileCfg(usd_path="{ISAAC_NUCLEUS_DIR}/Environments/Simple_Warehouse/warehouse.usd"),
    )

    # ── 桌子（6 张，网格分布）──
    packing_table  = AssetBaseCfg(pos=[0.0,  0.55,  -0.2])   # 正面中央
    packing_table_2 = AssetBaseCfg(pos=[-3.5, 0.55,  -0.2])  # 正面左侧
    packing_table_3 = AssetBaseCfg(pos=[3.5,  0.55,  -0.2])  # 正面右侧
    packing_table_4 = AssetBaseCfg(pos=[3.5,  -5.0,  -0.2])  # 背面右侧
    packing_table_5 = AssetBaseCfg(pos=[-3.5, -5.0,  -0.2])  # 背面左侧
    packing_table_6 = AssetBaseCfg(pos=[0.0,  -5.0,  -0.2])  # 背面中央
    # 所有桌子：kinematic_enabled=True（固定不动），z=-0.2

    # ── 物体：圆柱体 ──
    object = RigidObjectCfg(
        prim_path="/World/envs/env_.*/Object",
        pos=[-0.35, 0.40, 0.84],          # 初始位置：桌上（z=0.84 = 桌面高度）
        rot=[1, 0, 0, 0],                 # 无旋转
        spawn=sim_utils.CylinderCfg(
            radius=0.018,                  # 半径 1.8cm
            height=0.35,                   # 高度 35cm（细长圆柱）
            mass=0.4,                      # 质量 0.4kg
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(0.15, 0.15, 0.15),  # 深灰色
                metallic=1.0,                        # 金属质感
            ),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                kinematic_enabled=False,     # 动态物体（受物理引擎控制）
                disable_gravity=False,       # 受重力
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            material_props=sim_utils.MaterialPropertiesCfg(
                friction_combine_mode="max",     # 摩擦取最大值
                restitution_combine_mode="min",  # 弹性取最小值
                static_friction=1.5,             # 静摩擦
                dynamic_friction=1.5,            # 动摩擦
                restitution=0.0,                 # 无弹性
            ),
        ),
    )

    # ── 灯光 ──
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DomeLightCfg(
            color=(0.75, 0.75, 0.75),
            intensity=3000.0,               # 强光
        ),
    )

    # ── 世界摄像头（第三人称视角）──
    world_camera = CameraBaseCfg.get_camera_config(
        prim_path="/World/PerspectiveCamera",
        pos_offset=(-0.1, 3.6, 1.6),       # 在机器人后方高处
        rot_offset=(-0.00617, 0.00617, 0.70708, -0.70708),
        focal_length=16.5,
    )
```

#### 3.2.3 各任务物体物理参数对比

| 参数 | 圆柱体 | 红色方块 | 堆叠方块 | 抽屉方块 |
|------|--------|---------|---------|---------|
| **形状** | 圆柱 r=1.8cm, h=35cm | 立方体 6cm | 立方体 5cm | 立方体 5cm |
| **质量** | 0.4 kg | 1.0 kg | 1.0 kg/个 | **3.0 kg** |
| **静摩擦** | 1.5 | **10** | **10** | **10** |
| **动摩擦** | 1.5 | 1.5 | 0.5 | 0.5 |
| **弹性** | 0.0 | 0.01 | 0.0 | 0.0 |
| **颜色** | 深灰金属 | 纯红 | 红/黄/绿 | 红 |
| **初始高度 z** | 0.84 | 0.84 | 0.84 | 0.84 |
| **物体数量** | 1 | 1 | 3 | 1+柜子 |

#### 3.2.4 抽屉任务的特殊场景（最复杂）

抽屉任务场景包含一个**铰接体**（`ArticulationCfg`），不是简单的刚体：

```python
# 文件：tasks/common_scene/base_scene_pick_redblock_into_drawer.py

# 柜子（铰接体，有可动关节）
cabinet = ArticulationCfg(
    prim_path="/World/envs/env_.*/Cabinet",
    spawn=UsdFileCfg(usd_path=".../cabinet_collider.usd"),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(-2.5, -4.35, 0.45),              # 柜子位置
        rot=(0.7071, 0, 0, 0.7071),            # 绕 Z 轴旋转 90°
        joint_pos={
            "door_left_joint": 0.0,            # 左门：关闭
            "door_right_joint": 0.0,           # 右门：关闭
            "drawer_bottom_joint": 0.0,        # 下抽屉：关闭
            "drawer_top_joint": 0.15,          # 上抽屉：微开（15%）
        },
    ),
    actuators={
        # 抽屉关节驱动器
        "drawers": ImplicitActuatorCfg(
            joint_names_expr=["drawer_top_joint", "drawer_bottom_joint"],
            effort_limit_sim=100.0,            # 最大力矩 100Nm
            velocity_limit_sim=100.0,
            stiffness=100.0,                   # 刚度（位置控制增益）
            damping=1.0,                       # 阻尼
        ),
        # 门关节驱动器
        "doors": ImplicitActuatorCfg(
            joint_names_expr=["door_left_joint", "door_right_joint"],
            effort_limit_sim=100.0,
            velocity_limit_sim=100.0,
            stiffness=100.0,
            damping=1.0,
        ),
    },
)

# 柜子坐标系追踪器（用于感知抽屉把手位置）
cabinet_frame = FrameTransformerCfg(
    prim_path="/World/envs/env_.*/Cabinet/cabinet/sektion",       # 基准：柜体
    target_frames=[FrameTransformerCfg.FrameCfg(
        prim_path="/World/envs/env_.*/Cabinet/cabinet/drawer_handle_bottom",  # 目标：下抽屉把手
        name="drawer_handle_bottom",
        offset=OffsetCfg(
            pos=(0.305, 0.0, 0.01),          # 把手偏移
            rot=(0.5, 0.5, -0.5, -0.5),      # 对齐末端执行器坐标系
        ),
    )],
)
```

**抽屉任务的关键差异**：
- 没有桌子（`packing_table` 被注释掉），物体直接放在柜子旁边
- 物体质量 3.0kg（其他任务最大 1.0kg），更难抓取
- 有 4 个可动关节（2 个抽屉 + 2 个门）
- 有 `FrameTransformerCfg` 追踪抽屉把手位置（可用于 VLA 感知目标位置）

#### 3.2.5 全身任务的特殊场景

```python
# 文件：tasks/common_scene/base_scene_pickplace_cylindercfg_wholebody.py

# 只有 2 张桌子（不是 6 张），且桌子有旋转
packing_table1 = AssetBaseCfg(
    pos=[-2.35644, -3.45572, -0.2],
    rot=[0.70091, 0.0, 0.0, 0.71325],   # 约 90° 旋转
    usd_path=".../PackingTable_2/PackingTable.usd",  # 不同的桌子模型
)
packing_table2 = AssetBaseCfg(
    pos=[-3.97225, -4.3424, -0.2],
    rot=[1, 0, 0, 0],                    # 无旋转
    usd_path=".../PackingTable/PackingTable.usd",    # 标准桌子模型
)
```

#### 3.2.6 坐标系说明

所有场景使用**世界坐标系 XYZ**：
- **Z 轴**朝上：物体放在 z=0.84（桌面高度），桌子在 z=-0.2，柜子在 z=0.45
- **X、Y 轴**水平：圆柱体任务用正/小负坐标，仓库任务用负坐标（~-4.x）
- 四元数格式：**[w, x, y, z]**（Isaac Lab 的 `rot` 参数用 w-first）
- 摄像头偏移使用 **ROS 约定**

#### 3.2.7 场景实体引用方式

```python
# 在奖励函数/终止条件/观测函数中，通过字符串名称访问场景实体
robot = env.scene["robot"]           # 机器人（由 robot_configs.py 定义）
obj = env.scene["object"]            # 物体（由场景基类定义）
red = env.scene["red_block"]         # 堆叠任务的红色方块
cabinet = env.scene["cabinet"]       # 抽屉任务的柜子
camera = env.scene["front_camera"]   # 摄像头（由任务 env_cfg 添加）
```

**注意**：场景基类不定义机器人，机器人由每个任务的 `ObjectTableSceneCfg` 中通过 `G1RobotPresets` 添加。

### 3.3 奖励函数中的目标区域判定

**文件**：`tasks/common_rewards/base_reward_pickplace_cylindercfg.py`

**核心逻辑**：

```python
def compute_reward(env, object_cfg,
                   min_x, max_x, min_y, max_y, min_height,        # 有效区域
                   post_min_x, post_max_x,                        # 目标区域
                   post_min_y, post_max_y,
                   post_min_height, post_max_height):

    # 1. 读取物体位置
    object_pos = env.scene[object_cfg.name].data.root_pos_w
    x, y, z = object_pos[:, 0], object_pos[:, 1], object_pos[:, 2]

    # 2. 判断是否在有效区域内（没掉出去）
    done = (min_x < x < max_x) and (min_y < y < max_y) and (z > min_height)

    # 3. 判断是否到达目标位置
    done_post = (post_min_x < x < post_max_x) and \
                (post_min_y < y < post_max_y) and \
                (post_min_height < z < post_max_height)

    # 4. 返回奖励值
    # 物体不在有效区域 → -1.0（失败）
    # 物体在有效区域但未到目标 → 0.0（进行中）
    # 物体到达目标位置 → +1.0（成功）
```

**圆柱体任务的默认阈值**：

| 区域 | X 范围 | Y 范围 | Z 范围 |
|------|--------|--------|--------|
| 有效区域 | [-0.42, 1.0] | [0.2, 0.7] | > 0.5 |
| 目标位置 | [0.28, 0.96] | [0.24, 0.57] | [0.81, 0.9] |

**堆叠任务的层级奖励**（`tasks/common_rewards/base_reward_stack_rgyblock.py`）：

```python
# 三个方块都不在有效区域 → -1.0
# 第一个方块（底座）到位 → 0.3
# 前两个方块到位 → 0.6
# 三个方块全部到位 → 1.0
```

### 3.4 终止条件（完整详解）

所有终止函数都做同一件事：检测物体是否**超出有效区域**（掉出去了），如果是则终止当前 episode。**不检测成功**——成功由奖励函数 `reward=1.0` 体现，但不会提前终止。

#### 3.4.1 通用判定逻辑

```python
# 所有终止函数的核心逻辑
def reset_object_estimate(env, object_cfg, min_x, max_x, min_y, max_y, min_height):
    object = env.scene[object_cfg.name]          # 按名称获取物体
    pos = object.data.root_pos_w                 # [num_envs, 3] 世界坐标

    x, y, z = pos[:, 0], pos[:, 1], pos[:, 2]

    # 判断物体是否在有效区域内
    in_x = (min_x < x) and (x < max_x)          # X 在范围内
    in_y = (min_y < y) and (y < max_y)           # Y 在范围内
    in_z = (z > min_height)                       # 高度足够（没掉地上）

    in_bounds = in_x and in_y and in_z

    return not in_bounds   # True = 终止（物体出界），False = 继续
```

**注意**：代码用 Python `and` 而非 torch `&`，多环境并行时可能有 bug，但单环境（`num_envs=1`）下正常工作。

#### 3.4.2 四个终止函数的参数对比

| 文件 | 引用物体 | 有效区域 X | 有效区域 Y | 最低高度 | 说明 |
|------|---------|-----------|-----------|---------|------|
| `base_termination_pick_place_cylinder.py` | `"object"` | [-0.42, 1.0] | [0.2, 0.7] | 0.5 | 圆柱体任务 |
| `base_termination_pick_place_redblock.py` | `"object"` | [-5.4, -2.9] | [-5.05, -2.8] | 0.5 | 红色方块任务 |
| `base_termination_stack_rgyblock.py` | 3 个方块 | [-5.4, -2.9] | [-5.05, -2.8] | 0.5 | 堆叠任务（任一方块出界即终止） |
| `base_termination_pick_redblock_into_drawer.py` | `"object"` | [-2.7, -2.2] | [-4.15, -3.55] | **0.2** | 抽屉任务（区域更小，高度阈值更低） |

#### 3.4.3 堆叠任务的特殊逻辑

堆叠任务检测 3 个方块，**任一出界即终止**：

```python
# 文件：tasks/common_termination/base_termination_stack_rgyblock.py
def reset_object_estimate(env,
                          red_block_cfg,      # SceneEntityCfg("red_block")
                          yellow_block_cfg,   # SceneEntityCfg("yellow_block")
                          green_block_cfg,    # SceneEntityCfg("green_block")
                          min_x, max_x, min_y, max_y, min_height):

    # 分别检测三个方块是否在有效区域内
    red_in_bounds = check_bounds(env, red_block_cfg, ...)
    yellow_in_bounds = check_bounds(env, yellow_block_cfg, ...)
    green_in_bounds = check_bounds(env, green_block_cfg, ...)

    # 任一方块出界 → 终止
    all_in_bounds = red_in_bounds and yellow_in_bounds and green_in_bounds
    return not all_in_bounds
```

#### 3.4.4 终止条件与奖励函数的关系

```
Episode 运行中
    │
    ├── 每步检查终止条件
    │       │
    │       ├── 物体在有效区域内 → 继续
    │       └── 物体出界（掉了） → 终止 episode，重置环境
    │
    ├── 每步计算奖励
    │       │
    │       ├── 物体在目标位置 → reward = +1.0（成功）
    │       ├── 物体在有效区域但未到目标 → reward = 0.0（进行中）
    │       └── 物体出界 → reward = -1.0（失败，同时触发终止）
    │
    └── 达到 episode_length_s（20秒）→ 超时终止
```

**关键点**：成功（物体到位）不会提前终止 episode，会继续运行直到超时。只有物体掉出有效区域才会提前终止。

#### 3.4.5 各任务有效区域可视化

```
圆柱体任务（俯视图）：
  Y
  0.7 ┌─────────────────────┐
      │    有效区域           │
  0.2 │    X: [-0.42, 1.0]  │
      └─────────────────────┘
     -0.42                  1.0  → X

抽屉任务（俯视图，区域更紧凑）：
  Y
  -3.55 ┌────────┐
        │ 有效区域 │
  -4.15 │ X:[-2.7,-2.2] │
        └────────┘
       -2.7     -2.2  → X
```

### 3.5 物体随机化（事件系统）

**文件**：`tasks/common_event/event_manager.py`

每个任务在 `EventCfg` 中定义物体位置随机化：

```python
# 任务 env_cfg 中的事件配置
reset_object = EventTermCfg(
    func=mdp.reset_root_state_uniform,
    mode="reset",  # 每次环境重置时触发
    params={
        "pose_range": {
            "x": [-0.05, 0.05],   # X 轴随机 ±5cm
            "y": [-0.05, 0.05],   # Y 轴随机 ±5cm
        },
        "velocity_range": {},      # 速度不随机（从静止开始）
        "asset_cfg": SceneEntityCfg("object"),
    },
)
```

**SimpleEventManager**（DDS 远程重置用）：

```python
# 在 env_cfg.__post_init__ 中注册
self.event_manager = SimpleEventManager()

# 只重置物体位置
self.event_manager.register("reset_object_self", SimpleEvent(
    func=lambda env: base_mdp.reset_root_state_uniform(
        env, torch.arange(env.num_envs, device=env.device),
        pose_range={"x": [-0.05, 0.05], "y": [0.0, 0.05]},
        velocity_range={},
        asset_cfg=SceneEntityCfg("object"),
    )
))

# 重置整个场景（机器人回到初始位姿 + 物体重置）
self.event_manager.register("reset_all_self", SimpleEvent(
    func=lambda env: base_mdp.reset_scene_to_default(
        env, torch.arange(env.num_envs, device=env.device))
))
```

---

## 4. 动作规划与控制

### 4.1 控制系统架构

```
sim_main.py 主循环
    │
    ├── controller.step()                    # RobotController
    │       │
    │       ├── action_provider.get_action(env)  # 获取动作 tensor
    │       │       │
    │       │       ├── DDSActionProvider         # 从 DDS 接收外部命令
    │       │       ├── DDSRLActionProvider       # 本地 RL 策略推理
    │       │       └── FileActionProviderReplay  # 回放录制数据
    │       │
    │       ├── env.step(action)             # Isaac Lab 执行物理仿真
    │       │       ├── 应用关节目标位置
    │       │       ├── PhysX 物理求解
    │       │       ├── 计算观测（触发 observation 函数）
    │       │       ├── 计算奖励
    │       │       └── 检查终止条件
    │       │
    │       └── time.sleep()                 # 频率控制
    │
    └── （下一轮循环）
```

### 4.2 DDSActionProvider（遥操作模式）

**文件**：`action_provider/action_provider_dds.py`

这是最常用的动作来源——从外部程序（如遥操作系统）接收关节控制命令。

**`get_action(env)` 核心逻辑**：

```python
def get_action(self, env) -> Optional[torch.Tensor]:
    num_joints = env.scene["robot"].data.joint_pos.shape[1]

    # 1. 创建零动作 tensor
    action = torch.zeros((1, num_joints), device=env.device)

    # 2. 从 DDS 读取手臂控制命令（29 个电机的目标位置）
    robot_cmd = self.robot_dds.get_robot_command()  # dict: {motor_pos: [...29个...]}
    arm_positions = robot_cmd["motor_pos"][15:29]   # 索引 15-28 = 14 个手臂关节

    # 3. 映射到仿真关节索引
    # DDS 中的手臂关节索引 (0-13) → 仿真中的实际关节索引
    action[:, self.arm_sim_indices] = torch.tensor(arm_positions)

    # 4. 从灵巧手 DDS 读取手部控制命令
    hand_cmd = self.hand_dds.get_hand_command()
    action[:, self.hand_sim_indices] = torch.tensor(hand_cmd)

    return action
```

**关节映射表**：

```
DDS 命令格式（29 个电机）：
[左腿6, 右腿6, 腰3, 左臂7, 右臂7]
 0-5    6-11  12-14  15-21  22-28

手臂关节提取：motor_cmd[15:29] → 14 个值
映射到仿真关节：arm_sim_indices（由 robot_configs.py 中的预设决定）
```

### 4.3 DDSRLActionProvider（全身 RL 策略模式）

**文件**：`action_provider/action_provider_wh_dds.py`

这是最复杂的动作提供器——在本地运行一个 RL 策略网络，同时允许 DDS 覆盖手臂控制。

**策略模型加载**：

```python
def load_policy(self, path: str):
    if path.endswith('.onnx'):
        # ONNX Runtime 推理
        import onnxruntime as ort
        session = ort.InferenceSession(path)
        def run_onnx(obs):
            return session.run(None, {"obs": obs})[0]
        self.policy = run_onnx

    elif path.endswith('.pt'):
        # TorchScript 推理
        model = torch.jit.load(path)
        self.policy = lambda obs: model(obs)
```

**观测计算**（策略的输入）：

```python
def compute_current_observations(self, env) -> torch.Tensor:
    robot = env.scene["robot"]

    # 1. 角速度（体坐标系）
    ang_vel = robot.data.root_ang_vel_b          # [1, 3]

    # 2. 重力投影（体坐标系）
    gravity = robot.data.projected_gravity_b      # [1, 3]

    # 3. 运动命令 [vx, vy, vz, heading]
    command = self.run_command_dds.get_run_command()  # [4]

    # 4. 关节位置差（当前 - 默认）
    joint_pos = robot.data.joint_pos              # [1, num_joints]
    joint_pos_delta = joint_pos - self.default_joint_pos  # [1, 26]

    # 5. 关节速度
    joint_vel = robot.data.joint_vel              # [1, 26]

    # 6. 上一步动作
    last_action = self.last_action                # [1, 29]

    # 拼接：3+3+4+26+26+29 = 91 维
    obs = torch.cat([ang_vel, gravity, command,
                     joint_pos_delta, joint_vel, last_action], dim=-1)

    # 放入循环缓冲区（保留最近 10 步）
    self.obs_buffer.append(obs)
    full_obs = self.obs_buffer.get()  # [1, 910] = 91 × 10

    return full_obs
```

**动作执行流程**：

```python
def get_action(self, env) -> Optional[torch.Tensor]:
    # 1. 计算观测
    obs = self.compute_current_observations(env)

    # 2. 策略推理
    action = self.policy(obs)  # [1, 29] 关节目标位置

    # 3. 设置腿部和手臂关节目标
    action[:, leg_indices] = rl_output[:, leg_indices]
    action[:, arm_indices] = rl_output[:, arm_indices]
    action[:, waist_indices] = self.default_waist_pos  # 腰部用默认值

    # 4. DDS 手臂覆盖（遥操作可以覆盖 RL 的手臂输出）
    arm_cmd = self.robot_dds.get_robot_command()
    if arm_cmd is not None:
        action[:, arm_sim_indices] = arm_cmd["motor_pos"][15:29]

    # 5. 动作后处理
    action = self.delay_buffer(action)  # 延迟缓冲
    action = torch.clamp(action, -1.0, 1.0)  # 限幅
    action = action * 0.25 + self.default_pos  # 缩放 + 偏移

    # 6. 应用手部命令
    hand_cmd = self.hand_dds.get_hand_command()
    action[:, hand_sim_indices] = hand_cmd

    # 7. 内部步进仿真 4 次（全身任务的 decimation=4）
    for _ in range(4):
        env.scene.set_joint_position_target(action)
        env.scene.write_data_to_sim()
        env.sim.step(render=False)
        env.scene.update(action)

    # 8. 渲染 + 重新计算观测
    env.sim.render()

    return action
```

### 4.4 FileActionProviderReplay（数据回放模式）

**文件**：`action_provider/action_provider_replay.py`

从 JSON 文件回放之前录制的轨迹数据，主要用于：
- 数据验证
- 重新采集观测数据（图像 + 状态）生成训练数据集

### 4.5 RobotController（分层控制器，完整详解）

**文件**：`layeredcontrol/robot_control_system.py`

控制器是连接动作提供器和仿真环境的桥梁，负责频率控制和性能监控。

#### 4.5.1 ControlConfig 配置类

```python
@dataclass
class ControlConfig:
    step_hz: int = 500              # 控制频率（500Hz = 每 2ms 执行一次）
    replay_mode: bool = False       # 回放模式（跳过 env.step）
    use_rl_action_mode: bool = False # RL 模式（DDSRLActionProvider 内部自行步进）
```

#### 4.5.2 RobotController 内部状态

```python
class RobotController:
    def __init__(self, env, config: ControlConfig):
        self.env = env
        self.config = config
        self.action_provider = None     # 动作提供器（外部注入）
        self.is_running = False         # 运行标志

        # 频率控制
        self._step_interval = 1.0 / config.step_hz   # 2ms (500Hz)
        self._last_step_time = 0.0
        self._sleep_threshold = 0.0002    # 200us：低于此值不 sleep
        self._sleep_adjustment = 0.0001   # 100us：sleep 补偿

        # 动作缓存（当动作提供器返回 None 时使用上一次的动作）
        self._last_action = torch.zeros(
            len(env.scene["robot"].data.joint_names),
            device=env.device
        )

        # 性能统计
        self.step_count = 0
        self._profile_interval = 2000    # 每 2000 步打印一次性能
```

#### 4.5.3 step() 方法完整流程

```python
def step(self):
    if not self.is_running:
        return

    # ── 阶段 1：获取动作 ──
    # 同步调用，无线程竞争
    action = self.action_provider.get_action(self.env)

    if action is not None:
        self._last_action = action      # 缓存最新动作
    else:
        action = self._last_action      # 无新动作时用缓存

    # ── 阶段 2：执行仿真步进 ──
    with torch.inference_mode():
        if self.config.replay_mode or self.config.use_rl_action_mode:
            # 回放/RL 模式：跳过 env.step
            # DDSRLActionProvider 内部已经自行步进了 4 次
            pass
        else:
            # 正常模式：执行物理仿真
            # env.step(action) 内部会：
            #   1. 设置关节目标位置
            #   2. PhysX 物理求解
            #   3. 计算观测（触发 observation 函数）
            #   4. 计算奖励
            #   5. 检查终止条件
            self.env.step(action)

    self.step_count += 1

    # ── 阶段 3：频率控制 ──
    # 确保每步间隔不小于 _step_interval（2ms @ 500Hz）
    elapsed = time.perf_counter() - self._last_step_time
    sleep_needed = self._step_interval - elapsed

    if sleep_needed > self._sleep_threshold:
        # sleep 减去 100us 补偿 sleep 精度不足
        time.sleep(sleep_needed - self._sleep_adjustment)

    self._last_step_time = time.perf_counter()

    # ── 阶段 4：性能统计 ──
    self._profile_counter += 1
    if self._profile_counter >= self._profile_interval:
        # 打印：动作获取耗时 / 仿真步进耗时 / sleep 耗时 / 总耗时
        print(f"[Performance] A:{action_ms}ms, E:{env_ms}ms, "
              f"S:{sleep_ms}ms, T:{total_ms}ms")
        self._profile_counter = 0
```

#### 4.5.4 模式切换逻辑

| 模式 | 触发条件 | env.step() 由谁调用 | 适用场景 |
|------|---------|---------------------|---------|
| **正常模式** | `replay_mode=False`, `rl_action_mode=False` | `RobotController.step()` | DDS 遥操作 |
| **回放模式** | `replay_mode=True` | 不调用（跳过） | 数据回放 |
| **RL 模式** | `rl_action_mode=True` | `DDSRLActionProvider` 内部调用 | 全身 RL 策略 |

**为什么 RL 模式要跳过**：`DDSRLActionProvider` 的 `get_action()` 内部已经执行了 4 次 `env.step()`（因为 `decimation=4`），控制器不需要再调用。

#### 4.5.5 ActionProvider 基类

```python
# 文件：action_provider/action_base.py

class ActionProvider:
    name: str
    is_running: bool = False
    _thread = None                  # 后台线程（用于异步数据接收）

    def get_action(self, env) -> Optional[torch.Tensor]:
        """获取动作 tensor，返回 [1, num_joints] 或 None"""
        raise NotImplementedError

    def start(self):
        """启动后台线程（如 DDS 订阅线程）"""
        self.is_running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self):
        """默认轮询循环（100Hz），子类可覆盖"""
        while self.is_running:
            time.sleep(0.01)

    def stop(self):
        """停止后台线程"""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def cleanup(self):
        """清理资源"""
        pass
```

---

## 5. DDS 通信详解

### 5.1 DDS 架构

DDS（Data Distribution Service）是仿真与外部程序之间的通信桥梁。本项目使用宇树的 `unitree_sdk2py`，底层基于 CycloneDDS。

**DDS 节点基类**（`dds/dds_base.py`）：

```python
class DDSObject:
    def __init__(self, name, shm_input_name, shm_output_name):
        self.name = name
        self.input_shm = SharedMemoryManager(shm_input_name)   # 发布数据
        self.output_shm = SharedMemoryManager(shm_output_name) # 接收数据
```

**数据流向**：

```
仿真内部数据
    ↓
DDSObject.input_shm.write()  → 写入共享内存
    ↓
DDS 发布线程读取共享内存 → 发布到 DDS 网络
    ↓
外部程序订阅 DDS 话题

外部程序发布 DDS 话题
    ↓
DDS 订阅线程接收 → 写入共享内存
    ↓
DDSObject.output_shm.read() → 仿真内部读取
```

### 5.2 所有 DDS 话题一览

| DDS 节点 | 发布话题 | 订阅话题 | 数据类型 | 频率 |
|---------|---------|---------|---------|------|
| `G1RobotDDS` | `rt/lowstate` | `rt/lowcmd` | LowState_/LowCmd_ | 50Hz |
| `Dex3DDS` | `rt/dex3/left/state`, `rt/dex3/right/state` | `rt/dex3/left/cmd`, `rt/dex3/right/cmd` | HandState_/HandCmd_ | 50Hz |
| `GripperDDS` | `rt/dex1/left/state`, `rt/dex1/right/state` | `rt/dex1/left/cmd`, `rt/dex1/right/cmd` | MotorStates_/MotorCmds_ | 50Hz |
| `InspireDDS` | `rt/inspire/state` | `rt/inspire/cmd` | MotorStates_/MotorCmds_ | 50Hz |
| `SimStateDDS` | `rt/sim_state` | `rt/sim_state_cmd` | String_ (JSON) | 主循环频率 |
| `ResetPoseCmdDDS` | — | `rt/reset_pose/cmd` | String_ | 订阅 |
| `RewardsDDS` | `rt/rewards_state` | `rt/rewards_state_cmd` | String_ (JSON) | 奖励计算频率 |
| `RunCommandDDS` | — | `rt/run_command/cmd` | String_ | 订阅 |

### 5.3 G1RobotDDS 详解

**文件**：`dds/g1_robot_dds.py`

**发布数据（仿真 → 外部）**：

```python
def dds_publisher(self):
    # 从共享内存读取仿真数据
    data = self.input_shm.read()

    # 填充 LowState_ 消息
    state = LowState_()
    for i in range(29):
        state.motor_state[i].q = data["pos"][i]      # 关节位置
        state.motor_state[i].dq = data["vel"][i]     # 关节速度
        state.motor_state[i].tau_est = data["torque"][i]  # 力矩估计

    # IMU 数据
    state.imu_state.quaternion = data["imu"]["quat"]  # [x, y, z, w] 注意顺序！
    state.imu_state.accelerometer = data["imu"]["accel"]
    state.imu_state.gyroscope = data["imu"]["gyro"]

    # CRC 校验
    state.crc = compute_crc(state)

    # 发布到 DDS
    self.dds_writer.write(state)
```

**订阅数据（外部 → 仿真）**：

```python
def dds_subscriber(self):
    msg = self.dds_reader.read()  # 接收 LowCmd_

    # CRC 校验
    if msg.crc != compute_crc(msg):
        return

    # 提取 29 个电机的控制命令
    cmd = {
        "motor_pos": [msg.motor_cmd[i].q for i in range(29)],
        "motor_vel": [msg.motor_cmd[i].dq for i in range(29)],
        "motor_tau": [msg.motor_cmd[i].tau for i in range(29)],
        "motor_kp": [msg.motor_cmd[i].kp for i in range(29)],
        "motor_kd": [msg.motor_cmd[i].kd for i in range(29)],
    }

    # 写入共享内存
    self.output_shm.write(cmd)
```

### 5.4 共享内存管理器

**文件**：`dds/sharedmemorymanager.py`

简单的 JSON-over-shared-memory 实现：

```
┌──────────┬──────────┬──────────────────┐
│ 时间戳    │ 数据长度  │ JSON 数据         │
│ 4 bytes  │ 4 bytes  │ N bytes          │
└──────────┴──────────┴──────────────────┘
```

使用文件锁保证线程安全。

---

## 6. 任务配置详解

### 6.1 任务注册机制

```
tasks/g1_tasks/__init__.py
    ↓ import 每个任务模块
tasks/g1_tasks/pick_place_cylinder_g1_29dof_dex3/__init__.py
    ↓ gym.register(id="Isaac-PickPlace-Cylinder-G129-Dex3-Joint", ...)
gymnasium 环境注册表
    ↓
sim_main.py: gym.make(args.task, cfg=env_cfg)  # 按 ID 创建环境
```

### 6.2 任务配置文件结构

以 `pick_place_cylinder_g1_29dof_dex3` 为例，完整配置结构：

```python
@configclass
class PickPlaceCylinderG129Dex3JointEnvCfg(ManagerBasedRLEnvCfg):

    # 场景：房间 + 桌子 + 圆柱体 + 机器人 + 摄像头
    scene: ObjectTableSceneCfg

    # 动作：关节位置控制（所有关节，scale=1.0）
    actions: ActionsCfg

    # 观测：关节状态(87D) + 灵巧手状态(14D) + 摄像头图像
    observations: ObservationsCfg

    # 奖励：基于物体位置的区域判定
    rewards: RewardsCfg

    # 终止：物体出界检测
    terminations: TerminationsCfg

    # 事件：物体位置随机化
    events: EventCfg

    # 仿真参数
    decimation = 2              # 每 2 个物理步取 1 个控制步
    episode_length_s = 20.0     # 每轮最长 20 秒
    sim.dt = 0.005              # 物理步长 5ms
    # → 控制频率 = 1 / (0.005 × 2) = 100Hz
```

### 6.3 机器人预设配置（完整详解）

**文件**：`tasks/common_config/robot_configs.py`

#### 6.3.1 G1 机器人预设一览

| 预设方法 | 灵巧手 | 底座 | 腰部 | 适用任务 |
|---------|--------|------|------|---------|
| `g1_29dof_dex3_base_fix()` | Dex3 | **固定** | 固定 | 抓取/堆叠/抽屉 |
| `g1_29dof_dex3_wholebody()` | Dex3 | **可动** | 可动 | 全身移动 |
| `g1_29dof_dex1_base_fix()` | Dex1 | 固定 | 固定 | 抓取/堆叠/抽屉 |
| `g1_29dof_dex1_wholebody()` | Dex1 | 可动 | 可动 | 全身移动 |
| `g1_29dof_inspire_base_fix()` | Inspire | 固定 | 固定 | 抓取/堆叠 |
| `g1_29dof_inspire_wholebody()` | Inspire | 可动 | 可动 | 全身移动 |

#### 6.3.2 预设配置结构（以 Dex3 base_fix 为例）

```python
# 文件：tasks/common_config/robot_configs.py

class G1RobotPresets:
    @staticmethod
    def g1_29dof_dex3_base_fix():
        """G1 29DOF + Dex3 灵巧手，底座固定（用于桌面操作任务）"""
        return ArticulationCfg(
            prim_path="{ENV_REGEX_NS}/Robot",
            spawn=UsdFileCfg(
                usd_path="{PROJECT_ROOT}/assets/robots/g1_29dof_dex3/g1_29dof_dex3.usd"
            ),
            actuators={
                # ── 腿部关节（12 个）──
                # 左腿 6：hip_roll, hip_pitch, knee, ankle_roll, ankle_pitch, toe
                # 右腿 6：同上
                "legs": ImplicitActuatorCfg(
                    joint_names_expr=[".*hip.*", ".*knee.*", ".*ankle.*", ".*toe.*"],
                    stiffness=...,   # 位置控制刚度
                    damping=...,     # 阻尼系数
                ),
                # ── 腰部关节（3 个）──
                # waist_yaw, waist_roll, waist_pitch
                "waist": ImplicitActuatorCfg(
                    joint_names_expr=[".*waist.*"],
                    stiffness=...,
                    damping=...,
                ),
                # ── 手臂关节（14 个）──
                # 左臂 7：shoulder_pitch/roll/yaw, elbow, wrist_pitch/roll/yaw
                # 右臂 7：同上
                "arms": ImplicitActuatorCfg(
                    joint_names_expr=[".*shoulder.*", ".*elbow.*", ".*wrist.*"],
                    stiffness=...,
                    damping=...,
                ),
                # ── 灵巧手关节（14 个）──
                # 左手 7 + 右手 7（Dex3 每手 3 指，共 7 DOF）
                "hands": ImplicitActuatorCfg(
                    joint_names_expr=[".*hand.*", ".*finger.*"],
                    stiffness=...,
                    damping=...,
                ),
            },
            init_state=ArticulationCfg.InitialStateCfg(
                pos=(0.0, 0.0, 0.785),      # 站立高度 78.5cm
                rot=(1.0, 0.0, 0.0, 0.0),   # 无旋转
                joint_pos={...},              # 各关节默认角度（站立姿态）
            ),
        )
```

#### 6.3.3 base_fix vs wholebody 的区别

| 配置项 | base_fix（底座固定） | wholebody（全身可动） |
|--------|---------------------|---------------------|
| 底座 | 固定在初始位置，不能移动 | 自由移动（受物理引擎控制） |
| 腿部关节 | 有，但底座固定所以不生效 | 有，腿部可以行走/蹲下 |
| 腰部关节 | 固定 | 可以弯腰/转身 |
| 手臂关节 | 可动 | 可动 |
| 灵巧手 | 可动 | 可动 |
| decimation | 2（100Hz 控制） | 4（50Hz 控制） |
| action_source | `dds` | `dds_wholebody`（自动切换） |

#### 6.3.4 关节索引映射关系

```
Isaac Lab 内部关节顺序（USD 文件定义）：
  0  - left_hip_roll
  1  - left_hip_pitch
  2  - left_knee
  3  - left_ankle_roll
  4  - left_ankle_pitch
  5  - left_toe
  6  - right_hip_roll
  7  - right_hip_pitch
  8  - right_knee
  9  - right_ankle_roll
  10 - right_ankle_pitch
  11 - right_toe
  12 - waist_yaw
  13 - waist_roll
  14 - waist_pitch
  15~21 - 左臂 7 个关节
  22~28 - 右臂 7 个关节
  29~35 - 左手 7 个关节
  36~42 - 右手 7 个关节

DDS 外部顺序（用于通信）：
  [左腿6, 右腿6, 腰3, 左臂7, 右臂7] = 29 个
  → 索引 0~28，手臂在 15~28

观测函数使用的重排序索引：
  g1_29dof_indices = [0,3,6,9,13,17, 1,4,7,10,14,18, 2,5,8,11,15,19,
                      21,23,25,27, 12,16,20, 22,24,26,28]
```

#### 6.3.5 H1-2 机器人预设

```python
class H12RobotPresets:
    @staticmethod
    def h12_27dof_inspire_base_fix():
        """H1-2 机器人，27 DOF，Inspire 灵巧手，底座固定"""
        # H1-2 没有腰部关节（26 body joints vs G1 的 29）
        # 灵巧手用 Inspire（12 joints vs Dex3 的 14）
```

### 6.4 不同任务的差异对比

| 配置项 | 圆柱体任务 | 方块任务 | 堆叠任务 | 抽屉任务 | 全身任务 |
|--------|-----------|---------|---------|---------|---------|
| 物体数量 | 1 | 1 | 3 | 1+柜子 | 1 |
| 物体质量 | 0.4kg | 1.0kg | 1.0kg | 3.0kg | 0.4kg |
| 奖励函数 | 单物体 | 单物体 | 层级 | 无 | 无 |
| 终止条件 | 出界检测 | 出界检测 | 任一出界 | 无 | 无 |
| decimation | 2 | 2 | 2 | 2 | 4 |
| 控制频率 | 100Hz | 100Hz | 100Hz | 100Hz | 50Hz |
| 机器人预设 | base_fix | base_fix | base_fix | base_fix | wholebody |
| DDS 模式 | dds | dds | dds | dds | dds_wholebody |

---

## 7. 数据流完整梳理

### 7.1 状态数据流（仿真 → 外部）

```
Isaac Lab 物理引擎
    │
    ├── env.scene["robot"].data
    │       ├── joint_pos [N, num_joints]
    │       ├── joint_vel [N, num_joints]
    │       ├── applied_torque [N, num_joints]
    │       ├── root_state_w [N, 13]
    │       ├── body_link_pose_w [N, num_bodies, 7]
    │       └── body_link_vel_w [N, num_bodies, 6]
    │
    ├── env.scene["object"].data
    │       ├── root_pos_w [N, 3]
    │       ├── root_quat_w [N, 4]
    │       └── root_state_w [N, 13]
    │
    └── env.scene["front_camera"].data
            └── output["rgb"] [N, 480, 640, 3]
    │
    ↓
观测函数（common_observations/*.py）
    │
    ├── get_robot_boy_joint_states() → [N, 87] → DDS rt/lowstate
    ├── get_robot_dex3_joint_states() → [N, 14] → DDS rt/dex3/*/state
    ├── get_robot_imu_data() → [N, 13] → DDS rt/lowstate (IMU 部分)
    └── get_camera_image() → 共享内存 → teleimager 服务器
    │
    ↓
外部程序（遥操作/监控/数据采集）
```

### 7.2 控制数据流（外部 → 仿真）

```
外部程序（遥操作手柄/VLA 模型/录制回放）
    │
    ├── DDS rt/lowcmd → 29 个电机目标位置
    ├── DDS rt/dex3/*/cmd → 灵巧手控制命令
    └── DDS rt/run_command/cmd → 运动命令 [vx, vy, vz, heading]
    │
    ↓
DDS 订阅线程 → 共享内存
    │
    ↓
ActionProvider.get_action(env)
    │
    ├── DDSActionProvider: 直接映射 DDS 命令到仿真关节
    ├── DDSRLActionProvider: RL 策略推理 + DDS 手臂覆盖
    └── FileActionProviderReplay: 从文件读取
    │
    ↓
RobotController.step()
    │
    ├── env.step(action)
    │       ├── set_joint_position_target(action)
    │       ├── write_data_to_sim()
    │       ├── sim.step()  ← PhysX 物理求解
    │       └── scene.update()  ← 更新观测
    │
    └── time.sleep()  ← 频率控制
```

### 7.3 摄像头图像流

```
Isaac Lab Camera 渲染
    │
    ├── front_camera → [480, 640, 3] RGB tensor (GPU)
    ├── left_wrist_camera → [480, 640, 3] RGB tensor (GPU)
    └── right_wrist_camera → [480, 640, 3] RGB tensor (GPU)
    │
    ↓
get_camera_image() (tasks/common_observations/camera_state.py)
    │
    ├── tensor.cpu().numpy()  ← GPU → CPU
    ├── cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)  ← RGB → BGR
    └── async_queue.put(image)  ← 放入异步队列
    │
    ↓
MultiImageWriter（后台线程）
    │
    ├── 写入共享内存 isaac_head_image_shm
    ├── 写入共享内存 isaac_left_image_shm
    └── 写入共享内存 isaac_right_image_shm
    │
    ↓
teleimager 服务器 → WebRTC 推流 / 数据采集脚本
```

---

## 8. VLA 模型集成——代码接入点分析

### 8.1 当前缺失的部分

| 组件 | 当前状态 | 需要做的 |
|------|---------|---------|
| VLA Action Provider | 不存在 | 新建 `action_provider_vla.py` |
| 图像作为策略输入 | 图像只导出到共享内存，不进观测返回值 | 修改 `camera_state.py` 或新建观测函数 |
| 语言指令输入 | 不存在 | 新增 DDS 话题或参数传入 |
| `--action_source policy` | 有参数定义，无实现 | 在 `create_action_provider.py` 中添加 |

### 8.2 推荐的集成方案

**方案 A：新建 VLA ActionProvider**

```
action_provider/action_provider_vla.py
    │
    ├── __init__(env, model_path, ...)
    │       └── 加载 VLA 模型（PyTorch / ONNX）
    │
    ├── get_action(env) -> torch.Tensor
    │       ├── 1. 获取摄像头图像
    │       │       front = env.scene["front_camera"].data.output["rgb"][0]
    │       │       left = env.scene["left_wrist_camera"].data.output["rgb"][0]
    │       │       right = env.scene["right_wrist_camera"].data.output["rgb"][0]
    │       │
    │       ├── 2. 获取机器人状态
    │       │       joint_pos = env.scene["robot"].data.joint_pos
    │       │       joint_vel = env.scene["robot"].data.joint_vel
    │       │
    │       ├── 3. 获取任务指令（语言）
    │       │       task_instruction = self.language_instruction
    │       │
    │       ├── 4. VLA 模型推理
    │       │       action = self.vla_model.predict(images, state, instruction)
    │       │
    │       └── 5. 返回关节目标位置
    │               return action
    │
    └── start() / stop() / cleanup()
```

**方案 B：通过 DDS 桥接外部 VLA 推理**

```
外部 VLA 推理进程
    │
    ├── 订阅 DDS rt/lowstate → 获取机器人状态
    ├── 订阅共享内存 → 获取摄像头图像
    ├── 接收任务指令
    │
    ├── VLA 模型推理
    │
    └── 发布 DDS rt/lowcmd → 发送关节命令
    │
    ↓
仿真内部 DDSActionProvider 接收 → 控制机器人
```

### 8.3 关键 API 速查

**获取图像**：

```python
# 获取最新一帧图像（torch tensor, GPU）
front_img = env.scene["front_camera"].data.output["rgb"][0]  # [480, 640, 3]

# 转到 CPU numpy（用于模型输入）
front_np = front_img.cpu().numpy()  # [480, 640, 3], uint8, RGB
```

**获取关节状态**：

```python
robot = env.scene["robot"]
pos = robot.data.joint_pos[0]       # [num_joints] 当前关节位置
vel = robot.data.joint_vel[0]       # [num_joints] 当前关节速度
torque = robot.data.applied_torque[0]  # [num_joints] 当前力矩
```

**获取物体位置**：

```python
obj = env.scene["object"]
obj_pos = obj.data.root_pos_w[0]    # [3] 物体世界坐标
obj_quat = obj.data.root_quat_w[0]  # [4] 物体朝向四元数
```

**设置关节目标**：

```python
# 方式 1：通过 env.step()（推荐）
action = torch.tensor([[...]])  # [1, num_joints] 目标位置
env.step(action)

# 方式 2：直接写入（高级用法，DDSRLActionProvider 使用）
env.scene.set_joint_position_target(action)
env.scene.write_data_to_sim()
env.sim.step(render=False)
env.scene.update(action)
```

---

## 9. 场景实体访问方式汇总

### 9.1 按名称访问

```python
# 所有场景实体都通过 env.scene["名称"] 访问
robot = env.scene["robot"]           # 机器人 Articulation
obj = env.scene["object"]            # 物体 RigidObject
camera = env.scene["front_camera"]   # 摄像头

# 堆叠任务中有多个物体
red = env.scene["red_block"]
yellow = env.scene["yellow_block"]
green = env.scene["green_block"]
```

### 9.2 完整数据 API 表

**Articulation（机器人）数据**：

| API | 形状 | 说明 |
|-----|------|------|
| `.data.joint_pos` | `[N, J]` | 关节位置（弧度） |
| `.data.joint_vel` | `[N, J]` | 关节速度（弧度/秒） |
| `.data.applied_torque` | `[N, J]` | 施加的力矩（Nm） |
| `.data.joint_pos_target` | `[N, J]` | 目标关节位置 |
| `.data.root_state_w` | `[N, 13]` | 根状态：pos(3)+quat(4)+lin_vel(3)+ang_vel(3) |
| `.data.root_pos_w` | `[N, 3]` | 根位置（世界坐标） |
| `.data.root_quat_w` | `[N, 4]` | 根朝向四元数 |
| `.data.root_vel_w` | `[N, 6]` | 根速度（线+角） |
| `.data.root_ang_vel_b` | `[N, 3]` | 角速度（体坐标系） |
| `.data.projected_gravity_b` | `[N, 3]` | 重力投影（体坐标系） |
| `.data.body_names` | `list[str]` | 所有 body link 名称 |
| `.data.body_link_pose_w` | `[N, B, 7]` | 每个 body link 的世界位姿 |
| `.data.body_link_vel_w` | `[N, B, 6]` | 每个 body link 的世界速度 |

**RigidObject（物体）数据**：

| API | 形状 | 说明 |
|-----|------|------|
| `.data.root_pos_w` | `[N, 3]` | 世界位置 |
| `.data.root_quat_w` | `[N, 4]` | 世界朝向 |
| `.data.root_vel_w` | `[N, 6]` | 世界速度 |
| `.data.root_state_w` | `[N, 13]` | 完整状态 |

**Camera（摄像头）数据**：

| API | 形状 | 说明 |
|-----|------|------|
| `.data.output["rgb"]` | `[N, H, W, 4]` | RGBA 图像 |
| `.data.output["rgb"][0]` | `[H, W, 4]` | 第一个环境的图像 |

**注意**：Camera 的 RGB 输出实际是 4 通道（RGBA），取前 3 通道得到 RGB。

---

## 10. 仿真物理参数

### 10.1 时间参数

| 参数 | 默认值 | 说明 | 计算 |
|------|--------|------|------|
| `sim.dt` | 0.005s | 物理仿真步长 | 200Hz 物理频率 |
| `decimation` | 2 | 控制降频比 | 每 2 个物理步执行 1 次控制 |
| 控制频率 | 100Hz | 实际控制频率 | 1/(0.005×2) |
| `episode_length_s` | 20.0s | 每轮最长时间 | 2000 步 |
| `step_hz` | 500Hz | 主循环频率 | sim_main.py 参数 |

### 10.2 PhysX 物理参数

```python
self.sim.physx.bounce_threshold_velocity = 0.01      # 弹跳阈值
self.sim.physx.friction_correlation_distance = 0.00625  # 摩擦相关距离
self.sim.physx.gpu_found_lost_aggregate_pairs_capacity = 1024 * 1024 * 4
self.sim.physx.gpu_total_aggregate_pairs_capacity = 16 * 1024
```

---

## 11. 附录：所有 18 个任务的完整注册 ID

### G1 机器人任务（15 个）

| 任务 ID | 灵巧手 | 物体 | 动作 |
|---------|--------|------|------|
| `Isaac-PickPlace-Cylinder-G129-Dex3-Joint` | Dex3 | 圆柱体 | 抓取放置 |
| `Isaac-PickPlace-Cylinder-G129-Dex1-Joint` | Dex1 | 圆柱体 | 抓取放置 |
| `Isaac-PickPlace-Cylinder-G129-Inspire-Joint` | Inspire | 圆柱体 | 抓取放置 |
| `Isaac-PickPlace-RedBlock-G129-Dex3-Joint` | Dex3 | 红方块 | 抓取放置 |
| `Isaac-PickPlace-RedBlock-G129-Dex1-Joint` | Dex1 | 红方块 | 抓取放置 |
| `Isaac-PickPlace-RedBlock-G129-Inspire-Joint` | Inspire | 红方块 | 抓取放置 |
| `Isaac-Stack-RgyBlock-G129-Dex3-Joint` | Dex3 | 红绿黄方块 | 堆叠 |
| `Isaac-Stack-RgyBlock-G129-Dex1-Joint` | Dex1 | 红绿黄方块 | 堆叠 |
| `Isaac-Stack-RgyBlock-G129-Inspire-Joint` | Inspire | 红绿黄方块 | 堆叠 |
| `Isaac-Pick-Redblock-Into-Drawer-G129-Dex3-Joint` | Dex3 | 红方块+柜子 | 放入抽屉 |
| `Isaac-Pick-Redblock-Into-Drawer-G129-Dex1-Joint` | Dex1 | 红方块+柜子 | 放入抽屉 |
| `Isaac-Move-Cylinder-G129-Dex3-Wholebody` | Dex3 | 圆柱体 | 全身移动 |
| `Isaac-Move-Cylinder-G129-Dex1-Wholebody` | Dex1 | 圆柱体 | 全身移动 |
| `Isaac-Move-Cylinder-G129-Inspire-Wholebody` | Inspire | 圆柱体 | 全身移动 |

### H1-2 机器人任务（3 个）

| 任务 ID | 灵巧手 | 物体 | 动作 |
|---------|--------|------|------|
| `Isaac-PickPlace-Cylinder-H12-27dof-Inspire-Joint` | Inspire | 圆柱体 | 抓取放置 |
| `Isaac-PickPlace-RedBlock-H12-27dof-Inspire-Joint` | Inspire | 红方块 | 抓取放置 |
| `Isaac-Stack-RgyBlock-H12-27dof-Inspire-Joint` | Inspire | 红绿黄方块 | 堆叠 |

---

## 12. 关键发现与总结

### 12.1 架构优势

1. **模块化清晰**：观测、奖励、场景、动作完全解耦，每个模块可独立修改
2. **DDS 通信与实机一致**：仿真代码可直接搬到实机
3. **多灵巧手支持**：通过预设切换不同手型，无需改核心代码
4. **数据采集友好**：回放模式 + 图像导出 + 共享内存，方便生成训练数据

### 12.2 VLA 集成的关键约束

1. **图像不在观测返回值中**：`get_camera_image()` 返回占位符，实际图像走共享内存。VLA 需要直接从 `env.scene["camera"].data.output["rgb"]` 读取
2. **没有物体位姿的实时 DDS 发布**：物体位置只在奖励函数中读取，不通过 DDS 发布。VLA 如果需要物体位置，需要自己读取
3. **`--action_source policy` 未实现**：需要补全 `create_action_provider.py` 中的分支
4. **全身任务的 RL 策略是运动控制**：`DDSRLActionProvider` 中的 `policy.onnx` 只负责行走/站立，不负责操作

### 12.3 建议阅读顺序

```
1. sim_main.py                    ← 理解整体流程
2. tasks/common_observations/     ← 理解数据从哪来
3. action_provider/               ← 理解动作怎么执行
4. tasks/common_rewards/          ← 理解目标判定逻辑
5. dds/                           ← 理解通信机制
6. tasks/common_scene/            ← 理解场景构成
7. tasks/g1_tasks/.../env_cfg.py  ← 理解具体任务配置
```

---

## 13. RL 策略详解（强化学习策略）

### 13.1 什么是 RL（Reinforcement Learning）

RL = **强化学习**，核心思想是让机器人通过**试错**自己学会怎么做。

```
传统编程：
  人写规则 → 机器人执行
  "如果物体在左边，手臂往左伸 5cm"

RL 策略：
  机器人自己试 → 环境给奖励/惩罚 → 自己学会怎么做
  试了 100 万次后：自动学会"看到物体在左边就伸手"
```

### 13.2 RL 的基本要素

```
┌───────────┐     动作      ┌───────────┐
│  RL 策略   │──────────────→│  环境       │
│  (Policy)  │               │  (Env)     │
│            │←──────────────│            │
└───────────┘   状态+奖励    └───────────┘
               (观测+reward)
```

| 要素 | 英文 | 含义 | 本项目中的对应 |
|------|------|------|--------------|
| 环境 | Environment | 机器人所在的仿真世界 | Isaac Lab 仿真场景 |
| 状态 | State | 机器人当前感知到的信息 | 关节角度、角速度、重力方向 |
| 动作 | Action | 机器人可以做什么 | 29 个关节的目标位置 |
| 奖励 | Reward | 做得好不好 | 物体到目标位置 +1.0，掉出去 -1.0 |
| 策略 | Policy | 看到状态后决定做什么动作 | `policy.onnx` 这个模型 |

### 13.3 RL 训练过程

```
第 1 轮（随机乱动）：
  状态：手臂在初始位置
  动作：随机关节角度 → 手臂乱挥
  奖励：-1.0（物体掉了）
  结论：这个动作不好，降低这类动作的概率

第 1000 轮（开始有感觉）：
  状态：手臂在初始位置
  动作：稍微往物体方向伸
  奖励：0.0（物体没掉，但也没到位）
  结论：比之前好一点，稍微提高概率

第 100000 轮（学会了）：
  状态：手臂在初始位置
  动作：精准抓取 → 放到目标位置
  奖励：+1.0（成功！）
  结论：这个策略不错，保留并强化

最终产物：policy.onnx（训练好的策略模型文件）
```

### 13.4 本项目中的 RL 策略

**文件位置**：`action_provider/action_provider_wh_dds.py`

**加载方式**：

```python
def load_policy(self, path: str):
    if path.endswith('.onnx'):
        import onnxruntime as ort
        session = ort.InferenceSession(path)
        def run_onnx(obs):
            return session.run(None, {"obs": obs})[0]
        self.policy = run_onnx

    elif path.endswith('.pt'):
        model = torch.jit.load(path)
        self.policy = lambda obs: model(obs)
```

**输入（910 维纯数字，没有图像）**：

```python
# 每步 91 维 × 循环缓冲 10 步 = 910 维
obs_per_step = [
    角速度(3),           # 机器人身体旋转多快（体坐标系）
    重力投影(3),         # 重力在身体坐标系的方向（知道哪边是地）
    运动命令(4),         # 人给的数值命令：[vx, vy, vz, heading]
    关节位置差(26),      # 当前关节角度 vs 默认关节角度的偏差
    关节速度(26),        # 每个关节转动多快
    上一步动作(29),      # 上一帧做了什么动作
]
# 3 + 3 + 4 + 26 + 26 + 29 = 91 维/步
# 91 × 10 步（循环缓冲区）= 910 维
```

**输出（29 个关节的目标位置）**：

```python
action = policy(obs)  # → [1, 29]
# 29 个关节 = 左腿6 + 右腿6 + 腰3 + 左臂7 + 右臂7
```

**这个 RL 策略只负责走路和站立**，不负责操作物体。操作物体靠外部遥操作 DDS 命令覆盖手臂关节。

### 13.5 RL 策略的局限性

| 局限 | 说明 |
|------|------|
| 看不到物体 | 输入只有本体感知（关节角、速度），没有摄像头图像 |
| 听不懂人话 | 只接受数值命令 `[vx, vy, vz, heading]`，不能理解自然语言 |
| 任务单一 | 只会训练过的任务，换个物体就不会了 |
| 不能泛化 | 换个场景、换个物体大小，需要重新训练 |

---

## 14. VLA 模型详解（Vision-Language-Action）

### 14.1 什么是 VLA

VLA = **Vision-Language-Action**，是一类模型的统称，不是某一个具体模型。

核心思想：把**视觉理解**、**语言理解**、**动作生成**三件事用一个端到端模型搞定。

```
传统 RL 策略：
  关节角+速度（数字） → 策略网络 → 关节动作
  看不到物体，听不懂话

VLA 模型：
  摄像头图像 + 语言指令 → 大模型推理 → 关节动作
  "看到什么" + "要做什么" → "怎么做"
```

### 14.2 具体有哪些 VLA 模型

| 模型 | 来源 | 年份 | 开源 | 特点 |
|------|------|------|------|------|
| **RT-2** | Google DeepMind | 2023 | ❌ | 基于 PaLI-X 视觉语言模型 + 动作 token 化，第一个引起广泛关注的 VLA |
| **Octo** | UC Berkeley | 2024 | ✅ | Transformer 架构，支持多种机器人，可在自定义数据上微调 |
| **OpenVLA** | Stanford | 2024 | ✅ | 基于 Llama 2 + SigLIP 视觉编码器，7B 参数，可在消费级 GPU 上微调 |
| **π0 (Pi-Zero)** | Physical Intelligence | 2024 | ❌ | 基于 Flow Matching 的动作生成，性能很强 |
| **RoboVLM** | 多机构联合 | 2024 | ✅ | 统一框架，支持多种 VLM 骨干 |
| **GR-2** | 字节跳动 | 2024 | 部分 | 视频生成 + 动作预测 |

### 14.3 VLA 模型的工作原理（以 OpenVLA 为例）

```
输入：
  ┌─────────────────┐
  │ 摄像头 RGB 图像   │  480×640×3  ← 本项目已有
  └────────┬────────┘
           ↓
  ┌─────────────────┐
  │ "pick up the     │  自然语言指令  ← 本项目没有
  │  red block"      │
  └────────┬────────┘
           ↓
  ┌─────────────────────────────────────────┐
  │            视觉编码器 (SigLIP / CLIP)     │
  │  图像 → 视觉 token（把图片转成模型能理解的数字）│
  └────────┬────────────────────────────────┘
           ↓
  ┌─────────────────────────────────────────┐
  │            语言模型骨干 (Llama 2 7B)      │
  │  视觉token + 语言token → 理解场景和意图     │
  │  "图里有一个红色方块" + "要把它抓起来"       │
  │  → "我应该伸手到方块位置，然后合拢手指"      │
  └────────┬────────────────────────────────┘
           ↓
  ┌─────────────────────────────────────────┐
  │            动作解码头                      │
  │  → 离散动作 token（如 256 个 bin）          │
  │  → 或连续动作向量                          │
  └────────┬────────────────────────────────┘
           ↓
输出：
  7 维手臂动作 (Δx, Δy, Δz, Δrx, Δry, Δrz, gripper)
  或直接输出关节目标位置
```

### 14.4 RL 策略 vs VLA 模型对比

| 对比维度 | RL 策略（本项目已有） | VLA 模型（需要接入） |
|---------|---------------------|---------------------|
| **输入** | 数字：关节角、速度、重力 | 图像 + 语言指令 |
| **"看到"物体吗** | 看不到，只知道自己的关节状态 | 看得到，从摄像头图像理解场景 |
| **能听懂人话吗** | 不能，只接受 `vx, vy, heading` 数值命令 | 能，"把红色方块放到桌上" |
| **怎么学会的** | 仿真中试错几百万次，奖励引导 | 看大量机器人操作视频预训练 |
| **擅长什么** | 精确的运动控制（走路、站立） | 理解场景、泛化到新任务 |
| **训练成本** | 需要设计奖励函数 + 大量仿真时间 | 需要大量数据 + 大 GPU |
| **模型大小** | 小（几百 KB ~ 几 MB） | 大（几 GB，7B 参数级别） |
| **推理速度** | 快（毫秒级） | 慢（百毫秒级） |
| **泛化能力** | 弱，只会在训练过的场景工作 | 强，可以处理新物体、新场景 |
| **本项目文件** | `action_provider_wh_dds.py` 加载 `policy.onnx` | **不存在，需要新建** |

### 14.5 VLA 模型的输入输出与本项目的对应关系

| VLA 需要的输入 | 本项目是否已有 | 数据来源 |
|---------------|--------------|---------|
| 前置摄像头图像 | ✅ 已有 | `env.scene["front_camera"].data.output["rgb"][0]` |
| 左手腕摄像头图像 | ✅ 已有 | `env.scene["left_wrist_camera"].data.output["rgb"][0]` |
| 右手腕摄像头图像 | ✅ 已有 | `env.scene["right_wrist_camera"].data.output["rgb"][0]` |
| 机器人关节状态 | ✅ 已有 | `env.scene["robot"].data.joint_pos/vel` |
| 语言指令（任务描述） | ❌ 没有 | 需要新增输入方式（DDS 话题 / 命令行参数 / 配置文件） |
| 物体位置（可选） | ✅ 已有 | `env.scene["object"].data.root_pos_w` |

| VLA 的输出 | 本项目是否能接收 | 说明 |
|-----------|----------------|------|
| 关节目标位置 | ✅ 可以 | `env.step(action)` 接受 `[1, num_joints]` tensor |
| 末端位移 Δpose | ⚠️ 需要逆运动学 | 需要 IK 求解器转换为关节角度 |

### 14.6 VLA 集成的技术挑战

| 挑战 | 说明 | 可能的解决方案 |
|------|------|--------------|
| **动作空间不匹配** | VLA 通常输出 7D 末端动作，仿真需要关节角度 | 加逆运动学层，或选支持关节空间输出的 VLA |
| **控制频率** | VLA 推理 ~100ms，仿真控制 100Hz | 降频运行，或用 VLA 做高层规划 + 底层 PID |
| **图像预处理** | 不同 VLA 要求不同分辨率/归一化 | 按模型要求做 resize + normalize |
| **实时性** | 大模型推理慢 | GPU 推理优化、模型量化、TensorRT |
| **仿真到真实迁移** | 仿真训练的策略搬到真实机器人有 gap | 域随机化、真实数据微调 |

### 14.7 推荐的 VLA 选型（针对本项目）

| 模型 | 推荐度 | 理由 |
|------|--------|------|
| **OpenVLA** | ⭐⭐⭐⭐⭐ | 开源、7B 参数可微调、支持关节空间输出、社区活跃 |
| **Octo** | ⭐⭐⭐⭐ | 开源、轻量、专门为机器人设计、支持微调 |
| **RT-2** | ⭐⭐⭐ | 性能强但不开源，只能用 API |
| **π0** | ⭐⭐ | 最强但不开源 |

---

## 15. 术语速查表

| 术语 | 英文 | 含义 |
|------|------|------|
| RL | Reinforcement Learning | 强化学习，通过试错学习策略 |
| VLA | Vision-Language-Action | 视觉-语言-动作模型，端到端 |
| Policy | Policy | 策略，决定在某个状态做什么动作 |
| Observation | Observation | 观测，机器人感知到的状态信息 |
| Action | Action | 动作，机器人执行的控制指令 |
| Reward | Reward | 奖励，衡量动作好坏的数值 |
| Episode | Episode | 一轮，从开始到结束（成功/失败/超时）的一次尝试 |
| Decimation | Decimation | 控制降频比，每 N 个物理步执行 1 次控制 |
| DDS | Data Distribution Service | 数据分发服务，实时通信协议 |
| ONNX | Open Neural Network Exchange | 开放神经网络交换格式，跨框架模型格式 |
| DOF | Degrees of Freedom | 自由度，关节数量 |
| Articulation | Articulation | 铰接体，多关节刚体（如机器人） |
| RigidObject | Rigid Object | 刚体，不可变形的物体（如方块、圆柱） |
| IMU | Inertial Measurement Unit | 惯性测量单元，测量加速度和角速度 |
| IK | Inverse Kinematics | 逆运动学，从末端位姿反算关节角度 |
| FPS | Frames Per Second | 帧率，每秒执行步数 |

---

#机器人 #宇树 #仿真 #IsaacLab #代码架构 #VLA #RL #数据流 #强化学习 #策略模型
