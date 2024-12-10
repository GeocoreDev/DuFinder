import os
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# from stop_words import get_stop_words
import re
from unidecode import unidecode
from parsing import parsing, parse_with_timeout
import logging
import hashlib
from json import dumps
from utils.utils import (
    normalize_string,
    get_content_pdf_file
)
from utils.kmz_actions import (
    process_files_kmz_extract_coordinate_main
)
from maps_api_google.maps_api import (
    gms_to_decimal,
    transform_coordinates_north_west_lat_long,
    get_municipality_by_lat_long
)
from constants.constants import (
    PRODUCT_TYPES,
    CODES,
    DETAIL,
    SPECIFIC_DETAIL,
    PRODUCT_TYPE,
    CLIENT,
    PES,
    PRODUCT_TYPE_DETAIL,
    REPORT,
    KEY_WORDS_FOLDERS_DRILLING_LOGS,
    UBICATION_WORD,
    SECTOR_WORD,
    LAT,
    LONG,
    MUNICIPALITY,
    DEPARTMENT
)


logging.basicConfig(filename="log.log", level=logging.ERROR)

client = Elasticsearch(
  "https://c8f2e7b9937245778877ce752ca3f985.us-central1.gcp.cloud.es.io:443",
  api_key="ZFJ3dFZKTUJKdzUyTmx3dzFRYkk6Zm9Bc2lRMWRSSmF6VVkwNjk2S0FHUQ=="
)


def remove_empty_fields(array_de_dicts):
    for diccionario in array_de_dicts:
        # Utilizamos list(diccionario) para iterar sobre una copia de las claves
        # ya que no se pueden modificar las claves de un diccionario mientras se itera sobre ellas
        for clave in list(diccionario):
            if isinstance(diccionario[clave], dict):
                # Si el valor es otro diccionario, llamamos recursivamente a la función
                remove_empty_fields([diccionario[clave]])
                if not diccionario[
                    clave
                ]:  # Eliminamos el campo si el diccionario interno quedó vacío
                    del diccionario[clave]
            elif diccionario[clave] == "":
                # Eliminamos el campo si el valor es una cadena vacía
                del diccionario[clave]


def calcular_md5(texto):
    # Crea un objeto hash MD5
    md5_hash = hashlib.md5()

    # Actualiza el hash con el contenido del string
    md5_hash.update(texto.encode("utf-8"))

    # Obtiene el hash en formato hexadecimal
    resultado_md5 = md5_hash.hexdigest()

    return resultado_md5


def check_project_folder_name(input_string):
    match = re.match(r"^GYC( |-)\d{4}-\d{4} ", input_string)
    if match:
        return "A" if match.group(1) == " " else "B"
    return "False"


def is_project_processed(project_id):
    # Verificar si el proyecto ya ha sido procesado anteriormente
    # Puedes implementar la lógica de verificación según tus necesidades
    processed_projects_file = "processed_projects.json"
    try:
        with open(processed_projects_file, "r") as f:
            processed_projects = json.load(f)
            return project_id in processed_projects
    except FileNotFoundError:
        return False


def mark_project_as_processed(project_id):
    # Marcar un proyecto como procesado
    processed_projects_file = "processed_projects.json"
    try:
        with open(processed_projects_file, "r") as f:
            processed_projects = json.load(f)
    except FileNotFoundError:
        processed_projects = []

    processed_projects.append(project_id)

    with open(processed_projects_file, "w") as f:
        json.dump(processed_projects, f)


def index_objects_to_elasticsearch(objects):
    # Nombre del índice en el que se indexarán los objetos
    index_name = "projects"

    # Lista para almacenar los datos formateados para el índice
    bulk_data = []

    # Formatear los objetos para la indexación en Elasticsearch
    for obj in objects:
        # Aquí deberías adaptar cómo transformas tus objetos a un formato adecuado para Elasticsearch
        # Por ejemplo, si tus objetos son diccionarios con datos, podrías hacer lo siguiente:
        data_to_index = {
            "_op_type": "index",  # Usa 'index' para crear o reemplazar el documento
            "_index": index_name,
            "project": obj["project"],
            "doc": obj["doc"],
            "_id": calcular_md5(obj["doc"]["meta"]["file_path"]),
        }
        bulk_data.append(data_to_index)

    # Utilizar la función bulk para indexar los datos en Elasticsearch
    # success, _ = bulk(es, bulk_data, raise_on_error=True)
    try:
        # Uso de la función bulk para la indexación masiva
        success, _ = bulk(es, bulk_data, raise_on_error=True)
        logging.warning(f"{success} objetos indexados correctamente en Elasticsearch.")

        return success
    except Exception as e:
        logging.error(f"Error al indexar objetos en Elasticsearch: {e} ")
        return 0


