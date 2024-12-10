import os

def obtener_extensiones_y_cantidad(carpeta):
    extensiones_contador = {}

    # Iteramos sobre directorios y subdirectorios usando os.walk
    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            nombre, extension = os.path.splitext(archivo)
            # Obtener solo la última extensión después del último punto
            if extension:
                extension_sin_punto = extension.rsplit('.', 1)[-1]
                # Incrementar el contador para la extensión
                extensiones_contador[extension_sin_punto] = extensiones_contador.get(extension_sin_punto, 0) + 1

    return extensiones_contador

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
                    ruta_completa = os.path.normpath(os.path.join(directorio_actual, archivo))
                    rutas_archivos.append(ruta_completa)

    return rutas_archivos

def obtener_tamano_total_archivos(rutas_archivos):
    tamano_total = 0

    for ruta_archivo in rutas_archivos:
        try:
            tamano_total += os.path.getsize(ruta_archivo)
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo en la ruta {ruta_archivo}")

    return tamano_total

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Llamamos a la función y obtenemos las extensiones y sus cantidades
extensiones_y_cantidades = obtener_extensiones_y_cantidad(carpeta_a_analizar)

# Ordenamos las extensiones de mayor a menor cantidad
extensiones_ordenadas = sorted(extensiones_y_cantidades.items(), key=lambda x: x[1], reverse=True)

# Ruta del archivo de texto donde guardaremos las extensiones y cantidades ordenadas
archivo_salida_extensiones = "extensiones_y_cantidades_ordenadas.txt"

# Escribimos las extensiones y cantidades ordenadas en el archivo de texto
with open(archivo_salida_extensiones, "w") as archivo_extensiones:
    archivo_extensiones.write("Extensiones y cantidades encontradas (ordenadas de mayor a menor):\n")
    for extension, cantidad in extensiones_ordenadas:
        archivo_extensiones.write(f"{extension}: {cantidad} archivos\n")

print(f"Las extensiones y sus cantidades ordenadas se han guardado en {archivo_salida_extensiones}")

# Buscamos archivos DWG y obtenemos sus rutas
extension_busqueda_dwg = "dwg"
rutas_archivos_dwg = obtener_rutas_archivos_por_extension(carpeta_a_analizar, extension_busqueda_dwg)

# Ruta del archivo de texto donde guardaremos las rutas de archivos DWG
archivo_rutas_dwg = "archivos_dwg_encontrados.txt"

# Escribimos las rutas de archivos DWG en el archivo de texto
with open(archivo_rutas_dwg, "w", encoding='utf-8') as archivo_dwg:
    archivo_dwg.write("Rutas de archivos DWG encontrados:\n")
    for ruta in rutas_archivos_dwg:
        archivo_dwg.write(f"{ruta}\n")

print(f"Las rutas de archivos DWG se han guardado en {archivo_rutas_dwg}")

# Obtenemos el tamaño total de los archivos DWG
tamano_total_dwg = obtener_tamano_total_archivos(rutas_archivos_dwg)
print(f"Tamaño total de los archivos DWG: {tamano_total_dwg} bytes")
