# G1 + Dex3 + XR 遥操通信流程详解

> 对应代码：`xr_teleoperate/teleop/teleop_hand_and_arm.py`（官方正式 owner）
> 当前运行 profile：`G1_23 + dex3 + hand + 30Hz + --motion + --record + --project-no-deadman + --project-official-initial-follow`
> 运行脚本：`g1-dex3-care-vla/scripts/g1_official_xr_session_run.sh`
> 最后核对日期：2026-08-07

---

## 一、整体架构总览

三个物理节点，两条物理链路：

```
┌─────────────┐      WiFi 5G (WSS/HTTPS)       ┌──────────────┐      有线 enp3s0 (DDS + ZMQ + RPC)      ┌────────────────────────┐
│  Meta Quest3 │◄══════════════════════════════►│   主机 PC     │◄══════════════════════════════════════►│        G1 机器人         │
│  (XR 头显)   │     vuer :8012 (自签 HTTPS)     │ 192.168.123.99│                                        │ .161 运控 / .164 机载图像 │
└─────────────┘                                  └──────────────┘                                        └────────────────────────┘
       ▲                                                 ▲
       │ WiFi 是唯一无线段                                 │ 全部有线
       │ 视频下行 + 手部追踪上行                           │ DDS 控制双向 + ZMQ 图像下行 + RPC 模式切换
       └─────────── 卡顿/延迟的唯一瓶颈点 ──────────────────┘
```

**关键认知**：
- DDS 控制链路**全程有线**，不经 WiFi。WiFi 断了机器人不会失控，只会失去 XR 输入。
- WiFi **只服务 Quest**，频段/省电是 XR 体验的单一瓶颈点。
- `.161` 是运控（DDS lowstate/lowcmd），`.164` 是机载图像服务，两者都在 G1 侧、同子网、走同一根有线。

---

## 二、链路 1：主机 ↔ G1（DDS，有线，实时控制）

### 2.1 传输机制

- 走 `--network-interface enp3s0` 指定的网卡（192.168.123.99/24）
- DDS pub/sub 多播，Domain 0，同子网内所有参与者自动发现（非点对点 TCP）
- 用 `unitree_sdk2py` 的 `ChannelPublisher` / `ChannelSubscriber`
- 代码入口：`teleop/robot_control/robot_arm.py:18-20`

### 2.2 DDS Topic 一览

| Topic | 方向 | 消息类型 | 内容 | 频率 |
|---|---|---|---|---|
| `rt/lowstate` | G1 → 主机 | `hg_LowState` | 全身电机 q/dq、mode_machine | 订阅线程 2ms 轮询（~500Hz） |
| `rt/arm_sdk` | 主机 → G1 | `hg_LowCmd` | 双臂 10 关节 lowcmd（**motion mode**，固件侧平滑） | **250Hz**（`control_dt=1/250`） |
| `rt/lowcmd` | 主机 → G1 | `hg_LowCmd` | 双臂 lowcmd（**debug mode**，直驱电机） | 250Hz |
| `rt/dex3/left/cmd` | 主机 → G1 | `HandCmd_` | 左手 Dex3 7 指目标 | 30Hz |
| `rt/dex3/right/cmd` | 主机 → G1 | `HandCmd_` | 右手 Dex3 7 指目标 | 30Hz |
| `rt/dex3/left/state` | G1 → 主机 | `HandState_` | 左手手指状态 | — |
| `rt/dex3/right/state` | G1 → 主机 | `HandState_` | 右手手指状态 | — |

> 当前 profile 用 `--motion`，手臂命令走 `rt/arm_sdk`。`robot_arm.py:469` 的 `kNotUsedJoint0.q = 1.0` 是 motion mode 的启用标志位，固件见此位才接管平滑。

### 2.3 电机级参数（G1_23，`robot_arm.py:370-378`）

| 关节类别 | kp | kd | 说明 |
|---|---|---|---|
| 腿部等强电机 | 300.0 | 3.0 | `kp_high/kd_high`，锁住不动 |
| 肩/肘（弱电机） | 80.0 | 3.0 | `kp_low/kd_low`，跟随 XR |
| 腕 Roll | 40.0 | 1.5 | `kp_wrist/kd_wrist`，低刚度防扭伤 |

