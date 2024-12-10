import os
import mimetypes

def agregar_tipos_de_archivo_adicionales():
    # Asociaciones MIME adicionales
    mimetypes.add_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx")
    mimetypes.add_type("application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx")
    mimetypes.add_type("AutoCAD Drawing", ".dwg")
    mimetypes.add_type("Script", ".scr")
    mimetypes.add_type("Database", ".db")
    mimetypes.add_type("Data", ".dat")
    mimetypes.add_type("Slide", ".sli")
    mimetypes.add_type("Sequential Data", ".s01")
    mimetypes.add_type("AutoCAD Drawing", ".DWG")
    mimetypes.add_type("Log", ".log")
    mimetypes.add_type("Amiga Disk Format", ".adf")
    mimetypes.add_type("Slide", ".slt")
    mimetypes.add_type("11N", ".11N")
    mimetypes.add_type("11O", ".11O")
    mimetypes.add_type("M21", ".M21")
    mimetypes.add_type("per", ".per")
    mimetypes.add_type("Plot", ".PLT")
    mimetypes.add_type("Sequential Data", ".p01")
    mimetypes.add_type("RAR Archive", ".rar")
    mimetypes.add_type("Backup", ".bak")
    mimetypes.add_type("Microsoft Word Backup", ".wbk")
    mimetypes.add_type("nit", ".nit")
    mimetypes.add_type("pav", ".pav")
    mimetypes.add_type("Data", ".DAT")
    mimetypes.add_type("Slide", ".sld")
    mimetypes.add_type("Design Web Format", ".dwf")
    mimetypes.add_type("Drawing Exchange Format", ".dxf")
    mimetypes.add_type("AutoCAD Plot Style Table", ".ctb")
    mimetypes.add_type("Microsoft Access Database", ".mdb")
    mimetypes.add_type("AutoCAD Drawing Lock", ".dwl")
    mimetypes.add_type("gra", ".gra")
    mimetypes.add_type("Autodesk Inventor Part", ".IPT")
    mimetypes.add_type("Plot", ".plt")
    mimetypes.add_type("pci", ".pci")
    mimetypes.add_type("AutoCAD Drawing Lock", ".dwl2")
    mimetypes.add_type("CCITT Group 3 Fax", ".GP3")
    mimetypes.add_type("Temporary", ".tmp")
    mimetypes.add_type("OPT", ".OPT")
    mimetypes.add_type("Delphi Form", ".dfm")
    mimetypes.add_type("Database File", ".dbf")
    mimetypes.add_type("Output", ".OUT")
    mimetypes.add_type("Shapefile", ".shp")
    mimetypes.add_type("Shape Index", ".shx")
    mimetypes.add_type("Script", ".SCR")
    mimetypes.add_type("dTM", ".dTM")
    mimetypes.add_type("Error Log", ".err")
    mimetypes.add_type("fez", ".fez")
    mimetypes.add_type("dLP", ".dLP")
    mimetypes.add_type("dNP", ".dNP")
    mimetypes.add_type("dXP", ".dXP")
    mimetypes.add_type("ArcGIS Spatial Index", ".sbn")
    mimetypes.add_type("ArcGIS Spatial Index", ".sbx")
    mimetypes.add_type("Slide", ".slw")
    mimetypes.add_type("w01", ".w01")
    mimetypes.add_type("DPV", ".DPV")
    mimetypes.add_type("Microsoft Excel Macro-Enabled Workbook", ".xlsm")
    mimetypes.add_type("dRX", ".dRX")
    mimetypes.add_type("Binary", ".b")
    mimetypes.add_type("Pascal Source Code", ".pas")
    mimetypes.add_type("dCG", ".dCG")
    mimetypes.add_type("Project", ".prj")
    mimetypes.add_type("CorelDRAW Image", ".cdr")
    mimetypes.add_type("pca", ".pca")
    mimetypes.add_type("Dump", ".dmp")
    mimetypes.add_type("11G", ".11G")
    mimetypes.add_type("dSM", ".dSM")
    mimetypes.add_type("Backup", ".bkp")
    mimetypes.add_type("dDG", ".dDG")
    mimetypes.add_type("Secure Database", ".SDB")
    mimetypes.add_type("$2k", ".$2k")
    mimetypes.add_type("336", ".336")
    mimetypes.add_type("Slide", ".SLD")
    mimetypes.add_type("411", ".411")
    mimetypes.add_type("Log", ".LOG")
    mimetypes.add_type("dWM", ".dWM")
    mimetypes.add_type("Rich Text Format", ".rtf")
    mimetypes.add_type("XMJ", ".XMJ")
    mimetypes.add_type("Identification", ".ID")
    mimetypes.add_type("12n", ".12n")
    mimetypes.add_type("12o", ".12o")
    mimetypes.add_type("MAS", ".MAS")
    mimetypes.add_type("Database File", ".DBF")
    mimetypes.add_type("dSY", ".dSY")
    mimetypes.add_type("dDC", ".dDC")
    mimetypes.add_type("cgx", ".cgx")
    mimetypes.add_type("Eagle Workgroup", ".ewg")
    mimetypes.add_type("avl", ".avl")
    mimetypes.add_type("dIC", ".dIC")
    mimetypes.add_type("dIP", ".dIP")
    mimetypes.add_type("K3", ".K3")
    mimetypes.add_type("F3", ".F3")
    mimetypes.add_type("L3", ".L3")
    mimetypes.add_type("M3", ".M3")
    mimetypes.add_type("dCS", ".dCS")
    mimetypes.add_type("dQG", ".dQG")
    mimetypes.add_type("K", ".K")
    mimetypes.add_type("sbk", ".sbk")
    mimetypes.add_type("Revit Family", ".fam")
    mimetypes.add_type("Maya Binary Scene", ".mb")
    mimetypes.add_type("Pixel Image", ".px")
    mimetypes.add_type("Tableau Workbook", ".tv")
    mimetypes.add_type("val", ".val")
    mimetypes.add_type("PTE", ".PTE")
    mimetypes.add_type("Autodesk Inventor Part", ".ipt")
    mimetypes.add_type("Transaction Processing System", ".tps")
    mimetypes.add_type("dAN", ".dAN")
    mimetypes.add_type("054", ".054")
    mimetypes.add_type("dDR", ".dDR")
    mimetypes.add_type("fwd", ".fwd")
    mimetypes.add_type("Point Cloud", ".XYZ")
    mimetypes.add_type("Round Robin Database", ".rrd")
    mimetypes.add_type("T3", ".T3")
    mimetypes.add_type("Performance Monitor Counter File", ".$OG")
    mimetypes.add_type("EKO", ".EKO")
    mimetypes.add_type("JCJ", ".JCJ")
    mimetypes.add_type("JOB", ".JOB")
    mimetypes.add_type("LBL", ".LBL")
    mimetypes.add_type("LBM", ".LBM")
    mimetypes.add_type("MTL", ".MTL")
    mimetypes.add_type("PAT", ".PAT")
    mimetypes.add_type("ldb", ".ldb")
    mimetypes.add_type("LIS", ".LIS")
    mimetypes.add_type("PDE", ".PDE")
    mimetypes.add_type("SEL", ".SEL")
    mimetypes.add_type("pp", ".pp")
    mimetypes.add_type("onetoc2", ".onetoc2")
    mimetypes.add_type("set", ".set")
    mimetypes.add_type("U", ".U")
    mimetypes.add_type("R", ".R")
    mimetypes.add_type("109", ".109")
    mimetypes.add_type("RSI", ".RSI")
    mimetypes.add_type("U1", ".U1")
    mimetypes.add_type("s3z", ".s3z")
    mimetypes.add_type("out", ".out")
    mimetypes.add_type("nfl", ".nfl")
    mimetypes.add_type("csa", ".csa")
    mimetypes.add_type("csu", ".csu")
    mimetypes.add_type("epp", ".epp")
    mimetypes.add_type("ifo", ".ifo")

