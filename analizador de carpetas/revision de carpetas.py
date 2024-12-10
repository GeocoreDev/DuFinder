import os

def obtener_extensiones_recursivas(carpeta):
    extensiones = set()

    # Iteramos sobre directorios y subdirectorios usando os.walk
    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            _, extension = os.path.splitext(archivo)
            extensiones.add(extension)

    return extensiones

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Llamamos a la función y obtenemos las extensiones
extensiones_en_carpeta = obtener_extensiones_recursivas(carpeta_a_analizar)

# Ruta del archivo de texto donde guardaremos las extensiones
archivo_salida = "extensiones_en_carpeta.txt"

# Escribimos las extensiones en el archivo de texto
with open(archivo_salida, "w") as archivo:
    archivo.write("Extensiones encontradas:\n")
    for extension in extensiones_en_carpeta:
        archivo.write(extension + "\n")

print(f"Las extensiones se han guardado en {archivo_salida}")
