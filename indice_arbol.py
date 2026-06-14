import pickle

class Nodo:
    """
    Representa cada 'hoja' o elemento individual dentro del árbol.
    Guarda el ID de la ASADA, su posición en el archivo principal,
    y hacia dónde conectan sus "hijos" izquierdo y derecho.
    """
    def __init__(self, id_asada, posicion):
        self.id_asada = int(id_asada)
        self.posicion = posicion
        self.izquierdo = None
        self.derecho = None

class ArbolBinario:
    """
    Estructura del Árbol Binario de Búsqueda iterativo.
    Se encarga de acomodar los Nodos de forma ordenada utilizando ciclos
    para evitar errores de profundidad con la recursividad.
    """
    def __init__(self):
        self.raiz = None

    def insertar(self, id_asada, posicion):
        """Añade un nuevo ID y su posición al árbol de forma ordenada usando un ciclo."""
        id_asada = int(id_asada)
        nuevo_nodo = Nodo(id_asada, posicion)

        # Si el árbol está vacío, este es el primer nodo
        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        nodo_actual = self.raiz
        
        # Usamos un ciclo para bajar por el árbol hasta encontrar un espacio vacío
        while True:
            if id_asada < nodo_actual.id_asada:
                # Si es menor, vamos a la izquierda
                if nodo_actual.izquierdo is None:
                    nodo_actual.izquierdo = nuevo_nodo
                    break
                else:
                    nodo_actual = nodo_actual.izquierdo
            elif id_asada > nodo_actual.id_asada:
                # Si es mayor, vamos a la derecha
                if nodo_actual.derecho is None:
                    nodo_actual.derecho = nuevo_nodo
                    break
                else:
                    nodo_actual = nodo_actual.derecho
            else:
                # Si el ID ya existe, solo actualizamos su posición para no duplicar
                nodo_actual.posicion = posicion
                break

    def buscar(self, id_asada):
        """
        Busca un ID en el árbol usando un ciclo. 
        Devuelve la posición física en el archivo si lo encuentra, o None si no existe.
        """
        id_asada = int(id_asada)
        nodo_actual = self.raiz
        
        # Navegamos por el árbol hasta encontrarlo o llegar al final
        while nodo_actual is not None:
            if id_asada == nodo_actual.id_asada:
                return nodo_actual.posicion
            elif id_asada < nodo_actual.id_asada:
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
                
        return None

def guardar_arbol_binario(arbol, nombre_archivo="indice_arbol.bin"):
    """Guarda todo el árbol en un archivo binario usando pickle."""
    with open(nombre_archivo, "wb") as archivo:
        pickle.dump(arbol, archivo)
    print(f"¡Árbol binario guardado correctamente en {nombre_archivo}!")

def cargar_arbol_binario(nombre_archivo="indice_arbol.bin"):
    """Carga el árbol desde el archivo binario hacia la memoria para poder buscar."""
    try:
        with open(nombre_archivo, "rb") as archivo:
            arbol = pickle.load(archivo)
        print("¡Árbol cargado a la memoria exitosamente!")
        return arbol
    except FileNotFoundError:
        print("El archivo del árbol no existe aún.")
        return None