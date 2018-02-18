import numpy as np
from scipy.spatial import distance
import networkx as nx
import matplotlib.pyplot as plt

altura_vuelo_uav = 20
ancho_sensor = 1
distancia_focal = 0.5
angulo_inclinacion = 90

fraccion_solape = 0.4

x = 100
y = 200

'''
SUPOSICIONES:
- Las cámaras de los drones tienen las mismas características y están posicionadas con el mismo ángulo de inclinación.
- Los drones vuelan a la misma altura y velocidad.


VERSION 0:
- A mayores, para una primera versión no se va a considerar la orientación del dron para tomar las imagenes porque se 
    supone que van a estar orientadas hacia el suelo.
'''

def calcularFootprint (altura_vuelo_uav, ancho_sensor, distancia_focal, angulo_inclinacion):
    '''
    Calcula el número de metros que recoge la cámara del UAV.

    Parámetros
    ------------
    altura_vuelo_uav : float
        Distancia en metros del dron al suelo del área que se quiere cubrir.
    ancho_sensor : float
        Ancho del sensor de imagen en milimetros.
    distancia_focal : float
        Distancia focal de la cámara en milimetros.
    angulo_inclinacion : float
        Ángulo de inclinación de la cámara respecto al UAV en posición horizontal.

    Returns
    ---------
    float
        Número de metros capturados por la cámara del UAV.
    '''
    # TODO: calcular para angulo de inclinación distinto de 90º
    return altura_vuelo_uav * (ancho_sensor / distancia_focal)


def calcularNumeroFilasDistancia (lado_area_corto, footprint, fraccion_solape):
    '''
    Calcula el número de filas necesarias para cubrir todo el área rectangular en sentido perpendicular al lado más corto
    respecto a la porción de área cubierta por la cámara y una fracción de solape.

    Parámetros
    ------------
    lado_area_corto : float
        Longitud del lado más corto del área. Tiene que estar en las mismas unidades que el footprint.
    footprint : float
        Número de metros capturados por la cámara del UAV.
    fraccion_solape : float
        Fracción de solape entre las imágenes tomadas por los UAVs.

    Returns
    --------
    int
        Número de filas necesarias.
    float
        Distancia entre las filas.
    '''
    num_filas = np.ceil(lado_area_corto / (footprint * (1 - fraccion_solape)))
    return int(num_filas), (lado_area_corto/num_filas)


def calcularDivisionesArea (lado_area_corto, lado_area_largo, numero_filas, distancia_filas, footprint):
    '''
    Devuelve las divisiones en ambas cordenadas
    '''

    numero_divisiones_lado_largo = int(np.ceil(lado_area_largo / footprint))

    divisiones_lado_corto = [i * distancia_filas - (distancia_filas / 2) for i in range (1, numero_filas + 1)]
    divisiones_lado_largo = [i * footprint - (footprint / 2) for i in range (1, numero_divisiones_lado_largo + 1)]

    return divisiones_lado_largo, divisiones_lado_corto


def calcularNodosGrafo (divisiones_x, divisiones_y):
    '''
    Devuelve una lista con las coordenadas de cada nodo del grafo.
    '''

    #return [(pos_x, pos_y) for pos_x in divisiones_x for pos_y in divisiones_y]
    nodos = []
    id = 1
    for pos_x in divisiones_x:
        fila_nodos = []
        for pos_y in divisiones_y:
            fila_nodos.append([id, (pos_x, pos_y)])
            id += 1

            # fila_nodos.append(np.array([pos_x, pos_y]))
            # fila_nodos.append((pos_x, pos_y))
        nodos.append(fila_nodos)
    return nodos


def calcularGrafo (nodos):
    '''
    
    '''

    # Construimos el grafo con los nodos:
    grafo = nx.Graph()
    n_filas, n_columnas = len(nodos), len(nodos[0])
    for n_fila in range(n_filas):
        for n_columna in range (n_columnas):
            grafo.add_node(nodos[n_fila][n_columna][0], posicion = nodos[n_fila][n_columna][1], fila = n_fila, columna = n_columna)
            #grafo.add_node(nodos[n_fila][n_columna][0])

    # Establecemos los edges, lineas de conexion, entre los nodos:
    for n_fila in range(n_filas):
        for n_columna in range (n_columnas):
            for i, j in [[n_fila + 1, n_columna], [n_fila - 1, n_columna], [n_fila, n_columna + 1], [n_fila, n_columna - 1]]:
                if i < 0 or j < 0 or i >= n_filas or j >= n_columnas: # No existe el nodo
                    continue
                grafo.add_edge(nodos[n_fila][n_columna][0], nodos[i][j][0]) # nodos[n_fila][n_columna][0] ----(vecino)---- nodos[i][j][0]
    return grafo


def main (): # def calcularGrafo (x, y, altura_vuelo_uav, caracteristicas_sensor):
    lado_area_corto = x * (x < y) + y * (y < x) + x * (x == y)
    lado_area_largo = x * (x > y) + y * (y > x) + x * (x == y)

    footprint = calcularFootprint (altura_vuelo_uav, ancho_sensor, distancia_focal, angulo_inclinacion)
    numero_filas, distancia_filas = calcularNumeroFilasDistancia (lado_area_corto, footprint, fraccion_solape)

    if lado_area_largo == x:
        divisiones_x, divisiones_y = calcularDivisionesArea (lado_area_corto, lado_area_largo, numero_filas, distancia_filas, footprint)
    else:
        divisiones_y, divisiones_x = calcularDivisionesArea (lado_area_corto, lado_area_largo, numero_filas, distancia_filas, footprint)

    nodos = calcularNodosGrafo (divisiones_x, divisiones_y)

    grafo = calcularGrafo(nodos)

    nx.draw(grafo, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    main()