def obtener_tipos_de_archivo_y_cantidad(carpeta):
    tipos_de_archivo_contador = {}
    archivos_con_tipo_none = []
    archivos_con_tipo_text_plain = []

    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(directorio_actual, archivo)

            try:
                tipo_de_archivo, _ = mimetypes.guess_type(ruta_completa)

                if tipo_de_archivo is None:
                    tipo_de_archivo = f"Desconocido ({os.path.splitext(archivo)[1][1:].lower()})"
                    archivos_con_tipo_none.append(ruta_completa)
                elif tipo_de_archivo == 'text/plain':
                    archivos_con_tipo_text_plain.append(ruta_completa)

                tipos_de_archivo_contador[tipo_de_archivo] = tipos_de_archivo_contador.get(tipo_de_archivo, 0) + 1

            except mimetypes.MimeTypesFileTypeWarning:
                tipo_de_archivo = None

    return tipos_de_archivo_contador, archivos_con_tipo_none, archivos_con_tipo_text_plain

def obtener_archivos_csv(carpeta):
    archivos_csv = []

    for directorio_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(directorio_actual, archivo)
            
            try:
                tipo_de_archivo, _ = mimetypes.guess_type(ruta_completa)

                if tipo_de_archivo == 'text/csv':
                    archivos_csv.append(ruta_completa)

            except mimetypes.MimeTypesFileTypeWarning:
                tipo_de_archivo = None

    return archivos_csv

