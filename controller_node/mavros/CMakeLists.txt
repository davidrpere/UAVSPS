cmake_minimum_required(VERSION 3.10)
project(mavros)

set(CMAKE_CXX_STANDARD 11)

include_directories(ros/kinetic/include)

FIND_PACKAGE( Boost 1.66 COMPONENTS program_options REQUIRED )
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} )

add_executable(mavros to_rpi_guided/src/main.cpp)

TARGET_LINK_LIBRARIES( mavros LINK_PUBLIC ${Boost_LIBRARIES} )
