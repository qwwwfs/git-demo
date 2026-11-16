# RDK 二自由度机械臂 · ROS2 控制原型

基于 Python 与 ROS2 的二自由度关节控制项目骨架，面向 RDK/Linux 平台后续部署。

**当前版本是新生成的模拟控制原型，不是已有实物项目源码或实机运行证明。**
真实 CAN 报文、电机驱动适配及 RDK 实机验证尚未完成；模拟位置不是编码器反馈。

## 已实现

- 两关节位置目标输入（单位 rad），关节名称 joint1 / joint2。
- 目标有效性检查、关节角度范围检查、模拟运动速度限制。
- ROS2 指令订阅与 JointState 状态发布。
- 模拟驱动、配置文件、启动文件及无 ROS 依赖的演示。
- 平面二连杆正运动学示例（仅适用于两转轴平行的平面机械臂）。

## 目录

```text
rdk_arm/core.py             目标校验、模拟驱动、正运动学
rdk_arm/arm_node.py         ROS2 控制节点
rdk_arm/can_driver.py       真实 CAN 适配接口（未实现）
rdk_arm/demo.py             纯 Python 演示
config/arm.yaml             示例参数
launch/arm.launch.py        ROS2 启动入口
tests/test_core.py         核心逻辑测试
docs/hardware.md           实机接入待办
```

## 不连接硬件快速运行

在本仓库根目录执行（Python 3）：

```bash
python3 -m rdk_arm.demo
python3 -m unittest discover -s tests -v
```

终端输出两个模拟关节的角度，以及假设连杆长度下的末端坐标。
该演示不打开 CAN、不发送电机报文。

## ROS2 模拟运行

前提：已经安装适合目标系统的 ROS2、colcon、rosdep；先 source 对应 ROS2 环境。
本包使用 ament_python。当前未在 ROS2 或 RDK 实机环境验证，不能保证全部发行版兼容。

将整个仓库放到工作空间 src/rdk_two_dof_arm 下，在工作空间根目录执行：

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select rdk_arm
source install/setup.bash
ros2 launch rdk_arm arm.launch.py
```

另开终端，source 相同环境后发送目标：

```bash
ros2 topic pub --once /arm/target sensor_msgs/msg/JointState "{name: ['joint1', 'joint2'], position: [0.3, -0.2]}"
ros2 topic echo /joint_states
```

两个名字必须各出现一次，position 与 name 一一对应；velocity 和 effort 输入被忽略。
目标消息只设置一次位置目标，模拟器按限速移动到目标并保持，不需要持续发送。
Ctrl+C 停止模拟节点。

## 数据流程

ROS2 /arm/target → 目标校验 → 模拟关节驱动 → /joint_states。
未来实机链路：RDK → CAN 适配硬件 → 电机驱动器 → 两个关节；
需先按驱动器文档实现 can_driver.py，并将真实反馈接入控制节点。

## 参数

修改 config/arm.yaml 后重新构建并启动。角度、速度及长度全部是示例值，
不代表实际机械臂规格。默认范围 [-1.57, 1.57] rad，速度 0.5 rad/s，频率 50 Hz。

## 验证范围

纯 Python 单元测试覆盖目标顺序、非法输入、限速收敛、正运动学和真实驱动拒绝启动。
ROS2 通信、RDK 部署、CAN 收发和真实电机控制均待验证。
项目由 AI 辅助生成，应结合本人硬件与调试记录继续完善。