- `arm_velocity_limit = 20.0`（rad/s），`speed_gradual_max(t=5.0)` 在 `s` 启动后 5 秒线性爬到 30
- `clip_arm_q_target`（`robot_arm.py:460`）按 `velocity_limit * control_dt` 限幅单 tick 增量，防甩
- 发布线程 250Hz 独立跑（`robot_arm.py:467`），与 30Hz 主循环解耦

### 2.4 RPC 通道（非 DDS）

| 客户端 | 用途 | 触发时机 |
|---|---|---|
| `MotionSwitcherClient`（`utils/motion_switcher.py:9`） | debug/ai 模式切换 | 启动时 `Enter_Debug_Mode` 释放 ai 模式，让出 lowcmd 通道 |
| `LocoClient`（`utils/motion_switcher.py:33`） | 底盘行走 | **仅 `--input-mode controller` 时**调用 `Move/Damp`；当前 hand 模式不触发 |

---

## 三、链路 2：主机 ↔ G1 机载图像服务（ZMQ + TCP，有线）

### 3.1 传输机制

- G1 机载计算单元 `192.168.123.164` 跑 `ImageServer`，主机用 `ImageClient`（`teleimager/src/teleimager/image_client.py:677`）连接
- 启动时先 TCP REQ/REP 拉一次 `cam_config`，再按 config 起 ZMQ SUB 订阅各路相机
- 服务端配置：`teleimager/cam_config_server.yaml`；客户端默认：`teleimager/cam_config_client.yaml`

### 3.2 端口与数据流

| 端口 | 协议 | 方向 | 内容 |
|---|---|---|---|
| `.164:60000` | ZMQ REQ/REP（TCP） | 主机 → G1 | 启动时拉一次 `cam_config`（分辨率/帧率/各路开关/serial） |
| `.164:55555` | ZMQ PUB/SUB | G1 → 主机 | 头部相机 JPEG（quality 50，30fps） |
| `.164:55556` | ZMQ PUB/SUB | G1 → 主机 | 左腕相机 JPEG |
| `.164:55557` | ZMQ PUB/SUB | G1 → 主机 | 右腕相机 JPEG |
| `.164:60001-60003` | WebRTC（可选） | — | 当前未启用（`enable_webrtc: false` in client config） |

### 3.3 抗堆积机制（`image_client.py`）

- 客户端 `RCVHWM=1` + `LINGER=0`（`:415-416`）：只保最新帧，不排队
- 三环缓冲 `TripleRingBuffer`：写入/读取分离，避免读写竞争
- BGR 解码队列 `maxsize=1`（`:351`）：满了就丢最旧，单独解码线程
- 服务端 `SNDHWM=1`（`:148`）：发布侧也只保最新
- **结论**：主机侧不会堆积，延迟只可能来自服务端发布慢或网络

---

## 四、链路 3：主机 ↔ Quest（WebSocket，WiFi 5G）

### 4.1 传输机制

- televuer 在主机起 vuer 服务：`Vuer(host='0.0.0.0', cert=..., key=..., queue_len=3)`（`televuer.py:104`）
- 默认端口 **8012**，HTTPS + 自签证书（`televuer.py:104`）
- Quest 浏览器加载 `https://<主机IP>:8012`，建立 WSS 长连接
- **这是唯一走 WiFi 的链路**，也是卡顿/延迟的唯一无线瓶颈

### 4.2 双向数据流

| 流向 | 内容 | 频率/机制 | 代码 |
|---|---|---|---|
| 主机 → Quest | `ImageBackground`（JPEG quality 50，头部相机画面） | `display_fps=15`，即 67ms/帧 | `televuer.py:412-428` |
| Quest → 主机 | `Hands` 手部 25 关节关键点 pose（stream=True） | 60Hz 事件驱动 | `televuer.py:292-323` |
| Quest → 主机 | 头部位姿 `on_cam_move`（16 元矩阵） | 事件驱动 | `televuer.py:235` |
| Quest → 主机 | 手柄按键/摇杆（controller 模式） | 事件驱动 | `televuer.py:242+` |
| 主机 → Quest | ego 模式小窗反馈 | 同 display_fps | `televuer.py:507+` |

