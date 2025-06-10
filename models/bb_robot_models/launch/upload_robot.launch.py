import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    LogInfo,
    RegisterEventHandler,
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    gui = LaunchConfiguration("gui")
    use_sim_time = LaunchConfiguration("use_sim_time")
    namespace = LaunchConfiguration("namespace")
    x = LaunchConfiguration("x")
    y = LaunchConfiguration("y")
    z = LaunchConfiguration("z")
    roll = LaunchConfiguration("roll")
    pitch = LaunchConfiguration("pitch")
    yaw = LaunchConfiguration("yaw")
    vehicle = LaunchConfiguration("vehicle")

    args = [
        DeclareLaunchArgument(
            "gui",
            default_value="true",
            description="Flag to indicate whether to use simulation",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            description="Flag to indicate whether to use sim time",
        ),
        DeclareLaunchArgument(
            "namespace",
            default_value="auv4",
            description="Namespace",
        ),
        DeclareLaunchArgument(
            "x",
            default_value="0",
            description="Initial x position",
        ),
        DeclareLaunchArgument(
            "y",
            default_value="0",
            description="Initial y position",
        ),
        DeclareLaunchArgument(
            "z",
            default_value="0.0",
            description="Initial z position",
        ),
        DeclareLaunchArgument(
            "roll",
            default_value="0.0",
            description="Initial roll",
        ),
        DeclareLaunchArgument(
            "pitch",
            default_value="0.0",
            description="Initial pitch",
        ),
        DeclareLaunchArgument(
            "yaw",
            default_value="0.0",
            description="Initial yaw",
        ),
        DeclareLaunchArgument(
            "vehicle",
            default_value="auv4",
            description="Vehicle name",
        ),
    ]

    description_file = PathJoinSubstitution(
        [
            FindPackageShare("auv4_description"),
            "urdf",
            "auv4.gazebo.urdf",
        ]
    )

    gz_spawner = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            namespace,
            "-file",
            description_file,
            "-x",
            x,
            "-y",
            y,
            "-z",
            z,
            "-R",
            roll,
            "-P",
            pitch,
            "-Y",
            yaw,
        ],
        output="both",
        condition=IfCondition(gui),
        parameters=[{"use_sim_time": use_sim_time}],
    )

    nodes = [
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="world2world_ned",
            arguments=[
                "0",
                "0",
                "0",
                "0",
                "0",
                "3.141592653589793",
                "world",
                "world_ned",
            ],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="base_link2base_link_ned",
            arguments=[
                "0",
                "0",
                "0",
                "0",
                "0",
                "3.141592653589793",
                [vehicle, "/base_link"],
                [vehicle, "/base_link_ned"],
            ],
        ),
        Node(
            package="bb_robot_models",
            executable="bb_thrust_republisher.py",
            name="bb_thrust_republisher",
            namespace=namespace,
            output="screen",
        ),
        Node(
            package="bb_robot_models",
            executable="bb_odom_republisher.py",
            name="bb_odom_republisher",
            namespace=namespace,
            output="screen",
        ),
        Node(
            package="image_transport",
            executable="republish",
            name="image_republisher_front_cam",
            arguments=["raw", "compressed"],
            output="screen",
            remappings=[
                ("in", "/auv4/front_cam/color/image"),
                ("out/compressed", "/auv4/front_cam/color/image/compressed"),
            ],
        ),
        Node(
            package="image_transport",
            executable="republish",
            name="image_republisher_bot_cam",
            arguments=["raw", "compressed"],
            output="screen",
            remappings=[
                ("in", "/auv4/bot_cam/color/image"),
                ("out/compressed", "/auv4/bot_cam/color/image/compressed"),
            ],
        ),
        gz_spawner,
    ]

    robot_config = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                PathJoinSubstitution(
                    [
                        FindPackageShare("bb_robot_models"),
                        "config",
                        "robot_config.py",
                    ]
                )
            ]
        ),
        launch_arguments={
            "namespace": namespace,
        }.items(),
    )

    robot_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("auv4_description"),
                "launch",
                "tf.launch.py",
            )
        )
    )

    include = [robot_config, robot_description_launch]

    event_handlers = [
        RegisterEventHandler(
            OnProcessExit(
                target_action=gz_spawner, on_exit=LogInfo(msg="Robot Model Uploaded")
            )
        )
    ]

    return LaunchDescription(args + event_handlers + include + nodes)
