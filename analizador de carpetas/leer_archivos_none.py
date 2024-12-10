# Ruta del archivo de texto de entrada
ruta_archivo_entrada = r'C:\Script\analizador de carpetas\archivos_none.txt'

# Ruta del archivo de texto de salida
ruta_archivo_salida = 'cantidad_de_tipos_ordenados.txt'

def obtener_extensiones(archivo_entrada):
    try:
        with open(archivo_entrada, 'r') as file:
            lineas = file.readlines()

            # Obtener extensiones
            extensiones = [line.strip().split('.')[-1] for line in lineas]

            return extensiones

    except FileNotFoundError:
        print(f"El archivo {archivo_entrada} no fue encontrado.")
        return []

def guardar_cantidad_de_tipos(archivo_salida, extensiones):
    try:
        with open(archivo_salida, 'w') as file:
            # Crear un diccionario para almacenar la cantidad de cada extensión
            cantidad_tipos = {}

            # Contar la cantidad de cada extensión
            for extension in extensiones:
                cantidad_tipos[extension] = cantidad_tipos.get(extension, 0) + 1

            # Ordenar extensiones de mayor a menor cantidad
            extensiones_ordenadas = sorted(cantidad_tipos.items(), key=lambda x: x[1], reverse=True)

            # Escribir en el archivo de salida
            for extension, cantidad in extensiones_ordenadas:
                file.write(f"{extension}: {cantidad}\n")

        print(f"Se ha guardado la cantidad de tipos en {archivo_salida}")

    except Exception as e:
        print(f"Error al guardar la cantidad de tipos: {str(e)}")

if __name__ == "__main__":
    # Obtener extensiones del archivo de entrada
    extensiones_encontradas = obtener_extensiones(ruta_archivo_entrada)

    # Guardar la cantidad de tipos ordenados en el archivo de salida
    guardar_cantidad_de_tipos(ruta_archivo_salida, extensiones_encontradas)
