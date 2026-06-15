import pickle

class Nodo:
    def __init__(self, id_asada, posicion):
        self.id_asada = int(id_asada)
        self.posicion = posicion
        self.izquierdo = None
        self.derecho = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, id_asada, posicion):
        """Inserta un nuevo ID de forma iterativa."""
        id_asada = int(id_asada)
        nuevo_nodo = Nodo(id_asada, posicion)

        if self.raiz is None:
            self.raiz = nuevo_nodo
            return

        nodo_actual = self.raiz
        while True:
            if id_asada < nodo_actual.id_asada:
                if nodo_actual.izquierdo is None:
                    nodo_actual.izquierdo = nuevo_nodo
                    break
                else:
                    nodo_actual = nodo_actual.izquierdo
            elif id_asada > nodo_actual.id_asada:
                if nodo_actual.derecho is None:
                    nodo_actual.derecho = nuevo_nodo
                    break
                else:
                    nodo_actual = nodo_actual.derecho
            else:
                nodo_actual.posicion = posicion
                break

    def buscar(self, id_asada):
        """Busca un ID en el árbol de forma iterativa."""
        id_asada = int(id_asada)
        nodo_actual = self.raiz
        while nodo_actual is not None:
            if id_asada == nodo_actual.id_asada:
                return nodo_actual.posicion
            elif id_asada < nodo_actual.id_asada:
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
        return None

    def balancear(self):
        """
        Transforma el árbol para que crezca hacia los lados 
        en lugar de hacia abajo, reduciendo la profundidad drásticamente.
        """
        nodos_ordenados = []
        pila = []
        actual = self.raiz
        while pila or actual:
            while actual:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            nodos_ordenados.append((actual.id_asada, actual.posicion))
            actual = actual.derecho
        
        def construir_piramide(inicio, fin):
            if inicio > fin:
                return None
            
            medio = (inicio + fin) // 2
            id_asada, posicion = nodos_ordenados[medio]
            
            nuevo = Nodo(id_asada, posicion)
            nuevo.izquierdo = construir_piramide(inicio, medio - 1)
            nuevo.derecho = construir_piramide(medio + 1, fin)
            return nuevo
        
        self.raiz = construir_piramide(0, len(nodos_ordenados) - 1)

def guardar_arbol_binario(arbol, nombre_archivo="indice_arbol.bin"):
    """Aplica el balanceo hacia los lados y guarda el árbol en disco."""
    try:
        arbol.balancear() 
        
        with open(nombre_archivo, "wb") as archivo:
            pickle.dump(arbol, archivo)
        print(f"¡Árbol binario guardado perfectamente en {nombre_archivo}!")
        
    except Exception as e:
        print(f"Error al guardar el árbol binario: {e}")


def cargar_arbol_binario(nombre_archivo="indice_arbol.bin"):
    """Carga el árbol desde el archivo binario."""
    try:
        with open(nombre_archivo, "rb") as archivo:
            arbol = pickle.load(archivo)
        return arbol
    except Exception as e:
        print(f"No se pudo cargar el índice del árbol: {e}")
        return None