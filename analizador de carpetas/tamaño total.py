import os

def obtener_tamano_total_archivos(carpeta, extension_busqueda):
    tamano_total = 0

    # Iteramos sobre directorios y subdirectorios usando os.walk
    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            nombre, extension = os.path.splitext(archivo)
            if extension.lower() == extension_busqueda.lower():
                ruta_completa = os.path.join(directorio_actual, archivo)
                tamano_total += os.path.getsize(ruta_completa)

    return tamano_total

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Buscamos archivos DWG y obtenemos su tamaño total
extension_busqueda_dwg = "dwg"
tamano_total_dwg = obtener_tamano_total_archivos(carpeta_a_analizar, extension_busqueda_dwg)

print(f"Tamaño total de los archivos DWG en {carpeta_a_analizar}: {tamano_total_dwg} bytes")
