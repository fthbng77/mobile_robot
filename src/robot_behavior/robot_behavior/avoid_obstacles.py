#!/usr/bin/env python3
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class AvoidObstacles(Node):
    def __init__(self):
        super().__init__('avoid_obstacles')
        self.stop_distance = 0.45
        self.slow_distance = 0.80
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.last_mode = None

    @staticmethod
    def sector_min(msg: LaserScan, start_angle: float, end_angle: float):
        values = []
        for index, distance in enumerate(msg.ranges):
            angle = msg.angle_min + index * msg.angle_increment
            if start_angle <= angle <= end_angle:
                if math.isfinite(distance) and distance > 0.0:
                    values.append(distance)
        return min(values) if values else float('inf')

    def scan_callback(self, msg: LaserScan):
        # ROS LaserScan angles are measured counter-clockwise from the front.
        front = self.sector_min(msg, -0.52, 0.52)
        left = self.sector_min(msg, 0.52, 1.57)
        right = self.sector_min(msg, -1.57, -0.52)
        command = Twist()

        if front == float('inf'):
            # Do not drive blindly if the LiDAR has no usable front data.
            mode = 'safe_stop'
        elif front < self.stop_distance:
            command.angular.z = 0.8 if left >= right else -0.8
            mode = 'turn_left' if left >= right else 'turn_right'
        elif front < self.slow_distance:
            command.linear.x = 0.10
            command.angular.z = 0.3 if left >= right else -0.3
            mode = 'slow_and steer'
        else:
            command.linear.x = 0.25
            mode = 'forward'

        if mode != self.last_mode:
            self.get_logger().info(
                f'{mode}: front={front:.2f} m, left={left:.2f} m, right={right:.2f} m')
            self.last_mode = mode
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