### 4.3 关键设计

- `queue_len=3`：vuer WebSocket 发送队列上限 3 帧，超时丢旧（`televuer.py:104`）
- `display_fps=15.0`：commit `e80ea88` 把显示帧率从 30 降到 15，**优先保证手部追踪事件处理**，视频次之
- 手部追踪事件优先于视频协程调度（asyncio 事件循环内）
- 图像写入：`render_to_xr`（`televuer.py:215`）只设 `latest_frame` + `new_frame_event.set()`，由独立 writer 线程 BGR→RGB 拷进共享内存，非阻塞

---

## 五、主机内部进程/线程模型

### 5.1 进程结构

| 进程/线程 | 职责 | 频率 | IPC 方式 |
|---|---|---|---|
| **主进程主循环** | get_tele_data → IK → ctrl_dual_arm → record | 30Hz | — |
| Arm 发布线程（`threading.Thread`，`robot_arm.py:442`） | 读 q_target，clip，DDS publish `rt/arm_sdk` | **250Hz** | `ctrl_lock` 保护 q_target |
| Arm 订阅线程（`threading.Thread`，`robot_arm.py:449`） | 订阅 `rt/lowstate`，写 `lowstate_buffer` | 2ms 轮询 | `DataBuffer` |
| Dex3 手部 retarget 进程（`multiprocessing.Process`，`robot_hand_unitree.py:108`） | 读 hand_pos_array → retarget → 发 `rt/dex3/*/cmd` | 独立循环 | `multiprocessing.Array('d',75)` |
| Dex3 手状态订阅线程 | 订阅 `rt/dex3/*/state` | — | `Array` |
| ZMQ 相机订阅线程（每路一个，`image_client.py:326`） | ZMQ SUB recv → 三环缓冲 | 100ms poll | `TripleRingBuffer` |
| vuer 事件循环（asyncio） | WSS 收发、JPEG 编码推送 | display_fps=15 | `shared_memory` + `Array/Value` |
| 图像 writer 线程（`televuer.py:205`） | BGR→RGB 拷到 img2display 共享内存 | 事件驱动 | `shared_memory.SharedMemory` |

### 5.2 共享内存 IPC

- 主进程 ↔ televuer：`multiprocessing.Array/Value`
  - `left/right_hand_position_shared`（75 doubles，25 关节 × 3）
  - `head_pose_shared`、`left/right_arm_pose_shared`（16 doubles，4×4 矩阵）
  - `motion_data_ready_shared`（bool，XR 数据就绪标志）
  - 各种 pinch/squeeze/trigger 值
- 主进程 ↔ 图像显示：`shared_memory.SharedMemory`（`img2display`，大小 = `prod(img_shape) × 1` 字节）
- 主进程 ↔ Dex3：`multiprocessing.Array('d', 75)` 双手关键点 + `Lock`

### 5.3 频率分层

```
250Hz  ── Arm DDS 发布线程（motion mode 固件平滑）
 30Hz  ── 主循环（IK + 控制 + 录制 + 取 XR 数据）
 15Hz  ── vuer 视频推送（display_fps）
 ~60Hz ── Quest 手部追踪事件上报
 2ms   ── DDS lowstate 订阅轮询
```

`--affinity` 把主进程钉到核 0-3、子进程（televuer 等）钉到核 5-6、`nice -20`，保证 250Hz 发布线程不被抢占（`teleop_hand_and_arm.py:392-409`）。

---

## 六、端到端数据流路径

### 6.1 控制路径（手部 → 机器人，决定"卡不卡"）

