# ventana_controles.py
import tkinter as tk
from controles import pausar, reanudar, detener, aumentar_velocidad, reducir_velocidad

def crear_ventana_controles():
    ventana = tk.Tk()
    ventana.title("Controles de Enlaces")
    ventana.geometry("300x300")
    ventana.resizable(False, False)

    titulo = tk.Label(ventana, text="Controles de Enlaces", font=("Arial", 14, "bold"))
    titulo.pack(pady=10)

    btn_pausar = tk.Button(ventana, text="⏸ Pausar", width=20, command=pausar)
    btn_pausar.pack(pady=5)

    btn_reanudar = tk.Button(ventana, text="▶ Reanudar", width=20, command=reanudar)
    btn_reanudar.pack(pady=5)

    btn_detener = tk.Button(ventana, text="⛔ Detener", width=20, command=detener)
    btn_detener.pack(pady=5)

    btn_rapido = tk.Button(ventana, text="⏩ Aumentar Velocidad", width=20, command=aumentar_velocidad)
    btn_rapido.pack(pady=5)

    btn_lento = tk.Button(ventana, text="🐢 Reducir Velocidad", width=20, command=reducir_velocidad)
    btn_lento.pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    crear_ventana_controles()
