#La carpeta Algorithm está pensada para contener clases y código fuente relativos al algoritmo
#La carpeta Route_planner está pensada para contener definiciones relativas al planeador de rutas
#La carpeta Communication está pensada para contener la clase TCP_Port (El nombre da igual) que contendrá un
#método "send" para enviar información a un nodo
#La carpeta System está pensada para incluir librerías de terceros o cualquier cosa que necesitemos usar
#La carpeta Web está pensada para incluir las interfaces para interactuar con la web

#Este comando es para añadir una librería, Algorithm es una librería porque no tiene main
#Se deben añadir todos los .cpp que emplee, y en cada uno de ellos arriba incluir los precisos
add_library(Algorithm Algorithm/Algorithm.cpp)

#Este comando es para añadir un ejecutable, podríamos tener dos ejecutables diferentes y se crearían cada uno
#con su propio comando add_executable, debemos añadir los .cpp que sean precisos únicamente para el ejecutable
#fijaos que aquí no añadimos algorithm.cpp
add_executable(main main.cpp)

#Este comando hace la magia, enlazamos el ejecutable main con nuestra librería Algorithm, para que el compilador
#sepa qué debe hacer cuando se llame a los métodos definidos en Algorithm, esto debe ser así para cada librería
target_link_libraries(main Algorithm)
