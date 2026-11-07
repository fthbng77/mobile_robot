# Mobile Robot - ROS 2 and Gazebo

ROS 2 Lyrical and Gazebo Jetty mobile robot project. The robot is a custom
differential-drive vehicle designed to move through an obstacle world and
avoid obstacles using LiDAR data.

## Build

```bash
cd /path/to/mobile_robot
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## Run the simulation

```bash
source /opt/ros/lyrical/setup.bash
source install/setup.bash
ros2 launch robot_bringup bringup.launch.py
```

The single launch file starts Gazebo, spawns the robot, starts the
ROS-Gazebo bridges, starts the obstacle-avoidance node and opens RViz with
the saved configuration.

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

## ROS topics

| Topic | Message type | Direction | Purpose |
|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS to Gazebo | Drive command |
| `/odom` | `nav_msgs/msg/Odometry` | Gazebo to ROS | Wheel odometry |
| `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo to ROS | Transform data |
| `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo to ROS | LiDAR ranges |
| `/camera/image_raw` | `sensor_msgs/msg/Image` | Gazebo to ROS | Front camera image |
| `/camera/camera_info` | `sensor_msgs/msg/CameraInfo` | Gazebo to ROS | Camera calibration |

Check the active topics with:

```bash
ros2 topic list
ros2 topic echo /scan
ros2 topic echo /camera/image_raw
ros2 topic echo /odom
```

## Obstacle avoidance

`robot_behavior/avoid_obstacles.py` subscribes to `/scan` and publishes
`geometry_msgs/msg/Twist` messages on `/cmd_vel`.

- If the nearest valid LiDAR range is below `0.60 m`, the robot turns.
- Otherwise, the robot moves forward at `0.25 m/s`.

## ROS-Gazebo integration

`ros_gz_bridge` connects the ROS topics to Gazebo Transport topics. The
current bridges include `/cmd_vel`, `/odom`, `/tf`, `/clock`, `/scan`,
`/camera/image_raw` and `/camera/camera_info`.

## Packages

- `robot_description`: URDF/Xacro robot model.
- `robot_gazebo`: Gazebo world, simulation launch and ROS-Gazebo bridges.
- `robot_behavior`: sensor-based obstacle avoidance node.
- `robot_bringup`: combined launch entry point.

## Current status

- Custom URDF/Xacro robot: complete
- Differential-drive Gazebo plugin: complete
- ROS-Gazebo bridge: complete
- LiDAR and front camera: integrated
- LiDAR-based obstacle avoidance: integrated
- RViz auto-start and saved configuration: integrated
- IMU sensor: still to be added
- Contact sensor: optional for a two-person group
