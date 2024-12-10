import subprocess
import os
import time
import pyautogui
import keyboard
import shutil

def abrir_archivo_pdf_con_acrobat(ruta_archivo_dwg):
    try:
        # Comando para abrir el archivo DWG con el visor de PDF predeterminado
        subprocess.Popen(['start', '', ruta_archivo_dwg], shell=True)

        print(f"El archivo DWG se ha abierto con el visor de PDF predeterminado.")

        # Espera a que se abra Acrobat y el archivo (ajusta este tiempo según sea necesario)
        time.sleep(10)

        # Utiliza keyboard para activar la ventana de Acrobat
        keyboard.press_and_release('alt+tab')
        time.sleep(1)

        # Simular pulsaciones de teclas para guardar como PDF (ajusta según sea necesario)
        pyautogui.hotkey('ctrl', 's')  # Abre el cuadro de diálogo de impresión
        time.sleep(2)

        pyautogui.press('enter')  # Presiona Enter para confirmar la impresión
        time.sleep(5)  # Espera a que se procese la impresión (ajusta según sea necesario)
        pyautogui.press('enter')  # Presiona Enter para confirmar la impresión
        time.sleep(5)
        pyautogui.hotkey('alt', 'f4')  # Cierra la ventana de impresión
        print("Archivo DWG guardado como PDF.")
        return True

    except Exception as e:
        print(f"Error al abrir el archivo DWG con Acrobat: {e}")
        return False

def limpiar_carpeta_temporal(carpeta_temporal):
    try:
        # Esperar 10 segundos antes de borrar el contenido de la carpeta
        time.sleep(10)

        # Eliminar el contenido de la carpeta temporal
        for archivo in os.listdir(carpeta_temporal):
            ruta_archivo = os.path.join(carpeta_temporal, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)

        print(f"Contenido de la carpeta temporal ha sido eliminado.")
        return True

    except Exception as e:
        print(f"Error al limpiar la carpeta temporal: {e}")
        return False

# Ruta del archivo DWG
ruta_archivo_dwg = r'C:\Script\Son2.dwg'

# Ruta de la carpeta temporal
carpeta_temporal = r'C:\Script\carpeta temporal pdfs'

# Verificar si el archivo DWG existe
if os.path.exists(ruta_archivo_dwg):
    # Llama a la función para abrir el archivo DWG con Acrobat
    if abrir_archivo_pdf_con_acrobat(ruta_archivo_dwg):
        # Llama a la función para limpiar la carpeta temporal
        limpiar_carpeta_temporal(carpeta_temporal)
        print("Proceso completado.")
else:
    print(f"El archivo {ruta_archivo_dwg} no existe.")
