import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import threading  # Importar el módulo de hilos

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Cargar en modo RGB
    return np.array(img)

# Función de erosión manual según la figura seleccionada
def erosion(imagen, kernel, figura):
    filas, columnas, _ = imagen.shape
    pad = kernel.shape[0] // 2
    resultado = np.zeros_like(imagen)
    matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='constant')

    for i in range(1, filas + 1):
        for j in range(1, columnas + 1):
            if figura == 1:
                resultado[i - 1, j - 1] = np.min([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i + 1, j],
                    matrizExpandida[i, j - 1],
                    matrizExpandida[i, j + 1]
                ], axis=0)
            elif figura == 2:
                resultado[i - 1, j - 1] = np.min([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i, j - 1]
                ], axis=0)
            elif figura == 3:
                resultado[i - 1, j - 1] = np.min([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i, j + 1]
                ], axis=0)
            elif figura == 4:
                resultado[i - 1, j - 1] = np.min([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i + 1, j]
                ], axis=0)
            elif figura == 5:
                resultado[i - 1, j - 1] = np.min([
                    matrizExpandida[i, j],
                    matrizExpandida[i, j - 1]
                ], axis=0)
            elif figura == 6:
                resultado[i - 1, j - 1] = np.min([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j + 1],
                    matrizExpandida[i - 1, j - 1],
                    matrizExpandida[i + 1, j + 1],
                    matrizExpandida[i + 1, j - 1]
                ], axis=0)
            else:
                raise ValueError("Figura no válida. Elige una figura entre 1 y 6.")
    return resultado

# Función de dilatación manual según la figura seleccionada
def dilatacion(imagen, kernel, figura):
    filas, columnas, _ = imagen.shape
    pad = kernel.shape[0] // 2
    resultado = np.zeros_like(imagen)
    matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='constant')

    for i in range(1, filas + 1):
        for j in range(1, columnas + 1):
            if figura == 1:
                resultado[i - 1, j - 1] = np.max([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i + 1, j],
                    matrizExpandida[i, j - 1],
                    matrizExpandida[i, j + 1]
                ], axis=0)
            elif figura == 2:
                resultado[i - 1, j - 1] = np.max([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i, j - 1]
                ], axis=0)
            elif figura == 3:
                resultado[i - 1, j - 1] = np.max([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i, j + 1]
                ], axis=0)
            elif figura == 4:
                resultado[i - 1, j - 1] = np.max([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j],
                    matrizExpandida[i + 1, j]
                ], axis=0)
            elif figura == 5:
                resultado[i - 1, j - 1] = np.max([
                    matrizExpandida[i, j],
                    matrizExpandida[i, j - 1]
                ], axis=0)
            elif figura == 6:
                resultado[i - 1, j - 1] = np.max([
                    matrizExpandida[i, j],
                    matrizExpandida[i - 1, j + 1],
                    matrizExpandida[i - 1, j - 1],
                    matrizExpandida[i + 1, j + 1],
                    matrizExpandida[i + 1, j - 1]
                ], axis=0)
            else:
                raise ValueError("Figura no válida. Elige una figura entre 1 y 6.")
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

# Función para aplicar erosión según la figura seleccionada
def aplicar_erosion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_erosion():
        global img_rgb
        img_rgb = erosion(img_rgb, kernel, figura_seleccionada.get())
        mostrar_imagen(img_rgb, f"Erosión Figura {figura_seleccionada.get()} Aplicada")
    
    # Crear un hilo para ejecutar el proceso de erosión
    hilo_erosion = threading.Thread(target=proceso_erosion)
    hilo_erosion.start()

# Función para aplicar dilatación según la figura seleccionada
def aplicar_dilatacion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_dilatacion():
        global img_rgb
        img_rgb = dilatacion(img_rgb, kernel, figura_seleccionada.get())
        mostrar_imagen(img_rgb, f"Dilatación Figura {figura_seleccionada.get()} Aplicada")
    
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

# Variable para almacenar la figura seleccionada
figura_seleccionada = tk.IntVar(value=1)

# Botón para abrir la imagen
btn_abrir = tk.Button(ventana, text="Abrir Imagen", command=abrir_imagen)
btn_abrir.pack(pady=10)

# Crear opciones de selección de figuras
label_figura = tk.Label(ventana, text="Seleccionar Figura:")
label_figura.pack()

figuras = [
    ("Figura 1", 1),
    ("Figura 2", 2),
    ("Figura 3", 3),
    ("Figura 4", 4),
    ("Figura 5", 5),
    ("Figura 6", 6)
]

for texto, valor in figuras:
    radio = tk.Radiobutton(ventana, text=texto, variable=figura_seleccionada, value=valor)
    radio.pack(anchor="w")

# Botón para aplicar erosión
btn_aplicar_erosion = tk.Button(ventana, text="Aplicar Erosión", command=aplicar_erosion)
btn_aplicar_erosion.pack(pady=10)

# Botón para aplicar dilatación
btn_aplicar_dilatacion = tk.Button(ventana, text="Aplicar Dilatación", command=aplicar_dilatacion)
btn_aplicar_dilatacion.pack(pady=10)

# Etiqueta para mostrar la imagen
label_imagen = tk.Label(ventana)
label_imagen.pack(pady=10)

# Inicializar la ventana
ventana.mainloop()
