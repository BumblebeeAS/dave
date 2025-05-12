#!/bin/bash
#============================================================================
# Installation Script for ROS2 Humble and Gazebo Harmonic on Ubuntu 22.04
#============================================================================

# Check if the system is running Ubuntu 22.04
if [[ $(lsb_release -rs) != "22.04" ]]; then
	echo "ERROR: This script requires Ubuntu 22.04."
	echo "Current system: $(lsb_release -ds)"
	exit 1
fi

echo "Starting installation for Dave Sim..."

# Update package lists and upgrade installed packages
echo "Updating system packages..."
sudo apt -y update
sudo apt full-upgrade -y

# Install required dependencies and development tools
echo "Installing basic dependencies and development tools..."
sudo apt install -y build-essential cmake cppcheck curl git gnupg libeigen3-dev \
	libgles2-mesa-dev lsb-release pkg-config protobuf-compiler python3-dbg \
	python3-pip python3-venv qtbase5-dev ruby software-properties-common sudo wget

# Add Gazebo repository and key
echo "Adding Gazebo repository..."
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list >/dev/null
sudo apt -y update

# Install Gazebo Harmonic
echo "Installing Gazebo Harmonic..."
sudo apt install -y gz-harmonic
sudo apt install -y ros-humble-ros-gzharmonic

# Additional Gazebo repository setup (alternative method)
echo "Setting up additional Gazebo repositories..."
sudo apt install -y lsb-release
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt update -y

# Install Gazebo plugins and ROS2 controllers
echo "Installing Gazebo plugins and ROS2 controllers..."
sudo apt install -y libgz-plugin2-dev
sudo apt install -y ros-humble-ros2-control ros-humble-ros2-controllers

# Set environment variables for ROS2 and Gazebo
export DIST=humble
export GAZEBO=gz-harmonic

# Install ROS2 packages and tools
echo "Installing ROS2 packages and tools..."
sudo apt install -y ${GAZEBO} python3-rosdep python3-rosinstall-generator python3-vcstool \
	ros-${DIST}-effort-controllers ros-${DIST}-geographic-info ros-${DIST}-image-view \
	ros-${DIST}-joint-state-publisher ros-${DIST}-joy ros-${DIST}-joy-teleop \
	ros-${DIST}-key-teleop ros-${DIST}-moveit-planners \
	ros-${DIST}-moveit-simple-controller-manager ros-${DIST}-moveit-ros-visualization \
	ros-${DIST}-pcl-ros ros-${DIST}-robot-localization ros-${DIST}-robot-state-publisher \
	ros-${DIST}-ros-base ros-${DIST}-ros2-controllers ros-${DIST}-rqt \
	ros-${DIST}-rqt-common-plugins ros-${DIST}-rviz2 ros-${DIST}-teleop-tools \
	ros-${DIST}-teleop-twist-joy ros-${DIST}-teleop-twist-keyboard \
	ros-${DIST}-tf2-geometry-msgs ros-${DIST}-tf2-tools ros-${DIST}-urdfdom-py \
	ros-${DIST}-xacro

echo "Installation completed successfully!"