def remover_comas(array):
    return [elemento.replace(",", "") for elemento in array]


def quitar_tildes(texto):
    # Si es un string, quitar tildes directamente
    if isinstance(texto, str):
        return unidecode(texto)
    # Si es una lista de strings, quitar tildes de cada elemento
    elif isinstance(texto, list):
        resultado = []
        for palabra in texto:
            palabra_sin_tildes = unidecode(palabra)
            resultado.append(palabra_sin_tildes)
        return resultado
    else:
        raise ValueError(
            "Entrada no válida. Se espera un string o una lista de strings."
        )


def get_project_type_index_es(value):
    query = {
        "query": {
            "multi_match": {
                "query": value,
                "fields": ["codificacion^3", "detalle^2"],
            }
        }
    }

    resultado = es.search(index="project_types", body=query)

    if resultado["hits"]["total"]["value"] > 0:

        return resultado["hits"]["hits"][0]
    else:
        return {}


# def get_location(search_array):
#     counter = -1
#     print(search_array)
#     for value in search_array:
#         counter = counter + 1
#         # if value in stop_words or len(value) < 3:
#         #     continue
#         # Definir la consulta
#         query = {
#             "query": {
#                 "multi_match": {
#                     "query": value,
#                     "fields": ["Nombre Municipio^3", "Nombre Departamento^2"],
#                     "type": "most_fields",
#                 }
#             }
#         }

#         resultado = es.search(index="locations", body=query)

#         if resultado["hits"]["total"]["value"] == 1:
#             return resultado["hits"]["hits"][0]["_source"]

#         if resultado["hits"]["total"]["value"] > 1:

#             doc = resultado["hits"]["hits"][0]["_source"]

#             if value in quitar_tildes(doc["Nombre Municipio"].lower()):
#                 names = doc["Nombre Municipio"].split()
#                 names = [x.lower() for x in names]
#                 # names = [x for x in names if x not in stop_words]
#                 names = quitar_tildes(names)
#                 names = remover_comas(names)

#                 if len(names) == 1:
#                     return resultado["hits"]["hits"][0]["_source"]
#                 if len(names) > 1:
#                     try:
#                         if names[names.index(value) + 1] == search_array[counter + 1]:
#                             return resultado["hits"]["hits"][0]["_source"]
#                     except IndexError:
#                         pass
#                     try:
#                         if names[names.index(value) - 1] == search_array[counter - 1]:
#                             return resultado["hits"]["hits"][0]["_source"]
#                     except IndexError:
#                         pass

#             if value in quitar_tildes(doc["Nombre Departamento"].lower()):
#                 names = doc["Nombre Departamento"].split()
#                 names = [x.lower() for x in names]
#                 # names = [x for x in names if x not in stop_words]
#                 names = quitar_tildes(names)
#                 names = remover_comas(names)
#                 if len(names) == 1:
#                     return resultado["hits"]["hits"][0]["_source"]
#                 if len(names) > 1:
#                     try:
#                         if names[names.index(value) + 1] == search_array[counter + 1]:
#                             return resultado["hits"]["hits"][0]["_source"]
#                     except IndexError:
#                         pass
#                     try:
#                         if names[names.index(value) - 1] == search_array[counter - 1]:
#                             return resultado["hits"]["hits"][0]["_source"]
#                     except IndexError:
#                         pass

#     return {}

