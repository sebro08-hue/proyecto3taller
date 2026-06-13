import requests
import json

def descargar_datos_asadas():
    """
    Se conecta al sitio web de la ARESEP para descargar la información 
    de las ASADAS y la guarda en un archivo local llamado asadas.json.
    """
    url = "https://datos.aresep.go.cr/ws.datosabiertos/Services/IA/Asadas.svc/ObtenerInformacionUbicacionAsadas"
    
    try:
        respuesta = requests.get(url)
        
        respuesta.raise_for_status()
        
        datos = respuesta.json()
        
        with open("asadas.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
        print("¡Datos descargados y guardados correctamente en asadas.json!")
        return datos
        
    except requests.exceptions.RequestException as error:
        print(f"Hubo un problema al intentar descargar los datos: {error}")
        return None

if __name__ == "__main__":
    descargar_datos_asadas()