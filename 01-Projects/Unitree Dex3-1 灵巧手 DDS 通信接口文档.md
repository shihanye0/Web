# Unitree Dex3-1 灵巧手 DDS 通信接口文档

> 来源：
> - [基于DDS的上层通信方式](https://support.unitree.com/home/zh/dex3-1_hand/DDS-based_communication_method)
> - [灵巧手控制接口文件含义解释（IDL）](https://support.unitree.com/home/zh/dex3-1_hand/Dex_IDL_specification)
> 更新日期：2026-05-21
> 整理日期：2026-06-01

---

## 1. 概述

### 1.1 什么是 DDS 上层通信

Dex3-1 灵巧手接入宇树机器人（以 G1 人形机器人为例）后，通过 **DDS（Data Distribution Service，数据分发服务）协议** 进行上层控制。

```
用户程序  ──HandCmd_──>  G1 常驻服务  ──底层协议──>  Dex3-1 灵巧手
          <──HandState_──              <──状态反馈──
```

工作流程：
1. G1 机器人内部运行一个**常驻服务**，负责与 Dex3-1 灵巧手进行底层通信
2. 该服务将底层协议转换为 DDS 消息
3. 用户通过 `unitree_sdk2` 发送/接收 DDS 消息来控制灵巧手

### 1.2 前置依赖

| 依赖 | 说明 |
|------|------|
| SDK | `unitree_sdk2`（[获取地址](https://support.unitree.com/home/zh/G1_developer/get_sdk)） |
| 示例源码 | [GitHub - dex3_subscribe.cpp](https://github.com/unitreerobotics/unitree_sdk2/blob/main/example/g1/dex3/dex3_subscribe.cpp) |
| URDF 模型 | [unitree_ros](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description) |
| 快速开发 | [《快速开发》文档](https://support.unitree.com/home/zh/G1_developer/quick_development) |

### 1.3 头文件位置

```
/usr/local/include/unitree/hg_idl/HandCmd_.hpp
/usr/local/include/unitree/hg_idl/HandState_.hpp
```

---

## 2. 灵巧手关节结构

### 2.1 基本参数

Dex3-1 每只手有 **3 根手指**（拇指、食指、中指），共 **7 个电机**：

| 手指 | 关节数 | 说明 |
|------|--------|------|
| 拇指（Thumb） | 3 个 | thumb_0, thumb_1, thumb_2 |
| 中指（Middle） | 2 个 | middle_0, middle_1 |
| 食指（Index） | 2 个 | index_0, index_1 |

### 2.2 IDL 消息排序（程序使用）

`HandCmd_.motor_cmd` 和 `HandState_.motor_state` 中的电机顺序：

| 索引 | 关节名称 | 手指 |
|:----:|---------|------|
| 0 | thumb_0 | 拇指 |
| 1 | thumb_1 | 拇指 |
| 2 | thumb_2 | 拇指 |
| 3 | middle_0 | 中指 |
| 4 | middle_1 | 中指 |
| 5 | index_0 | 食指 |
| 6 | index_1 | 食指 |

### 2.3 URDF 排序（仿真使用）

URDF 中的关节顺序与 IDL 不同，且左右手有差异：

**左手 URDF 映射：**

| URDF 索引 | IDL 索引 | 关节名称 |
|:---------:|:--------:|---------|
| left_hand_zero | 0 | thumb_0 |
| left_hand_one | 1 | thumb_1 |
| left_hand_two | 2 | thumb_2 |
| left_hand_five | 3 | middle_0 |
| left_hand_six | 4 | middle_1 |
| left_hand_three | 5 | index_0 |
| left_hand_four | 6 | index_1 |

**右手 URDF 映射：**

| URDF 索引 | IDL 索引 | 关节名称 |
|:---------:|:--------:|---------|
| right_hand_zero | 0 | thumb_0 |
| right_hand_one | 1 | thumb_1 |
| right_hand_two | 2 | thumb_2 |
| right_hand_three | 3 | middle_0 |
| right_hand_four | 4 | middle_1 |
| right_hand_five | 5 | index_0 |
| right_hand_six | 6 | index_1 |

> **注意**：右手的 URDF 索引是连续的（zero~six），而左手的 URDF 索引顺序为 zero, one, two, **five, six**, three, four，这一点在做坐标系转换时要特别注意。

---

## 3. DDS 通信接口

### 3.1 话题（Topic）

```
rt/dex3/{hand}/cmd       # 灵巧手指令订阅（hand = left | right）
rt/dex3/{hand}/state     # 灵巧手状态发布（hand = left | right）
```

| 方向 | 话题名称 | 消息类型 | 命名空间 | 发送频率 |
|------|---------|---------|---------|---------|
| 发送（控制） | `rt/dex3/left/cmd` | `HandCmd_` | `unitree_hg::msg::dds_::HandCmd_` | 建议 10~1000 Hz |
| 发送（控制） | `rt/dex3/right/cmd` | `HandCmd_` | 同上 | 建议 10~1000 Hz |
| 接收（状态） | `rt/dex3/left/state` | `HandState_` | `unitree_hg::msg::dds_::HandState_` | 1000 Hz |
| 接收（状态） | `rt/dex3/right/state` | `HandState_` | 同上 | 1000 Hz |

> **频率说明**：控制命令建议 10~1000 Hz；状态反馈由灵巧手以 1000 Hz 固定发布。

---

## 4. 核心数据结构详解（IDL 规范）

> 以下为 DDS 层实际使用的 C++ 类定义，与底层 C 结构体（`MotorCmd_t`、`RIS_Mode_t`）的对应关系见 §4.7。

### 4.1 控制结构体 `HandCmd_`

```cpp
class HandCmd_ {
    std::vector<MotorCmd_> motor_cmd_;       // 所有关节电机的控制命令列表（长度=7）
    std::array<uint32_t, 4> reserve_ = {};   // 4 个 32 位预留字段，用于功能扩展
};
```

`motor_cmd` 是一个长度为 7 的 vector，每个元素对应一个电机（索引顺序见 §2.2）。

### 4.2 电机控制命令 `MotorCmd_`

```cpp
class MotorCmd_ {
    uint8_t mode_  = 0;       // 电机控制模式：0=锁定，1=FOC 控制
    float   q_     = 0.0f;    // 目标关节位置，单位：rad
    float   dq_    = 0.0f;    // 目标关节速度，单位：rad/s
    float   tau_   = 0.0f;    // 目标关节力矩，单位：N·m
    float   kp_    = 0.0f;    // 位置控制刚度系数，单位：Nm/rad
    float   kd_    = 0.0f;    // 速度控制阻尼系数，单位：Nm/(rad/s)
    uint32_t reserve_ = 0;    // 32 位预留字段
};
```

**字段详解：**

| 字段 | 类型 | 单位 | 读写 | 说明 |
|------|------|------|:----:|------|
| `mode` | uint8_t | - | 写 | 控制模式。`0` = 锁定（电机不动），`1` = FOC（力矩闭环控制） |
| `q` | float | rad | 写 | 目标关节位置。需要在电机限位范围内 |
| `dq` | float | rad/s | 写 | 目标关节速度。通常设为 0（位置控制模式） |
| `tau` | float | N·m | 写 | 前馈力矩。用于补偿重力等已知外力，通常设为 0 |
| `kp` | float | Nm/rad | 写 | 位置刚度系数。值越大，电机追踪目标位置的力越强 |
| `kd` | float | Nm/(rad/s) | 写 | 速度阻尼系数。提供阻尼防止振荡，典型值 0.1~0.5 |
| `reserve` | uint32_t | - | 写 | 预留字段，暂不使用 |

**控制原理（PD 控制器）：**

```
输出力矩 = kp × (q - q_actual) + kd × (dq - dq_actual) + tau
```

即：电机输出的力矩 = 位置误差产生的弹性力 + 速度误差产生的阻尼力 + 前馈力矩。

### 4.3 状态结构体 `HandState_`

```cpp
class HandState_ {
    std::vector<MotorState_>       motor_state_;          // 所有关节电机的状态列表（长度=7）
    std::vector<PressSensorState_> press_sensor_state_;   // 触觉传感器状态列表
    IMUState_                      imu_state_;            // IMU 姿态传感器状态
    float   power_v_   = 0.0f;     // 主板供电电压
    float   power_a_   = 0.0f;     // 主板供电电流
    float   system_v_  = 0.0f;     // 系统电压（暂未使用）
    float   device_v_  = 0.0f;     // 设备电压（暂未使用）
    std::array<uint32_t, 2> error_   = {};   // 错误状态字段（error_[0] = 主板错误）
    std::array<uint32_t, 2> reserve_ = {};   // 预留字段（reserve_[0] = 电源状态）
};
```

**字段详解：**

| 字段 | 类型 | 单位 | 读 | 说明 |
|------|------|------|:--:|------|
| `motor_state` | MotorState_[7] | - | ✓ | 每个电机的状态反馈 |
| `press_sensor_state` | PressSensorState_[] | - | ✓ | 手指表面压力传感器数据 |
| `imu_state` | IMUState_ | - | ✓ | 惯性测量单元数据 |
| `power_v` | float | V | ✓ | 主板供电电压 |
| `power_a` | float | A | ✓ | 主板供电电流 |
| `system_v` | float | V | ✓ | 系统电压（暂未使用） |
| `device_v` | float | V | ✓ | 设备电压（暂未使用） |
| `error[0]` | uint32_t | - | ✓ | 主板错误状态 |
| `reserve[0]` | uint32_t | - | ✓ | 电源状态 |

### 4.4 电机状态 `MotorState_`

```cpp
class MotorState_ {
    uint8_t mode_  = 0;                           // 电机当前工作模式
    float   q_     = 0.0f;                        // 当前关节位置，单位：rad
    float   dq_    = 0.0f;                        // 当前关节速度，单位：rad/s
    float   ddq_   = 0.0f;                        // 当前关节加速度（暂未使用）
    float   tau_est_ = 0.0f;                      // 估计关节力矩，单位：N·m
    std::array<int16_t, 2>  temperature_ = {};     // 电机温度数组，单位：°C
    float   vol_   = 0.0f;                        // 电机电压（暂未使用）
    std::array<uint32_t, 2> sensor_      = {};    // 传感器数据（暂未使用）
    uint32_t motorstate_ = 0;                     // 电机状态字（暂未使用）
    std::array<uint32_t, 4> reserve_     = {};    // 预留字段（reserve_[0] = 对应电机错误码）
};
```

**字段详解：**

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| `mode` | uint8_t | - | 当前工作模式（0=锁定，1=FOC） |
| `q` | float | rad | 当前关节位置 |
| `dq` | float | rad/s | 当前关节速度 |
| `ddq` | float | rad/s² | 当前关节加速度（暂未使用） |
| `tau_est` | float | N·m | 估计关节力矩（由电流估算） |
| `temperature[0]` | int16_t | °C | 电机线圈温度 |
| `temperature[1]` | int16_t | °C | 电机驱动板温度 |
| `vol` | float | V | 电机电压（暂未使用） |
| `reserve[0]` | uint32_t | - | **对应电机的错误码** |

### 4.5 触觉传感器 `PressSensorState_`

```cpp
class PressSensorState_ {
    std::array<float, 12> pressure_    = {};   // 12 路触觉压力传感器数据
    std::array<float, 12> temperature_ = {};   // 12 路传感器温度（暂未使用）
    uint32_t lost_     = 0;                    // 传感器数据丢失标志
    uint32_t reserve_  = 0;                    // 预留字段
};
```

**传感器数据规则：**

| 条件 | 含义 |
|------|------|
| `pressure[i] >= 100000` | **有效数据**。建议除以 10000 转换显示（如 100000 → 10.0000） |
| `pressure[i] == 30000` | **无数据**（传感器未连接或未触发） |
| `temperature[i]` | 传感器温度值（暂未使用） |
| `lost` | 数据丢失标志位 |

**传感器物理位置：**

每只手有 12 个压力传感器，分布在手指的不同区域。`pressure[i]` 的索引 i 与物理传感器位置的对应关系请参考官方传感器布局图：

- 左手：[传感器分布图](https://doc-cdn.unitree.com/static/2024/12/25/82cc7af5d0e64162bb0a5c078f87a256_7680x4320.png)
- 右手：[传感器分布图](https://doc-cdn.unitree.com/static/2024/12/25/64b093c7752344e7a8567524fc0c69cd_7680x4320.png)

### 4.6 IMU 姿态传感器 `IMUState_`

```cpp
struct IMUState_ {
    std::array<float, 4>  quaternion_    = {};   // 姿态四元数 [w, x, y, z]
    std::array<float, 3>  gyroscope_     = {};   // 三轴角速度，单位：rad/s [x, y, z]
    std::array<float, 3>  accelerometer_ = {};   // 三轴加速度，单位：m/s² [x, y, z]
    std::array<float, 3>  rpy_           = {};   // 欧拉角 [roll, pitch, yaw]，单位：rad
    int16_t               temperature_   = 0;    // IMU 温度，单位：°C
};
```

**字段详解：**

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| `quaternion[4]` | float[4] | - | 姿态四元数，顺序为 [w, x, y, z] |
| `gyroscope[3]` | float[3] | rad/s | 三轴角速度 [x, y, z] |
| `accelerometer[3]` | float[3] | m/s² | 三轴加速度 [x, y, z] |
| `rpy[3]` | float[3] | rad | 欧拉角 [roll, pitch, yaw] |
| `temperature` | int16_t | °C | IMU 芯片温度 |

> **用途**：IMU 可以感知灵巧手的姿态和运动状态，用于抓取过程中的力反馈控制、滑动检测等高级应用。

### 4.7 DDS 层 vs 底层 C 结构体对照

DDS 通信文档中还展示了一套底层 C 结构体（`MotorCmd_t` / `RIS_Mode_t`），这是灵巧手内部的串口通信格式。实际 DDS 开发中使用的是上文 §4.2 的 `MotorCmd_` 类。两者对照：

| DDS 层（实际使用）                        | 底层 C 结构体                          | 区别                                           |
| ---------------------------------- | --------------------------------- | -------------------------------------------- |
| `MotorCmd_.mode` (uint8_t, 0/1)    | `MotorCmd_t.mode` (RIS_Mode_t 位域) | DDS 层简化为 0=锁定/1=FOC；底层位域包含 id/status/timeout |
| `MotorCmd_.q` (float, rad)         | `MotorCmd_t.pos_des` (int32_t)    | DDS 层为浮点弧度；底层为整数原始值                          |
| `MotorCmd_.dq` (float, rad/s)      | `MotorCmd_t.spd_des` (int16_t)    | 同上                                           |
| `MotorCmd_.tau` (float, N·m)       | `MotorCmd_t.tor_des` (int16_t)    | 同上                                           |
| `MotorCmd_.kp` (float, Nm/rad)     | `MotorCmd_t.k_pos` (int16_t)      | 同上                                           |
| `MotorCmd_.kd` (float, Nm/(rad/s)) | `MotorCmd_t.k_spd` (int16_t)      | 同上                                           |
| 无                                  | head[2], CRC32                    | 底层需要包头和校验，DDS 层自动处理                          |

> **结论**：DDS 层是对底层协议的封装，开发者只需使用 §4.1~4.6 的 C++ 类，无需关心包头、CRC、位域拼接等底层细节。

---

## 5. C++ 控制接口函数示例

### 5.1 前置定义

```cpp
#define MOTOR_MAX 7

// 左手各电机的最大/最小限位值（具体值需根据实际标定确定）
float maxTorqueLimits_left[MOTOR_MAX]  = { /* 各电机最大值 rad */ };
float minTorqueLimits_left[MOTOR_MAX]  = { /* 各电机最小值 rad */ };

// 右手各电机的最大/最小限位值
float maxTorqueLimits_right[MOTOR_MAX] = { /* 各电机最大值 rad */ };
float minTorqueLimits_right[MOTOR_MAX] = { /* 各电机最小值 rad */ };

// DDS 发布者和订阅者（初始化方式参考 unitree_sdk2 文档）
// handcmd_publisher:   发布 HandCmd_ 到 "rt/dex3/(left|right)/cmd"
// handstate_subscriber: 订阅 "rt/dex3/(left|right)/state" 更新 state
```

### 5.2 电机旋转测试 `rotateMotors()`

**功能**：控制灵巧手所有电机做正弦波满行程运动，用于测试电机是否正常工作。

```cpp
void rotateMotors(bool isLeftHand) {
    static int _count = 1;  // 计数器，驱动正弦波
    static int dir = 1;     // 方向控制：1=正向，-1=反向
    const float* maxTorqueLimits = isLeftHand ? maxTorqueLimits_left : maxTorqueLimits_right;
    const float* minTorqueLimits = isLeftHand ? minTorqueLimits_left : minTorqueLimits_right;

    for (int i = 0; i < MOTOR_MAX; i++) {
        // --- 构造 mode 字段（底层位域拼接） ---
        RIS_Mode_t ris_mode;
        ris_mode.id = i;            // 电机 ID
        ris_mode.status = 0x01;     // FOC 模式
        ris_mode.timeout = 0x01;    // 开启超时保护

        uint8_t mode = 0;
        mode |= (ris_mode.id & 0x0F);
        mode |= (ris_mode.status & 0x07) << 4;
        mode |= (ris_mode.timeout & 0x01) << 7;

        // --- 设置电机控制参数 ---
        msg.motor_cmd()[i].mode(mode);
        msg.motor_cmd()[i].tau(0);          // 前馈力矩 = 0
        msg.motor_cmd()[i].kp(0.5);         // 位置刚度
        msg.motor_cmd()[i].kd(0.1);         // 速度阻尼

        // --- 计算正弦波目标位置 ---
        float range = maxTorqueLimits[i] - minTorqueLimits[i];
        float mid = (maxTorqueLimits[i] + minTorqueLimits[i]) / 2.0;
        float amplitude = range / 2.0;
        float q = mid + amplitude * sin(_count / 20000.0 * M_PI);

        msg.motor_cmd()[i].q(q);            // 设置目标位置
    }

    // --- 发布命令 ---
    handcmd_publisher->Write(msg);

    // --- 更新计数和方向 ---
    _count += dir;
    if (_count >= 10000)  dir = -1;   // 到达正向极限，反转
    if (_count <= -10000) dir = 1;    // 到达反向极限，正转

    usleep(100);  // 100μs 间隔，≈10kHz 控制频率
}
```

**关键参数解读：**

| 参数 | 值 | 说明 |
|------|:--:|------|
| kp | 0.5 | 位置刚度，控制电机追踪目标位置的力度 |
| kd | 0.1 | 速度阻尼，防止振荡 |
| tau | 0 | 前馈力矩为 0，完全靠 kp/kd 控制 |
| usleep | 100 | 100μs ≈ 10kHz 控制频率 |
| sin 周期 | 20000 步 | 约 2 秒完成一个完整正弦波周期 |

### 5.3 抓握控制 `gripHand()`

**功能**：控制灵巧手所有电机移动到中间位置并保持抓握姿态。

```cpp
void gripHand(bool isLeftHand) {
    const float* maxTorqueLimits = isLeftHand ? maxTorqueLimits_left : maxTorqueLimits_right;
    const float* minTorqueLimits = isLeftHand ? minTorqueLimits_left : minTorqueLimits_right;

    for (int i = 0; i < MOTOR_MAX; i++) {
        // --- 构造 mode 字段 ---
        RIS_Mode_t ris_mode;
        ris_mode.id = i;
        ris_mode.status = 0x01;     // FOC 模式
        ris_mode.timeout = 0;       // 禁用超时保护（持续抓握不需要超时）

        uint8_t mode = 0;
        mode |= (ris_mode.id & 0x0F);
        mode |= (ris_mode.status & 0x07) << 4;
        mode |= (ris_mode.timeout & 0x01) << 7;

        msg.motor_cmd()[i].mode(mode);
        msg.motor_cmd()[i].tau(0);

        // --- 目标位置 = 限位中间值 ---
        float mid = (maxTorqueLimits[i] + minTorqueLimits[i]) / 2.0;
        msg.motor_cmd()[i].q(mid);      // 位置 = 中间值
        msg.motor_cmd()[i].dq(0);       // 速度 = 0（保持静止）
        msg.motor_cmd()[i].kp(1.5);     // 较高的位置刚度（抓得更紧）
        msg.motor_cmd()[i].kd(0.1);     // 阻尼
    }

    msg.reserve()[0] = 0;
    handcmd_publisher->Write(msg);
    usleep(1000000);  // 1 秒发送一次（低频维持）
}
```

**与 rotateMotors 的区别：**

| 对比项 | rotateMotors | gripHand |
|--------|-------------|----------|
| 运动方式 | 正弦波连续运动 | 固定位置保持 |
| kp | 0.5 | 1.5（更强的位置保持力） |
| timeout | 开启（1s） | 禁用 |
| 控制频率 | 100μs（10kHz） | 1s（1Hz） |
| 用途 | 电机测试 | 持续抓握 |

### 5.4 停止电机 `stopMotors()`

**功能**：停止所有电机运动。通过将 kp、kd、q 全部设为 0 来释放电机。

```cpp
void stopMotors() {
    for (int i = 0; i < MOTOR_MAX; i++) {
        RIS_Mode_t ris_mode;
        ris_mode.id = i;
        ris_mode.status = 0x01;     // FOC 模式（保持使能但不输出力矩）
        ris_mode.timeout = 0x01;

        uint8_t mode = 0;
        mode |= (ris_mode.id & 0x0F);
        mode |= (ris_mode.status & 0x07) << 4;
        mode |= (ris_mode.timeout & 0x01) << 7;

        msg.motor_cmd()[i].mode(mode);
        msg.motor_cmd()[i].tau(0);      // 扭矩 = 0
        msg.motor_cmd()[i].dq(0);       // 速度 = 0
        msg.motor_cmd()[i].kp(0);       // 位置刚度 = 0（不追踪位置）
        msg.motor_cmd()[i].kd(0);       // 速度阻尼 = 0（无阻尼）
        msg.motor_cmd()[i].q(0);        // 目标位置 = 0
    }

    handcmd_publisher->Write(msg);
    usleep(1000000);  // 1 秒发送一次
}
```

> **注意**：停止时 status 仍然设为 0x01（FOC），而非 0x00（锁定）。如果需要完全锁定电机，应将 status 设为 0x00。

### 5.5 打印电机状态 `printState()`

**功能**：读取当前电机状态并将位置归一化到 [0, 1] 范围显示。

```cpp
void printState(bool isLeftHand) {
    Eigen::Matrix<float, 7, 1> q;
    const float* maxTorqueLimits = isLeftHand ? maxTorqueLimits_left : maxTorqueLimits_right;
    const float* minTorqueLimits = isLeftHand ? minTorqueLimits_left : minTorqueLimits_right;

    for (int i = 0; i < 7; i++) {
        q(i) = state.motor_state()[i].q();     // 读取当前位置（rad）
        // 归一化到 [0, 1]
        q(i) = (q(i) - minTorqueLimits[i]) / (maxTorqueLimits[i] - minTorqueLimits[i]);
        q(i) = std::clamp(q(i), 0.0f, 1.0f);  // 钳位防止越界
    }

    if (isLeftHand)
        std::cout << " L: " << q.transpose() << std::endl;
    else
        std::cout << " R: " << q.transpose() << std::endl;

    usleep(0.1 * 1e6);  // 100ms 间隔
}
```

**输出示例：**

```
 L: 0.52 0.31 0.78 0.45 0.60 0.22 0.85
 R: 0.48 0.29 0.75 0.43 0.58 0.20 0.82
```

每个值对应一个电机的归一化位置（0 = 最小限位，1 = 最大限位）。

### 5.6 读取 IMU 和传感器数据示例

```cpp
void printSensorData() {
    // --- IMU 数据 ---
    auto& imu = state.imu_state();
    std::cout << "=== IMU ===" << std::endl;
    std::cout << "  Quaternion [w,x,y,z]: ["
              << imu.quaternion()[0] << ", " << imu.quaternion()[1] << ", "
              << imu.quaternion()[2] << ", " << imu.quaternion()[3] << "]" << std::endl;
    std::cout << "  Gyroscope [x,y,z]: ["
              << imu.gyroscope()[0] << ", " << imu.gyroscope()[1] << ", "
              << imu.gyroscope()[2] << "] rad/s" << std::endl;
    std::cout << "  Accelerometer [x,y,z]: ["
              << imu.accelerometer()[0] << ", " << imu.accelerometer()[1] << ", "
              << imu.accelerometer()[2] << "] m/s^2" << std::endl;
    std::cout << "  RPY [r,p,y]: ["
              << imu.rpy()[0] << ", " << imu.rpy()[1] << ", "
              << imu.rpy()[2] << "] rad" << std::endl;
    std::cout << "  Temperature: " << imu.temperature() << " C" << std::endl;

    // --- 压力传感器 ---
    auto& press = state.press_sensor_state();
    std::cout << "=== Pressure Sensors ===" << std::endl;
    for (int i = 0; i < 12; i++) {
        float p = press.pressure()[i];
        if (p >= 100000) {
            std::cout << "  Sensor[" << i << "]: " << p / 10000.0 << std::endl;
        } else if (p == 30000) {
            std::cout << "  Sensor[" << i << "]: N/A" << std::endl;
        }
    }

    // --- 电源状态 ---
    std::cout << "=== Power ===" << std::endl;
    std::cout << "  Voltage: " << state.power_v() << " V" << std::endl;
    std::cout << "  Current: " << state.power_a() << " A" << std::endl;

    // --- 错误码 ---
    std::cout << "=== Errors ===" << std::endl;
    std::cout << "  Board error: " << state.error()[0] << std::endl;
    for (int i = 0; i < 7; i++) {
        std::cout << "  Motor[" << i << "] error: "
                  << state.motor_state()[i].reserve()[0] << std::endl;
    }
}
```

---

## 6. 编程要点总结

### 6.1 mode 字段速查

```cpp
// 底层位域拼接方式（示例代码中的写法）
uint8_t mode = (i & 0x0F) | (0x01 << 4) | (0x01 << 7);
//               id=0~6      status=FOC    timeout=ON

// DDS 层简化方式（如果不需要底层控制）
msg.motor_cmd()[i].mode(1);   // 1 = FOC
msg.motor_cmd()[i].mode(0);   // 0 = 锁定
```

### 6.2 控制模式选择

| 场景 | kp | kd | tau | timeout | 频率 | 说明 |
|------|:--:|:--:|:---:|:-------:|:----:|------|
| 电机测试 | 0.5 | 0.1 | 0 | ON | 10kHz | 正弦波全行程测试 |
| 抓握保持 | 1.5 | 0.1 | 0 | OFF | 1Hz | 持续抓取物体 |
| 停止电机 | 0 | 0 | 0 | ON | 1Hz | 释放电机 |
| 精细控制 | 可调 | 可调 | 可调 | ON | ≥1kHz | 灵巧操作 |

### 6.3 PD 控制器调参指南

```
输出力矩 = kp × (q_target - q_actual) + kd × (0 - dq_actual) + tau
```

| 参数 | 增大效果 | 减小效果 | 典型范围 |
|------|---------|---------|---------|
| kp | 位置跟踪更快更准，但可能振荡 | 响应变慢，位置误差增大 | 0.1 ~ 2.0 |
| kd | 阻尼增大，减少振荡 | 阻尼减小，可能振荡 | 0.01 ~ 0.5 |
| tau | 增加前馈力矩 | 减少前馈力矩 | 根据负载计算 |

### 6.4 常见注意事项

1. **左右手限位值不同**：左手和右手的电机限位值需要分别标定和存储
2. **URDF 与 IDL 索引不一致**：做仿真-实物迁移时要注意映射关系（§2.3）
3. **传感器有效值判断**：`pressure >= 100000` 才是有效数据，`30000` 表示无数据
4. **超时保护**：默认 1 秒超时，需要持续发送命令；超时后电机自动停止
5. **控制频率**：命令建议 10~1000 Hz；状态反馈固定 1000 Hz
6. **错误码**：`HandState_.error[0]` 为主板错误，`MotorState_.reserve[0]` 为各电机错误码
7. **温度监控**：`MotorState_.temperature[0]` = 线圈温度，`[1]` = 驱动板温度

---

## 7. 参考链接

| 资源 | 链接 |
|------|------|
| DDS 通信文档 | [基于DDS的上层通信方式](https://support.unitree.com/home/zh/dex3-1_hand/DDS-based_communication_method) |
| IDL 接口规范 | [灵巧手控制接口文件含义解释](https://support.unitree.com/home/zh/dex3-1_hand/Dex_IDL_specification) |
| unitree_sdk2 | [SDK 获取](https://support.unitree.com/home/zh/G1_developer/get_sdk) |
| 示例代码 | [GitHub - dex3_subscribe.cpp](https://github.com/unitreerobotics/unitree_sdk2/blob/main/example/g1/dex3/dex3_subscribe.cpp) |
| URDF 模型 | [unitree_ros](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description) |
| MotorState_ 定义 | [H1 底层服务接口](https://support.unitree.com/home/zh/H1_developer/H1-2_Basic_Services_Interface) |
| 错误码说明 | [G1 电机状态错误](https://support.unitree.com/home/zh/G1_developer/common_istakes_and_definitions) |

---

## 8. Tag

#机器人 #宇树 #Dex3-1 #灵巧手 #DDS #SDK #接口文档 #G1 #IMU #触觉传感器
