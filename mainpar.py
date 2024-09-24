import numpy as np
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import random

class GestionImagenes:
    def __init__(self, path):
        self.image = np.array(Image.open(path))
        self.alto, self.ancho, _ = self.image.shape

    def sal_pimienta(self, porcentaje, num_hilos=4):
        imagen = np.copy(self.image)
        pixeles = int((self.alto * self.ancho) * (porcentaje / 100))

        def aplicar_ruido(start, end):
            for _ in range(pixeles // num_hilos):
                yy = random.randint(start, end - 1)
                xx = random.randint(0, self.ancho - 1)
                if random.randint(0, 1) == 0:
                    imagen[yy, xx][:3] = [0, 0, 0]  # Pimienta (negro)
                else:
                    imagen[yy, xx][:3] = [255, 255, 255]  # Sal (blanco)

        # Divide la imagen en 'num_hilos' partes y aplica ruido en paralelo
        with ThreadPoolExecutor(max_workers=num_hilos) as executor:
            step = self.alto // num_hilos
            futures = [executor.submit(aplicar_ruido, i * step, (i + 1) * step) for i in range(num_hilos)]
            for future in futures:
                future.result()

        img = Image.fromarray(imagen)
        img.save(f'pr1/img/tipo_Ruido_{porcentaje}_paralela.png')

# Uso del código
g = GestionImagenes("pr1/img/img_1.png")
g.sal_pimienta(50)  # Solución secuencial
g.sal_pimienta(50, num_hilos=4)  # Solución paralela con 4 hilos