def convert_text_to_coordinates_structure_north_west(text_coordinates):
    """
    Convierte el texto a la estructura general de coordenadas
    """

    text_coordinates_without_spaces = text_coordinates.replace(" ", "")

    if "N=" in text_coordinates_without_spaces or "N:" in text_coordinates_without_spaces or "°" in text_coordinates_without_spaces:
        # print(">>>>>>>>>>>>>>>>>>>>>>>El texto contiene coordenadas<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        if "N:" in text_coordinates_without_spaces:
            northing = re.split(r'\s*\n\s*', text_coordinates_without_spaces.split("N:")[1], maxsplit=1)[0]
        if "N=" in text_coordinates_without_spaces:
            northing = re.split(r'\s*\n\s*', text_coordinates_without_spaces.split("N=")[1], maxsplit=1)[0].split(" ")[0].split("E")[0].split("W")[0]

        if "E:" in text_coordinates_without_spaces:
            westing = re.split(r'\s*\n\s*', text_coordinates_without_spaces.split("E:")[1], maxsplit=1)[0]
        if "E=" in text_coordinates_without_spaces:
            westing = re.split(r'\s*\n\s*', text_coordinates_without_spaces.split("E=")[1], maxsplit=1)[0]
        if "W:" in text_coordinates_without_spaces:
            westing = re.split(r'\s*\n\s*', text_coordinates_without_spaces.split("W:")[1], maxsplit=1)[0]
        if "W=" in text_coordinates_without_spaces:
            westing = re.split(r'\s*\n\s*', text_coordinates_without_spaces.split("W=")[1], maxsplit=1)[0]
        
        if northing:
            northing = northing.split(" ")[0].split("E")[0].split("W")[0]
        if westing:
            westing = westing.split(" ")[0].split("N")[0]

        print(".....................Respuesta............", northing, westing)
        return northing, westing

    return None





def get_location_main(path_project):
    latitude, longitude = None, None
    for route, folders, files in os.walk(path_project):
        for folder in folders:
            if any(word_main.upper() in normalize_string(folder).upper() for word_main in KEY_WORDS_FOLDERS_DRILLING_LOGS):
                complete_route = os.path.join(route, folder)
                # print(f"Carpeta encontrada: {folder}")
                pdfs = [file for file in os.listdir(complete_route) if file.lower().endswith(".pdf")]
                # print(f"Archivos PDF encontrados en {folder}: {pdfs}")
                for pdf_file in pdfs:
                    route_pdf = os.path.join(complete_route, pdf_file)
                    content_pdf = get_content_pdf_file(route_pdf)
                    if isinstance(content_pdf, str):
                        text_pdf_upper = content_pdf.upper()
                        if UBICATION_WORD in text_pdf_upper:
                            # print("******************")
                            location_main = re.split(r'\s*\n\s*', text_pdf_upper.split(UBICATION_WORD)[1], maxsplit=1)[0].split("COTA")[0]
                            # print(f"Existe la palabra ubicacion: {location_main}")
                            text_to_coordinates = convert_text_to_coordinates_structure_north_west(location_main)
                            
                            if text_to_coordinates is not None:
                                north_found = text_to_coordinates[0]
                                west_found = text_to_coordinates[1]
                                print("Text to coordinates", text_to_coordinates[0], text_to_coordinates[1])
                                if "°" in north_found:
                                    latitude = gms_to_decimal(north_found, "N")
                                    longitude = gms_to_decimal(west_found, "W")
                                else :
                                    latitude, longitude = transform_coordinates_north_west_lat_long(float(north_found), float(west_found))
                                print("Ubicaciones a latitud y longitud: ", latitude, longitude)
                                return {LAT: latitude, LONG:longitude}
            
        if latitude is None:
            files_kmz = []
            for file in files:
                if file.lower().endswith(".kmz"):
                    files_kmz.append(os.path.join(route, file))
            
            if len(files_kmz) > 0:
                data_files_kmz = process_files_kmz_extract_coordinate_main(files_kmz)
                if data_files_kmz is not None:
                    return {LAT: data_files_kmz[LAT], LONG: data_files_kmz[LONG]}

    return None


def get_product_type_by_folder_name(pryvalues):
    product_type = None
    for word_value in pryvalues:
        product_type = next(
            (
                product_t
                for product_t in PRODUCT_TYPES
                if normalize_string(word_value.replace(" ", "")).upper()
                in product_t[CODES]
            ),
            None,
        )
        if product_type:
            return product_type
    return product_type


def get_product_type_detail_by_folder_name(project_type, project_name):
    product_detail = None
    if len(project_type[SPECIFIC_DETAIL]) == 1:
        product_detail = project_type[SPECIFIC_DETAIL][0]
    else:
        for product_det in project_type[SPECIFIC_DETAIL]:
            product_detail = (
                product_det
                if normalize_string(product_det)
                in normalize_string(project_name)
                or normalize_string(product_det[:-1])
                in normalize_string(project_name)
                else None
            )
            if product_detail is not None:
                product_detail = product_det
                return product_detail
    return product_detail


