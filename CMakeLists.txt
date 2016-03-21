cmake_minimum_required(VERSION 2.8.3)
project(ros_plate_detection_node)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(
  CATKIN_DEPENDS
    rospy
)

install(PROGRAMS
  ros/scripts/ros_plate_detection_node
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
