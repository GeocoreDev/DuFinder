import os
import json
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from stop_words import get_stop_words
import re
from unidecode import unidecode
from parsing import parsing, parse_with_timeout
import logging
import hashlib
from json import dumps


logging.basicConfig(filename='log.log', level=logging.ERROR)


es = Elasticsearch(['https://elastic:bujYRL5udHXfLlo@11a5f5082bb74949a62e4bc8f1950a72.us-east-2.aws.elastic-cloud.com'])
stop_words = get_stop_words('es')


def remove_empty_fields(array_of_dicts):
    # Iterate through each dictionary in the array
    for dictionary in array_of_dicts:
        # Use dictionary comprehension to filter out empty string values
        dictionary = {key: value for key, value in dictionary.items() if value != ""}
        # Update the dictionary in the array with non-empty string values
        array_of_dicts[array_of_dicts.index(dictionary)] = dictionary
    return array_of_dicts

def calcular_md5(texto):
    # Crea un objeto hash MD5
    md5_hash = hashlib.md5()

    # Actualiza el hash con el contenido del string
    md5_hash.update(texto.encode('utf-8'))

    # Obtiene el hash en formato hexadecimal
    resultado_md5 = md5_hash.hexdigest()

    return resultado_md5

def check_string(input_string):
    if (bool(re.match(r"^GYC \d{4}-\d{4} ", input_string))):
        return "A"
    if (bool(re.match(r"^GYC-\d{4}-\d{4} ", input_string))):
        return "B"
    return "False"

def index_objects_to_elasticsearch(objects):
    # Nombre del índice en el que se indexarán los objetos
    index_name = 'projects'

    # Lista para almacenar los datos formateados para el índice
    bulk_data = []

    # Formatear los objetos para la indexación en Elasticsearch
    for obj in objects:
        # Aquí deberías adaptar cómo transformas tus objetos a un formato adecuado para Elasticsearch
        # Por ejemplo, si tus objetos son diccionarios con datos, podrías hacer lo siguiente:
        data_to_index = {
            '_op_type': 'index',  # Usa 'index' para crear o reemplazar el documento
            '_index': index_name,
            'project': obj['project'],
            'doc': obj['doc'],
            '_id': calcular_md5(obj['doc']['meta']['file_path'])
        }
        bulk_data.append(data_to_index)

    # Utilizar la función bulk para indexar los datos en Elasticsearch
    try:
        # Uso de la función bulk para la indexación masiva
        success, _ = bulk(es, bulk_data, raise_on_error=True)
        logging.warning(f"{success} objetos indexados correctamente en Elasticsearch.")
    except Exception as e:
        logging.error(f"Error al indexar objetos en Elasticsearch: {e}")




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
        raise ValueError("Entrada no válida. Se espera un string o una lista de strings.")

def get_project_type(value):
    query = {
            "query": {
                "multi_match": {
                    "query": value,
                    "fields": ["codificacion^3", "detalle^2"],
                }
            }
        }

    resultado = es.search(index="project_types", body=query)

    if resultado['hits']['total']['value'] > 0:

        return resultado['hits']['hits'][0]
    else:
        return {}

#Get aprox Location
def get_location(search_array):
    counter = -1
    for  value in  search_array:
        counter = counter + 1
        if value in stop_words:
            continue
        if len(value) < 3:
            continue
        # Definir la consulta
        query = {
            "query": {
                "multi_match": {
                    "query": value,
                    "fields": ["Nombre Municipio^3", "Nombre Departamento^2"],
                    "type": "most_fields"
                }
            }
        }

        resultado = es.search(index="locations", body=query)

        if resultado['hits']['total']['value'] > 0:
            
            doc = resultado['hits']['hits'][0]['_source']
            if value in quitar_tildes(doc['Nombre Municipio'].lower()):
                names = doc['Nombre Municipio'].split()
                names = [x.lower() for x in names]
                names = [x for x in names if x not in stop_words]
                names = quitar_tildes(names)
                if len(names) == 1:
                    return resultado['hits']['hits'][0]['_source']
                if len(names) > 1:
                    try:
                        if names[names.index(value) + 1] == search_array[counter + 1]:
                            return resultado['hits']['hits'][0]['_source']
                    except IndexError:
                        pass 
                    try:
                        if names[names.index(value) - 1] == search_array[counter - 1]:
                            return resultado['hits']['hits'][0]['_source']
                    except IndexError:
                        pass 
            if value in quitar_tildes(doc['Nombre Departamento'].lower()):
                names = doc['Nombre Departamento'].split()
                names = [x.lower() for x in names]
                names = [x for x in names if x not in stop_words]
                names = quitar_tildes(names)
                if len(names) == 1:
                    return resultado['hits']['hits'][0]['_source']
                if len(names) > 1:
                    try:
                        if names[names.index(value) + 1] == search_array[counter + 1]:
                            return resultado['hits']['hits'][0]['_source']
                    except IndexError:
                        pass 
                    try:
                        if names[names.index(value) - 1] == search_array[counter - 1]:
                            return resultado['hits']['hits'][0]['_source']
                    except IndexError:
                        pass 
                        

        
    return {}
    

def get_client(pryname):
    return ""