```
Quest 手部 25 关节 pose
   │  (WSS, WiFi 5G, ~60Hz 事件)
   ▼
vuer:8012 事件循环  ──►  extract_hand_poses  ──►  left/right_hand_position_shared (Array, 75 doubles)
   │
   ▼
主循环 get_tele_data (30Hz)  ──►  tele_data.left/right_wrist_pose + hand_pos
   │
   ├──► 双手：left_hand_pos_array (Array) ──► Dex3 retarget 进程 ──► rt/dex3/{l,r}/cmd (DDS)
   │
   └──► 双臂：ArmIK.solve_ik(left_wrist, right_wrist, current_q, current_dq) ──► sol_q, sol_tauff
          │
          ▼
       arm_ctrl.ctrl_dual_arm(sol_q, sol_tauff)  ──►  q_target (ctrl_lock 保护)
          │
          ▼
       Arm 发布线程 (250Hz) ──► clip_arm_q_target ──► DDS rt/arm_sdk ──► G1 固件 ──► 电机
```

**延迟敏感点**：WiFi 抖动 → hand pose 到达时间不规律 → IK 输入跳变 → sol_q 跳变 → 手臂抖。这是 2.4G 时"卡"的机理。

### 6.2 视频路径（相机 → 头显，决定"延迟感"）

```
G1 头部相机 (realsense/uvc, 30fps)
   │  (ZMQ PUB, 有线, .164:55555, SNDHWM=1)
   ▼
ImageClient ZMQ SUB 线程 (RCVHWM=1, 三环缓冲)
   │  get_head_frame() → bgr
   ▼
主循环 tv_wrapper.render_to_xr(bgr)  ──►  latest_frame + new_frame_event.set()
   │
   ▼
writer 线程 (BGR→RGB, 拷到 img2display 共享内存)
   │
   ▼
vuer async 协程 main_image_*_zmq (display_fps=15)
   │  ImageBackground(JPEG quality=50) → session.upsert
   ▼
vuer WSS:8012  ──►  WiFi 5G  ──►  Quest 浏览器渲染
```

**延迟敏感点**：WiFi 带宽不够 → vuer `queue_len=3` 队列顶爆 → 帧累积 → 10s 延迟。5G 掉 2.4G 时链路速率从 351Mb/s 掉到 52Mb/s，必爆。

### 6.3 录制路径（写入磁盘）

```
主循环 30Hz
   ├── colors: img_client.get_{head,left_wrist,right_wrist}_frame() → JPEG 写 colors/ 目录
   ├── states: arm_ctrl.get_current_dual_arm_q/dq + dual_hand_state_array
   ├── actions: sol_q + dual_hand_action_array
   └──► EpisodeWriter buffer
          │
          ▼ (s 键结束 segment)
       data.json + colors/ + depths/ + audios/  ──►  data/episodes/official-xr-native/<task>/<task>/episode_NNNN/
          │
          ▼ (并行)
       ProjectTraceWriter  ──►  data/episodes/official-xr-v3/<task>-<ts>/  (V3 trace，含 writer_facts)
```

- `--project-no-deadman` + `--project-official-initial-follow`：从启动即连续 IK 跟随，无需 Space deadman
- V3 不把手势停止、事件过期或 Quest 断连当作 release；`q` 是正常停止入口，退出后手臂保持当时姿态，不会自动回零
- V3 schema：`unitree_official_xr_trace_v3`，含 `writer_facts_after_observation_v1` 控制证据
- 单 segment 上限 180 秒（`--project-max-episode-seconds 180`）

---

## 七、关键参数速查

### 7.1 运行脚本参数（`g1_official_xr_session_run.sh:132-144`）

```bash
--frequency 30                 # 主循环频率
--input-mode hand              # 手部追踪（非手柄）
--display-mode ego             # 中心小窗显示机器人视角
--arm G1_23 --ee dex3          # 23 自由度 G1 + Dex3 灵巧手
--img-server-ip 192.168.123.164
--network-interface enp3s0     # DDS 走有线
--headless --record --motion --affinity   # 无 GUI / 录制 / 运控模式 / CPU 亲和
--project-no-deadman           # V3 免 deadman 连续跟随
--project-official-initial-follow  # 启动即 IK 跟随
--project-max-episode-seconds 180
```

### 7.2 可调优参数位置

