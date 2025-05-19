# procesar_links.py (añade estas líneas al inicio)
from crear_carpetas import crear_estructura_carpetas
import pandas as pd
import re
import sys
import os
import subprocess

def transformar_link(link):
    # Extraer el ID del archivo
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', link)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    else:
        # Si es otro tipo de link (por ejemplo un "sharing link"), intentar extraer el ID por otro patrón
        match_alt = re.search(r'id=([a-zA-Z0-9_-]+)', link)
        if match_alt:
            file_id = match_alt.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
    return None  # Si no se puede transformar

def buscar_y_descargar_links(archivo_excel, columna, navegador, fila_desde, fila_hasta):
    ruta_destino = crear_estructura_carpetas()
    if archivo_excel.endswith('.xlsx'):
        df = pd.read_excel(archivo_excel)
    elif archivo_excel.endswith('.csv'):
        df = pd.read_csv(archivo_excel)
    else:
        print("❌ Formato no soportado.")
        return

    if columna not in df.columns:
        print(f"❌ La columna '{columna}' no existe.")
        return

    link_pattern = re.compile(r'https://drive\.google\.com/[^\s,"]+')
    encontrados = []

    df_rango = df.iloc[fila_desde:fila_hasta]

    for val in df_rango[columna].dropna():
        links = link_pattern.findall(str(val))
        for link in links:
            nuevo_link = transformar_link(link)
            if nuevo_link:
                encontrados.append(nuevo_link)

    if not encontrados:
        print("⚠️ No se encontraron enlaces válidos en ese rango.")
        return

    print(f"🔗 Se encontraron {len(encontrados)} enlaces de descarga. Abriendo en navegador {navegador}...")

    rutas = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }

    if navegador not in rutas:
        print(f"❌ Navegador no soportado.")
        return

    exe_navegador = rutas[navegador]

    for link in encontrados:
        print(f"⬇️ Descargando: {link}")
        subprocess.Popen([exe_navegador, link])

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Uso: python procesar_links.py <archivo_excel> <nombre_columna> <navegador> <fila_desde> <fila_hasta>")
        sys.exit(1)

    archivo_excel = sys.argv[1]
    nombre_columna = sys.argv[2]
    navegador = sys.argv[3].lower()
    fila_desde = int(sys.argv[4]) - 1
    fila_hasta = int(sys.argv[5])

    if not os.path.exists(archivo_excel):
        print(f"❌ El archivo '{archivo_excel}' no existe.")
        sys.exit(1)

    buscar_y_descargar_links(archivo_excel, nombre_columna, navegador, fila_desde, fila_hasta)
