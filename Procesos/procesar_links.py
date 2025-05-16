import pandas as pd
import webbrowser
import re
import sys
import os
import time
# from controles import pausar, reanudar, detener, aumentar_velocidad, reducir_velocidad, obtener_estado

def buscar_y_abrir_links(archivo_excel, columna, navegador, fila_desde, fila_hasta):
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

    # Seleccionar rango de filas (ajustando por índice 0)
    df_rango = df.iloc[fila_desde - 1:fila_hasta]

    for val in df_rango[columna].dropna():
        links = link_pattern.findall(str(val))
        encontrados.extend(links)

    if not encontrados:
        print("⚠️ No se encontraron enlaces en ese rango.")
        return

    print(f"🔗 Se encontraron {len(encontrados)} enlaces. Abriendo...")

    rutas = {
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }

    if navegador not in rutas:
        print(f"❌ Navegador no soportado.")
        return

    webbrowser.register(navegador, None, webbrowser.BackgroundBrowser(rutas[navegador]))
    navegador_web = webbrowser.get(navegador)

    for link in encontrados:
        navegador_web.open_new_tab(link)
        time.sleep(1)  # Espera entre pestañas (puedes ajustar)

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Uso: python procesar_links.py <archivo_excel> <nombre_columna> <navegador> <fila_desde> <fila_hasta>")
        sys.exit(1)

    archivo_excel = sys.argv[1]
    nombre_columna = sys.argv[2]
    navegador = sys.argv[3].lower()
    fila_desde = int(sys.argv[4])
    fila_hasta = int(sys.argv[5])

    if not os.path.exists(archivo_excel):
        print(f"❌ El archivo '{archivo_excel}' no existe.")
        sys.exit(1)

    buscar_y_abrir_links(archivo_excel, nombre_columna, navegador, fila_desde, fila_hasta)
