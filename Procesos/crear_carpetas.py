# crear_carpetas.py
import os

def crear_estructura_carpetas():
    carpeta_principal = os.path.join(os.path.expanduser('~'), 'Downloads', 'ARCHIVOS TITULADA')
    subcarpetas = ['TECNICO', 'TECNOLOGO', 'AUXILIAR', 'OPERARIO']

    try:
        if not os.path.exists(carpeta_principal):
            os.makedirs(carpeta_principal)
            print(f"📁 Carpeta principal creada: {carpeta_principal}")
        else:
            print(f"📂 Carpeta principal ya existe: {carpeta_principal}")

        for sub in subcarpetas:
            ruta_sub = os.path.join(carpeta_principal, sub)
            if not os.path.exists(ruta_sub):
                os.makedirs(ruta_sub)
                print(f"✅ Subcarpeta creada: {ruta_sub}")
            else:
                print(f"🔄 Subcarpeta ya existe: {ruta_sub}")
        
        return carpeta_principal

    except Exception as e:
        print(f"❌ Error al crear las carpetas: {e}")
        return None

def crear_carpetas_por_fila(ruta_base, nombres):
    for nombre in nombres:
        ruta_carpeta = os.path.join(ruta_base, str(nombre).strip())
        try:
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
                print(f"📁 Carpeta creada: {ruta_carpeta}")
            else:
                print(f"🔄 Carpeta ya existe: {ruta_carpeta}")
        except Exception as e:
            print(f"❌ Error al crear carpeta '{nombre}': {e}")

if __name__ == "__main__":
    base = crear_estructura_carpetas()
    if base:
        crear_carpetas_por_fila(base, ["Ejemplo1", "Ejemplo2", "Ejemplo3"])
