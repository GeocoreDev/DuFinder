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

# Buscamos archivos DOC y obtenemos sus rutas
extension_busqueda_doc = "doc"
rutas_archivos_doc = obtener_rutas_archivos_por_extension(carpeta_a_analizar, extension_busqueda_doc)

# Ruta del archivo de texto donde guardaremos las rutas de archivos DOC
archivo_rutas_doc = "archivos_doc_encontrados.txt"

# Escribimos las rutas de archivos DOC en el archivo de texto
with open(archivo_rutas_doc, "w", encoding='utf-8') as archivo_doc:
    archivo_doc.write("Rutas de archivos DOC encontrados:\n")
    for ruta in rutas_archivos_doc:
        archivo_doc.write(f"{ruta}\n")

print(f"Las rutas de archivos DOC se han guardado en {archivo_rutas_doc}")
