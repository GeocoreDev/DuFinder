import os
import mimetypes

def obtener_tipos_de_archivo_y_cantidad(carpeta):
    tipos_de_archivo_contador = {}
    archivos_con_tipo_none = []

    # Iteramos sobre directorios y subdirectorios usando os.walk
    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(directorio_actual, archivo)
            tipo_de_archivo, _ = mimetypes.guess_type(ruta_completa)

            # Incrementar el contador para el tipo de archivo
            tipos_de_archivo_contador[tipo_de_archivo] = tipos_de_archivo_contador.get(tipo_de_archivo, 0) + 1

            # Almacenar las rutas de los archivos con tipo None
            if tipo_de_archivo is None:
                archivos_con_tipo_none.append(ruta_completa)

    return tipos_de_archivo_contador, archivos_con_tipo_none

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Llamamos a la función y obtenemos los tipos de archivo y sus cantidades, así como las rutas de archivos con tipo None
tipos_de_archivo_y_cantidades, archivos_con_tipo_none = obtener_tipos_de_archivo_y_cantidad(carpeta_a_analizar)

# Ordenamos los tipos de archivo de mayor a menor cantidad
tipos_de_archivo_ordenados = sorted(tipos_de_archivo_y_cantidades.items(), key=lambda x: x[1], reverse=True)

# Ruta del archivo de texto donde guardaremos los tipos de archivo y cantidades ordenados
archivo_salida = "tipos_de_archivo_y_cantidades_ordenados.txt"

# Ruta del archivo de texto donde guardaremos las rutas de archivos con tipo None
archivo_archivos_none = "archivos_none.txt"

# Escribimos los tipos de archivo y cantidades ordenados en el archivo de texto
with open(archivo_salida, "w") as archivo:
    archivo.write("Tipos de archivo y cantidades encontradas (ordenados de mayor a menor):\n")
    for tipo_de_archivo, cantidad in tipos_de_archivo_ordenados:
        archivo.write(f"{tipo_de_archivo}: {cantidad} archivos\n")

# Escribimos las rutas de archivos con tipo None en el archivo de texto
with open(archivo_archivos_none, "w") as archivo_none:
    archivo_none.write("Rutas de archivos con tipo None:\n")
    for ruta in archivos_con_tipo_none:
        archivo_none.write(f"{ruta}\n")

print(f"Los tipos de archivo y sus cantidades ordenados se han guardado en {archivo_salida}")
print(f"Las rutas de archivos con tipo None se han guardado en {archivo_archivos_none}")
