#include <iostream>
#include <Algorithm/Algorithm.h>

int main() {
    std::cout << "Hola! Yo soy el proceso que se debe ejecutar en la estación base" << std::endl;

    Algorithm instancia;

    std::cout << "Mi instancia de algorithm tiene " << std::to_string(instancia.get_num_nodos()) << " nodos" << std::endl;

    instancia.set_num_nodos(10);

    std::cout << "Ahh pero ahora tiene " << std::to_string(instancia.get_num_nodos()) << " nodos" << std::endl;

    return 0;
}