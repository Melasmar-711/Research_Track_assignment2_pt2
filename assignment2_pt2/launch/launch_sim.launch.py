from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    robot_desc = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('robot_urdf'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    minimal_publisher_node = Node(
        package='assignment2_pt2',
        executable='move_robot',
        name='control_speed',
        output='screen',

    )

    return LaunchDescription([
        robot_desc,
        minimal_publisher_node,
    ])

