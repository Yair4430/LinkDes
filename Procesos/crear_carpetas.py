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

if __name__ == "__main__":
    crear_estructura_carpetas()
