"""Pure Python simulation; all angles in radians."""
import math

JOINTS = ("joint1", "joint2")


def ordered_target(names, positions, lower, upper):
    if len(names) != 2 or len(positions) != 2 or set(names) != set(JOINTS):
        raise ValueError("Provide joint1 and joint2 exactly once with two positions")
    values = dict(zip(names, positions))
    result = [float(values[name]) for name in JOINTS]
    if any(not math.isfinite(q) or q < lower or q > upper for q in result):
        raise ValueError("Target must be finite and inside joint limits")
    return result


class MockDriver:
    """Rate-limited kinematic simulation, NOT a physical motor model."""
    def __init__(self, lower=-1.57, upper=1.57, speed=0.5):
        if not all(math.isfinite(v) for v in (lower, upper, speed)):
            raise ValueError("Parameters must be finite")
        if not lower <= 0 <= upper or lower >= upper or speed <= 0:
            raise ValueError("Limits must include zero; speed must be positive")
        self.lower, self.upper, self.speed = lower, upper, speed
        self.position = [0.0, 0.0]
        self.target = [0.0, 0.0]

    def command(self, names, positions):
        self.target = ordered_target(names, positions, self.lower, self.upper)

    def step(self, dt):
        if not math.isfinite(dt) or dt <= 0:
            raise ValueError("dt must be finite and positive")
        delta = self.speed * dt
        self.position = [q + max(-delta, min(delta, t-q))
                         for q, t in zip(self.position, self.target)]
        return list(self.position)


def forward_kinematics(q1, q2, l1=0.15, l2=0.12):
    """Planar 2R model, sample lengths in metres, q2 relative to link1."""
    if not all(math.isfinite(v) for v in (q1, q2, l1, l2)) or min(l1, l2) <= 0:
        raise ValueError("Finite angles and positive lengths required")
    return (l1*math.cos(q1)+l2*math.cos(q1+q2),
            l1*math.sin(q1)+l2*math.sin(q1+q2))
