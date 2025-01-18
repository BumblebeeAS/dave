from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    namespace = LaunchConfiguration("namespace").perform(context)

    thruster_joints = []
    for thruster in range(1, 7 + 1):
        thruster_joints.append(f"/model/{namespace}/joint/thruster_{thruster}_joint")

    thruster_cmd_thrust_args = [
        f"{joint}/cmd_thrust@std_msgs/msg/Float64@gz.msgs.Double"
        for joint in thruster_joints
    ]
    thruster_ang_vel_args = [
        f"{joint}/ang_vel@std_msgs/msg/Float64@gz.msgs.Double"
        for joint in thruster_joints
    ]
    thruster_enable_deadband_args = [
        f"{joint}/enable_deadband@std_msgs/msg/Bool@gz.msgs.Boolean"
        for joint in thruster_joints
    ]
    thruster_args = (
        thruster_cmd_thrust_args + thruster_ang_vel_args + thruster_enable_deadband_args
    )

    arguments = thruster_args + [
        # f"/model/{namespace}/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry",
        # f"/model/{namespace}/odometry_with_covariance@nav_msgs/msg/Odometry@gz.msgs.OdometryWithCovariance",
        # f"/model/{namespace}/pose@geometry_msgs/msg/PoseArray@gz.msgs.Pose_V",
        f"/model/{namespace}/imu@sensor_msgs/msg/Imu@gz.msgs.IMU",
        # f"/model/{namespace}/magnetometer@sensor_msgs/msg/MagneticField@gz.msgs.Magnetometer",
        # f"/model/{namespace}/camera/image@sensor_msgs/msg/Image@gz.msgs.Image",
        # f"/model/{namespace}/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
    ]

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=arguments,
        output="screen",
    )

    return [bridge]


def generate_launch_description():
    args = [
        DeclareLaunchArgument(
            "namespace",
            default_value="",
            description="Namespace",
        ),
    ]

    return LaunchDescription(args + [OpaqueFunction(function=launch_setup)])