def read_file_finds_client(path_file_main):
    """
        Metodo encargado de encontrar el cliente en los archivos
    """
    client = ""
    text_page = get_content_pdf_file(path_file_main)
    text_page_upper = text_page.upper() if isinstance(text_page, str) else ""
    if "SEÑOR" in text_page_upper:
        lines = text_page_upper.split("SEÑOR")[1].split("\n")
        for index, line in enumerate(lines):
            if index > 0 and ":" not in line and "GYC" not in line and "GEOTECNIA" not in line and line != "\n":
                if "CIUDAD" not in line:
                    return line
                else : 
                    return ""

    return client

def read_file_finds_product_type_detail_from_pes(path_file_main, data_response):
    """
        Extrae el tipo del producto del archivo PES
    """
    try:
        text_page = get_content_pdf_file(path_file_main)
        text_page_upper = text_page.upper() if isinstance(text_page, str) else ""
        if "REF." in normalize_string(text_page_upper):
            text_ref = text_page_upper.split("REF.")[1].split("ESTIMAD")[0]
            if data_response[PRODUCT_TYPE] is None:
                words_ref = text_ref.split(" ")
                product_type = None
                for word in words_ref:
                    print("Worddd", word, type(word))
                    product_type = next(
                        (
                            product_t
                            for product_t in PRODUCT_TYPES
                            if normalize_string(word.replace(" ", ""))
                            in product_t[CODES]
                        ),
                        None,
                    )
                
                data_response[PRODUCT_TYPE] = product_type
            if data_response[PRODUCT_TYPE] is not None and data_response[PRODUCT_TYPE_DETAIL] is None:
                options_data_detail = [
                    normalize_string(option)
                    for option in data_response[PRODUCT_TYPE][SPECIFIC_DETAIL]
                ]

                for option_detail in options_data_detail:
                    if option_detail in normalize_string(text_ref) or option_detail[:-1] in normalize_string(text_ref):
                        data_response[PRODUCT_TYPE_DETAIL] = option_detail

        return data_response

    except Exception as e:
        print(f"Error al procesar para tipo de producto {path_file_main}: {e}")
        return None


def read_file_finds_product_type_detail_from_report(path_file_main, data_response):
    """
        Extrae el tipo del producto del archivo PES
    """
    try:
        text_page = get_content_pdf_file(path_file_main)
        text_page_upper = text_page.upper() if isinstance(text_page, str) else ""

        if "SEÑOR" in text_page_upper and data_response[CLIENT] != "":
            text_page_upper = text_page_upper.replace("SEÑORES", "SEÑOR")
            data_response[CLIENT] = text_page_upper.split("SEÑOR")[1].split("ATT")[0]
        text_page_upper = text_page_upper.replace("REF:", "REF.")
        if "REF." in text_page_upper:
            text_page_upper = text_page_upper.replace("RESPETADO", "ESTIMADO")
            text_ref = text_page_upper.split("REF.")[1].split("ESTIMAD")[0]
            if data_response[PRODUCT_TYPE] is None:
                words_ref = text_ref.split(" ")
                product_type = None
                for word in words_ref:
                    product_type = next(
                        (
                            product_t
                            for product_t in PRODUCT_TYPES
                            if normalize_string(word.replace(" ", ""))
                            in product_t[CODES]
                        ),
                        None,
                    )
                
                data_response[PRODUCT_TYPE] = product_type
            if data_response[PRODUCT_TYPE] is not None and data_response[PRODUCT_TYPE_DETAIL] is None:
                options_data_detail = [
                    normalize_string(option)
                    for option in data_response[PRODUCT_TYPE][SPECIFIC_DETAIL]
                ]

                for option_detail in options_data_detail:
                    if option_detail in normalize_string(text_ref) or option_detail[:-1] in normalize_string(text_ref):
                        # data_response[PRODUCT_TYPE_DETAIL] = option_detail.upper()
                        print(f"option detail: {option_detail}")
                        data_response[PRODUCT_TYPE_DETAIL] = option_detail.upper()

        return data_response

    except Exception as e:
        print(f"Error al procesar para tipo de producto {path_file_main}: {e}")
        return None

def process_file(file_path, file, data_response):

    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".pdf":
      client = read_file_finds_client(file_path)
      if client and data_response[CLIENT] == "":
        data_response[CLIENT] = client

      if data_response[PRODUCT_TYPE_DETAIL] is None:
        if PES in file.upper():
            data_response = read_file_finds_product_type_detail_from_pes(file_path, data_response)
        if REPORT in file.upper():
            data_response = read_file_finds_product_type_detail_from_report(file_path, data_response)
    return data_response