| 参数 | 位置 | 默认 | 说明 |
|---|---|---|---|
| `display_fps` | `televuer.py:73`（传参处 `teleop_hand_and_arm.py:292`） | 15.0 | 视频推送帧率，WiFi 不够可降到 10 |
| JPEG `quality` | `televuer.py:368/379/421` | 50 | 图像质量，影响带宽 |
| `kp_low/kd_low` | `robot_arm.py:372-373` | 80/3 | 肩肘刚度，官方默认勿乱改 |
| `arm_velocity_limit` | `robot_arm.py:378` | 20→30 | 关节速度限幅，`speed_gradual_max` 5 秒爬升 |
| `control_dt` | `robot_arm.py:379` | 1/250 | DDS 发布频率 |
| `queue_len` | `televuer.py:104` | 3 | vuer WebSocket 队列上限 |

---

## 八、已知故障模式与排查

### 8.1 相机延迟 10s + 手臂卡顿（WiFi 掉 2.4G）

**根因**：USB WiFi 网卡（`wlx6c1ff7875269`）发热时从 5G 漫游到 2.4G，SSID 仍叫 `-5G` 但实际频率 2.4GHz，链路速率 52Mb/s 不够传视频。

**排查**：
```bash
iwconfig wlx6c1ff7875269 | grep -E "Frequency|Power Management"
# 健康：Frequency:5.x GHz + Power Management:off
# 异常：Frequency:2.4xx GHz → 重插网卡或强制 5G
```

**修复**：
- 重插网卡恢复 5G
- 关省电：`sudo iwconfig wlx6c1ff7875269 power off`（运行时）+ `sudo nmcli connection modify "X80-8F96FF-5G" wifi.powersave 2`（持久化）
- 注意：本机没装 `iw`，用 `iwconfig`

### 8.2 motion mode 仍卡（CPU 抖动）

**根因**：250Hz 发布线程被抢占。

**修复**：加 `--affinity`（已加入脚本），主进程钉核 0-3、子进程钉核 5-6、`nice -20`。无 root 也能生效 CPU 亲和性，仅 `nice` 会 warning。

### 8.3 开局特别卡

**根因**：`--project-official-initial-follow` 从第一帧就连续 IK 跟随，但 XR 追踪初始化阶段 pose 噪声大 + `speed_gradual_max` 5 秒爬速。

**修复**：等几秒稳定后再正式操作；属正常过渡。

---

## 九、网络配置快照（2026-08-06 已优化）

| 项 | 值 |
|---|---|
| 主机有线 | `enp3s0` 192.168.123.99/24（DDS + ZMQ + RPC） |
| 主机 WiFi | `wlx6c1ff7875269`，SSID `X80-8F96FF-5G`，5.785 GHz，351 Mb/s |
| WiFi 省电 | off（NM profile `wifi.powersave 2` + 运行时 `iwconfig power off`） |
| G1 运控 | 192.168.123.161（DDS lowstate/arm_sdk） |
| G1 图像服务 | 192.168.123.164（ZMQ 55555-55557 + TCP 60000） |
| vuer 服务 | 0.0.0.0:8012（HTTPS/WSS，自签证书） |
| Quest | 经 WiFi 连主机 8012 |

---

## 十、参考代码位置

| 模块 | 文件 |
|---|---|
| 主循环 | `xr_teleoperate/teleop/teleop_hand_and_arm.py` |
| G1_23 手臂控制 | `xr_teleoperate/teleop/robot_control/robot_arm.py:359` |
| Dex3 手控制 | `xr_teleoperate/teleop/robot_control/robot_hand_unitree.py:46` |
| 手部 retarget | `xr_teleoperate/teleop/robot_control/hand_retargeting.py` |
| IK 求解 | `xr_teleoperate/teleop/robot_control/robot_arm_ik.py` |
| 图像客户端 | `xr_teleoperate/teleop/teleimager/src/teleimager/image_client.py:677` |
| 相机配置 | `xr_teleoperate/teleop/teleimager/cam_config_server.yaml` |
| televuer（Quest 侧） | `xr_teleoperate/teleop/televuer/src/televuer/televuer.py` |
| 模式切换/底盘 | `xr_teleoperate/teleop/utils/motion_switcher.py` |
| 运行脚本 | `g1-dex3-care-vla/scripts/g1_official_xr_session_run.sh` |
