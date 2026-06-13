import json

def crear_archivo_binario(datos_json):
    """
    Toma los datos descargados en formato JSON y los guarda en un 
    archivo binario secuencial.
    """
    lista_asadas = datos_json.get('value', [])
    
    posiciones = {} 
    
    with open("asadas_principal.bin", "wb") as archivo_binario:
        
        for asada in lista_asadas:
            posicion_actual = archivo_binario.tell()
            
            id_asada = asada.get("id_Asada")
            
            if id_asada:
                posiciones[id_asada] = posicion_actual
            
            texto_asada = json.dumps(asada, ensure_ascii=False) + "\n"
            bytes_asada = texto_asada.encode('utf-8')
            
            archivo_binario.write(bytes_asada)
            
    print(f"¡Se guardaron {len(lista_asadas)} ASADAS en el archivo binario secuencial!")
    
    return posiciones

if __name__ == "__main__":
    try:
        with open("asadas.json", "r", encoding="utf-8") as f:
            datos_prueba = json.load(f)
            
        posiciones_obtenidas = crear_archivo_binario(datos_prueba)
        
        print("Posiciones obtenidas para las primeras 3 ASADAS:", list(posiciones_obtenidas.items())[:3])
        
    except FileNotFoundError:
        print("Primero debes correr el script de descarga para tener el asadas.json")