def get_client_product_detail_from_files(
    main_route_project, project_name, project_name_values
):  
    project_type = get_product_type_by_folder_name(project_name_values)
    project_type_detail = (
        get_product_type_detail_by_folder_name(project_type, project_name)
        if project_type is not None
        else None
    )
    data_response = {CLIENT: "", PRODUCT_TYPE: project_type, PRODUCT_TYPE_DETAIL: project_type_detail}

    for current_folder, _, files in os.walk(main_route_project):
        for file in files:
            file_path = os.path.join(current_folder, file)
            process_file(file_path, file, data_response)

            if data_response[CLIENT] and data_response[PRODUCT_TYPE] and data_response[PRODUCT_TYPE_DETAIL]:
                return data_response

    return data_response




def get_metadata_project(project_name, path, year, project_type, project_id):
    components = project_name.split("-")

    # Determinar gyc_code y pryname según el prtype
    if project_type == "A":
        gyc_code = components[1].split()[0]
        project_name = project_name.split(gyc_code)[1]
    elif project_type == "B":
        gyc_code = components[2].split()[0]
        project_name = components[2].split()[1] if " " in components[2] else ""

    # Pryvalues y ubicación
    project_name_values = re.split(r"\s+|-", project_name.lower())
    print(
        f"project_name {project_name} -------"
    )
    # location = get_location(pryvalues)
    location = get_location_main(path)

    # Geolocalización
    geolocation, municipality, department = None, "", ""
    if location is not None:
        geolocation = {
            LAT: float(location[LAT]),
            LONG: float(location[LONG]),
        }
        municipality_data = get_municipality_by_lat_long(geolocation[LAT], geolocation[LONG])

        municipality = municipality_data[MUNICIPALITY]
        department = municipality_data[DEPARTMENT]

    # Cliente y tipo de proyecto
    data_client_product_detail = get_client_product_detail_from_files(path, project_name, project_name_values)

    # # Fecha del proyecto
    folder_year = int(year)
    month = (
        int(components[0].split()[1][:2])
        if project_type == "A"
        else int(components[1][1][:2])
    )
    project_date = datetime(folder_year, month, 1).strftime("%Y-%m-%d")
    # Metadata
    metadata = {
        "project_id": project_id,
        "gyc_code": gyc_code,
        "client": data_client_product_detail[CLIENT],
        "geolocation": geolocation,
        "municipality": municipality,
        "department": department,
        "project_type": data_client_product_detail[PRODUCT_TYPE] if data_client_product_detail[PRODUCT_TYPE] is not None else "",
        "project_type_detail": data_client_product_detail[PRODUCT_TYPE_DETAIL] if data_client_product_detail[PRODUCT_TYPE_DETAIL] is not None else "",
        "project_date": project_date,
        "project_path": path,
        "full_name": project_name[1:] if project_name.startswith(" ") else project_name,
    }
    return metadata


def is_in_september(date_str):
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Check if the month component is equal to 9 (September)
    return date_obj.month == 9


