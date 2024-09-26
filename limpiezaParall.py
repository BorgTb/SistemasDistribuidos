import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import time
import threading
import psutil  # Importar psutil para medir el uso de recursos

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Cargar en modo RGB
    return np.array(img)

# Función de erosión manual según la figura seleccionada
def erosion(imagen, kernel, figura):
    filas, columnas, _ = imagen.shape
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
        time_label.config(text=f"Tiempo de erosión: {execution_time:.4f} seconds")
        memory_label.config(text=f"Memoria usada: {memory_used:.4f} MB")
        cpu_label.config(text=f"CPU usada: {cpu_used:.4f} %")

    if modo_paralelo.get():
        # Crear un hilo para ejecutar el proceso de erosión
        hilo_erosion = threading.Thread(target=proceso_erosion)
        hilo_erosion.start()
    else:
        proceso_erosion()

# Función para aplicar dilatación según la figura seleccionada
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
        time_label.config(text=f"Tiempo de dilatación: {execution_time:.4f} seconds")
        memory_label.config(text=f"Memoria utilizada: {memory_used:.4f} MB")
        cpu_label.config(text=f"CPU usada: {cpu_used:.4f} %")

    if modo_paralelo.get():
        # Crear un hilo para ejecutar el proceso de dilatación
        hilo_dilatacion = threading.Thread(target=proceso_dilatacion)
        hilo_dilatacion.start()
    else:
        proceso_dilatacion()

# Función para cargar la imagen desde el archivo y mostrarla
def abrir_imagen():
    ruta_imagen = filedialog.askopenfilename()
    if ruta_imagen:
        global img_rgb
        img_rgb = cargar_imagen(ruta_imagen)
        mostrar_imagen(img_rgb, "Imagen Original")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Procesamiento de Imágenes")

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

# Etiquetas para mostrar tiempos de ejecución y uso de memoria
time_label = tk.Label(ventana, text="Tiempo de Erosión: ")
time_label.pack()

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
