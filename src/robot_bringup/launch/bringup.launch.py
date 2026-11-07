from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('robot_description'), 'launch', 'description.launch.py'])
        )
    )
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('robot_gazebo'), 'launch', 'simulation.launch.py'])
        )
    )
    behavior = Node(
        package='robot_behavior',
        executable='avoid_obstacles',
        output='screen',
    )
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([
            FindPackageShare('robot_bringup'), 'rviz', 'mobile_robot.rviz'
        ])],
        output='screen',
    )
    return LaunchDescription([description, simulation, behavior, rviz])
