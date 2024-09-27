import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import threading
import time
import psutil

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)
    return np.array(img), img

import numpy as np

def erosion(imagen, kernel, figura):
    # Verificar si la imagen tiene más de un canal (RGB) o es en escala de grises
    if len(imagen.shape) == 3:
        filas, columnas, canales = imagen.shape
    else:
        filas, columnas = imagen.shape
        canales = 1
        imagen = np.expand_dims(imagen, axis=-1)  # Expandir a 3D para que funcione igual para grayscale

    # Crear una imagen de resultados con las mismas dimensiones
    resultado = np.zeros_like(imagen)

    # Expandir la matriz de imagen con padding para manejar bordes
    matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='edge')

    # Mapeo de figuras a los offsets de vecinos
    vecinos = {
        1: [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
        2: [(0, 0), (-1, 0), (0, -1)],
        3: [(0, 0), (-1, 0), (0, 1)],
        4: [(0, 0), (-1, 0), (1, 0)],
        5: [(0, 0), (0, -1)],
        6: [(0, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]
    }

    # Obtener los desplazamientos de los vecinos según la figura seleccionada
    offsets = vecinos[figura]

    # Procesar la erosión para cada canal (en caso de imágenes RGB) o para la única capa de escala de grises
    for c in range(canales):
        # Extraemos las ventanas correspondientes a los vecinos para cada offset
        ventanas = [matrizExpandida[1+dx:filas+1+dx, 1+dy:columnas+1+dy, c] for dx, dy in offsets]
        # Calculamos el mínimo a lo largo de las ventanas
        resultado[..., c] = np.min(ventanas, axis=0)

    # Si era una imagen en escala de grises, devolvemos el formato 2D original
    if canales == 1:
        resultado = np.squeeze(resultado, axis=-1)

    return resultado


# Función de dilatación corregida
def dilatacion(imagen, kernel, figura):
    # Verificar si la imagen es en escala de grises o en color
    if len(imagen.shape) == 3:  # RGB
        filas, columnas, canales = imagen.shape
    else:  # Grayscale
        filas, columnas = imagen.shape
        canales = 1

    # Crear un array de resultados
    resultado = np.zeros_like(imagen, dtype=np.uint8)

    # Expandir la matriz para evitar problemas en los bordes
    if canales > 1:
        matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='edge')
    else:
        matrizExpandida = np.pad(imagen, ((1, 1), (1, 1)), mode='edge')

    # Mapeo de figuras a las coordenadas de vecindad
    figuras_vecinos = {
        1: [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
        2: [(0, 0), (-1, 0), (0, -1)],
        3: [(0, 0), (-1, 0), (0, 1)],
        4: [(0, 0), (-1, 0), (1, 0)],
        5: [(0, 0), (0, -1)],
        6: [(0, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)],
    }

    vecinos = figuras_vecinos.get(figura, [])
    
    # Procesar dilatación para cada canal si es RGB
    if canales > 1:
        for c in range(canales):
            for dx, dy in vecinos:
                resultado[..., c] = np.maximum(resultado[..., c], matrizExpandida[1+dx:filas+1+dx, 1+dy:columnas+1+dy, c])
    else:  # Procesar para escala de grises
        for dx, dy in vecinos:
            resultado = np.maximum(resultado, matrizExpandida[1+dx:filas+1+dx, 1+dy:columnas+1+dy])

    # Asegurarnos de que los valores de píxeles se mantengan en el rango 0-255
    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)

# Función para mostrar la imagen en el canvas de Tkinter
def mostrar_imagen(imagen_array, titulo):
    imagen_pil = Image.fromarray(imagen_array.astype('uint8'))
    imagen_tk = ImageTk.PhotoImage(imagen_pil)
    canvas.config(scrollregion=canvas.bbox("all"))
    canvas.create_image(0, 0, anchor="nw", image=imagen_tk)
    canvas.image = imagen_tk
    ventana.title(titulo)

# Función para aplicar erosión
def aplicar_erosion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_erosion():
        global img_rgb
        img_rgb = erosion(img_rgb, kernel, figura_seleccionada.get())
        mostrar_imagen(img_rgb, f"Erosión Figura {figura_seleccionada.get()} Aplicada")

    if modo_paralelo.get():
        threading.Thread(target=proceso_erosion).start()
    else:
        proceso_erosion()

# Función para aplicar dilatación
def aplicar_dilatacion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_dilatacion():
        global img_rgb
        img_rgb = dilatacion(img_rgb, kernel, figura_seleccionada.get())
        mostrar_imagen(img_rgb, f"Dilatación Figura {figura_seleccionada.get()} Aplicada")

    if modo_paralelo.get():
        threading.Thread(target=proceso_dilatacion).start()
    else:
        proceso_dilatacion()

# Función para cargar la imagen desde el archivo y mostrarla
def abrir_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
    if ruta_imagen:
        global img_rgb, img_pil
        img_rgb, img_pil = cargar_imagen(ruta_imagen)
        mostrar_imagen(img_rgb, "Imagen Original")

def guardar_imagen():
    if img_rgb is not None:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if ruta_guardado:
            imagen_pil = Image.fromarray(img_rgb)
            imagen_pil.save(ruta_guardado)
            tk.messagebox.showinfo("Guardado", f"Imagen guardada correctamente en: {ruta_guardado}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Erosión y Dilatación Interactiva")
ventana.geometry("1240x960")

# Crear un canvas y añadir scrollbars
canvas = tk.Canvas(ventana, bg="white")
scroll_x = tk.Scrollbar(ventana, orient="horizontal", command=canvas.xview)
scroll_y = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)

canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Crear el marco de selección de figura
figura_seleccionada = tk.IntVar()
marco_figura = tk.Frame(ventana)
marco_figura.pack(pady=10)

# Botones para seleccionar figura
for i in range(6):
    boton_figura = tk.Radiobutton(marco_figura, variable=figura_seleccionada, value=i + 1, text=f"Figura {i+1}", indicatoron=False, padx=10, pady=10)
    boton_figura.pack(side=tk.LEFT)

# Botones de acción
boton_abrir = tk.Button(ventana, text="Abrir Imagen", command=abrir_imagen)
boton_abrir.pack(pady=5)

boton_erosion = tk.Button(ventana, text="Aplicar Erosión", command=aplicar_erosion)
boton_erosion.pack(pady=5)

boton_dilatacion = tk.Button(ventana, text="Aplicar Dilatación", command=aplicar_dilatacion)
boton_dilatacion.pack(pady=5)

boton_guardar = tk.Button(ventana, text="Guardar Imagen", command=guardar_imagen)
boton_guardar.pack()

# Opción para seleccionar modo de ejecución
modo_paralelo = tk.BooleanVar()
check_modo = tk.Checkbutton(ventana, text="Ejecutar en modo paralelo", variable=modo_paralelo)
check_modo.pack()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
