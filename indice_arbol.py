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
    Estructura del Árbol Binario de Búsqueda.
    Se encarga de acomodar los Nodos de forma ordenada para que
    las búsquedas sean súper rápidas.
    """
    def __init__(self):
        self.raiz = None

    def insertar(self, id_asada, posicion):
        """Añade un nuevo ID y su posición al árbol de forma ordenada."""
        if self.raiz is None:
            self.raiz = Nodo(id_asada, posicion)
        else:
            self._insertar_recursivo(self.raiz, int(id_asada), posicion)

    def _insertar_recursivo(self, nodo_actual, id_asada, posicion):
        """Función auxiliar que busca el lugar correcto para el nuevo nodo."""
        if id_asada < nodo_actual.id_asada:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(id_asada, posicion)
            else:
                self._insertar_recursivo(nodo_actual.izquierdo, id_asada, posicion)
        elif id_asada > nodo_actual.id_asada:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(id_asada, posicion)
            else:
                self._insertar_recursivo(nodo_actual.derecho, id_asada, posicion)

    def buscar(self, id_asada):
        """
        Busca un ID en el árbol. 
        Devuelve la posición física en el archivo principal si lo encuentra, o None si no existe.
        """
        return self._buscar_recursivo(self.raiz, int(id_asada))

    def _buscar_recursivo(self, nodo_actual, id_asada):
        """Función auxiliar que navega por las ramas del árbol para encontrar el ID."""
        if nodo_actual is None:
            return None
        if nodo_actual.id_asada == id_asada:
            return nodo_actual.posicion
        elif id_asada < nodo_actual.id_asada:
            return self._buscar_recursivo(nodo_actual.izquierdo, id_asada)
        else:
            return self._buscar_recursivo(nodo_actual.derecho, id_asada)


def guardar_arbol_binario(arbol, nombre_archivo="indice_arbol.bin"):
    """Guarda todo el árbol en un segundo archivo binario usando pickle."""
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

if __name__ == "__main__":
    posiciones_de_prueba = {
        "1790": 0,
        "200": 150,
        "3000": 300
    }
    
    mi_arbol = ArbolBinario()
    for asada_id, pos in posiciones_de_prueba.items():
        mi_arbol.insertar(asada_id, pos)
        
    guardar_arbol_binario(mi_arbol)
    
    arbol_recuperado = cargar_arbol_binario()
    if arbol_recuperado:
        pos_encontrada = arbol_recuperado.buscar("1790")
        print(f"Resultado de búsqueda para 1790: Se encuentra en el byte {pos_encontrada}")