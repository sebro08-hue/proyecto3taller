import socket
import json
from mapas import generar_mapa_asadas

HOST = '127.0.0.1'
PUERTO = 5000

def enviar_peticion(peticion):
    """Establece conexión con el servidor, pide datos y captura la respuesta."""
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST, PUERTO))
        
        cliente.sendall(json.dumps(peticion).encode('utf-8'))
        
        datos_recibidos = cliente.recv(65536) 
        if datos_recibidos:
            return json.loads(datos_recibidos.decode('utf-8'))
    except ConnectionRefusedError:
        print("Error: El servidor remoto no está encendido o rechazó la conexión.")
    except Exception as e:
        print(f"Error de red inesperado: {e}")
    return None

def ejecutar_menu():
    while True:
        print("\n=============================================")
        print("  SISTEMA DISTRIBUIDO DE CONSULTAS - ARESEP   ")
        print("=============================================")
        print("1. Buscar ASADA individual por ID")
        print("2. Exploración Geográfica Jerárquica")
        print("3. Salir")
        opcion = input("Seleccione su opción: ").strip()

        if opcion == "1":
            id_ingresado = input("Digite el ID de la ASADA: ").strip()
            peticion = {"tipo": "POR_ID", "id": id_ingresado}
            
            respuesta = enviar_peticion(peticion)
            if respuesta and respuesta.get("estado") == "ok":
                asada = respuesta.get("contenido")
                print("\n --- ASADA ENCONTRADA VIA RED ---")
                print(f"-> ID: {asada.get('id_Asada')}")
                print(f"-> Nombre/Operador: {asada.get('operador')}")
                print(f"-> Ubicación: {asada.get('provincia')}, {asada.get('canton')}, {asada.get('distrito')}")
                print(f"-> Contacto: Tel: {asada.get('telefono')} | Correo: {asada.get('correo')}")
                
                ver_mapa = input("\n¿Desea abrir esta ASADA en el mapa web? (s/n): ").strip().lower()
                if ver_mapa == 's':
                    generar_mapa_asadas([asada])
            else:
                detalles = respuesta.get("contenido") if respuesta else "Servidor fuera de línea."
                print(f"\nError: {detalles}")

        elif opcion == "2":
            print("\nCargando Provincias...")
            resp_p = enviar_peticion({"tipo": "OBTENER_PROVINCIAS"})
            if not resp_p or resp_p.get("estado") != "ok":
                print("No se pudo obtener la división política.")
                continue
            
            provincias = resp_p.get("contenido")
            for idx, prov in enumerate(provincias, 1):
                print(f"  {idx}. {prov}")
            
            sel_p = int(input("Seleccione el número de provincia: ")) - 1
            prov_nom = provincias[sel_p]

            resp_c = enviar_peticion({"tipo": "OBTENER_CANTONES", "provincia": prov_nom})
            cantones = resp_c.get("contenido")
            print(f"\n--- Cantones de {prov_nom} ---")
            for idx, cant in enumerate(cantones, 1):
                print(f"  {idx}. {cant}")
            
            sel_c = int(input("Seleccione el número de cantón: ")) - 1
            cant_nom = cantones[sel_c]

            resp_d = enviar_peticion({"tipo": "OBTENER_DISTRITOS", "provincia": prov_nom, "canton": cant_nom})
            distritos = resp_d.get("contenido")
            print(f"\n--- Distritos de {cant_nom} ---")
            for idx, dist in enumerate(distritos, 1):
                print(f"  {idx}. {dist}")
            
            sel_d = int(input("Seleccione el número de distrito: ")) - 1
            dist_nom = distritos[sel_d]

            resp_a = enviar_peticion({
                "tipo": "OBTENER_ASADAS_DISTRITO", 
                "provincia": prov_nom, 
                "canton": cant_nom, 
                "distrito": dist_nom
            })
            asadas_resultado = resp_a.get("contenido")
            
            print(f"\nASADAS encontradas en el distrito {dist_nom} ({len(asadas_resultado)}):")
            for asada in asadas_resultado:
                print(f"  • ID [{asada.get('id_Asada')}]: {asada.get('operador')}")
            
            if asadas_resultado:
                ver_mapa = input("\n¿Desea trazar TODAS estas ASADAS en el mapa interactivo? (s/n): ").strip().lower()
                if ver_mapa == 's':
                    generar_mapa_asadas(asadas_resultado)
            else:
                print("No hay ASADAS con coordenadas registradas para este distrito geográfico.")

        elif opcion == "3":
            print("Cerrando la aplicación cliente. ¡Buen día!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    ejecutar_menu()