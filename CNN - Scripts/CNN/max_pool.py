import numpy as np

class Max_pooling:
    def __init__(self, dimesion, paso):
        self.dimension = dimesion
        self.paso = paso
    
    def forward(self, imagen):
        self.estructura = imagen
        alto, ancho, profundidad = imagen.shape
        salida_alto = int((alto - self.dimension)/self.paso) + 1
        salida_ancho = int((ancho - self.dimension)/self.paso) + 1
        salida = np.zeros((salida_alto, salida_ancho, profundidad))
        for i in range(salida_alto):
            for j in range(salida_ancho):
                imagen_parte = imagen[i*self.paso:i*self.paso+self.dimension,
                                        j*self.paso:j*self.paso+self.dimension, :]
                salida[i, j, :] = np.amax(imagen_parte, axis=(0, 1))
        return salida
    
    def backward(self, error):
        ex = np.zeros_like(self.estructura)
        alto, ancho, profundidad = self.estructura.shape
        salida_alto = int((alto - self.dimension)/self.paso) + 1
        salida_ancho = int((ancho - self.dimension)/self.paso) + 1
        for i in range(salida_alto):
            for j in range(salida_ancho):
                imagen_parte = self.estructura[i*self.paso:i*self.paso+self.dimension,
                                                  j*self.paso:j*self.paso+self.dimension, :]
                max_capa = (imagen_parte == np.amax(imagen_parte, axis=(0, 1), keepdims=True))
                ex[i*self.paso:i*self.paso+self.dimension,
                    j*self.paso:j*self.paso+self.dimension, :] += (error[i, j, :])[None, None, :] * max_capa
        return ex