def get_metadata(project_name, path, year, prtype):
    if prtype == "A":
        # Splitting the project name based on '-' to extract relevant metadata
        components = project_name.split('-')
        consecutive = components[1].split()[0]
        pryname = project_name.split(consecutive)[1]
        pryvalues = re.split(r'\s+|-', pryname.lower())

        location = get_location(pryvalues)

        if len(location) > 0:
            geolocation = {
                "lat": float(location['Latitud'].replace(',', '.')),
                "lon": float(location['Longitud'].replace(',', '.'))
            }
            municipio = location['Nombre Municipio'].capitalize()
            departamento = location['Nombre Departamento'].capitalize()

        # Extracting client, geolocation, project type from the project name
        client = " ".join(components[-1].split()[2:])

        # Hace falta el project Type
        myType = {
            "_score": 0
        }
        for value in  pryvalues:
            temp = get_project_type(value)
            if len(temp) == 0:
                continue
            if temp['_score'] > myType['_score']:
                myType = temp
                
        project_type = ""

        if myType['_score'] > 0:
            project_type = myType['_source']['codificacion']
            project_type_detail = myType['_source']['detalle']

        # project_type = components[-1].split()[1]
        
        # Extracting project date assuming it is the year from the folder name
        folder_year = int(year)
        project_date = datetime(folder_year, int(components[0].split()[1][:2]), 1).strftime('%Y-%m-%d')

        metadata = {
            key: value for key, value in {
                'consecutive': locals().get('consecutive', None),
                'client': locals().get('client', None),
                'location': locals().get('geolocation', None),
                'municipality': locals().get('municipio', None),
                'state': locals().get('departamento', None),
                'project_type': locals().get('project_type', None),
                'project_type_detail': locals().get('project_type_detail', None),
                'project_date': locals().get('project_date', None),
                'full_name': locals().get('pryname', None),
            }.items() if value is not None
        }

        return metadata

    if prtype == "B":
        # Splitting the project name based on '-' to extract relevant metadata
        components = project_name.split('-')
        consecutive = components[2].split()[0]
        if (" " in components[2]):
            pryname = components[2].split()[1]
        else: 
            pryname = ""

        pryvalues = re.split(r'\s+|-', pryname.lower())

        location = get_location(pryvalues)

        if len(location) > 0:
            geolocation = {
                "lat": float(location['Latitud'].replace(',', '.')),
                "lon": float(location['Longitud'].replace(',', '.'))
            }
            municipio = location['Nombre Municipio'].capitalize()
            departamento = location['Nombre Departamento'].capitalize()

        # Extracting client, geolocation, project type from the project name
        client = get_client(pryname)

        # Hace falta el project Type
        myType = {
            "_score": 0
        }

        for value in  pryvalues:
            temp = get_project_type(value)
            if len(temp) == 0:
                continue
            if temp['_score'] > myType['_score']:
                myType = temp
                
        project_type = ""

        if myType['_score'] > 0:
            project_type = myType['_source']['codificacion']
            project_type_detail = myType['_source']['detalle']

        # project_type = components[-1].split()[1]
        
        # Extracting project date assuming it is the year from the folder name
        folder_year = int(year)
        project_date = datetime(folder_year, int(components[1][1][:2]), 1).strftime('%Y-%m-%d')

        metadata = {
            key: value for key, value in {
                'consecutive': locals().get('consecutive', None),
                'client': locals().get('client', None),
                'location': locals().get('geolocation', None),
                'municipality': locals().get('municipio', None),
                'state': locals().get('departamento', None),
                'project_type': locals().get('project_type', None),
                'project_type_detail': locals().get('project_type_detail', None),
                'project_date': locals().get('project_date', None),
                'full_name': locals().get('pryname', None),
            }.items() if value is not None
        }

        # index_metadata_to_elasticsearch(metadata)

        print (metadata)
        print (components)
        print (project_name)
        print ("-------------")
        return metadata

def process_project(project_path, year):

    project_name = os.path.basename(project_path)
    checkProjec = check_string(project_name)
    if checkProjec == "False":
        logging.error(f'Error al procesar el proyecto: {project_path}')
        return
        
    if checkProjec == "A":
        metadata = get_metadata(project_name, project_path, year, "A")
    
    if checkProjec == "B":
        metadata = get_metadata(project_name, project_path, year, "B")

    project_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = str(os.path.join(root, file)).replace("\\\\","\\")
            file_extension = os.path.splitext(file_path)[1][1:]  # Obtiene la extensión del archivo
            
            print(file_path)
            result = parse_with_timeout(file_path, file_extension, 5)
            if "error" in result['data']:
                doc = {
                    "doc": {
                        "meta": {
                            "path" : file_path,
                        },
                        "status": "Error",
                        **result
                    }
                }
            else:
                doc = {
                    "doc": {
                        "meta": result['data']['metadata'],
                        "status": "Done",
                        "content": result['data']['text']
                    }
                }
            doc['doc']['meta']['file_path'] = file_path
            print(doc['doc']['meta'])
            print(doc['doc']['status'])

            project_files.append(doc)
            if file_extension.lower() in ['jpeg', 'jpg']:
                #Obtener geolocalizacion a paritir de imagenes
                pass
    for proj in project_files:
        proj['project'] = {}
        proj['project']['meta'] = metadata
    
    project_files = remove_empty_fields(project_files)
    index_objects_to_elasticsearch(project_files)

def process_year_directory(year_path, year):
    projects = os.listdir(year_path)
    for project in projects:
        project_path = os.path.join(year_path, project)
        if os.path.isdir(project_path):
            process_project(project_path, year)
            # try:
            #     logging.warning(f"Procesando proyecto {project_path}.")
            #     process_project(project_path, year)
            # except Exception as e:
            #     logging.error(f'Error al procesar el proyecto: {project_path} Error: {e}')

def iterate_years(main_directory, start_year):
    years = os.listdir(main_directory)
    for year in years:
        year_path = os.path.join(main_directory, year)
        if os.path.isdir(year_path) and year.isdigit() and int(year) >= start_year:
            print(year_path)
            process_year_directory(year_path, year)

if __name__ == "__main__":
    main_directory = 'D:\\'
    start_year = 2013  # Especifica aquí el año de inicio que desees
    iterate_years(main_directory, start_year)
