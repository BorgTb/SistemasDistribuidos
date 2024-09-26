import numpy as np
import threading
from PIL import Image

# Función para cargar la imagen
def cargar_imagen(ruta):
    img = Image.open(ruta)  # Cargar en modo RGB
    return np.array(img)

# Función de erosión manual
def erosion(imagen, kernel):
    # Tamaño del kernel
    kernel_size = len(kernel)
    pad = kernel_size // 2
    filas, columnas = imagen.shape
    resultado = np.zeros((filas, columnas), dtype=np.uint8)

    # Aplicar erosión
    for i in range(pad, filas - pad):
        for j in range(pad, columnas - pad):
            region = imagen[i - pad:i + pad + 1, j - pad:j + pad + 1]
            if np.array_equal(region & kernel, kernel):
                resultado[i, j] = np.min(region)
            else:
                resultado[i, j] = 0

    return resultado

# Función de dilatación manual
def dilatacion(imagen, kernel):
    kernel_size = len(kernel)
    pad = kernel_size // 2
    filas, columnas = imagen.shape
    resultado = np.zeros((filas, columnas), dtype=np.uint8)

    # Aplicar dilatación
    for i in range(pad, filas - pad):
        for j in range(pad, columnas - pad):
            region = imagen[i - pad:i + pad + 1, j - pad:j + pad + 1]
            if np.any(region & kernel):
                resultado[i, j] = np.max(region)
            else:
                resultado[i, j] = 0

    return resultado

# Función para mezclar los resultados de erosión y dilatación
def apertura_y_cierre(imagen_rgb, kernel, output):
    # Separar los canales de color R, G, B
    canales = [imagen_rgb[:, :, i] for i in range(3)]
    
    # Aplicar erosión y luego dilatación (Apertura)
    erosion_canal = [erosion(canal, kernel) for canal in canales]
    apertura = [dilatacion(ero, kernel) for ero in erosion_canal]
    
    # Aplicar dilatación y luego erosión (Cierre)
    dilatacion_canal = [dilatacion(canal, kernel) for canal in canales]
    cierre = [erosion(dil, kernel) for dil in dilatacion_canal]
    
    # Crear la imagen resultado de apertura y cierre combinados
    resultado_apertura = np.stack(apertura, axis=-1)
    resultado_cierre = np.stack(cierre, axis=-1)
    
    # Mezclar los resultados (promediar apertura y cierre)
    resultado_final = np.clip((resultado_apertura + resultado_cierre) // 2, 0, 255).astype(np.uint8)
    
    output.append(('Resultado_Mezcla', resultado_final))

# Función principal que ejecuta las operaciones con hilos
def procesar_imagen_con_hilos(ruta_imagen):
    imagen_rgb = cargar_imagen(ruta_imagen)

    # Definir un kernel (elemento estructurante)
    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

    # Lista para almacenar los resultados
    output = []

    # Crear hilo para aplicar apertura y cierre
    hilo_mezcla = threading.Thread(target=apertura_y_cierre, args=(imagen_rgb, kernel, output))

    # Iniciar el hilo
    hilo_mezcla.start()

    # Esperar a que el hilo termine
    hilo_mezcla.join()

    # Guardar y mostrar el resultado
    for name, result in output:
        Image.fromarray(result).save(f"{name}.png")
        Image.fromarray(result).show()

# Ejecutar el procesamiento
ruta_imagen = 'img/tipo_Ruido_50.png'  # Ruta de la imagen
procesar_imagen_con_hilos(ruta_imagen)
