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
            default_value="asv5",
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
    ]

    description_file = PathJoinSubstitution(
        [
            FindPackageShare("asv5_description"),
            "models",
            "model.sdf",  # TO CHANGE ONCE REFACTORED
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
            name="world2map",
            arguments=[
                "0",
                "0",
                "0",
                "0",
                "0",
                "0",
                "world",
                "map",
            ],
        ),
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
            name="map2map_ned",
            arguments=[
                "0",
                "0",
                "0",
                "0",
                "0",
                "3.141592653589793",
                "map",
                "map_ned",
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
                [namespace, "/base_link"],
                [namespace, "/base_link_ned"],
            ],
        ),
        # Node(
        #     package="bb_robot_models",
        #     executable="auv4_thrust_repub.py",
        #     name="auv4_thrust_repub",
        #     namespace=namespace,
        #     output="screen",
        # ),
        Node(
            package="bb_robot_models",
            executable="flu_to_ned_odom_repub.py",
            name="asv5_flu_to_ned_odom_repub",
            namespace=namespace,
            output="screen",
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
                        namespace,
                        "robot_config.py",
                    ]
                )
            ]
        ),
        launch_arguments={
            "namespace": namespace,
        }.items(),
    )

    include = [robot_config]

    event_handlers = [
        RegisterEventHandler(
            OnProcessExit(
                target_action=gz_spawner, on_exit=LogInfo(msg="Robot Model Uploaded")
            )
        )
    ]

    return LaunchDescription(args + event_handlers + include + nodes)
