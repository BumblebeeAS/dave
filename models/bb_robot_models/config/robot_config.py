from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    namespace = LaunchConfiguration("namespace").perform(context)

    # Define base topics for both source (Gazebo) and target (ROS2)
    gz_base = f"/model/{namespace}"
    ros_base = f"/{namespace}"

    # Helper function to create remapping pairs
    def create_remapping(gz_topic, ros_topic):
        return (f"{gz_base}{gz_topic}", f"{ros_base}{ros_topic}")

    # Create remapping rules for thrusters
    remappings = []
    for thruster in range(1, 7 + 1):
        ros_thruster = thruster - 1
        joint_base = f"/joint/thruster_{thruster}_joint"
        remappings.extend(
            [
                create_remapping(
                    f"{joint_base}/cmd_thrust", f"/sim/thruster/t{ros_thruster}/force"
                ),
                create_remapping(f"{joint_base}/ang_vel", f"{joint_base}/ang_vel"),
                create_remapping(
                    f"{joint_base}/enable_deadband", f"{joint_base}/enable_deadband"
                ),
            ]
        )

    # Add remappings for other topics
    additional_remappings = [
        create_remapping("/odometry", "/odometry"),
        create_remapping("/odometry_with_covariance", "/map_odom_ned"),
        create_remapping("/pose", "/pose"),
        create_remapping("/imu", "/imu"),
        # Commented out as in original file
        # create_remapping("/magnetometer", "/magnetometer"),
        # create_remapping("/camera/image", "/camera/image"),
        # create_remapping("/camera/camera_info", "/camera/camera_info"),
        # Unable to add sim dvl because of the special Dave Message type
    ]
    remappings.extend(additional_remappings)

    # Create topic arguments for the bridge
    thruster_joints = []
    for thruster in range(1, 7 + 1):
        thruster_joints.append(f"{gz_base}/joint/thruster_{thruster}_joint")

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
        f"{gz_base}/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry",
        f"{gz_base}/odometry_with_covariance@nav_msgs/msg/Odometry@gz.msgs.OdometryWithCovariance",
        f"{gz_base}/pose@geometry_msgs/msg/PoseArray@gz.msgs.Pose_V",
        f"{gz_base}/imu@sensor_msgs/msg/Imu@gz.msgs.IMU",
        f"/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        # f"{gz_base}/magnetometer@sensor_msgs/msg/MagneticField@gz.msgs.Magnetometer",
        # f"{gz_base}/camera/image@sensor_msgs/msg/Image@gz.msgs.Image",
        # f"{gz_base}/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
    ]

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=arguments,
        remappings=remappings,
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
