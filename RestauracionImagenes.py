import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import psutil
import concurrent.futures

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)
    return np.array(img), img

# Función de erosión
def erosion(imagen, kernel, figura):
    if len(imagen.shape) == 3:
        filas, columnas, canales = imagen.shape
    else:
        filas, columnas = imagen.shape
        canales = 1
        imagen = np.expand_dims(imagen, axis=-1)  

    resultado = np.zeros_like(imagen)
    matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='edge')

    vecinos = {
        1: [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
        2: [(0, 0), (-1, 0), (0, -1)],
        3: [(0, 0), (-1, 0), (0, 1)],
        4: [(0, 0), (-1, 0), (1, 0)],
        5: [(0, 0), (0, -1)],
        6: [(0, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)]
    }

    offsets = vecinos[figura]
    for c in range(canales):
        ventanas = [matrizExpandida[1+dx:filas+1+dx, 1+dy:columnas+1+dy, c] for dx, dy in offsets]
        resultado[..., c] = np.min(ventanas, axis=0)

    if canales == 1:
        resultado = np.squeeze(resultado, axis=-1)

    return resultado

# Función de dilatación
def dilatacion(imagen, kernel, figura):
    if len(imagen.shape) == 3:  
        filas, columnas, canales = imagen.shape
    else:  
        filas, columnas = imagen.shape
        canales = 1

    resultado = np.zeros_like(imagen, dtype=np.uint8)

    if canales > 1:
        matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='edge')
    else:
        matrizExpandida = np.pad(imagen, ((1, 1), (1, 1)), mode='edge')

    figuras_vecinos = {
        1: [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)],
        2: [(0, 0), (-1, 0), (0, -1)],
        3: [(0, 0), (-1, 0), (0, 1)],
        4: [(0, 0), (-1, 0), (1, 0)],
        5: [(0, 0), (0, -1)],
        6: [(0, 0), (-1, 1), (-1, -1), (1, 1), (1, -1)],
    }

    vecinos = figuras_vecinos.get(figura, [])
    
    if canales > 1:
        for c in range(canales):
            for dx, dy in vecinos:
                resultado[..., c] = np.maximum(resultado[..., c], matrizExpandida[1+dx:filas+1+dx, 1+dy:columnas+1+dy, c])
    else:  
        for dx, dy in vecinos:
            resultado = np.maximum(resultado, matrizExpandida[1+dx:filas+1+dx, 1+dy:columnas+1+dy])

    resultado = np.clip(resultado, 0, 255)
    return resultado.astype(np.uint8)

# Función para dividir la imagen en partes
def dividir_imagen(imagen, num_partes):
    return np.array_split(imagen, num_partes, axis=0)  # Dividir por filas

# Función para unir las partes de la imagen
def unir_imagen(partes):
    return np.vstack(partes)

# Función de erosión modificada para recibir un segmento de la imagen
def erosion_parcial(segmento, kernel, figura):
    return erosion(segmento, kernel, figura)

# Función de dilatación modificada para recibir un segmento de la imagen
def dilatacion_parcial(segmento, kernel, figura):
    return dilatacion(segmento, kernel, figura)

# Función para ejecutar erosión en paralelo
def erosion_multihilo(imagen, kernel, figura, num_hilos):
    partes = dividir_imagen(imagen, num_hilos)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = list(executor.map(erosion_parcial, partes, [kernel] * num_hilos, [figura] * num_hilos))
    return unir_imagen(resultados)

# Función para ejecutar dilatación en paralelo
def dilatacion_multihilo(imagen, kernel, figura, num_hilos):
    partes = dividir_imagen(imagen, num_hilos)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = list(executor.map(dilatacion_parcial, partes, [kernel] * num_hilos, [figura] * num_hilos))
    return unir_imagen(resultados)

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
        start_time = time.time()
        if modo_paralelo.get():
            img_rgb = erosion_multihilo(img_rgb, kernel, figura_seleccionada.get(), num_hilos=4)  # Ajusta num_hilos según tu hardware
        else:
            img_rgb = erosion(img_rgb, kernel, figura_seleccionada.get())
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_sequential_label.config(text=f"Tiempo Ejecucion: {elapsed_time:.4f} segundos")
        mostrar_imagen(img_rgb, f"Erosión Figura {figura_seleccionada.get()} Aplicada")
        actualizar_recursos()

    threading.Thread(target=proceso_erosion).start()

# Función para aplicar dilatación
def aplicar_dilatacion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_dilatacion():
        global img_rgb
        start_time = time.time()
        if modo_paralelo.get():
            img_rgb = dilatacion_multihilo(img_rgb, kernel, figura_seleccionada.get(), num_hilos=4)  # Ajusta num_hilos según tu hardware
        else:
            img_rgb = dilatacion(img_rgb, kernel, figura_seleccionada.get())
        end_time = time.time()
        elapsed_time = end_time - start_time
        time_sequential_label.config(text=f"Tiempo Ejecucion: {elapsed_time:.4f} segundos")
        mostrar_imagen(img_rgb, f"Dilatación Figura {figura_seleccionada.get()} Aplicada")
        actualizar_recursos()

    threading.Thread(target=proceso_dilatacion).start()

# Función para cargar la imagen desde el archivo y mostrarla
def abrir_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
    
    if ruta_imagen:
        global img_rgb, img_pil
        img_rgb, img_pil = cargar_imagen(ruta_imagen)
        mostrar_imagen(img_rgb, "Imagen Original")
        mostrar_tamanyo_imagen()
        
        

def guardar_imagen():
    if img_rgb is not None:
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if ruta_guardado:
            imagen_pil = Image.fromarray(img_rgb)
            imagen_pil.save(ruta_guardado)
            messagebox.showinfo("Guardado", f"Imagen guardada correctamente en: {ruta_guardado}")

# Función para actualizar los recursos de CPU y memoria
def actualizar_recursos():
    cpu_usada = psutil.cpu_percent(interval=1)
    memoria_usada = psutil.virtual_memory().percent
    cpu_label.config(text=f"CPU usada: {cpu_usada}%")
    memory_label.config(text=f"Memoria usada: {memoria_usada}%")
def mostrar_tamanyo_imagen():
    if img_rgb is not None:
        filas, columnas = img_rgb.shape[:2]
        tamano_label.config(text=f"Tamaño de la imagen: {columnas} x {filas} píxeles")


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

# Cargar imágenes para los botones de figura
imagenes_botones = [ImageTk.PhotoImage(Image.open(f"img/botones/btn{i+1}.png")) for i in range(6)]

# Botones para seleccionar figura con imágenes
for i in range(6):
    boton_figura = tk.Radiobutton(marco_figura, variable=figura_seleccionada, value=i + 1, image=imagenes_botones[i], indicatoron=False, padx=10, pady=10)
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


time_sequential_label = tk.Label(ventana, text="Tiempo Ejecucion: ")
time_sequential_label.pack()

memory_label = tk.Label(ventana, text="Memoria usada: ")
memory_label.pack()

cpu_label = tk.Label(ventana, text="CPU usada: ")
cpu_label.pack()


tamano_label = tk.Label(ventana, text="Tamaño de la imagen: ")
tamano_label.pack()

# Opción para seleccionar modo de ejecución
modo_paralelo = tk.BooleanVar()
check_modo = tk.Checkbutton(ventana, text="Ejecutar en modo paralelo", variable=modo_paralelo)
check_modo.pack()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
