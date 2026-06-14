import socket
import threading
import json
from indice_arbol import cargar_arbol_binario
from listas_geograficas import cargar_estructura_geografica

HOST = '127.0.0.1'  
PUERTO = 5000       

print("--- INICIANDO SERVIDOR CENTRAL DE ASADAS ---")
arbol_indices = cargar_arbol_binario()
estructura_geo = cargar_estructura_geografica()

def leer_registro_principal(posicion_byte):
    """Salta directamente al byte indicado en el archivo binario principal y lee la ASADA."""
    try:
        with open("asadas_principal.bin", "rb") as archivo:
            archivo.seek(posicion_byte)
            linea = archivo.readline()
            return json.loads(linea.decode('utf-8').strip())
    except Exception as e:
        print(f"Error al leer el archivo principal en byte {posicion_byte}: {e}")
        return None

def manejar_cliente(conexion, direccion):
    """Administra la sesión de comunicación con un cliente específico."""
    print(f"Nueva conexión establecida desde {direccion}")
    try:
        while True:
            datos_recibidos = conexion.recv(4096)
            if not datos_recibidos:
                break 
                
            peticion = json.loads(datos_recibidos.decode('utf-8'))
            tipo_consulta = peticion.get("tipo")
            respuesta = {"estado": "error", "contenido": "Consulta inválida o no reconocida."}
            
            #CONSULTA 1: Búsqueda rápida por ID
            if tipo_consulta == "POR_ID":
                id_buscar = peticion.get("id")
                if arbol_indices:
                    posicion = arbol_indices.buscar(id_buscar)
                    if posicion is not None:
                        datos_asada = leer_registro_principal(posicion)
                        if datos_asada:
                            respuesta = {"estado": "ok", "contenido": datos_asada}
                        else:
                            respuesta = {"estado": "error", "contenido": "No se pudo recuperar el registro físico."}
                    else:
                        respuesta = {"estado": "error", "contenido": f"ASADA con ID {id_buscar} no registrada."}
                else:
                    respuesta = {"estado": "error", "contenido": "Índice de árbol binario no cargado en el servidor."}
            
            #CONSULTA 2: Obtener todas las provincias
            elif tipo_consulta == "OBTENER_PROVINCIAS":
                if estructura_geo:
                    respuesta = {"estado": "ok", "contenido": estructura_geo.obtener_provincias()}
                else:
                    respuesta = {"estado": "error", "contenido": "Índice geográfico no disponible."}
            
            #CONSULTA 3: Obtener cantones
            elif tipo_consulta == "OBTENER_CANTONES":
                prov = peticion.get("provincia")
                if estructura_geo:
                    respuesta = {"estado": "ok", "contenido": estructura_geo.obtener_cantones(prov)}
            
            #CONSULTA 4: Obtener distritos 
            elif tipo_consulta == "OBTENER_DISTRITOS":
                prov = peticion.get("provincia")
                cant = peticion.get("canton")
                if estructura_geo:
                    respuesta = {"estado": "ok", "contenido": estructura_geo.obtener_distritos(prov, cant)}
            
            #CONSULTA 5: Obtener ASADAS de un distrito
            elif tipo_consulta == "OBTENER_ASADAS_DISTRITO":
                prov = peticion.get("provincia")
                cant = peticion.get("canton")
                dist = peticion.get("distrito")
                if estructura_geo:
                    lista_tuplas = estructura_geo.obtener_asadas_distrito(prov, cant, dist)
                    
                    lista_asadas_completas = []
                    for id_asada, posicion in lista_tuplas:
                        datos_asada = leer_registro_principal(posicion)
                        if datos_asada:
                            lista_asadas_completas.append(datos_asada)
                            
                    respuesta = {"estado": "ok", "contenido": lista_asadas_completas}

            conexion.sendall(json.dumps(respuesta).encode('utf-8'))
            
    except Exception as e:
        print(f"Alerta! procesando cliente {direccion}: {e}")
    finally:
        conexion.close()
        print(f"Conexión finalizada de forma segura con {direccion}")

def arrancar_servidor():
    """Inicializa el socket de escucha TCP/IP."""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    servidor.bind((HOST, PUERTO))
    servidor.listen()
    print(f"Servidor en línea, escuchando peticiones en {HOST}:{PUERTO}...")
    
    while True:
        conexion, direccion = servidor.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
        hilo_cliente.daemon = True
        hilo_cliente.start()

if __name__ == "__main__":
    arrancar_servidor()