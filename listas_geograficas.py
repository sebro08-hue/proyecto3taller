import pickle

class NodoAsadaGeografica:
    """Nodo final de la lista. Guarda la referencia física al archivo principal."""
    def __init__(self, id_asada, posicion_principal):
        self.id_asada = int(id_asada)
        self.posicion_principal = posicion_principal
        self.siguiente = None  

class NodoDistrito:
    """Nodo de Distrito. Contiene una lista enlazada de ASADAS."""
    def __init__(self, nombre):
        self.nombre = nombre.strip().upper()
        self.sublista_asadas = None  
        self.siguiente = None        

class NodoCanton:
    """Nodo de Cantón. Apunta hacia abajo a sus distritos."""
    def __init__(self, nombre):
        self.nombre = nombre.strip().upper()
        self.sublista_distritos = None    
        self.siguiente = None           

class NodoProvincia:
    """Nodo Raíz por región. Apunta hacia abajo a sus cantones."""
    def __init__(self, nombre):
        self.nombre = nombre.strip().upper()
        self.sublista_cantones = None   
        self.siguiente = None           

class EstructuraGeografica:
    """Lista enlazada de listas (Jerárquica multipuntero)."""
    def __init__(self):
        self.raiz_provincias = None  

    def insertar_asada(self, provincia_nom, canton_nom, distrito_nom, id_asada, posicion_principal):
        """Inserta de forma ordenada y jerárquica cada registro."""
        prov_nom = provincia_nom.strip().upper()
        cant_nom = canton_nom.strip().upper()
        dist_nom = distrito_nom.strip().upper()

        prov = self._buscar_o_crear_provincia(prov_nom)
        
        cant = self._buscar_o_crear_canton(prov, cant_nom)
        
        dist = self._buscar_o_crear_distrito(cant, dist_nom)
        
        self._insertar_asada_ordenada(dist, id_asada, posicion_principal)

    def _buscar_o_crear_provincia(self, nombre):
        actual = self.raiz_provincias
        anterior = None
        while actual and actual.nombre != nombre:
            anterior = actual
            actual = actual.siguiente
        if actual:
            return actual
        nuevo = NodoProvincia(nombre)
        if anterior:
            anterior.siguiente = nuevo
        else:
            self.raiz_provincias = nuevo
        return nuevo

    def _buscar_o_crear_canton(self, provincia, nombre):
        actual = provincia.sublista_cantones
        anterior = None
        while actual and actual.nombre != nombre:
            anterior = actual
            actual = actual.siguiente
        if actual:
            return actual
        nuevo = NodoCanton(nombre)
        if anterior:
            anterior.siguiente = nuevo
        else:
            provincia.sublista_cantones = nuevo
        return nuevo

    def _buscar_o_crear_distrito(self, canton, nombre):
        actual = canton.sublista_distritos
        anterior = None
        while actual and actual.nombre != nombre:
            anterior = actual
            actual = actual.siguiente
        if actual:
            return actual
        nuevo = NodoDistrito(nombre)
        if anterior:
            anterior.siguiente = nuevo
        else:
            canton.sublista_distritos = nuevo
        return nuevo

    def _insertar_asada_ordenada(self, distrito, id_asada, posicion_principal):
        id_num = int(id_asada)
        nuevo = NodoAsadaGeografica(id_asada, posicion_principal)
        
        actual = distrito.sublista_asadas
        anterior = None
        
        while actual and actual.id_asada < id_num:
            anterior = actual
            actual = actual.siguiente
            
        if actual and actual.id_asada == id_num:
            return 
            
        nuevo.siguiente = actual
        if anterior:
            anterior.siguiente = nuevo
        else:
            distrito.sublista_asadas = nuevo

    def obtener_provincias(self):
        lista = []
        actual = self.raiz_provincias
        while actual:
            lista.append(actual.nombre)
            actual = actual.siguiente
        return sorted(lista)

    def obtener_cantones(self, provincia_nom):
        lista = []
        actual_p = self.raiz_provincias
        while actual_p and actual_p.nombre != provincia_nom.upper():
            actual_p = actual_p.siguiente
        if actual_p:
            actual_c = actual_p.sublista_cantones
            while actual_c:
                lista.append(actual_c.nombre)
                actual_c = actual_c.siguiente
        return sorted(lista)

    def obtener_distritos(self, provincia_nom, canton_nom):
        lista = []
        actual_p = self.raiz_provincias
        while actual_p and actual_p.nombre != provincia_nom.upper():
            actual_p = actual_p.siguiente
        if actual_p:
            actual_c = actual_p.sublista_cantones
            while actual_c and actual_c.nombre != canton_nom.upper():
                actual_c = actual_c.siguiente
            if actual_c:
                actual_d = actual_c.sublista_distritos
                while actual_d:
                    lista.append(actual_d.nombre)
                    actual_d = actual_d.siguiente
        return sorted(lista)

    def obtener_asadas_distrito(self, provincia_nom, canton_nom, distrito_nom):
        lista = []
        actual_p = self.raiz_provincias
        while actual_p and actual_p.nombre != provincia_nom.upper():
            actual_p = actual_p.siguiente
        if actual_p:
            actual_c = actual_p.sublista_cantones
            while actual_c and actual_c.nombre != canton_nom.upper():
                actual_c = actual_c.siguiente
            if actual_c:
                actual_d = actual_c.sublista_distritos
                while actual_d and actual_d.nombre != distrito_nom.upper():
                    actual_d = actual_d.siguiente
                if actual_d:
                    actual_a = actual_d.sublista_asadas
                    while actual_a:
                        lista.append((actual_a.id_asada, actual_a.posicion_principal))
                        actual_a = actual_a.siguiente
        return lista 

def guardar_estructura_geografica(estructura, nombre_archivo="indice_geografico.bin"):
    """Serializa y almacena la lista enlazada jerárquica en formato binario."""
    with open(nombre_archivo, "wb") as archivo:
        pickle.dump(estructura, archivo)
    print(f"¡Estructura geográfica guardada en {nombre_archivo}!")

def cargar_estructura_geografica(nombre_archivo="indice_geografico.bin"):
    try:
        with open(nombre_archivo, "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return None