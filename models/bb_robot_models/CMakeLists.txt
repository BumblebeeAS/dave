cmake_minimum_required(VERSION 3.8)
project(bb_robot_models)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)

install(
  DIRECTORY launch config
  DESTINATION share/bb_robot_models
)

ament_environment_hooks(
  "${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  republishers/bb_odom_republisher.py
  republishers/bb_thrust_republisher.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
