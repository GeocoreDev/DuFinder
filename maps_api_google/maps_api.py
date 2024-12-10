import urllib.parse
import urllib.request
import googlemaps
import json
import re
from pyproj import Proj, Transformer

from constants.constants import (
    ORIGIN_CRS,
    DESTINATION_CRS,
    MUNICIPALITY,
    DEPARTMENT
)

api_key_google = 'AIzaSyCvcI9PXHinU7C0mvbXD6i8W5k_EP7QSA8'

def gms_to_decimal(coordinate, direction):
    # Expresión regular para extraer grados, minutos y segundos
    patron = re.match(r"([NSEW])(\d+)°(\d+)'([\d.]+)\"", direction + coordinate)
    if not patron:
        raise ValueError(f"Formato inválido: {coordinate}")

    degrees = int(patron.group(2))
    minutes = int(patron.group(3))
    seconds = float(patron.group(4))

    # Convertir a decimal
    location = degrees + (minutes / 60) + (seconds / 3600)

    # Negar el valor si es S o W
    if direction in "SW":
        location *= -1

    return location

def transform_coordinates_north_west_lat_long(northing, westing):
    """
    Se encarga de transformar coordenadas de tipo 1039353.15 a latitud y longitud
    """
    print(type(northing), type(westing))
    transformer_main = Transformer.from_crs(ORIGIN_CRS, DESTINATION_CRS)

    latitud, longitud = transformer_main.transform(northing, westing)

    return latitud, longitud


def get_municipality_by_lat_long(latitude, longitude):
    """
    Obtiene el nombre del municipio utilizando la API de Google Maps.

    Args:
        latitud (float): Latitud de la coordenada.
        longitud (float): Longitud de la coordenada.

    Returns:
        str: Nombre del municipio si se encuentra, de lo contrario 'Municipio no encontrado'.
    """
    gmaps = googlemaps.Client(key=api_key_google)
    results = gmaps.reverse_geocode((latitude, longitude), language="es")
    if not results:
        return None

    data_municipality = {MUNICIPALITY: None, DEPARTMENT: None}
    municipality_types = {"locality", "administrative_area_level_2"}
    department_types = {"administrative_area_level_1"}

    # Recorrer componentes y buscar datos relevantes
    for component in results[0]["address_components"]:
        types_data = set(component["types"])
        if types_data & municipality_types:  # Buscar municipio
            data_municipality[MUNICIPALITY] = component["long_name"]
        if types_data & department_types:  # Buscar departamento
            data_municipality[DEPARTMENT] = component["long_name"]

        # Detener búsqueda si ambos valores están completos
        if all(data_municipality.values()):
            break

    # Retornar datos si se encontró el municipio
    return data_municipality if data_municipality[MUNICIPALITY] else None


def obtener_coordenadas_direccion(direccion):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    parametros = {
        'address': direccion,
        'key': api_key_google,
    }

    # Codificar los parámetros y construir la URL
    url = f"{endpoint}?{urllib.parse.urlencode(parametros)}"

    try:
        # Realizar la solicitud a la API de Google Maps
        respuesta = urllib.request.urlopen(url)
        datos = json.loads(respuesta.read().decode('utf-8'))

        # Verificar si la solicitud fue exitosa
        if datos['status'] == 'OK':
            ubicacion = datos['results'][0]['geometry']['location']
            latitud = ubicacion['lat']
            longitud = ubicacion['lng']
            return latitud, longitud
        else:
            print(f"No se pudo obtener las coordenadas. Estado: {datos['status']}")
            if 'error_message' in datos:
                print(f"Mensaje de error: {datos['error_message']}")
            return None
    except Exception as e:
        print(f"Error al realizar la solicitud: {e}")
        return None


if __name__ == "__main__":
    # Ingresa la dirección como argumento
    direccion = input("Ingresa la dirección: ")

    coordenadas = obtener_coordenadas_direccion(direccion)

    if coordenadas:
        print(f"Coordenadas de {direccion}: Latitud {coordenadas[0]}, Longitud {coordenadas[1]}")
