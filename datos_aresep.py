import requests
import json
import os

def verificar_actualizacion():
    """
    Verifica los metadatos remotos en ARESEP.
    Descarga y regenera los datos solo si hubo cambios reales.
    """
    url = "https://datos.aresep.go.cr/ws.datosabiertos/Services/IA/Asadas.svc/ObtenerInformacionUbicacionAsadas"
    archivo_meta = "metadatos_actualizacion.json"
    archivo_datos = "asadas.json"
    
    try:
        respuesta_head = requests.head(url)
        
        metadato_remoto = (
            respuesta_head.headers.get('Last-Modified') or 
            respuesta_head.headers.get('ETag') or 
            respuesta_head.headers.get('Content-Length')
        )
        
        datos_en_memoria = None
        
        if not metadato_remoto:
            respuesta_get = requests.get(url)
            respuesta_get.raise_for_status()
            metadato_remoto = str(len(respuesta_get.content))
            datos_en_memoria = respuesta_get.json()
            
        metadato_local = None
        if os.path.exists(archivo_meta):
            try:
                with open(archivo_meta, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                    metadato_local = meta.get("metadato_guardado")
            except Exception:
                metadato_local = None
        
        if metadato_remoto != metadato_local or not os.path.exists(archivo_datos):
            print("Cambio detectado (o primera ejecución). Descargando base de datos...")
            
            if not datos_en_memoria:
                respuesta = requests.get(url)
                respuesta.raise_for_status()
                datos_en_memoria = respuesta.json()
            
            with open(archivo_datos, "w", encoding="utf-8") as f:
                json.dump(datos_en_memoria, f, indent=4, ensure_ascii=False)
                
            with open(archivo_meta, "w", encoding="utf-8") as f:
                json.dump({"metadato_guardado": metadato_remoto}, f)
                
            return datos_en_memoria, True 
            
        else:
            print("La información ya está al día.")
            with open(archivo_datos, "r", encoding="utf-8") as f:
                datos = json.load(f)
            return datos, False
            
    except requests.exceptions.RequestException as e:
        print(f"Error de red al intentar conectar con ARESEP: {e}")
        
        if os.path.exists(archivo_datos):
            print("Rescatando datos locales de 'asadas.json' por falta de conexión...")
            try:
                with open(archivo_datos, "r", encoding="utf-8") as f:
                    datos_locales = json.load(f)
                return datos_locales, False
            except Exception as error_lectura:
                print(f"Error leyendo el respaldo local: {error_lectura}")
                return None, False
        else:
            print("No hay conexión a internet y no existe un respaldo local.")
            return None, False