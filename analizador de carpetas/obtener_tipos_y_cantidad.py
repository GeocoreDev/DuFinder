import os
import mimetypes

def obtener_tipos_de_archivo_y_cantidad(carpeta):
    tipos_de_archivo_contador = {}

    # Iteramos sobre directorios y subdirectorios usando os.walk
    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(directorio_actual, archivo)
            tipo_de_archivo, _ = mimetypes.guess_type(ruta_completa)
            
            # Incrementar el contador para el tipo de archivo
            tipos_de_archivo_contador[tipo_de_archivo] = tipos_de_archivo_contador.get(tipo_de_archivo, 0) + 1

    return tipos_de_archivo_contador

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Llamamos a la función y obtenemos los tipos de archivo y sus cantidades
tipos_de_archivo_y_cantidades = obtener_tipos_de_archivo_y_cantidad(carpeta_a_analizar)

# Ordenamos los tipos de archivo de mayor a menor cantidad
tipos_de_archivo_ordenados = sorted(tipos_de_archivo_y_cantidades.items(), key=lambda x: x[1], reverse=True)

# Ruta del archivo de texto donde guardaremos los tipos de archivo y cantidades ordenados
archivo_salida = "tipos_de_archivo_y_cantidades_ordenados.txt"

# Escribimos los tipos de archivo y cantidades ordenados en el archivo de texto
with open(archivo_salida, "w") as archivo:
    archivo.write("Tipos de archivo y cantidades encontradas (ordenados de mayor a menor):\n")
    for tipo_de_archivo, cantidad in tipos_de_archivo_ordenados:
        archivo.write(f"{tipo_de_archivo}: {cantidad} archivos\n")

print(f"Los tipos de archivo y sus cantidades ordenados se han guardado en {archivo_salida}")
