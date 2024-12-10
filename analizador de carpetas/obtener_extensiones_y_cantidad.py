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

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Llamamos a la función y obtenemos las extensiones y sus cantidades
extensiones_y_cantidades = obtener_extensiones_y_cantidad(carpeta_a_analizar)

# Ordenamos las extensiones de mayor a menor cantidad
extensiones_ordenadas = sorted(extensiones_y_cantidades.items(), key=lambda x: x[1], reverse=True)

# Ruta del archivo de texto donde guardaremos las extensiones y cantidades ordenadas
archivo_salida = "extensiones_y_cantidades_ordenadas.txt"

# Escribimos las extensiones y cantidades ordenadas en el archivo de texto
with open(archivo_salida, "w") as archivo:
    archivo.write("Extensiones y cantidades encontradas (ordenadas de mayor a menor):\n")
    for extension, cantidad in extensiones_ordenadas:
        archivo.write(f"{extension}: {cantidad} archivos\n")

print(f"Las extensiones y sus cantidades ordenadas se han guardado en {archivo_salida}")
