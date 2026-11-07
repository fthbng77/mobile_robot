#!/usr/bin/env python3
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class AvoidObstacles(Node):
    def __init__(self):
        super().__init__('avoid_obstacles')
        self.stop_distance = 0.60
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)

    def scan_callback(self, msg: LaserScan):
        valid = [r for r in msg.ranges if math.isfinite(r) and r > 0.0]
        nearest = min(valid) if valid else float('inf')
        command = Twist()
        if nearest < self.stop_distance:
            command.angular.z = 0.8
            self.get_logger().info(f'Obstacle detected at {nearest:.2f} m; turning')
        else:
            command.linear.x = 0.25
        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = AvoidObstacles()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
