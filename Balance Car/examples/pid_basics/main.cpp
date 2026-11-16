#include "pid_controller.hpp"

#include <iomanip>
#include <iostream>

int main() {
    // Simple first-order *teaching* plant: dy/dt = (u - y) / tau.
    // It is NOT a physically accurate balancing robot / inverted pendulum model.
    learning::PidConfig cfg;
    cfg.kp = 2.0;
    cfg.ki = 1.0;
    cfg.kd = 0.05;
    cfg.output_min = -3.0;
    cfg.output_max = 3.0;
    learning::PidController pid(cfg);

    constexpr double dt = 0.01;
    constexpr double tau = 0.35;
    constexpr double target = 1.0;
    double measured = 0.0;

    std::cout << "time_s,target,measurement,control\n";
    std::cout << std::fixed << std::setprecision(5);
    for (int i = 0; i < 500; ++i) {
        const double t = i * dt;
        const double control = pid.update(target, measured, dt);
        measured += dt * (control - measured) / tau;
        std::cout << t << ',' << target << ',' << measured << ',' << control << '\n';
    }
}
