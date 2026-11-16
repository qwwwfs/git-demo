import math
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from .core import JOINTS, MockDriver


class ArmNode(Node):
    def __init__(self):
        super().__init__("arm_controller")
        defaults = {"lower": -1.57, "upper": 1.57, "speed": 0.5, "rate": 50.0}
        for key, value in defaults.items():
            self.declare_parameter(key, value)
        params = {key: float(self.get_parameter(key).value) for key in defaults}
        rate = params.pop("rate")
        if not math.isfinite(rate) or not 1 <= rate <= 1000:
            raise ValueError("rate must be between 1 and 1000 Hz")
        self.driver = MockDriver(**params)
        self.pub = self.create_publisher(JointState, "/joint_states", 10)
        self.sub = self.create_subscription(JointState, "/arm/target", self.command, 10)
        self.last_tick = time.monotonic()
        self.timer = self.create_timer(1.0/rate, self.tick)
        self.get_logger().info("SIMULATION ONLY: no CAN hardware connected")

    def command(self, msg):
        try:
            self.driver.command(msg.name, msg.position)
        except (ValueError, TypeError) as exc:
            self.get_logger().warning(f"Rejected target: {exc}")

    def tick(self):
        now = time.monotonic()
        # Cap integration after process stalls to avoid a large simulated jump.
        dt = min(now - self.last_tick, 0.1)
        self.last_tick = now
        if dt <= 0:
            return
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(JOINTS)
        msg.position = self.driver.step(dt)
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = ArmNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