# Ruta de la carpeta que deseas analizar
carpeta_a_analizar = "D:/"

# Llamamos a la función y obtenemos los tipos de archivo y sus cantidades, así como las rutas de archivos con tipo None y las de tipo text/plain
tipos_de_archivo_y_cantidades, archivos_con_tipo_none, archivos_con_tipo_text_plain = obtener_tipos_de_archivo_y_cantidad(carpeta_a_analizar)

# Llamamos a la función y obtenemos las rutas de archivos CSV
archivos_csv = obtener_archivos_csv(carpeta_a_analizar)

# Ordenamos los tipos de archivo de mayor a menor cantidad
tipos_de_archivo_ordenados = sorted(tipos_de_archivo_y_cantidades.items(), key=lambda x: x[1], reverse=True)

# Ruta del archivo de texto donde guardaremos los tipos de archivo y cantidades ordenados
archivo_salida = "tipos_de_archivo_y_cantidades_ordenados.txt"

# Ruta del archivo de texto donde guardaremos las rutas de archivos con tipo None
archivo_archivos_none = "archivos_none.txt"

# Ruta del archivo de texto donde guardaremos las rutas de archivos con tipo text/plain
archivo_archivos_text_plain = "text_plain_rutas.txt"

# Ruta del archivo de texto donde guardaremos las rutas de archivos CSV
archivo_csv = "archivos_csv.txt"

# Escribimos los tipos de archivo y cantidades ordenados en el archivo de texto
with open(archivo_salida, "w") as archivo:
    archivo.write("Tipos de archivo y cantidades encontradas (ordenados de mayor a menor):\n")
    for tipo_de_archivo, cantidad in tipos_de_archivo_ordenados:
        archivo.write(f"{tipo_de_archivo}: {cantidad} archivos\n")

# Escribimos las rutas de archivos con tipo None en el archivo de texto
with open(archivo_archivos_none, "w", encoding='utf-8') as archivo_none:
    archivo_none.write("Rutas de archivos con tipo None:\n")
    for ruta in archivos_con_tipo_none:
        archivo_none.write(f"{ruta}\n")

# Escribimos las rutas de archivos con tipo text/plain en el archivo de texto
with open(archivo_archivos_text_plain, "w", encoding='utf-8') as archivo_text_plain:
    archivo_text_plain.write("Rutas de archivos con tipo text/plain:\n")
    for ruta in archivos_con_tipo_text_plain:
        archivo_text_plain.write(f"{ruta}\n")

# Escribimos las rutas de archivos CSV en el archivo de texto
with open(archivo_csv, "w", encoding='utf-8') as archivo_csv:
    archivo_csv.write("Rutas de archivos CSV:\n")
    for ruta in archivos_csv:
        archivo_csv.write(f"{ruta}\n")

print(f"Los tipos de archivo y sus cantidades ordenados se han guardado en {archivo_salida}")
print(f"Las rutas de archivos con tipo None se han guardado en {archivo_archivos_none}")
print(f"Las rutas de archivos con tipo text/plain se han guardado en {archivo_archivos_text_plain}")
print(f"Las rutas de archivos CSV se han guardado en {archivo_csv}")