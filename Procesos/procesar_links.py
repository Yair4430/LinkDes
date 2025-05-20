# procesar_links.py
from crear_carpetas import crear_estructura_carpetas, crear_carpetas_por_fila
import pandas as pd
import re
import sys
import os
import subprocess
import time
import shutil
import PyPDF2  # Asegúrate de instalar esta biblioteca con `pip install PyPDF2`

def esperar_descarga_completa(nombre_archivo_base, timeout=30):
    carpeta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
    archivo_crdownload = os.path.join(carpeta_descargas, f"{nombre_archivo_base}.crdownload")
    tiempo_espera = 0

    while os.path.exists(archivo_crdownload) and tiempo_espera < timeout:
        print("⏳ Esperando que termine la descarga...")
        time.sleep(1)
        tiempo_espera += 1

    return not os.path.exists(archivo_crdownload)

def es_pdf_valido(ruta_pdf):
    try:
        with open(ruta_pdf, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return len(reader.pages) > 0  # Verifica que el PDF tenga al menos una página
    except Exception:
        return False

def mover_ultimo_pdf_a_carpeta(destino):
    carpeta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
    archivos_pdf = [f for f in os.listdir(carpeta_descargas) if f.endswith('.pdf')]

    if not archivos_pdf:
        print("❌ No se encontraron archivos PDF en Descargas.")
        return None

    archivos_pdf.sort(key=lambda f: os.path.getctime(os.path.join(carpeta_descargas, f)), reverse=True)
    archivo_mas_reciente = archivos_pdf[0]
    nombre_base = os.path.splitext(archivo_mas_reciente)[0]

    if not esperar_descarga_completa(nombre_base):
        print("❌ Descarga no se completó dentro del tiempo esperado.")
        return None

    ruta_origen = os.path.join(carpeta_descargas, archivo_mas_reciente)
    ruta_destino = os.path.join(destino, archivo_mas_reciente)

    # Verificar que el PDF sea válido
    if not es_pdf_valido(ruta_origen):
        print("❌ El archivo PDF está corrupto y no se moverá.")
        return None

    try:
        shutil.move(ruta_origen, ruta_destino)
        print(f"✅ PDF movido a: {ruta_destino}")
        return ruta_destino
    except Exception as e:
        print(f"❌ Error al mover archivo: {e}")
        return None

def transformar_link(link):
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', link)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    else:
        match_alt = re.search(r'id=([a-zA-Z0-9_-]+)', link)
        if match_alt:
            file_id = match_alt.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
    return None

def buscar_y_descargar_links(archivo_excel, columna, navegador, fila_desde, fila_hasta, columna_carpeta):
    ruta_destino = crear_estructura_carpetas()

    if archivo_excel.endswith('.xlsx'):
        df = pd.read_excel(archivo_excel)
    elif archivo_excel.endswith('.csv'):
        df = pd.read_csv(archivo_excel)
    else:
        print("❌ Formato no soportado.")
        return

    if columna not in df.columns or columna_carpeta not in df.columns:
        print(f"❌ Las columnas '{columna}' o '{columna_carpeta}' no existen.")
        return

    rutas = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }

    if navegador not in rutas:
        print(f"❌ Navegador no soportado.")
        return

    exe_navegador = rutas[navegador]
    df_rango = df.iloc[fila_desde:fila_hasta]  # Asegúrate de que esto esté correcto

    nombres_carpetas = df_rango[columna_carpeta].dropna().unique()
    crear_carpetas_por_fila(ruta_destino, nombres_carpetas)

    link_pattern = re.compile(r'https://drive\.google\.com/[^\s,"]+')
    total_descargas = 0

    # Abre todos los enlaces simultáneamente
    for i, row in df_rango.iterrows():
        val = row[columna]
        nombre_carpeta = str(row[columna_carpeta])
        links = link_pattern.findall(str(val))

        # Asegúrate de que solo se abran los enlaces encontrados
        for link in links:
            nuevo_link = transformar_link(link)
            if nuevo_link:
                print(f"⬇️ Abriendo: {nuevo_link}")
                subprocess.Popen([exe_navegador, nuevo_link])

    print("⏳ Esperando 1 minuto para que se descarguen los PDFs...")
    time.sleep(60)  # Espera 60 segundos

    # Mueve los PDFs a las carpetas correspondientes
    for i, row in df_rango.iterrows():
        nombre_carpeta = str(row[columna_carpeta])
        destino_final = os.path.join(ruta_destino, nombre_carpeta)
        os.makedirs(destino_final, exist_ok=True)

        if mover_ultimo_pdf_a_carpeta(destino_final):
            total_descargas += 1

    if total_descargas == 0:
        print("⚠️ No se movió ningún archivo PDF.")
    else:
        print(f"✅ Se movieron {total_descargas} archivos PDF correctamente.")

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Uso: python procesar_links.py <archivo_excel> <nombre_columna> <navegador> <fila_desde> <fila_hasta> <columna_carpeta>")
        sys.exit(1)

    archivo_excel = sys.argv[1]
    nombre_columna = sys.argv[2]
    navegador = sys.argv[3].lower()
    fila_desde = int(sys.argv[4]) -1
    fila_hasta = int(sys.argv[5])
    columna_carpeta = sys.argv[6]

    if not os.path.exists(archivo_excel):
        print(f"❌ El archivo '{archivo_excel}' no existe.")
        sys.exit(1)

    buscar_y_descargar_links(archivo_excel, nombre_columna, navegador, fila_desde, fila_hasta, columna_carpeta)
