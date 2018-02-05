#Este es el fichero CMakeLists.txt, en él se especifican las opciones de compilación del proyecto
#Aquí, definimos el nombre del proyecto, la versión de CMake requerida y podemos ajustar alguna variable
#Como veis, añado un subdirectorio, en donde habrá otro fichero CMakeLists.txt que le indicará al compilador qué hacer
#CMake únicamente genera ficheros de forma que podamos compilar después escribiendo "make" en la terminal
#Es tan sencillo como crear una carpeta (mkdir cmake-build-debug, cd cmake-build-debug) y escribir
#el comando cmake seguido de la ruta al CMakeLists.txt principal, en este caso "cmake ../", y se generará un fichero
# "Makefile" para compilar. Una vez termine el comando cmake, escribimos make y se generará nuestro proyecto compilado

cmake_minimum_required(VERSION 3.9)
project(controller_base)

#aquí se configura el estándar del lenguaje, en este caso c++11, no me preguntéis por qué, yo siempre le echo 20€
set(CMAKE_CXX_STANDARD 11)

#aquí añadimos el directorio include, esto significa que cuando queramos hacer #include <xxx/yyy> la raíz de ese comando
#será la carpeta include, es decir, si queremos añadir Algorithm.h será #include <Algorithm/Algorithm.h>
include_directories(include)

#aquí añadimos el subdirectorio src, porque dentro hay más chicha. Allí hay otro CMakeLists que define las reglas
add_subdirectory(src)
