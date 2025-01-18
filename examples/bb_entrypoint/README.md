```bash
ros2 launch bb_entrypoint bb_robot.launch.py z:=-5 namespace:=auv4 world_name:=dave_ocean_waves paused:=false
```

See available topics with:

```bash
ros2 topic list
```

```bash
gz topic -l
```

# Test Controls

```bash
ros2 run control moveFrontTest
```
