cmake_minimum_required(VERSION 3.8)
project(bb_robot_models)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)

install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_environment_hooks(
  "${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  bb_robot_models/flu_to_ned_odom_repub.py
  bb_robot_models/auv4/auv4_thrust_repub.py
  bb_robot_models/auv4/grabber_action_server.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
