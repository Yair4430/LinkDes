# controles.py
import threading

# Variables de control
pausado = threading.Event()
detenido = threading.Event()
velocidad = 1  # 1 por defecto, 0.5 rápido, 2 lento

# Iniciar en modo activo (no pausado, no detenido)
pausado.set()
detenido.clear()

def pausar():
    pausado.clear()
    print("⏸️ Pausado")

def reanudar():
    pausado.set()
    print("▶️ Reanudado")

def detener():
    detenido.set()
    print("⛔ Detenido")

def aumentar_velocidad():
    global velocidad
    velocidad = 0.5
    print("⏩ Velocidad aumentada")

def reducir_velocidad():
    global velocidad
    velocidad = 2
    print("🐢 Velocidad reducida")

def obtener_estado():
    return pausado, detenido, velocidad
