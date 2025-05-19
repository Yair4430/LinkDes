import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import sys
import os

def seleccionar_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo Excel o CSV",
        filetypes=[("Archivos Excel", "*.xlsx"), ("Archivos CSV", "*.csv")]
    )
    if ruta:
        entry_archivo.delete(0, tk.END)
        entry_archivo.insert(0, ruta)

def iniciar():
    archivo = entry_archivo.get().strip()
    columna = entry_columna.get().strip()
    navegador = navegador_var.get()
    fila_desde = entry_fila_desde.get().strip()
    fila_hasta = entry_fila_hasta.get().strip()
    columna_carpeta = entry_columna_carpeta.get().strip()

    if not archivo or not os.path.isfile(archivo):
        messagebox.showerror("Error", "Selecciona un archivo válido.")
        return
    if not columna:
        messagebox.showerror("Error", "Escribe el nombre exacto de la columna donde están los links.")
        return
    if navegador not in ["Firefox", "Chrome", "Edge"]:
        messagebox.showerror("Error", "Selecciona un navegador válido.")
        return
    if not fila_desde.isdigit() or not fila_hasta.isdigit():
        messagebox.showerror("Error", "Las filas deben ser números enteros.")
        return
    if not columna_carpeta:
        messagebox.showerror("Error", "Escribe el nombre exacto de la columna para crear las carpetas.")
        return

    ruta_procesar = os.path.join(os.path.dirname(__file__), "procesar_links.py")
    subprocess.Popen([
        sys.executable, ruta_procesar, archivo, columna, navegador.lower(), fila_desde, fila_hasta, columna_carpeta
    ])

# Crear ventana
ventana = tk.Tk()
ventana.title("Abrir Links desde Excel")
ventana.geometry("600x350")

# Archivo Excel
tk.Label(ventana, text="Selecciona el archivo Excel o CSV:").pack(pady=(10,0))
frame_archivo = tk.Frame(ventana)
frame_archivo.pack(pady=5)
entry_archivo = tk.Entry(frame_archivo, width=50)
entry_archivo.pack(side=tk.LEFT, padx=(0,5))
btn_examinar = tk.Button(frame_archivo, text="Examinar", command=seleccionar_archivo)
btn_examinar.pack(side=tk.LEFT)

# Nombre columna
tk.Label(ventana, text="Nombre exacto de la columna con los links:").pack(pady=(15,0))
entry_columna = tk.Entry(ventana, width=30)
entry_columna.pack()

# Nueva entrada para nombre de columna de carpetas
tk.Label(ventana, text="Nombre exacto de la columna para nombrar las carpetas:").pack(pady=(10,0))
entry_columna_carpeta = tk.Entry(ventana, width=30)
entry_columna_carpeta.pack()

# Navegador
tk.Label(ventana, text="Selecciona el navegador para abrir los links:").pack(pady=(15,0))
navegador_var = tk.StringVar()
navegador_var.set("Chrome")  # valor por defecto
navegador_opciones = tk.OptionMenu(ventana, navegador_var, "Firefox", "Chrome", "Edge")
navegador_opciones.pack()

# Fila desde
tk.Label(ventana, text="Fila desde (ej. 2):").pack(pady=(15,0))
entry_fila_desde = tk.Entry(ventana, width=10)
entry_fila_desde.pack()

# Fila hasta
tk.Label(ventana, text="Fila hasta (ej. 20):").pack(pady=(10,0))
entry_fila_hasta = tk.Entry(ventana, width=10)
entry_fila_hasta.pack()

# Botón iniciar
tk.Button(ventana, text="Iniciar", command=iniciar).pack(pady=20)

ventana.mainloop()
