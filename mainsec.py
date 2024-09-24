from PIL import Image
import numpy as np
import random

class GestionImagenes:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.ancho, self.alto = self.image.size
        self.image = np.array(self.image)

    def get_values(self, tipo):
        values = np.zeros((self.alto, self.ancho))
        for y in range(self.alto):
            for x in range(self.ancho):
                pixel = self.image[y, x]
                if tipo == 'R':
                    values[y, x] = pixel[0]  # Rojo
                elif tipo == 'G':
                    values[y, x] = pixel[1]  # Verde
                elif tipo == 'B':
                    values[y, x] = pixel[2]  # Azul
                elif tipo == 'Z':
                    values[y, x] = np.mean(pixel[:3])  # Promedio de RGB
        return values

    def guardar(self, tipo):
        canal = self.get_values(tipo)
        imagen = np.zeros((self.alto, self.ancho, 3), dtype=np.uint8)
        for i in range(self.alto):
            for j in range(self.ancho):
                gray = int(canal[i, j])
                imagen[i, j] = [gray, gray, gray]  # Escala de grises
        img = Image.fromarray(imagen)
        img.save(f'pr1/img/img_{tipo}.png')

    def clamp(self, value, min_val, max_val):
        return max(min_val, min(max_val, value))

    def rgb_to_int(self, red, green, blue):
        red = self.clamp(red, 0, 255)
        green = self.clamp(green, 0, 255)
        blue = self.clamp(blue, 0, 255)
        return (red << 16) | (green << 8) | blue

    def sal_pimienta(self, porcentaje):
        imagen = np.copy(self.image)
        pixeles = int((self.alto * self.ancho) * (porcentaje / 100))
        original = np.copy(imagen)

        while pixeles > 0:
            valor_entero = random.randint(0, 1)
            yy = random.randint(0, self.alto - 1)
            xx = random.randint(0, self.ancho - 1)

            if valor_entero == 0:
                imagen[yy, xx][:3] = [0, 0, 0]  # Pimienta (negro) en RGB, dejando el canal alfa intacto
            else:
                imagen[yy, xx][:3] = [255, 255, 255]  # Sal (blanco) en RGB, dejando el canal alfa intacto
            pixeles -= 1

        img = Image.fromarray(imagen)
        img.save(f'pr1/img/tipo_Ruido_{porcentaje}.png')


g = GestionImagenes("pr1/img/img_1.png")
g.sal_pimienta(50)

g.guardar('R')
g.guardar('G')
g.guardar('B')
g.guardar('Z')
