# Mobile Robot - ROS 2 and Gazebo

ROS 2 Lyrical and Gazebo Jetty mobile robot project.

## Build

```bash
source /opt/ros/lyrical/setup.bash
cd mobile_robot
colcon build --symlink-install
source install/setup.bash
```

## Run the simulation

```bash
source /opt/ros/lyrical/setup.bash
source install/setup.bash
ros2 launch robot_bringup bringup.launch.py
```

## Send a movement command

```bash
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist \\
  "{linear: {x: 0.3}, angular: {z: 0.0}}"
```

Stop the robot with:

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \\
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

## Packages

- `robot_description`: URDF/Xacro robot model.
- `robot_gazebo`: Gazebo world, simulation launch and ROS-Gazebo bridges.
- `robot_behavior`: sensor-based obstacle avoidance node.
- `robot_bringup`: combined launch entry point.

The LiDAR, camera, IMU, contact sensor and RViz integration are planned next.
