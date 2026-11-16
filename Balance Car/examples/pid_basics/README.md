# PID 基础实验：独立 C++ 示例

这个例子演示 PID 控制器的 **P（比例）/ I（积分）/ D（微分）** 计算、输出限幅和简单的积分抗饱和。使用的是一个**一阶教学被控对象**，方便测试，不是倒立摆模型，也没有连接 STM32、电机或 FreeRTOS。

## 运行

在仓库根目录（CMake + C++ 编译器）：

```bash
cmake -S examples/pid_basics -B build/pid-basics
cmake --build build/pid-basics
ctest --test-dir build/pid-basics --output-on-failure
```

运行演示并保存 CSV：

```bash
./build/pid-basics/pid_step_demo > pid_step.csv
```

（Windows 上的可执行文件通常带 `.exe`，命令或路径可能需要调整。）

CSV 四列分别为 `time_s,target,measurement,control`，可以用 Excel 或 Python/Matplotlib 画出控制响应曲线。

## 算法原理

- 误差：`error = setpoint - measurement`
- 比例项：`Kp * error`
- 积分项：`Ki * integral(error, dt)`
- 微分项：`-Kd * d(measurement)/dt`（对测量值求导，避免目标阶跃时微分冲击）
- 把最终输出限制在安全范围；演示中使用简化的积分抗饱和逻辑。

**实物平衡车需要不同的建模、采样周期、环路设计和参数调试。不能直接把本示例参数烧到电机控制器上。**

## 实验数据与画图

`results/pid_step.csv` 是**电脑端教学模型**在本次整理时真实运行程序生成的输出，不是实际平衡车的传感器数据。

安装 Matplotlib 后，可运行 `python examples/pid_basics/plot_pid.py` 生成响应曲线；该图片仅用于展示 PID 算法实验。

GitHub Actions 的 `pid-unit-tests.yml` 仅自动检查这个电脑端 PID 示例，**不会验证 STM32 原固件或实体小车**。
