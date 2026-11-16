#pragma once

// Platform-independent PID learning example. NOT wired into the STM32 firmware.
namespace learning {
struct PidConfig {
    double kp = 1.0;
    double ki = 0.0;
    double kd = 0.0;
    double integral_min = -10.0;
    double integral_max = 10.0;
    double output_min = -10.0;
    double output_max = 10.0;
};

class PidController {
public:
    explicit PidController(PidConfig config) : config_(config) {}
    double update(double setpoint, double measurement, double dt_seconds);
    void reset();

private:
    PidConfig config_;
    double integral_ = 0.0;
    double last_measurement_ = 0.0;
    bool initialized_ = false;
};
}  // namespace learning
