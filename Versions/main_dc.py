import os
from datetime import datetime
import fitz
import argparse
import json

GYC = "GYC"
PROJECT_PATH = "project_path"
CODE = "code"
CODES = "codes"
DATE = "date"
CLIENT = "client"
PRODUCT_TYPE = "product_type"
DESCRIPTION = "description"
LOCATION = "location"

SPECIFIC_DETAIL = "spec_detail"
LIST_DETAILS = "list_details"
SPACE = " "
POINT = "."
MIDDLE_DASH = " - "
PES = "PES"

DETAIL = "detail"
PROJECT_TYPES = [
  {CODES: ["ES"], DETAIL: "Estudio de Suelos", SPECIFIC_DETAIL: ["Edificios", "Casas", "Bodegas", "Subestaciones", "Tuberías", "Líneas de Conducción", "Validaciones", "Actualizaciones de Estados de Suelos"]},
  {CODES: ["DP"], DETAIL: "Diseño de Pavimentos", SPECIFIC_DETAIL: ["Índice de Estado", "Auscultación"]},
  {CODES: ["EG"], DETAIL: "Estudio Geotécnico", SPECIFIC_DETAIL: ["Puentes", "Viaductos", "Intersecciones", "Cortes", "Muros", "Zodmes", "Botaderos", "Box Coulvert", "Revisión de Estudios y Diseños de Geología y Geotecnia", "Concepto Técnico", "Línea Sísmica"]},
  {CODES: ["EE"], DETAIL: "Estudio de Estabilidad", SPECIFIC_DETAIL: ["Sitios Inestables", "Concepto", "Actualización"]},
  {CODES: ["FWD"], DETAIL: "Ensayo de Deflectometria", SPECIFIC_DETAIL: ["Ensayo de Deflectometria"]},
  {CODES: ["PCI"], DETAIL: "Pavement condition index", SPECIFIC_DETAIL: ["Pavement condition index", "Indice de condición del pavimento"]},
  {CODES: ["INST", "IN"], DETAIL: "Instrumentación", SPECIFIC_DETAIL: ["Instrumentación", "Campañas de Lectura"]},
  {CODES: ["PERF"], DETAIL: "Perforaciones", SPECIFIC_DETAIL: ["Perforaciones", "Ensayos de Laboratorio"]},
  {CODES: ["PIT"], DETAIL: "Prueba de Integridad de Pilotes", SPECIFIC_DETAIL: ["Prueba de Integridad de Pilotes", "Prueba de Carga Estática"] },
  {CODES: ["ERM"], DETAIL: "Estudio de Remoción en Masa", SPECIFIC_DETAIL: ["Estudio de Riesgo Geológico", "Análisis de Riesgos"]},
  {CODES: ["ACOMP"], DETAIL: "Acompañamiento", SPECIFIC_DETAIL: ["Acompañamiento"]},
  {CODES: ["ERL"], DETAIL: "Estudio de respuesta local", SPECIFIC_DETAIL: ["Estudio de respuesta local"]},
  {CODES: ["EYD"], DETAIL: "Estudio y diseños integrales", SPECIFIC_DETAIL: ["Estudio y diseños integrales"]},
  {CODES: ["LAB"], DETAIL: "Ensayo de laboratorio", SPECIFIC_DETAIL: ["Ensayo de laboratorio"]}
]


def obtain_gyc_code(folder_gyc):
  """
    Metodo encargado de extraer el codio gyc del proyecto
  """
  folder_gyc_without_spaces = folder_gyc.replace(" ", "")
  return folder_gyc_without_spaces.split("GYC")[1][:9]


def read_file_finds_client(path_file_main):
  """
    Metodo encargado de encontrar el cliente en los archivos
  """
  client = ""
  try:
    with fitz.open(path_file_main) as pdf_doc:
      page = pdf_doc[0]
      text_page = page.get_text()
      text_page_upper = text_page.upper()
      if "SEÑOR" in text_page_upper:
        lines = text_page_upper.split("SEÑOR")[1].split("\n")
        for index, line in enumerate(lines):
          if index > 0 and ":" not in line and "GYC" not in line and "GEOTECNIA" not in line and line != "\n":
            if "CIUDAD" not in line:
              return line
            else : 
              return ""

  except Exception as e:
    print(f"Error al procesar {path_file_main}: {e}")
  return client

