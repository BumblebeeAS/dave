cmake_minimum_required(VERSION 3.8)
project(bb_entrypoint)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch
  DESTINATION share/bb_entrypoint
)

ament_package()
