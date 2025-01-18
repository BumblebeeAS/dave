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
