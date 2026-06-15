import json
import os
from datos_aresep import verificar_actualizacion
from indice_arbol import ArbolBinario, guardar_arbol_binario
from listas_geograficas import EstructuraGeografica, guardar_estructura_geografica

def generar_archivos_y_estructuras(datos_json):
    lista_asadas = datos_json.get('value', [])
    arbol = ArbolBinario()
    estructura_geo = EstructuraGeografica()
    
    print("Construyendo archivos binarios e índices...")
    
    with open("asadas_principal.bin", "wb") as archivo_binario:
        for asada in lista_asadas:
            posicion_actual = archivo_binario.tell()
            
            texto_asada = json.dumps(asada, ensure_ascii=False) + "\n"
            archivo_binario.write(texto_asada.encode('utf-8'))
            
            id_asada = asada.get("id_Asada")
            provincia = asada.get("provincia", "DESCONOCIDA")
            canton = asada.get("canton", "DESCONOCIDO")
            distrito = asada.get("distrito", "DESCONOCIDO")
            
            if id_asada:
                arbol.insertar(id_asada, posicion_actual)
                estructura_geo.insertar_asada(provincia, canton, distrito, id_asada, posicion_actual)

    print(f"¡Se guardaron {len(lista_asadas)} ASADAS en el archivo binario principal!")
    guardar_arbol_binario(arbol)
    guardar_estructura_geografica(estructura_geo)
    print("¡Índices guardados con éxito!")

if __name__ == "__main__":
    print("--- INICIANDO SISTEMA DE INDEXACIÓN DE ASADAS ---")
    
    datos_aresep = None
    hay_cambios = False
    
    try:
        resultado = verificar_actualizacion()
        if isinstance(resultado, tuple) and len(resultado) >= 2:
            datos_aresep = resultado[0]
            hay_cambios = resultado[1]
        else:
            datos_aresep = resultado
    except Exception as e:
        print(f"Alerta al verificar actualización: {e}")

    if datos_aresep is None and os.path.exists("asadas.json"):
        print("Cargando respaldo local de 'asadas.json'...")
        try:
            with open("asadas.json", "r", encoding="utf-8") as f:
                datos_aresep = json.load(f)
        except Exception:
            datos_aresep = None

    faltan_archivos = not (os.path.exists("asadas_principal.bin") and 
                           os.path.exists("indice_arbol.bin") and 
                           os.path.exists("indice_geografico.bin"))
                           
    if hay_cambios or faltan_archivos:
        if datos_aresep is not None:
            generar_archivos_y_estructuras(datos_aresep)
        else:
            print("Error crítico: No se obtuvieron datos remotos ni locales.")
    else:
        print("Las bases de datos e índices locales ya están al día. Listos para iniciar el servidor.")