---
title: G1 SDK、DDS、ROS 2 快速说明与当前安排
date: 2026-07-15
tags: [Unitree, G1, SDK, DDS, ROS2, 调试模式]
---

# G1 SDK、DDS、ROS 2 快速说明与当前安排

## 当前已确认

- 机器人：宇树 **G1 EDU+ CN，23DoF**。
- 主机连接 G1 的网卡：`enp3s0`。
- 主机地址：`192.168.123.99/24`；G1 机载电脑：`192.168.123.161`。
- 网络已验证：`ping -I enp3s0 -c 4 -W 2 192.168.123.161` 为 4/4 成功、0% 丢包。
- 机器人尚未开机进入调试模式；DDS 的实际 domain、topic、消息类型、频率和 ROS 2 配置等待实机回读。

本项目从真实机器人通信重新起步。此前仿真、VLA、训练和推理资料不影响当前 SDK 通信基线；后续学习系统以新的真实数据和任务证据重新建立。

## 一句话理解

- **DDS**：机器人与电脑之间传消息的底层“总线”。
- **unitree_sdk2（SDK）**：宇树提供的 C++ 工具箱，把 DDS 的初始化、订阅和回调封装成易用 API。
- **ROS 2**：建立在 DDS 之上的机器人软件框架，提供 node、topic、QoS、参数、launch 和命令行工具。

当前先用 SDK 直连 G1 验证真实消息；ROS 2 随后观察同一消息源。这样每一步都基于已确认事实。

## DDS：消息怎样从机器人到电脑

DDS 是发布/订阅模型：

```text
G1 发布状态消息
  -> 同一 DDS domain 内按 topic 发现订阅者
  -> 消息类型与 QoS 匹配
  -> 电脑上的 subscriber 收到消息并触发 callback
```

收到消息取决于五件事：**网卡、domain、topic 名、消息类型、QoS**。其中任意一项不匹配，订阅器就收不到状态。

官方给出的首个候选入口：

| 候选 topic | 候选类型 | 用途 | 当前状态 |
|---|---|---|---|
| `rt/lowstate` | `unitree_hg::msg::dds_::LowState_` | G1 的模式、IMU、电机等原始状态 | 调试模式后验证 |
| `rt/lf/lowstate` | `LowState_` | 低频状态 | 调试模式后验证 |
| `rt/dex3/<left|right>/state` | `HandState_` | Dex3 状态 | Dex3 实机确认后验证 |

这些名称是官方候选，不是本机已经确认的事实。

## SDK：当前要负责的部分

`unitree_sdk2` 是当前主线。它把 DDS 的 participant、topic 和 subscriber 封装为 `ChannelFactory`、`ChannelSubscriber` 等对象。

概念上的读取流程：

```text
选择 G1 网卡 enp3s0
  -> 初始化 DDS domain
  -> 创建状态 topic 的 subscriber
  -> 注册消息 callback
  -> 每收到一帧：提取摘要、更新计数、显示、判断事件
```

本机安装的 SDK 头文件当前显示初始化签名为 `Init(domain_id, network_interface)`；官方较新页面出现过不同写法。调试前以本机安装头文件与实际消息为准。

SDK 第一阶段的输出只包含：

- 消息是否到达、首次到达时间、样本数；
- 实测频率和断流；
- 真实 topic、type、domain、SDK 身份；
- 允许展示的状态摘要与“模式变化”等应用事件。

当前不建立命令 publisher 或动作 RPC。

## ROS 2：SDK 验证后的观察层

ROS 2 的 node 通过 RMW（ROS Middleware）使用 DDS。它不是替代 SDK 的另一套硬件假设，而是把已验证的状态源组织成标准节点与工具链。

当前学习重点：

| 概念 | 作用 |
|---|---|
| node | 一个独立运行的 ROS 2 程序/组件 |
| topic | 连续消息通道 |
| message type | topic 的数据结构 |
| QoS | 可靠性、队列深度、历史策略；不匹配会收不到消息 |
| RMW | ROS 2 与 DDS 实现之间的抽象层 |
| `ROS_DOMAIN_ID` | ROS 2 使用的 DDS domain 配置，须与实机通信事实核对 |

ROS 2 的发行版、RMW 和 QoS 目前都保持待确认，开机后再由本机环境与 G1 实测决定。

## 当前最小闭环

```text
G1 状态 DDS topic
  -> unitree_sdk2 subscriber
  -> 控制台显示（计数、频率、模式、消息年龄）
  -> 规则事件（首次消息、模式变化、断流）
  -> 操作者看到结果并保存报告
```

这里的“反应”是**电脑应用对真实消息的显示和事件**，用于证明读取、解析和业务判断已经打通。

## 计算机—机器人—计算机的两层闭环

### 第一层：状态观察闭环（当前目标）

```text
G1 -> DDS 状态 -> 电脑 SDK -> 显示/事件 -> 人工确认
```

### 第二层：带机器人回读的请求闭环（第一层稳定后）

```text
电脑请求 -> 经实机确认的官方接口 -> G1 处理
  -> 状态或服务结果返回 -> 电脑显示和核对
```

具体机器人可见响应在第一层通过后，基于实际可用的官方接口另行确定。关节、手臂、Dex3 写入和高难度动作不属于当前阶段。

## 开机进入调试模式后的顺序

1. 按官方流程进入调试模式，记录固件与时间。
2. 记录 SDK 来源、安装路径、版本、实际头文件 API、网卡和 DDS 配置。
3. 以 SDK 只读订阅一个实机确认的状态 topic，连续观察至少 60 秒。
4. 记录接收数、频率、消息年龄、模式字段、断流和停止原因，更新项目合同与报告。
5. 使用 ROS 2 对同一状态源做只读观察，核对 topic、类型、频率和时间字段。
6. 第一层稳定后，再为一个机器人可见响应单独定义接口、输入、回读字段和验收条件。

## 项目内说明书

- `~/github-product/g1-dex3-care-vla/docs/08-SDK_DDS_ROS2_通信闭环.md`
- `~/github-product/g1-dex3-care-vla/docs/03-实机就绪门禁.md`
- `~/github-product/g1-dex3-care-vla/reports/gate0_network_probe_20260715.md`
- `~/github-product/g1-dex3-care-vla/docs/official/unitree_g1_dex3/README.md`
