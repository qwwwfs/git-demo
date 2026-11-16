#include "pid_controller.hpp"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace learning {
namespace {
double clamp(double value, double low, double high) {
    return std::max(low, std::min(value, high));
}
}  // namespace

double PidController::update(double setpoint, double measurement, double dt_seconds) {
    // This demonstration runs on a PC; errors can be reported with exceptions.
    // MCU firmware would need a suitable error-handling strategy instead.
    if (!std::isfinite(setpoint) || !std::isfinite(measurement) ||
        !std::isfinite(dt_seconds) || dt_seconds <= 0.0) {
        throw std::invalid_argument("finite inputs and positive dt_seconds required");
    }
    if (config_.integral_min > config_.integral_max ||
        config_.output_min > config_.output_max) {
        throw std::invalid_argument("invalid PID saturation limits");
    }

    const double error = setpoint - measurement;
    const double derivative = initialized_ ?
        -(measurement - last_measurement_) / dt_seconds : 0.0;
    const double trial_integral = clamp(integral_ + error * dt_seconds,
                                        config_.integral_min, config_.integral_max);
    const double unconstrained = config_.kp * error +
                                 config_.ki * trial_integral +
                                 config_.kd * derivative;

    // Freeze integrator when its error would push an already saturated output further.
    const bool pushing_high = unconstrained > config_.output_max && error > 0.0;
    const bool pushing_low = unconstrained < config_.output_min && error < 0.0;
    if (!pushing_high && !pushing_low) {
        integral_ = trial_integral;
    }

    last_measurement_ = measurement;
    initialized_ = true;
    const double output = config_.kp * error + config_.ki * integral_ +
                          config_.kd * derivative;
    return clamp(output, config_.output_min, config_.output_max);
}

void PidController::reset() {
    integral_ = 0.0;
    last_measurement_ = 0.0;
    initialized_ = false;
}
}  // namespace learning
