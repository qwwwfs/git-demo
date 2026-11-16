#include "pid_controller.hpp"

#include <cassert>
#include <cmath>
#include <stdexcept>

int main() {
    using learning::PidConfig;
    using learning::PidController;
    PidConfig cfg;
    cfg.kp = 2.0;
    cfg.ki = 0.0;
    cfg.kd = 0.0;
    cfg.output_min = -3.0;
    cfg.output_max = 3.0;
    PidController pid(cfg);

    // Correct sign and output saturation.
    assert(std::abs(pid.update(1.0, 0.0, 0.01) - 2.0) < 1e-10);
    assert(std::abs(pid.update(2.0, 0.0, 0.01) - 3.0) < 1e-10);
    assert(std::abs(pid.update(-2.0, 0.0, 0.01) + 3.0) < 1e-10);

    // A setpoint step does not trigger derivative kick (derivative on measurement).
    cfg.kp = 0.0;
    cfg.kd = 1.0;
    pid = PidController(cfg);
    assert(std::abs(pid.update(0.0, 0.0, 0.01)) < 1e-10);
    assert(std::abs(pid.update(10.0, 0.0, 0.01)) < 1e-10);
    assert(std::abs(pid.update(10.0, 1.0, 0.01) + 3.0) < 1e-10);
    pid.reset();
    assert(std::abs(pid.update(0.0, 0.0, 0.01)) < 1e-10);

    bool rejected = false;
    try { pid.update(0.0, 0.0, 0.0); }
    catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected);

    // PI controller converges on a first-order test plant.
    cfg.kp = 2.0;
    cfg.ki = 1.0;
    cfg.kd = 0.05;
    pid = PidController(cfg);
    double y = 0.0;
    for (int i = 0; i < 1000; ++i) {
        const double u = pid.update(1.0, y, 0.01);
        y += 0.01 * (u - y) / 0.35;
    }
    assert(std::abs(y - 1.0) < 0.05);
}
