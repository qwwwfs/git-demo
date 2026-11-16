import math
import unittest
from rdk_arm.core import MockDriver, ordered_target, forward_kinematics, JOINTS
from rdk_arm.can_driver import CANDriver


class CoreTests(unittest.TestCase):
    def test_order(self):
        self.assertEqual(ordered_target(["joint2", "joint1"], [0.2, 0.3], -1, 1), [0.3, 0.2])

    def test_rejection_preserves_target(self):
        d = MockDriver()
        d.command(JOINTS, [0.1, 0.2])
        for names, values in [(JOINTS, [math.nan, 0]), (JOINTS, [math.inf, 0]),
                              (JOINTS, [2, 0]), (["joint1", "joint1"], [0, 0]),
                              (JOINTS, [0])]:
            with self.assertRaises(ValueError):
                d.command(names, values)
            self.assertEqual(d.target, [0.1, 0.2])

    def test_rate_and_convergence(self):
        d = MockDriver(speed=0.5)
        d.command(JOINTS, [0.3, -0.2])
        previous = [0, 0]
        for _ in range(100):
            current = d.step(0.02)
            for a, b in zip(previous, current):
                self.assertLessEqual(abs(a-b), 0.010000001)
            previous = current
        self.assertEqual(current, [0.3, -0.2])

    def test_invalid_parameters(self):
        for kwargs in ({"speed": 0}, {"lower": 1}, {"upper": math.inf}):
            with self.assertRaises(ValueError):
                MockDriver(**kwargs)
        with self.assertRaises(ValueError):
            MockDriver().step(-1)

    def test_kinematics(self):
        x, y = forward_kinematics(0, 0)
        self.assertAlmostEqual(x, 0.27)
        self.assertAlmostEqual(y, 0)
        x, y = forward_kinematics(math.pi/2, 0)
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 0.27)

    def test_real_driver_unavailable(self):
        with self.assertRaises(NotImplementedError):
            CANDriver()
