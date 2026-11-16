# 代码架构与数据流

本页基于这份代码实际实现，而不是通用的 PID / FreeRTOS 示意。

## 系统启动

1. `Core/Src/main.c`：`HAL_Init()`、系统时钟以及 `GPIO`、`ADC1`、`TIM1/2/3/4`、`USART1/3` 等外设初始化。
2. `main.c` 调用 `my_main()`。
3. `Core/CODE/car_main.cpp`：`initModules()` 初始化电机、编码器、MPU6050、LQR、超声波、遥控、OLED 等模块。
4. `car_app_scheduler.start()` 启动 TIM2 中断定时，设置前台循环要处理的任务标志。
5. `my_main()` 前台循环通过标志检查与 `HAL_Delay(1)` 处理显示、按键与状态刷新。

## 平衡闭环（真正的电机控制路径）

```text
MPU6050 PA12 数据就绪外部中断
  -> HAL_GPIO_EXTI_Callback()
  -> car::controller.handleImuInterrupt()
  -> 读取 TIM3/TIM4 编码器
  -> 软件 I2C 读取 MPU6050
  -> car::pitch_kalman.update() 估计俯仰角
  -> 倾角过大/传感器异常检查
  -> car::lqr.update() 计算左右 PWM
  -> car::motor.set() 通过 TIM1 和方向 GPIO 驱动左右电机
```

在 `car_config.hpp` 中设置了 `BALANCE_SAMPLE_PERIOD_S = 0.005f`（200 Hz 的设计参数）。**实际控制触发来自 MPU6050 外部中断，不能仅凭参数常数断言已经实测到稳定 200 Hz。**

## TIM2 调度器不等于 FreeRTOS

`Core/CODE/car_app_scheduler.cpp` 维护 5 ms 定时标志，前台循环消费标志。该调度器没有使用 `xTaskCreate()`、`vTaskStartScheduler()` 或 FreeRTOS 任务 API，因此本仓库目前不是 FreeRTOS 工程。

## LQR 与 PID 的区别

- `car_lqr_control.cpp`：基于位置、速度、俯仰角、角速度、偏航角、偏航角速度等状态及参考增益计算左右输出，是 **LQR 风格的多状态反馈控制**。
- `examples/pid_basics/`：电脑端**独立**的 PID 练习，实现误差的 P/I/D 控制和限幅，并未接入车端。
- 不能因为两者都属于反馈控制，就把 LQR 代码改名为 PID。

## 主要参数

`Core/CODE/car_config.hpp` 中包括车轮几何参数、LQR 增益、零位角、PWM 限幅、编码器及电机正负方向、遥控速度和超声波距离等。

## 尚未验证的内容

这次代码整理未运行 STM32 ARM 交叉编译，也未连接实际小车，**没有验证** OLED、超声波、遥控和低压保护在现场的表现。特别注意默认 `BALANCE_ENABLE_BATTERY_MONITOR = 0`、`BALANCE_ENABLE_BATTERY_PROTECTION = 0`。
