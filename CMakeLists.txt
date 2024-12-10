cmake_minimum_required(VERSION 3.5)
project(camera_pkg)

# Vind de nodige ROS2-pakketten
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

# Installeer de Python-package
ament_python_install_package(${PROJECT_NAME})

# Installeer Python-scripts
install(PROGRAMS
  camera_pkg/camera_node.py
  DESTINATION lib/${PROJECT_NAME}
)


# Installeer de launch-bestanden
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/launch
)

# Installeer de package.xml
install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
