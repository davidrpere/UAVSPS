# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pi/catkin_ws/src

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pi/catkin_ws/build

# Include any dependencies generated for this target.
include ex1/CMakeFiles/takeoff_n_land.dir/depend.make

# Include the progress variables for this target.
include ex1/CMakeFiles/takeoff_n_land.dir/progress.make

# Include the compile flags for this target's objects.
include ex1/CMakeFiles/takeoff_n_land.dir/flags.make

ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o: ex1/CMakeFiles/takeoff_n_land.dir/flags.make
ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o: /home/pi/catkin_ws/src/ex1/takeoff_n_land.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/pi/catkin_ws/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o"
	cd /home/pi/catkin_ws/build/ex1 && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o -c /home/pi/catkin_ws/src/ex1/takeoff_n_land.cpp

ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.i"
	cd /home/pi/catkin_ws/build/ex1 && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/pi/catkin_ws/src/ex1/takeoff_n_land.cpp > CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.i

ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.s"
	cd /home/pi/catkin_ws/build/ex1 && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/pi/catkin_ws/src/ex1/takeoff_n_land.cpp -o CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.s

ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.requires:

.PHONY : ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.requires

ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.provides: ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.requires
	$(MAKE) -f ex1/CMakeFiles/takeoff_n_land.dir/build.make ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.provides.build
.PHONY : ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.provides

ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.provides.build: ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o


# Object files for target takeoff_n_land
takeoff_n_land_OBJECTS = \
"CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o"

# External object files for target takeoff_n_land
takeoff_n_land_EXTERNAL_OBJECTS =

/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: ex1/CMakeFiles/takeoff_n_land.dir/build.make
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libmavros.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libGeographic.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libclass_loader.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/libPocoFoundation.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libdl.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libroslib.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/librospack.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libpython2.7.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_program_options.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libtinyxml.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libtf2_ros.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libactionlib.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libmessage_filters.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libroscpp.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_signals.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_filesystem.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/librosconsole.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/librosconsole_log4cxx.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/librosconsole_backend_interface.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/liblog4cxx.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_regex.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libxmlrpcpp.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libtf2.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libmavconn.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libeigen_conversions.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/liborocos-kdl.so.1.3.0
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libroscpp_serialization.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/librostime.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /opt/ros/kinetic/lib/libcpp_common.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_system.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_thread.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_chrono.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_date_time.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libboost_atomic.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libpthread.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: /usr/lib/arm-linux-gnueabihf/libconsole_bridge.so
/home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land: ex1/CMakeFiles/takeoff_n_land.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/pi/catkin_ws/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable /home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land"
	cd /home/pi/catkin_ws/build/ex1 && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/takeoff_n_land.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
ex1/CMakeFiles/takeoff_n_land.dir/build: /home/pi/catkin_ws/devel/lib/ex1/takeoff_n_land

.PHONY : ex1/CMakeFiles/takeoff_n_land.dir/build

ex1/CMakeFiles/takeoff_n_land.dir/requires: ex1/CMakeFiles/takeoff_n_land.dir/takeoff_n_land.cpp.o.requires

.PHONY : ex1/CMakeFiles/takeoff_n_land.dir/requires

ex1/CMakeFiles/takeoff_n_land.dir/clean:
	cd /home/pi/catkin_ws/build/ex1 && $(CMAKE_COMMAND) -P CMakeFiles/takeoff_n_land.dir/cmake_clean.cmake
.PHONY : ex1/CMakeFiles/takeoff_n_land.dir/clean

ex1/CMakeFiles/takeoff_n_land.dir/depend:
	cd /home/pi/catkin_ws/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pi/catkin_ws/src /home/pi/catkin_ws/src/ex1 /home/pi/catkin_ws/build /home/pi/catkin_ws/build/ex1 /home/pi/catkin_ws/build/ex1/CMakeFiles/takeoff_n_land.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : ex1/CMakeFiles/takeoff_n_land.dir/depend

