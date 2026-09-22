# ROS2 核心概念总结

> [!info] 基本信息
> - **ROS2 版本**：Humble Hawksbill (2022-2027 LTS)
> - **适用系统**：Ubuntu 22.04
> - **官方文档**：https://docs.ros.org/en/humble/

---

## 1. 工作空间 (Workspace)

工作空间是存放 ROS2 包的根目录。

### 目录结构

```
ros2_ws/                    ← 工作空间根目录
├── src/                    ← 源代码空间（所有包放这里）
│   ├── my_package/
│   └── my_robot_bringup/
├── build/                  ← 构建空间（编译中间产物）
├── install/                ← 安装空间（可执行文件、launch、配置）
└── log/                    ← 日志
```

### 三个空间的作用

| 空间 | 作用 | 说明 |
|------|------|------|
| **src/** | 源代码 | 开发者编写代码的地方 |
| **build/** | 编译产物 | colcon 自动生成，可删除重建 |
| **install/** | 运行时文件 | 编译后的可执行文件、launch、配置 |

> [!warning] 关键点
> 每次开新终端必须执行 `source install/setup.bash`，否则找不到 ROS2 包。

### 常用命令

```bash
# 创建工作空间
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws

# 构建
colcon build                              # 构建所有包
colcon build --packages-select 包名        # 构建指定包
colcon build --packages-select pkg1 pkg2  # 构建多个包

# 清理
rm -rf build/ install/ log/               # 完整清理重建

# 环境配置
source /opt/ros/humble/setup.bash         # 加载 ROS2 基础环境
source install/setup.bash                 # 加载工作空间环境
```

---

## 2. 包 (Package)

包是 ROS2 的基本组织单元，一个包 = 一组相关的功能。

### 包的类型

| 类型 | 构建工具 | 典型用途 |
|------|---------|---------|
| `ament_cmake` | CMake | C++ 节点、纯资源包 |
| `ament_python` | setuptools | Python 节点 |

### 包的目录结构

```
my_package/
├── package.xml              ← 包的"身份证"（名字、依赖、描述）
├── CMakeLists.txt           ← C++ 包的构建规则
├── setup.py                 ← Python 包的构建规则
├── launch/                  ← launch 文件
├── msg/                     ← 自定义消息定义
├── srv/                     ← 自定义服务定义
├── action/                  ← 自定义动作定义
├── src/                     ← C++ 源码（ament_cmake）
└── my_package/              ← Python 模块（ament_python）
```

### package.xml 详解

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_robot_bringup</name>          <!-- 包名 -->
  <version>1.0.0</version>               <!-- 版本号 -->
  <description>Bringup package</description>
  <maintainer email="user@example.com">user</maintainer>
  <license>MIT</license>

  <!-- 构建依赖（编译时需要） -->
  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- 运行时依赖 -->
  <depend>rclcpp</depend>                 <!-- C++ 客户端库 -->
  <depend>rclpy</depend>                  <!-- Python 客户端库 -->

  <!-- 可选依赖 -->
  <exec_depend>launch_ros</exec_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

### 依赖类型对比

| 标签 | 含义 | 场景 |
|------|------|------|
| `<depend>` | 同时是 build + exec + build_export | 最常用 |
| `<build_depend>` | 仅编译时需要 | 头文件、生成器 |
| `<exec_depend>` | 仅运行时需要 | launch、配置文件 |
| `<buildtool_depend>` | 构建工具 | ament_cmake、ament_python |

---

## 3. 节点 (Node)

节点是 ROS2 中**最小的执行单元**，每个节点做一件事。

### C++ 节点

```cpp
#include <rclcpp/rclcpp.hpp>

class NumberPublisher : public rclcpp::Node {
public:
    NumberPublisher() : Node("number_publisher_node") {  // ← 节点名
        publisher_ = this->create_publisher<std_msgs::msg::Int32>("number", 10);
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&NumberPublisher::timer_callback, this));
    }

private:
    void timer_callback() {
        auto msg = std_msgs::msg::Int32();
        msg.data = 42;
        publisher_->publish(msg);
    }

    rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NumberPublisher>());
    rclcpp::shutdown();
    return 0;
}
```

### Python 节点

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class NumberPublisher(Node):
    def __init__(self):
        super().__init__('number_publisher_node')  # ← 节点名
        self.publisher_ = self.create_publisher(Int32, 'number', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Int32()
        msg.data = 42
        self.publisher_.publish(msg)

def main(args=None):
    rclcpp = rclpy.init(args=args)
    node = NumberPublisher()
    rclcpp.spin(node)
    node.destroy_node()
    rclcpp.shutdown()

if __name__ == '__main__':
    main()
```

### 节点的三大能力

| 能力 | 说明 | 适用场景 |
|------|------|---------|
| **发布/订阅 (Pub/Sub)** | 异步通信 | 传感器数据、持续流 |
| **服务 (Service)** | 请求-响应 | 一次性查询、触发操作 |
| **动作 (Action)** | 长时间任务 | 导航、抓取、规划 |

---

## 4. ⭐ 核心易混淆概念

> [!danger] 最重要的部分
> 以下概念是 ROS2 中**最容易搞混**的，务必理解清楚。

### 4.1 包名 vs 可执行文件名 vs 节点名

| 概念 | 定义位置 | 作用 | 示例 |
|------|---------|------|------|
| **包名** | `package.xml` → `<name>` | 标识包的身份 | `my_cpp_pkg` |
| **可执行文件名** | `CMakeLists.txt` → `add_executable(...)` | 编译后生成的二进制文件 | `number_publisher` |
| **节点名** | 代码中 `Node('name')` | 运行时在 ROS2 网络中的标识 | `number_publisher_node` |

### 关系图

```
包 (my_cpp_pkg)
  └── CMakeLists.txt 定义可执行文件: add_executable(number_publisher src/main.cpp)
        └── 代码中定义节点名: Node("number_publisher_node")
              └── 运行时: ros2 run my_cpp_pkg number_publisher
                           ↑包名        ↑可执行文件名
                           → 节点名是代码里定义的 "number_publisher_node"
```

### 实际示例

```cpp
// CMakeLists.txt
add_executable(number_publisher src/number_publisher.cpp)  ← 可执行文件名

// number_publisher.cpp
class NumberPublisher : public rclcpp::Node {
    NumberPublisher() : Node("number_publisher_node") {}  ← 节点名
};

// 运行命令
ros2 run my_cpp_pkg number_publisher
//         ↑包名     ↑可执行文件名    → 节点名是代码里定义的 number_publisher_node

// 查看节点
ros2 node list
// 输出: /number_publisher_node   ← 这是节点名
```

### 4.2 命名空间 (Namespace)

命名空间 = 节点的**父级前缀**，用于隔离和组织节点。

```bash
# 不带命名空间
ros2 run my_pkg my_node
# 节点名: /my_node

# 带命名空间
ros2 run my_pkg my_node --ros-args -r __ns:=/robot1
# 节点名: /robot1/my_node
```

### 命名空间的作用：多机器人隔离

```
/                              ← 根命名空间
├── robot1/                    ← 命名空间 robot1
│   ├── camera_node            → /robot1/camera_node
│   └── lidar_node             → /robot1/lidar_node
└── robot2/                    ← 命名空间 robot2
    ├── camera_node            → /robot2/camera_node（同名但不冲突）
    └── lidar_node             → /robot2/lidar_node
```

### Launch 文件中设置命名空间

```xml
<launch>
    <node pkg="my_pkg" exec="my_node" namespace="robot1" />
    <!-- 运行后节点名为: /robot1/my_node -->
</launch>
```

### 4.3 全限定名 (Fully Qualified Name)

```
/robot1/camera_node
│  │      │
│  │      └── 节点名
│  └── 命名空间
└── 根命名空间
```

### 4.4 概念对比表

| 容易混淆 | 区别 |
|---------|------|
| **包名 vs 节点名** | 包名是文件夹名（静态），节点名是代码里定义的（运行时） |
| **可执行文件名 vs 节点名** | 可执行文件名是编译产物，节点名是 `Node('xxx')` 里的字符串 |
| **命名空间 vs 节点名** | 命名空间是 `/ns/node_name` 中的 `/ns` 部分 |
| **build/ vs install/** | build 是编译中间产物，install 是可运行的最终产物 |
| **launch vs ros2 run** | launch 同时启动多个节点，ros2 run 启动单个节点 |

---

## 5. 通信机制

### 5.1 话题 (Topic)

话题是 ROS2 中最常用的通信方式，**异步、一对多**。

```
发布者 (Publisher)  ─── 话题 /camera/image  ──→  订阅者 (Subscriber)
                         (持续数据流)
```

**特点：**
- 发布-订阅模式，异步通信
- 一对多：一个话题可以有多个发布者和订阅者
- 消息队列：缓冲未处理的消息

**C++ 示例：**

```cpp
// 发布者
auto pub = node->create_publisher<std_msgs::msg::String>("chatter", 10);
auto msg = std_msgs::msg::String();
msg.data = "Hello";
pub->publish(msg);

// 订阅者
auto sub = node->create_subscription<std_msgs::msg::String>(
    "chatter", 10,
    [](const std_msgs::msg::String::SharedPtr msg) {
        RCLCPP_INFO(node->get_logger(), "Received: %s", msg->data.c_str());
    });
```

**Python 示例：**

```python
# 发布者
pub = self.create_publisher(String, 'chatter', 10)
msg = String()
msg.data = "Hello"
pub.publish(msg)

# 订阅者
sub = self.create_subscription(String, 'chatter', self.callback, 10)

def callback(self, msg):
    self.get_logger().info(f"Received: {msg.data}")
```

### 5.2 服务 (Service)

服务是**同步、一对一**的请求-响应通信。

```
客户端 (Client)  ─── 请求 ──→  服务端 (Server)
                               │
客户端 (Client)  ←── 响应 ───  服务端 (Server)
```

**特点：**
- 请求-响应模式，同步通信
- 客户端发送请求后阻塞等待响应
- 适合一次性查询、触发操作

**服务定义文件 (.srv)：**

```srv
# AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

### 5.3 动作 (Action)

动作是**长时间运行任务**，支持取消和进度反馈。

```
客户端 (Client)  ─── 目标 ──→  服务端 (Server)
                               │
客户端 (Client)  ←── 反馈 ───  服务端 (Server)  (持续更新进度)
                               │
客户端 (Client)  ←── 结果 ───  服务端 (Server)  (最终结果)
```

**特点：**
- 目标-反馈-结果模式
- 支持取消长时间运行的任务
- 适合导航、抓取、规划等场景

**动作定义文件 (.action)：**

```action
# Fibonacci.action
int32 order          # 目标（Goal）
---
int32[] sequence     # 结果（Result）
---
int32[] partial_sequence  # 反馈（Feedback）
```

### 5.4 通信方式对比

| 特性 | Topic | Service | Action |
|------|-------|---------|--------|
| 通信模式 | 发布/订阅 | 请求/响应 | 目标/反馈/结果 |
| 方向 | 单向（多对多） | 双向（一对一） | 双向 |
| 是否阻塞 | 非阻塞 | 阻塞等待响应 | 非阻塞+反馈 |
| 适用场景 | 传感器数据、持续流 | 一次性查询 | 长时间任务 |
| 消息文件 | `.msg` | `.srv` | `.action` |

### 5.5 QoS（Quality of Service）

QoS 控制话题通信的可靠性、持久性等。

| QoS 策略 | 说明 |
|---------|------|
| `RELIABLE` | 保证消息送达（可能重复） |
| `BEST_EFFORT` | 尽力送达，不保证（适合传感器） |
| `VOLATILE` | 不保存历史消息 |
| `TRANSIENT_LOCAL` | 保存最近 N 条消息（新订阅者可获取） |
| `KEEP_LAST(n)` | 保留最近 n 条消息 |
| `KEEP_ALL` | 保留所有消息 |

---

## 6. 参数 (Parameter)

参数是节点的**配置项**，运行时可以修改。

### 代码中声明参数

```cpp
// C++
this->declare_parameter("rate", 10);           // 带默认值
this->declare_parameter("topic_name", "data"); // 字符串参数
int rate = this->get_parameter("rate").as_int();
```

```python
# Python
self.declare_parameter('rate', 10)
rate = self.get_parameter('rate').value
```

### 参数设置方式

```bash
# 方式 1：命令行
ros2 run my_pkg my_node --ros-args -p rate:=20

# 方式 2：YAML 文件
ros2 run my_pkg my_node --ros-args --params-file config.yaml

# 方式 3：Launch 文件
<node pkg="my_pkg" exec="my_node">
    <param name="rate" value="20" />
</node>
```

### 参数命令

```bash
ros2 param list                    # 列出所有参数
ros2 param get /node_name rate     # 获取某个参数值
ros2 param set /node_name rate 30  # 修改参数值
ros2 param dump /node_name         # 导出参数到文件
ros2 param load /node_name config.yaml  # 加载参数文件
```

---

## 7. Launch 文件

Launch 文件 = 同时启动多个节点 + 配置参数 + 设置命名空间。

### 三种格式

| 格式 | 语言 | 后缀 | 推荐度 |
|------|------|------|--------|
| XML | XML | `.launch.xml` | ⭐⭐⭐ 简洁 |
| Python | Python | `.launch.py` | ⭐⭐⭐ 灵活 |
| YAML | YAML | `.launch.yaml` | ⭐⭐ 简单 |

### XML 示例

```xml
<launch>
    <!-- 启动节点 -->
    <node pkg="my_py_pkg" exec="number_publisher" />
    <node pkg="my_cpp_pkg" exec="number_counter" />

    <!-- 设置命名空间 -->
    <node pkg="my_pkg" exec="my_node" namespace="robot1" />

    <!-- 传入参数 -->
    <node pkg="my_pkg" exec="my_node">
        <param name="rate" value="20" />
    </node>

    <!-- 设置重映射 -->
    <node pkg="my_pkg" exec="my_node" remapping话题名:=新话题名" />
</launch>
```

### Python 示例

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_py_pkg',
            executable='number_publisher',
            output='screen'
        ),
        Node(
            package='my_cpp_pkg',
            executable='number_counter',
            output='screen'
        ),
    ])
```

### 运行 launch 文件

```bash
# 方式 1：指定文件名
ros2 launch my_robot_bringup number_app.launch.xml

# 方式 2：如果有 default_launch_file
ros2 launch my_robot_bringup
```

---

## 8. 消息/服务/动作文件

### 自定义消息 (.msg)

```
my_package/
└── msg/
    └── Num.msg
```

```msg
# Num.msg
int64 num
string name
```

### 自定义服务 (.srv)

```
my_package/
└── srv/
    └── AddTwoInts.srv
```

```srv
# AddTwoInts.srv（--- 分隔请求和响应）
int64 a
int64 b
---
int64 sum
```

### 自定义动作 (.action)

```
my_package/
└── action/
    └── Fibonacci.action
```

```action
# Fibonacci.action（--- 分隔目标、结果、反馈）
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

### CMakeLists.txt 中启用接口生成

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
    "msg/Num.msg"
    "srv/AddTwoInts.srv"
    "action/Fibonacci.action"
)

ament_package()
```

---

## 9. TF2 坐标变换

TF2 用于管理机器人各部件之间的坐标变换关系。

### 坐标系树

```
map（地图坐标系）
└── odom（里程计坐标系）
    └── base_link（机器人本体坐标系）
        ├── laser（激光雷达坐标系）
        └── camera（摄像头坐标系）
```

### 广播坐标变换

```cpp
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/msg::transform_stamped.hpp>

// 创建广播器
tf2_ros::TransformBroadcaster broadcaster(node);

// 发布变换
geometry_msgs::msg::TransformStamped t;
t.header.stamp = node->now();
t.header.frame_id = "odom";
t.child_frame_id = "base_link";
t.transform.translation.x = 1.0;
t.transform.rotation.w = 1.0;
broadcaster.sendTransform(t);
```

---

## 10. 常用命令速查表

### 节点命令

```bash
ros2 node list                    # 列出所有节点
ros2 node info /节点名            # 查看节点详细信息（话题、服务、参数）
```

### 话题命令

```bash
ros2 topic list                   # 列出所有话题
ros2 topic echo /话题名           # 监听话题数据
ros2 topic info /话题名           # 查看话题信息（类型、发布者、订阅者）
ros2 topic hz /话题名             # 查看话题发布频率
ros2 topic bw /话题名             # 查看话题带宽
ros2 topic find 消息类型          # 查找使用指定消息类型的话题
```

### 服务命令

```bash
ros2 service list                 # 列出所有服务
ros2 service info /服务名         # 查看服务信息
ros2 service call /服务名 类型    # 调用服务
```

### 参数命令

```bash
ros2 param list                   # 列出所有参数
ros2 param get /节点名 参数名     # 获取参数值
ros2 param set /节点名 参数名 值  # 修改参数值
ros2 param dump /节点名           # 导出参数
```

### 运行命令

```bash
ros2 run 包名 可执行文件名        # 运行单个节点
ros2 launch 包名 launch文件名     # 运行 launch 文件
```

### 调试命令

```bash
ros2 doctor                       # 检查 ROS2 环境
ros2 doctor --report              # 详细环境报告
ros2 bag record -a                # 录制所有话题
ros2 bag play 某个bag文件          # 回放 bag 文件
```

---

## 11. CMakeLists.txt 关键配置

### C++ 包的 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

# 添加编译选项
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# 添加可执行文件
add_executable(number_publisher src/number_publisher.cpp)

# 链接依赖库
ament_target_dependencies(number_publisher rclcpp std_msgs)

# 安装
install(TARGETS number_publisher
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/)

ament_package()
```

---

## 12. 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `package 'xxx' not found` | 没有 source 环境 | `source install/setup.bash` |
| `file 'None' was not found` | launch 文件名错误或为空 | 检查文件名和内容 |
| `Unable to find package` | 包没有构建 | `colcon build --packages-select 包名` |
| 节点找不到话题 | 话题名不一致 | 检查发布者和订阅者的话题名 |
| N+1 查询问题 | 循环中查询 | 使用预加载或 JOIN |

---

## 13. ROS2 vs ROS1 对比

| 特性 | ROS1 | ROS2 |
|------|------|------|
| 通信 | TCP/UDP 直连 | DDS（数据分发服务） |
| 节点发现 | roscore | 自动发现（去中心化） |
| 安全 | 无 | DDS-Security、SROS2 |
| 实时性 | 不支持 | 支持实时调度 |
| 多机器人 | 复杂 | 命名空间天然支持 |
| 构建工具 | catkin | colcon |
| 客户端库 | roscpp/rospy | rclcpp/rclpy |

---

> [!tip] 学习建议
> 1. 先理解 **包名 vs 可执行文件名 vs 节点名** 的区别
> 2. 多用 `ros2 node list`、`ros2 topic list` 调试
> 3. launch 文件是组织多节点的关键，务必熟练
> 4. QoS 配置在实际项目中非常重要

---

**创建时间**：2026-07-08
**最后更新**：2026-07-08
**标签**：#ROS2 #机器人 #编程
