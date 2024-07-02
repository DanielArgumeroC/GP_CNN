import numpy as np
from concurrent.futures import ThreadPoolExecutor
class Convolucion:
    def __init__(self, filtros, profundidad, dimension, paso):
        self.tamaño_filtro = dimension
        self.n_filtros = filtros
        self.profundidad = profundidad
        self.filtros = np.random.randn(dimension, dimension, profundidad, filtros)
        self.paso = paso
        self.bias = np.random.randn(filtros, 1, 1)
    
    def forward(self, imagen):  
        salida_alto = int((imagen.shape[0] - self.tamaño_filtro)/self.paso) + 1
        salida_ancho = int((imagen.shape[1] - self.tamaño_filtro)/self.paso) + 1
        salida = np.zeros((salida_alto, salida_ancho, self.n_filtros))
        filtros = self.filtros
        
        def calculate_output(i, j):
            imagen_parte = imagen[i*self.paso:i*self.paso+self.tamaño_filtro,
                                  j*self.paso:j*self.paso+self.tamaño_filtro]
            for k in range(self.n_filtros):
                filtro = filtros[:, :, :, k]
                salida[i, j, k] = np.sum(imagen_parte * filtro) * self.bias[k, 0, 0]
        
        with ThreadPoolExecutor() as executor:
            for i in range(salida_alto):
                for j in range(salida_ancho):
                    executor.submit(calculate_output, i, j)
        
        return salida
    
    def backward(self, error, imagen):
        ex = np.zeros_like(imagen)
        ep = np.zeros_like(self.filtros)
        eb = np.zeros_like(self.bias)
        
        def calculate_gradients(i, j):
            imagen_parte = imagen[i*self.paso:i*self.paso+self.tamaño_filtro,
                                  j*self.paso:j*self.paso+self.tamaño_filtro]
            for k in range(self.n_filtros):
                ep[:, :, :, k] += np.sum(imagen_parte * np.expand_dims(error[i, j, k], axis=(0, 1, 2)), axis=0)
            eb += np.sum(error[i, j, :])
            ex[i*self.paso:i*self.paso+self.tamaño_filtro,
                j*self.paso:j*self.paso+self.tamaño_filtro] += np.sum(self.filtros * np.expand_dims(error[i, j], axis=0), axis=3)
        
        with ThreadPoolExecutor() as executor:
            for i in range(error.shape[0]):
                for j in range(error.shape[1]):
                    executor.submit(calculate_gradients, i, j)
        
        self.filtros -= ep
        self.bias -= eb
        
        return ex
