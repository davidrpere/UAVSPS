cmake_minimum_required(VERSION 2.8.3)
project(uavsps_guided)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS
        roscpp
        rospy
        std_msgs
        genmsg
        mavros
        sensor_msgs)

## Generate added messages and services
generate_messages(DEPENDENCIES std_msgs)

## Declare a catkin package
catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS})

## load in pkg-config support
find_package(PkgConfig)
## use pkg-config to get hints for 0mq locations
pkg_check_modules(PC_ZeroMQ QUIET zmq)

## use the hint from above to find where 'zmq.hpp' is located
find_path(ZeroMQ_INCLUDE_DIR
        NAMES zmq.hpp
        PATHS ${PC_ZeroMQ_INCLUDE_DIRS}
        )

## use the hint from about to find the location of libzmq
find_library(ZeroMQ_LIBRARY
        NAMES zmq
        PATHS ${PC_ZeroMQ_LIBRARY_DIRS}
        )

add_executable(uavsps_guided
        src/main.cpp
        src/client_waypoints_fotos.cpp
        src/client_waypoints_fotos.h
        src/publisher_gps_fotos.cpp
        src/publisher_gps_fotos.h)

target_link_libraries(uavsps_guided ${catkin_LIBRARIES})

## add the include directory to our compile directives
target_include_directories(uavsps_guided PUBLIC ${ZeroMQ_INCLUDE_DIR})
## at the 0mq library to our link directive
target_link_libraries(uavsps_guided PUBLIC ${ZeroMQ_LIBRARY})

add_dependencies(uavsps_guided uavsps_guided_generate_messages_cpp)

install(
        TARGETS uavsps_guided
        ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
        LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
        RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})


