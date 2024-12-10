import os
import zipfile
from xml.etree import ElementTree as ET
from constants.constants import (
  LAT,
  LONG
)
from utils.utils import (
  is_colombian_coordinates
)

def extract_kml_from_kmz(kmz_path, output_folder="/tmp"):
    """Extraer el archivo .kml de un .kmz y devolver la ruta del .kml extraído."""
    try:
        with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
            # Buscar el archivo .kml dentro del .kmz
            for archivo in zip_ref.namelist():
                if archivo.endswith(".kml"):
                    # Extraer el archivo .kml
                    zip_ref.extract(archivo, output_folder)
                    return os.path.join(output_folder, archivo)
    except Exception as e:
        print(f"Error al extraer {kmz_path}: {e}")
    return None

def get_data_from_kml(kml_path):
    """Extraer información relevante de un archivo .kml."""
    try:
        tree = ET.parse(kml_path)
        root = tree.getroot()

        # Espacio de nombres de KML
        namespace = {"kml": "http://www.opengis.net/kml/2.2"}

        # Buscar nombres, descripciones y coordenadas
        informacion = []
        for placemark in root.findall(".//kml:Placemark", namespace):
            name = placemark.find("kml:name", namespace)
            description = placemark.find("kml:description", namespace)
            coordinates = placemark.find(".//kml:coordinates", namespace)

            informacion.append({
                "name": name.text if name is not None else "Sin nombre",
                "description": description.text if description is not None else "Sin descripción",
                "coordinates": coordinates.text.strip() if coordinates is not None else "Sin coordenadas"
            })

        return informacion
    except Exception as e:
        print(f"Error al procesar {kml_path}: {e}")
    return []


def process_files_kmz_extract_coordinate_main(files_kmz):

    for kmz_path in files_kmz:
      kml_path = extract_kml_from_kmz(kmz_path)

      if kml_path:
        information = get_data_from_kml(kml_path)
        for item in information:
          latitude = item['coordinates'].split(",")[1].split(",")[0]
          longitude = item['coordinates'].split(",")[0]
          if is_colombian_coordinates(latitude, longitude):
            return {LAT: latitude, LONG: longitude}

    return None