# DAVE

See the original project at [http://dave-ros2.notion.site](http://dave-ros2.notion.site)

## Installation

### 1. Install DAVE Sim Interfaces

#### Ubuntu 22.04

See https://www.notion.so/nusbbas/Simulation-1673cacaefa180a5a61efbbbef7b6a23#1673cacaefa18009944ccfa6b8a8fffc

#### Ubuntu 24.04

Run `dave_sim_install.sh`. Then run `gz_packages_install.sh`.

### 2. Clone and Build AUV Description

Clone https://github.com/BumblebeeAS/auv4_description using under the `sim-test` branch:

```bash
git clone https://github.com/BumblebeeAS/auv4_description -b sim-test
```

## Quickstart

See [`examples/bb_entrypoint/README.md`](examples/bb_entrypoint/README.md)

## Issues

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

