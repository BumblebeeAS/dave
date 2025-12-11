import os
import tempfile

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def substitute_namespace_in_config(config_content, namespace):
    """
    Replace ${namespace} placeholder in YAML config content with actual namespace.

    Args:
        config_content: String content of the YAML file
        namespace: The namespace value to substitute

    Returns:
        String with substituted namespace
    """
    return config_content.replace("${namespace}", namespace)


def launch_setup(context, *args, **kwargs):
    """
    Launch setup function that reads YAML config and substitutes namespace.
    """
    namespace = LaunchConfiguration("namespace").perform(context)

    pkg_share = get_package_share_directory("bb_robot_models")
    config_file_path = os.path.join(
        pkg_share, "config", namespace, "ros_gz_bridge_config.yaml"
    )

    with open(config_file_path, "r") as f:
        config_content = f.read()

    config_content = substitute_namespace_in_config(config_content, namespace)

    config_data = yaml.safe_load(config_content)

    temp_config = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml")
    temp_config.write(config_content)
    temp_config.close()

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {
                "config_file": temp_config.name,
            }
        ],
        output="screen",
    )

    return [bridge]


def generate_launch_description():
    """
    Generate the launch description.
    """
    args = [
        DeclareLaunchArgument(
            "namespace",
            default_value="",
            description="Namespace",
        ),
    ]

    return LaunchDescription(args + [OpaqueFunction(function=launch_setup)])
