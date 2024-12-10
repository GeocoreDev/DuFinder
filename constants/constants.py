GYC = "GYC"
PROJECT_PATH = "project_path"
CODE = "code"
CODES = "codes"
DATE = "date"
CLIENT = "client"
PRODUCT_TYPE = "product_type"
PRODUCT_TYPE_DETAIL = "product_type_detail"
DESCRIPTION = "description"
LOCATION = "location"

SPECIFIC_DETAIL = "spec_detail"
LIST_DETAILS = "list_details"
SPACE = " "
POINT = "."
MIDDLE_DASH = " - "
PES = "PES"
REPORT = "INFORME"

DETAIL = "detail"
PRODUCT_TYPES = [
  {CODES: ["ES"], DETAIL: "Estudio de Suelos", SPECIFIC_DETAIL: ["Edificios", "Casas", "Bodegas", "Subestaciones", "Tuberías", "Líneas de Conducción", "Validaciones", "Actualizaciones de Estados de Suelos"]},
  {CODES: ["DP"], DETAIL: "Diseño de Pavimentos", SPECIFIC_DETAIL: ["Índice de Estado", "Auscultación"]},
  {CODES: ["EG"], DETAIL: "Estudio Geotécnico", SPECIFIC_DETAIL: ["Puentes", "Peatonal", "Viaductos", "Intersecciones", "Cortes", "Muros", "Zodmes", "Botaderos", "Box Coulvert", "Revisión de Estudios y Diseños de Geología y Geotecnia", "Concepto Técnico", "Línea Sísmica"]},
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

KEY_WORDS_FOLDERS_DRILLING_LOGS = [
  "PERFORACION", "EXPLORACION"
]
LAT = "lat"
LONG = "long"
UBICATION_WORD = "UBICACION"
SECTOR_WORD = "SECTOR"

MUNICIPALITY = "municipality"
DEPARTMENT = "department"

ORIGIN_CRS = "EPSG:32618"  # Proyección de las coordenadas de entrada (UTM zona 18N)
DESTINATION_CRS = "EPSG:4326"  # Sistema de salida (WGS84 Lat/Lon)

# api key elasticsearch
# {
#   "id": "Zhz5U5MBJw52NlwwCgZL",
#   "name": "projects_gyc",
#   "api_key": "TMtJN9-IRfer_h9lvuNavw",
#   "encoded": "Wmh6NVU1TUJKdzUyTmx3d0NnWkw6VE10Sk45LUlSZmVyX2g5bHZ1TmF2dw==",
#   "beats_logstash_format": "Zhz5U5MBJw52NlwwCgZL:TMtJN9-IRfer_h9lvuNavw"
# }
# YUJ6OVU1TUJKdzUyTmx3d0hnYVM6TGo0Mjd3NjNUUmlfV180T1pLeDJvQQ==

# export ES_URL="https://c8f2e7b9937245778877ce752ca3f985.us-central1.gcp.cloud.es.io:443"
# export API_KEY="YUJ6OVU1TUJKdzUyTmx3d0hnYVM6TGo0Mjd3NjNUUmlfV180T1pLeDJvQQ=="