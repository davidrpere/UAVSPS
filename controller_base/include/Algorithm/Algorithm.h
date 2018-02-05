//
// Created by David Rodriguez Pereira on 5/2/18.
//

#ifndef CONTROLLER_BASE_ALGORITHM_H
#define CONTROLLER_BASE_ALGORITHM_H


class Algorithm {

public:

    Algorithm()
        : num_nodos(0)
    {
        std::cout << "Este es el constructor por defecto de algorithm" << std::endl;
    }

    void set_num_nodos(int n_nodos);

    int get_num_nodos();

private:

    int num_nodos;

};


#endif //CONTROLLER_BASE_ALGORITHM_H
