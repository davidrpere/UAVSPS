# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

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
CMAKE_COMMAND = "/Users/drodriguez/Library/Application Support/JetBrains/Toolbox/apps/CLion/ch-0/181.4203.549/CLion.app/Contents/bin/cmake/bin/cmake"

# The command to remove a file.
RM = "/Users/drodriguez/Library/Application Support/JetBrains/Toolbox/apps/CLion/ch-0/181.4203.549/CLion.app/Contents/bin/cmake/bin/cmake" -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/drodriguez/PycharmProjects/UAVSPS/controller_node

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/controller_node.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/controller_node.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/controller_node.dir/flags.make

CMakeFiles/controller_node.dir/main.cpp.o: CMakeFiles/controller_node.dir/flags.make
CMakeFiles/controller_node.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/controller_node.dir/main.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/controller_node.dir/main.cpp.o -c /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/main.cpp

CMakeFiles/controller_node.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/controller_node.dir/main.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/main.cpp > CMakeFiles/controller_node.dir/main.cpp.i

CMakeFiles/controller_node.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/controller_node.dir/main.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/main.cpp -o CMakeFiles/controller_node.dir/main.cpp.s

CMakeFiles/controller_node.dir/main.cpp.o.requires:

.PHONY : CMakeFiles/controller_node.dir/main.cpp.o.requires

CMakeFiles/controller_node.dir/main.cpp.o.provides: CMakeFiles/controller_node.dir/main.cpp.o.requires
	$(MAKE) -f CMakeFiles/controller_node.dir/build.make CMakeFiles/controller_node.dir/main.cpp.o.provides.build
.PHONY : CMakeFiles/controller_node.dir/main.cpp.o.provides

CMakeFiles/controller_node.dir/main.cpp.o.provides.build: CMakeFiles/controller_node.dir/main.cpp.o


# Object files for target controller_node
controller_node_OBJECTS = \
"CMakeFiles/controller_node.dir/main.cpp.o"

# External object files for target controller_node
controller_node_EXTERNAL_OBJECTS =

controller_node: CMakeFiles/controller_node.dir/main.cpp.o
controller_node: CMakeFiles/controller_node.dir/build.make
controller_node: CMakeFiles/controller_node.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable controller_node"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/controller_node.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/controller_node.dir/build: controller_node

.PHONY : CMakeFiles/controller_node.dir/build

CMakeFiles/controller_node.dir/requires: CMakeFiles/controller_node.dir/main.cpp.o.requires

.PHONY : CMakeFiles/controller_node.dir/requires

CMakeFiles/controller_node.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/controller_node.dir/cmake_clean.cmake
.PHONY : CMakeFiles/controller_node.dir/clean

CMakeFiles/controller_node.dir/depend:
	cd /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/drodriguez/PycharmProjects/UAVSPS/controller_node /Users/drodriguez/PycharmProjects/UAVSPS/controller_node /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug /Users/drodriguez/PycharmProjects/UAVSPS/controller_node/cmake-build-debug/CMakeFiles/controller_node.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/controller_node.dir/depend

