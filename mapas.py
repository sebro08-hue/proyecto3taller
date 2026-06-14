import os
import webbrowser
from pathlib import Path
import folium
from pyproj import Transformer

def generar_mapa_asadas(lista_asadas, nombre_archivo="mapa_asadas.html"):
    """
    Recibe una lista de diccionarios de ASADAS (con sus datos completos),
    convierte sus coordenadas CRTM05 a WGS84 y genera un mapa HTML con marcadores.
    Abre el mapa en el navegador predeterminado.
    """
    if not lista_asadas:
        print("No se proporcionaron ASADAS para graficar en el mapa.")
        return False

    print(f"Generando mapa para {len(lista_asadas)} ASADAS...")

    try:
        transformador = Transformer.from_crs("EPSG:5367", "EPSG:4326", always_xy=True)
    except Exception as e:
        print(f"Error al inicializar pyproj: {e}. Asegúrate de tener la librería instalada.")
        return False

    suma_lat = 0
    suma_lon = 0
    asadas_validas = []

    for asada in lista_asadas:
        try:
            x_crtm05 = float(asada.get('coordenadaX', 0))
            y_crtm05 = float(asada.get('coordenadaY', 0))
            
            if x_crtm05 != 0 and y_crtm05 != 0:
                lon, lat = transformador.transform(x_crtm05, y_crtm05)
                asada['latitud'] = lat
                asada['longitud'] = lon
                
                suma_lat += lat
                suma_lon += lon
                asadas_validas.append(asada)
        except (ValueError, TypeError):
            continue

    if not asadas_validas:
        print("Ninguna de las ASADAS proporcionadas tiene coordenadas válidas.")
        return False

    centro_lat = suma_lat / len(asadas_validas)
    centro_lon = suma_lon / len(asadas_validas)

    mapa = folium.Map(location=[centro_lat, centro_lon], zoom_start=10)

    for asada in asadas_validas:
        nombre = asada.get('operador', 'ASADA sin nombre')
        id_asada = asada.get('id_Asada', 'N/A')
        
        popup_info = f"<b>{nombre}</b><br>ID: {id_asada}<br>Provincia: {asada.get('provincia')}"
        
        folium.Marker(
            [asada['latitud'], asada['longitud']],
            popup=popup_info,
            tooltip="Click para ver info",
            icon=folium.Icon(color="blue", icon="tint")
        ).add_to(mapa)

    try:
        mapa.save(nombre_archivo)
        print(f"Mapa guardado correctamente como: {nombre_archivo}")
        
        ruta_absoluta = Path(nombre_archivo).resolve()
        webbrowser.open(f"file://{ruta_absoluta}")
        return True
        
    except Exception as e:
        print(f"Error al guardar o abrir el mapa: {e}")
        return False

if __name__ == "__main__":
    import json
    try:
        with open("asadas.json", "r", encoding="utf-8") as f:
            datos_completos = json.load(f)
            lista_prueba = datos_completos.get('value', [])[:5]
            generar_mapa_asadas(lista_prueba)
    except FileNotFoundError:
        print("El archivo asadas.json no existe. Corre el script principal primero.")