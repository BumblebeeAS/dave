# DAVE

See the original project at [http://dave-ros2.notion.site](http://dave-ros2.notion.site)

## Installation

### Ubuntu 22.04

Follow the instructions at [software-auv-4](https://github.com/BumblebeeAS/software-auv-4/tree/robosub-25).

### Ubuntu 24.04

Run `dave_sim_install.sh`. Then run `gz_packages_install.sh`.

## Core Components

### 1. Entry Point (`bb_entrypoint`)
- **Main Launch File**: `bb_robot.launch.py` - Primary entry point for launching the simulation
- Coordinates the startup of Gazebo simulation and robot models
- Configurable parameters for world selection, robot positioning, and simulation settings

### 2. Robot Models (`bb_robot_models`)
- **Main Launch File**: `upload_robot.launch.py` - Handles robot model instantiation in Gazebo and launches the ROS-Gazebo bridge and republishers
- **Bridge Configuration**: `robot_config.py` - Configures ROS-Gazebo message bridge for communication between ROS2 and Gazebo. Bridges thruster topics, TFs, and more.
- **Data Republishers**:
  - `bb_odom_republisher.py` - Converts odometry from FLU to NED
  - `bb_thrust_republisher.py` - Maps thruster commands sent to thruster topic via allocator to Gazebo force input topics
- **Transform Publishers**: Static transforms for world ↔ world_ned and base_link ↔ base_link_ned
- **Image Processing**: Republishes camera feeds with compression

## Issues

### Poor RTF in simulation

If you are on a system with both an integrated GPU and a discrete GPU, offloading rendering of the simulation to the discrete GPU can help greatly. Launch the main simulation launch file prepended with `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia`:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ros2 launch bb_entrypoint bb_robot.launch.py x:=-3.0 y:=-0.6 z:=-1.35 yaw:=1.57 namespace:=auv4 world_name:=robosub_2025_pool paused:=false
```

### WSLg

When running Gazebo on WSL, some graphics are not well supported.

Quicklinks:
- https://devblogs.microsoft.com/commandline/d3d12-gpu-video-acceleration-in-the-windows-subsystem-for-linux-now-available/
- https://github.com/microsoft/WSL/issues/11838
- https://askubuntu.com/questions/1514352/ubuntu-24-04-with-nvidia-driver-libegl-warning-egl-failed-to-create-dri2-scre

A fix would be to update the `apt` repository to use the latest `mesa` drivers. But do note that these versions may not be stable:

```bash
sudo add-apt-repository ppa:oibaf/graphics-drivers -y

sudo apt update
sudo apt install -y \
  mesa-utils \
  vainfo \
  mesa-va-drivers
```

If `ppa:oibaf/graphics-drivers` is not stable / does not work, try `ppa:kisak/kisak-mesa`.

A few other configs can be set as well (not tested):

```
MESA_D3D12_DEFAULT_ADAPTER_NAME: NVIDIA
XDG_RUNTIME_DIR: /mnt/wslg/runtime-dir
LD_LIBRARY_PATH: /usr/lib/wsl/lib
LIBVA_DRIVER_NAME: d3d12
# The env var DISPLAY in WSL Docker Desktop is wrong.
DISPLAY: :0
---
- /usr/lib/wsl:/usr/lib/wsl
- /mnt/wslg:/mnt/wslg
- /mnt/wslg/.X11-unix:/tmp/.X11-unix
---
privileged: true
group_add:
      - video
```