def get_product_type(text_upper):

  product_type = PROJECT_TYPES[0]
  for product in PROJECT_TYPES:
    for code in product[CODES]:
      if SPACE + code + SPACE in text_upper or SPACE + code + POINT in text_upper:
        product_type = product

  product_detail = None
  if len(product_type[SPECIFIC_DETAIL]) > 0:
    if len(product_type[SPECIFIC_DETAIL]) == 1:
      product_detail = product_type[SPECIFIC_DETAIL][0]
    else :
      for product_det in product_type[SPECIFIC_DETAIL]:
        if product_det.upper() in text_upper:
          product_detail = product_det
          break
  return {PRODUCT_TYPE: product_type[CODES][0] + SPACE + '-' + SPACE + product_type[DETAIL], LIST_DETAILS: product_type[SPECIFIC_DETAIL], SPECIFIC_DETAIL: product_detail}

def get_product_detail_from_text(product_type, text_upper):
  product_detail = None
  if len(product_type[LIST_DETAILS]) > 0:
    for product_det in product_type[LIST_DETAILS]:
      if product_det.upper() in text_upper:
        product_detail = product_det
        break
  else :
    product_detail = product_type[LIST_DETAILS][0]
  return product_detail

def read_file_finds_product_type_detail_from_pes(product_type, path_file_main):
  
  try:
    with fitz.open(path_file_main) as pdf_doc:
      text_page = pdf_doc[0].get_text().upper()
      # print(text_page)
      if "REF." in text_page:
        product_detail = text_page.split("REF.")[1].split("ESTIMAD")[0]
        return product_detail

      else:
        return None
  except Exception as e:
    print(f"Error al procesar para tipo de producto {path_file_main}: {e}")
    return None

def get_product_type_from_folder_name(folder_gyc):
  return get_product_type(folder_gyc.upper())


def get_client_product_type_full_files(main_route, folder_gyc):
  data_response = {
      CLIENT: "",
      PRODUCT_TYPE: ""
  }

  def process_file(file_path, file):
    nonlocal data_response

    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".pdf":
      client = read_file_finds_client(file_path)
      if client and not data_response[CLIENT]:
        data_response[CLIENT] = client

      product_type = get_product_type_from_folder_name(folder_gyc)
      if product_type and not data_response[PRODUCT_TYPE]:
        data_response[PRODUCT_TYPE] = product_type
      if not data_response[PRODUCT_TYPE][SPECIFIC_DETAIL]:
        if PES in file.upper():
          product_type = read_file_finds_product_type_detail_from_pes(product_type, file_path)
          if product_type is not None:
            data_response[PRODUCT_TYPE] = product_type

  for current_folder, _, files in os.walk(main_route):
    for file in files:
      file_path = os.path.join(current_folder, file)
      process_file(file_path, file)

      if data_response[CLIENT] and data_response[PRODUCT_TYPE]:
        return data_response

  return data_response

def process_project(project_path, year):
  """
    Metodo encargado de procesar cada proyecto en el anio (year) especificado
  """
  project_name = os.path.basename(project_path)

  if GYC in project_name.upper():
    code_project = obtain_gyc_code(project_name)
    date_project = datetime(int(year), int(code_project.split("-")[0][0:2]), 1)
    data_client_product_type = get_client_product_type_full_files(project_path, project_name)
    project_client = data_client_product_type[CLIENT].replace("\n", "").strip()
    product_type_project = data_client_product_type[PRODUCT_TYPE]
    general_data = {
      PROJECT_PATH: project_path,
      CODE: code_project,
      DATE: str(date_project)[:10],
      CLIENT: project_client,
      PRODUCT_TYPE: product_type_project
    }
    print(f"Informacion general del proyecto: {general_data}")
    print("---------------------------------------------------------------------------------------------------------------")



def process_year_directory(year_path, year):
  """
    Metodo encargado de recorrer los proyectos en el anio de revision 
  """
  projects = os.listdir(year_path) # lista de proyectos en el anio year 
  for project in projects:
    project_path = os.path.join(year_path, project)
    if os.path.isdir(project_path):
      process_project(project_path, year)


def iterate_years(main_directory, start_year):
  """
    Metodo encargado de recorrer cada uno de los anios desde start_year
  """
  years = os.listdir(main_directory)
  for year in years:
      year_path = os.path.join(main_directory, year)

      if os.path.isdir(year_path) and year.isdigit() and int(year) == start_year:
          process_year_directory(year_path, year)

if __name__ == "__main__":
    main_directory = '/home/user/Documentos/GYC/Proyectos/' # Ubicacion general de los anios que contienen los proyectos
    start_year = 2008  # Especifica aquí el año de inicio que desees
    iterate_years(main_directory, start_year)

    