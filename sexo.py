import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import threading  # Importar el módulo de hilos

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Cargar en modo RGB
    return np.array(img)

# Función de erosión manual
def erosion(imagen, kernel):
    filas, columnas, _ = imagen.shape
    pad = kernel.shape[0] // 2
    resultado = np.zeros_like(imagen)

    for i in range(pad, filas - pad):
        for j in range(pad, columnas - pad):
            region = imagen[i - pad:i + pad + 1, j - pad:j + pad + 1]
            resultado[i, j] = np.min(region, axis=(0, 1))

    return resultado

# Función de dilatación manual
def dilatacion(imagen, kernel):
    filas, columnas, _ = imagen.shape
    pad = kernel.shape[0] // 2
    resultado = np.zeros_like(imagen)

    for i in range(pad, filas - pad):
        for j in range(pad, columnas - pad):
            region = imagen[i - pad:i + pad + 1, j - pad:j + pad + 1]
            resultado[i, j] = np.max(region, axis=(0, 1))

    return resultado

# Función para mostrar una imagen en la ventana de Tkinter
def mostrar_imagen(imagen_np, titulo):
    imagen_pil = Image.fromarray(imagen_np)
    imagen_pil.thumbnail((300, 300))  # Redimensionar para ajustarse a la ventana
    imagen_tk = ImageTk.PhotoImage(imagen_pil)
    
    # Mostrar en la interfaz
    label_imagen.config(image=imagen_tk)
    label_imagen.image = imagen_tk  # Necesario para que Tkinter mantenga la referencia

    # Actualizar título
    ventana.title(titulo)

# Función para aplicar erosión en un hilo
def aplicar_erosion():
    global img_rgb
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_erosion():
        global img_rgb
        img_rgb = erosion(img_rgb, kernel)
        mostrar_imagen(img_rgb, "Erosión Aplicada")
    
    # Crear un hilo para ejecutar el proceso de erosión
    hilo_erosion = threading.Thread(target=proceso_erosion)
    hilo_erosion.start()

# Función para aplicar dilatación en un hilo
def aplicar_dilatacion():
    global img_rgb
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_dilatacion():
        global img_rgb
        img_rgb = dilatacion(img_rgb, kernel)
        mostrar_imagen(img_rgb, "Dilatación Aplicada")
    
    # Crear un hilo para ejecutar el proceso de dilatación
    hilo_dilatacion = threading.Thread(target=proceso_dilatacion)
    hilo_dilatacion.start()

# Función para cargar la imagen desde el archivo y mostrarla
def abrir_imagen():
    ruta_imagen = filedialog.askopenfilename()
    if ruta_imagen:
        global img_rgb
        img_rgb = cargar_imagen(ruta_imagen)
        mostrar_imagen(img_rgb, "Imagen Original")

# Crear la interfaz gráfica usando Tkinter
ventana = tk.Tk()
ventana.title("Erosión y Dilatación Interactiva")

# Botón para abrir la imagen
btn_abrir = tk.Button(ventana, text="Abrir Imagen", command=abrir_imagen)
btn_abrir.pack(pady=10)

# Botones para aplicar las operaciones
btn_aplicar_erosion = tk.Button(ventana, text="Aplicar Erosión", command=aplicar_erosion)
btn_aplicar_erosion.pack(pady=10)

btn_aplicar_dilatacion = tk.Button(ventana, text="Aplicar Dilatación", command=aplicar_dilatacion)
btn_aplicar_dilatacion.pack(pady=10)

# Etiqueta para mostrar la imagen
label_imagen = tk.Label(ventana)
label_imagen.pack(pady=10)

# Inicializar la ventana
ventana.mainloop()
