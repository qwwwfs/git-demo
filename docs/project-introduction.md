# 项目介绍与黑客松材料（根据实际完成情况修改）

## 目前这份 GitHub 代码可以支撑的介绍

**项目名称：基于 STM32 的两轮自平衡小车控制与调试**

- **项目内容：** 参与制作与调试两轮自平衡小车，学习基于 STM32 的姿态检测、编码器反馈和电机控制，整理并分析相应的 C/C++ 固件工程。
- **实现功能：** 通过 MPU6050 获取姿态数据，结合姿态估计与反馈控制调节左右轮电机，完成实体小车基本自主平衡（实体成果由项目实践者提供，建议附视频）。
- **技术栈（这份固件）：** STM32F103、C/C++、STM32 HAL、MPU6050、Kalman 滤波、LQR、PWM、电机编码器。
- **补充学习：** 基于标准 C++ 实现独立 PID 算法小实验，进行基础单元测试；不等于已在小车上部署 PID。

> 这段可以用于 GitHub 项目介绍，但需要根据个人真实参与程度（独立制作 / 团队制作 / 学习和改进开源工程）修改。

## 如果申请表仍写“FreeRTOS + PID”

当前上传的源码**不足以支持**这个技术描述。建议二选一：

- 把简历对应项目改为“基于 STM32 的两轮自平衡小车”，使用上面经过代码核实的技术栈。
- 或者另行上传你**真正使用过**的 FreeRTOS + PID 版本，附实际调试记录，再保留原简历写法。

## GitHub 仓库简介（About）

`STM32F103 two-wheel self-balancing robot: IMU, Kalman filter, LQR, motor PWM, encoder feedback; plus an independent PID learning demo.`

## 建议添加的展示素材

- `images/robot.jpg`：实体平衡车照片
- `images/balance-demo.gif`：实测平衡短动图（或外部真实视频链接）
- `images/debug.jpg`：OLED、串口、示波器等调试界面
- `images/wiring.jpg`：真实接线和模块特写

请仅放自己拥有使用权的照片、视频、代码，且不要发布个人身份信息、Wi-Fi 密码、密钥或其他敏感信息。
