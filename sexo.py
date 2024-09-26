import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk  # Importar ttk para usar ComboBox
import threading  # Hilos

# Función para cargar la imagen y asegurarse de que sea RGB
def cargar_imagen(ruta):
    img = Image.open(ruta).convert("RGB")  # Convertir la imagen a RGB, eliminando canal alfa
    return np.array(img)

# Función de erosión mejorada
def erosion(imagen, kernel):
    filas, columnas, canales = imagen.shape
    pad = kernel.shape[0] // 2
    resultado = np.zeros_like(imagen)

    for i in range(pad, filas - pad):
        for j in range(pad, columnas - pad):
            for c in range(canales):  # Aplicar el kernel por canal
                region = imagen[i - pad:i + pad + 1, j - pad:j + pad + 1, c]
                # Aplicar erosión: tomar el mínimo valor en la región donde el kernel es 1
                resultado[i, j, c] = np.min(region[kernel == 1])
    return resultado

# Función de dilatación manual
def dilatacion(imagen, kernel):
    filas, columnas, canales = imagen.shape
    pad = kernel.shape[0] // 2
    resultado = np.zeros_like(imagen)

    for i in range(pad, filas - pad):
        for j in range(pad, columnas - pad):
            for c in range(canales):  # Aplicar el kernel por canal
                region = imagen[i - pad:i + pad + 1, j - pad:j + pad + 1, c]
                resultado[i, j, c] = np.max(region * kernel)  # Aplicar el kernel
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

# Función para obtener el kernel seleccionado
def obtener_kernel():
    kernel_tipo = combo_elemento.get()

    if kernel_tipo == "Elemento estructurante 1":
        return np.array([[0, 1, 1],
                         [0, 0, 1],
                         [0, 0, 0]], dtype=np.uint8)
    elif kernel_tipo == "Elemento estructurante 2":
        return np.array([[0, 0, 1],
                         [0, 1, 1],
                         [0, 0, 0]], dtype=np.uint8)
    elif kernel_tipo == "Elemento estructurante 3":
        return np.array([[1, 1, 1],
                         [0, 0, 0],
                         [0, 0, 0]], dtype=np.uint8)
    elif kernel_tipo == "Elemento estructurante 4":
        return np.array([[0, 1, 0],
                         [0, 1, 0],
                         [0, 0, 0]], dtype=np.uint8)
    elif kernel_tipo == "Elemento estructurante 5":
        return np.array([[1, 0, 1],
                         [0, 1, 0],
                         [1, 0, 1]], dtype=np.uint8)

# Función para aplicar erosión en un hilo
def aplicar_erosion():
    global img_rgb
    kernel = obtener_kernel()

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
    kernel = obtener_kernel()

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

# Menú desplegable para seleccionar el elemento estructurante
combo_elemento = ttk.Combobox(ventana, values=[
    "Elemento estructurante 1",
    "Elemento estructurante 2",
    "Elemento estructurante 3",
    "Elemento estructurante 4",
    "Elemento estructurante 5"])
combo_elemento.current(0)  # Seleccionar el primer elemento por defecto
combo_elemento.pack(pady=10)

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