def process_project(project_path, year):

    project_name = os.path.basename(project_path)
    check_project = check_project_folder_name(project_name)
    project_id = calcular_md5(project_name)  # Utilizar una función única para identificar el proyecto
    # project_id = project_path

    if check_project == "False":
        print(check_project)
        logging.error(f"Error al procesar el proyecto: {project_path}")
        return

    metadata = get_metadata_project(project_name, project_path, year, check_project, project_id)
    
    print("Metadata project", metadata)
    project_files = []
    # for root, dirs, files in os.walk(project_path):
    #     for file in files:
    #         file_path = str(os.path.join(root, file)).replace("\\\\","\\")
    #         file_extension = os.path.splitext(file_path)[1][1:]  # Obtiene la extensión del archivo

    #         #Falta DWG y dxf
    #         if not (file_extension in ['jpeg', 'jpg', 'png', 'gif' ,'pdf', 'xlsx', 'xls', 'xlsm', 'xlsb', 'xltx', 'xlt', 'txt', 'out', 'ipt', 'plt', 'sli', 'csv', 'docx', 'docm', 'dotx', 'dotm', 'doc', 'bmp','dxf']):
    #             continue
    #         print(file_path)
    #         result = parse_with_timeout(file_path, file_extension, 15)
    #         if 'data' in result:
    #             if "error" in result['data']:
    #                 doc = {
    #                     "doc": {
    #                         "meta": {
    #                             "path" : file_path,
    #                         },
    #                         "status": "Error",
    #                         **result
    #                     }
    #                 }
    #             else:
    #                 doc = {
    #                     "doc": {
    #                         "meta": result['data']['metadata'],
    #                         "status": "Done",
    #                         "parsed": 1,
    #                         "content": result['data']['text']
    #                     }
    #                 }
    #         else:
    #             doc = {
    #                     "doc": {
    #                         "meta": {
    #                             "path" : file_path,
    #                         },
    #                         "status": "Error before parsing",
    #                     }
    #                 }
    #         doc['doc']['meta']['file_path'] = file_path
    #         print(doc['doc']['meta'])
    #         print(doc['doc']['status'])
    #         doc['doc']['file_extension'] = file_extension.lower()
    #         project_files.append(doc)

    #         if file_extension.lower() in ['jpeg', 'jpg'] and 'GPSInfo' in doc['doc']['meta']:
    #             gps_info = doc['doc']['meta']['GPSInfo']

    #             if 'Latitude' in gps_info and 'Longitude' in gps_info:
    #                 geolocation = {
    #                     "lat": gps_info['Latitude'],
    #                     "lon": gps_info['Longitude']
    #                 }
    #                 metadata['location'] = geolocation

    #         if not "project_type" in metadata and doc['doc']['status'] == "Done" and file_extension.lower() in ['doc', 'docx',]:
    #             count = 0
    #             for word in  doc['doc']['content'].split():
    #                 count += 1
    #                 if (count >= 50):
    #                     break
    #                 resp = get_project_type(word)

    #                 if len(resp) == 0:
    #                     continue
    #                 if resp['_score'] > 0:
    #                     metadata["project_type"] = resp['_source']['codificacion']
    #                     metadata["project_type_detail"] = resp['_source']['detalle']
    #                     break

    #         if not "location" in metadata and doc['doc']['status'] == "Done" and file_extension.lower() in ['doc', 'docx']:
    #             doc_to_search = doc['doc']['content'].split()

    #             location = get_location(doc_to_search)
    #             if len(location) > 0:
    #                 geolocation = {
    #                     "lat": float(location['Latitud'].replace(',', '.')),
    #                     "lon": float(location['Longitud'].replace(',', '.'))
    #                 }
    #                 metadata['location'] = geolocation
    #                 metadata['municipality'] = location['Nombre Municipio'].capitalize()
    #                 metadata['state'] = location['Nombre Departamento'].capitalize()

    #             print("<----------------------->")
    #             print(doc_to_search)
    #             print (metadata)
    #         if file_extension.lower() in ['jpeg', 'jpg']:
    #             #Obtener geolocalizacion a paritir de imagenes
    #             pass

    # for proj in project_files:
    #     proj['project'] = {}
    #     proj['project']['meta'] = metadata
    # remove_empty_fields(project_files)
    # docs_count = index_objects_to_elasticsearch(project_files)

    # if docs_count > 0:
    #     mark_project_as_processed(project_id)


def process_year_directory(year_path, year):
    projects = os.listdir(year_path)
    for project in projects:
        project_path = os.path.join(year_path, project)
        if os.path.isdir(project_path):
            # process_project(project_path, year)
            try:
                logging.warning(f"Procesando proyecto {project_path}.")
                process_project(project_path, year)
            except Exception as e:
                logging.error(
                    f"Error al procesar el proyecto: {project_path} Error: {e}"
                )


def iterate_years(main_directory, start_year):
    # client.info()
    years = os.listdir(main_directory)
    for year in years:
        year_path = os.path.join(main_directory, year)
        if os.path.isdir(year_path) and year.isdigit() and int(year) >= start_year:
            print(year_path)
            process_year_directory(year_path, year)


def read_start_year_from_file(file_path):
    file = open(file_path, "r")
    start_year = int(file.readline().strip())
    file.close()
    return start_year


if __name__ == "__main__":
    main_directory = "/home/user/Documentos/GYC/Proyectos"
    config_file_path = "config.txt"  # Reemplaza 'ruta_al_archivo' con la ruta real
    start_year = read_start_year_from_file(config_file_path)
    iterate_years(main_directory, start_year)
