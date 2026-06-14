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
            with open(archivo_meta, "r", encoding="utf-8") as f:
                meta = json.load(f)
                metadato_local = meta.get("metadato_guardado")
        
        if metadato_remoto != metadato_local or not os.path.exists(archivo_datos):
            print("Cambio detectado en la información. Actualizando base de datos...")
            
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
            print("La información ya está al día. No es necesario regenerar los archivos binarios.")
            with open(archivo_datos, "r", encoding="utf-8") as f:
                datos = json.load(f)
            return datos, False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con ARESEP: {e}")
        if os.path.exists(archivo_datos):
            print("Usando datos locales por falta de conexión.")
            with open(archivo_datos, "r", encoding="utf-8") as f:
                return json.load(f), False
        return None, False