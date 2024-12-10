import os

def obtener_rutas_archivos_por_extension(carpeta, extension_busqueda):
    rutas_archivos = []

    # Iteramos sobre directorios y subdirectorios usando os.walk
    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            nombre, extension = os.path.splitext(archivo)
            if extension:
                extension_sin_punto = extension.rsplit('.', 1)[-1].lower()
                # Verificar si la extensión coincide con la búsqueda (ignorando mayúsculas y minúsculas)
                if extension_sin_punto == extension_busqueda.lower():
                    ruta_completa = os.path.join(directorio_actual, archivo)
                    rutas_archivos.append(ruta_completa)

    return rutas_archivos

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Buscamos archivos KML y obtenemos sus rutas
extension_busqueda_kml = "kml"
rutas_archivos_kml = obtener_rutas_archivos_por_extension(carpeta_a_analizar, extension_busqueda_kml)

# Ruta del archivo de texto donde guardaremos las rutas de archivos KML
archivo_rutas_kml = "archivos_kml_encontrados.txt"

# Escribimos las rutas de archivos KML en el archivo de texto
with open(archivo_rutas_kml, "w", encoding='utf-8') as archivo_kml:
    archivo_kml.write("Rutas de archivos KML encontrados:\n")
    for ruta in rutas_archivos_kml:
        archivo_kml.write(f"{ruta}\n")

print(f"Las rutas de archivos KML se han guardado en {archivo_rutas_kml}")
