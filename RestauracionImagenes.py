import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import time
import threading
import psutil  # Para medir el uso de recursos

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Cargar en modo RGB
    return np.array(img), img  # Devolver la imagen como array y como objeto PIL

# Función de erosión manual según la figura seleccionada
def erosion(imagen, kernel, figura):
    filas, columnas, _ = imagen.shape
    resultado = np.zeros_like(imagen)
    matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='edge')

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
    resultado = np.zeros_like(imagen)
    matrizExpandida = np.pad(imagen, ((1, 1), (1, 1), (0, 0)), mode='edge')

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

# Función para mostrar una imagen en el canvas de Tkinter
def mostrar_imagen(imagen_pil, titulo):
    # Convertir la imagen PIL a un formato que Tkinter pueda usar
    imagen_tk = ImageTk.PhotoImage(imagen_pil)
    canvas.config(scrollregion=canvas.bbox("all"))  # Actualizar el scrollregion del canvas
    canvas.create_image(0, 0, anchor="nw", image=imagen_tk)
    canvas.image = imagen_tk  # Mantener la referencia a la imagen

    ventana.title(titulo)

# Función para aplicar erosión
def aplicar_erosion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_erosion():
        global img_rgb
        start_time = time.time()
        process = psutil.Process()
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)
        
        img_rgb = erosion(img_rgb, kernel, figura_seleccionada.get())
        
        end_time = time.time()
        end_memory = process.memory_info().rss
        end_cpu = process.cpu_percent(interval=None)
        
        execution_time = end_time - start_time
        memory_used = (end_memory - start_memory) / (1024 * 1024)  # Convertir a MB
        cpu_used = end_cpu - start_cpu
        
        mostrar_imagen(img_rgb, f"Erosión Figura {figura_seleccionada.get()} Aplicada")
        
        if modo_paralelo.get():
            time_parallel_label.config(text=f"Tiempo paralelo: {execution_time:.4f} seconds")
        else:
            time_sequential_label.config(text=f"Tiempo secuencial: {execution_time:.4f} seconds")
        
        memory_label.config(text=f"Memoria usada: {memory_used:.4f} MB")
        cpu_label.config(text=f"CPU usada: {cpu_used:.4f} %")

    if modo_paralelo.get():
        hilo_erosion = threading.Thread(target=proceso_erosion)
        hilo_erosion.start()
    else:
        proceso_erosion()

# Función para aplicar dilatación
def aplicar_dilatacion():
    global img_rgb, figura_seleccionada
    kernel = np.ones((3, 3, 3), dtype=np.uint8)

    def proceso_dilatacion():
        global img_rgb
        start_time = time.time()
        process = psutil.Process()
        start_memory = process.memory_info().rss
        start_cpu = process.cpu_percent(interval=None)
        
        img_rgb = dilatacion(img_rgb, kernel, figura_seleccionada.get())
        
        end_time = time.time()
        end_memory = process.memory_info().rss
        end_cpu = process.cpu_percent(interval=None)
        
        execution_time = end_time - start_time
        memory_used = (end_memory - start_memory) / (1024 * 1024)  # Convertir a MB
        cpu_used = end_cpu - start_cpu
        
        mostrar_imagen(img_rgb, f"Dilatación Figura {figura_seleccionada.get()} Aplicada")
        
        if modo_paralelo.get():
            time_parallel_label.config(text=f"Tiempo paralelo: {execution_time:.4f} seconds")
        else:
            time_sequential_label.config(text=f"Tiempo secuencial: {execution_time:.4f} seconds")
        
        memory_label.config(text=f"Memoria usada: {memory_used:.4f} MB")
        cpu_label.config(text=f"CPU usada: {cpu_used:.4f} %")

    if modo_paralelo.get():
        hilo_dilatacion = threading.Thread(target=proceso_dilatacion)
        hilo_dilatacion.start()
    else:
        proceso_dilatacion()

# Función para cargar la imagen desde el archivo y mostrarla
def abrir_imagen():
    ruta_imagen = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
    if ruta_imagen:
        global img_rgb, img_pil
        img_rgb, img_pil = cargar_imagen(ruta_imagen)
        mostrar_imagen(img_pil, "Imagen Original")

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

# Configurar el layout
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Crear el marco de selección de figura
figura_seleccionada = tk.IntVar()
marco_figura = tk.Frame(ventana)
marco_figura.pack(pady=10)

# Cargar las imágenes de los botones
ruta_botones = "img/botones/"
imagenes_botones = [ImageTk.PhotoImage(Image.open(f"{ruta_botones}btn{i}.png").resize((50, 50))) for i in range(1, 7)]

# Crear botones para seleccionar figura
for i in range(6):
    boton_figura = tk.Radiobutton(marco_figura, variable=figura_seleccionada, value=i + 1, 
                                    image=imagenes_botones[i], indicatoron=False, padx=10, pady=10)
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

# Etiquetas para mostrar tiempos de ejecución
time_parallel_label = tk.Label(ventana, text="Tiempo paralelo: ")
time_parallel_label.pack()

time_sequential_label = tk.Label(ventana, text="Tiempo secuencial: ")
time_sequential_label.pack()

# Etiquetas para mostrar el uso de memoria y CPU
memory_label = tk.Label(ventana, text="Memoria usada: ")
memory_label.pack()

cpu_label = tk.Label(ventana, text="CPU usada: ")
cpu_label.pack()

# Opción para seleccionar modo de ejecución
modo_paralelo = tk.BooleanVar()
check_modo = tk.Checkbutton(ventana, text="Ejecutar en modo paralelo", variable=modo_paralelo)
check_modo.pack()

# Crear una etiqueta para mostrar la imagen
label_imagen = tk.Label(ventana)
label_imagen.pack(pady=10)
# Iniciar el bucle principal de la ventana
ventana.mainloop()
