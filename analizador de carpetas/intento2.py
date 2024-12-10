from pathlib import Path

def obtener_tamano_total_archivos(carpeta, extension_busqueda):
    tamano_total = 0

    # Utilizamos pathlib.Path para una manipulación más eficiente de las rutas
    carpeta_path = Path(carpeta)

    # Iteramos sobre los archivos de la carpeta y sus subcarpetas
    for archivo_path in carpeta_path.rglob(f"*.{extension_busqueda}"):
        tamano_total += archivo_path.stat().st_size

    return tamano_total

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Buscamos archivos DWG y obtenemos su tamaño total
extension_busqueda_dwg = "dwg"
tamano_total_dwg = obtener_tamano_total_archivos(carpeta_a_analizar, extension_busqueda_dwg)

print(f"Tamaño total de los archivos DWG en {carpeta_a_analizar}: {tamano_total_dwg} bytes")
