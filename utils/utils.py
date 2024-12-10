import unicodedata
import PyPDF2 

def normalize_string(s):
    # Convierte a minúsculas y normaliza eliminando tildes
    return (
        unicodedata.normalize("NFKD", s)
        .encode("ASCII", "ignore")
        .decode("utf-8")
        .lower()
    )

def get_content_pdf_file(file_name):
  try:
      with open(file_name, 'rb') as pdf_file:
          pdf_reader = PyPDF2.PdfReader(pdf_file)
          num_pages = len(pdf_reader.pages)
          pdf_text = ''

          for page_num in range(num_pages):
              page = pdf_reader.pages[page_num]
              pdf_text += page.extract_text()

          return pdf_text

  except Exception as e:
      return {'error': f'Error al leer el archivo pdf: {e}'}



def is_colombian_coordinates(latitude, longitude):
    """
    Verifica si una coordenada de latitud y longitud está dentro de los límites de Colombia.
    
    Args:
        latitud (float): Latitud de la coordenada.
        longitud (float): Longitud de la coordenada.
    
    Returns:
        bool: True si la coordenada está dentro de los límites de Colombia, False en caso contrario.
    """
    # Rango de latitudes y longitudes para Colombia
    latitud_min, latitud_max = -4.227, 12.550
    longitud_min, longitud_max = -81.734, -66.869

    # Verificar si la coordenada está dentro del rango
    return latitud_min <= float(latitude) <= latitud_max and longitud_min <= float(longitude) <= longitud_max