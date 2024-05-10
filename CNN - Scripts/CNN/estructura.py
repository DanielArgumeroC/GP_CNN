import convolucion, relu, max_pool, flaten

class estructura:
    def __init__(self):
        self.c1 = convolucion.Convolucion(32, 3, 3, 1)
        self.r1 = relu.Relu()
        self.mp1 = max_pool.Max_pooling(2, 2)

        self.c2 = convolucion.Convolucion(64, 32, 3, 1)
        self.r2 = relu.Relu()
        self.mp2 = max_pool.Max_pooling(2, 2)
        
        self.c3 = convolucion.Convolucion(64, 64, 3, 1)
        self.r3 = relu.Relu()
        self.mp3 = max_pool.Max_pooling(2, 2)

        self.f = flaten.Flaten()

    
    def forward(self, imagen):
        salida = self.c1.forward(imagen)
        salida = self.r1.forward(salida)
        self.imagen2 = self.mp1.forward(salida)
        salida = self.c2.forward(self.imagen2)
        salida = self.r2.forward(salida)
        self.imagen3 = self.mp2.forward(salida)
        salida = self.c3.forward(self.imagen3)
        salida = self.r3.forward(salida)
        salida = self.mp3.forward(salida)
        salida = self.f.forward(salida)
        return salida
    
    def backward(self, error, imagen):
        retro = self.f.backward(error)
        retro = self.mp3.backward(retro)
        retro = self.r3.backward(retro)
        retro = self.c3.backward(retro, self.imagen3)
        retro = self.mp2.backward(retro)
        retro = self.r2.backward(retro)
        retro = self.c2.backward(retro, self.imagen2)
        retro = self.mp1.backward(retro)
        retro = self.r1.backward(retro)
        retro = self.c1.backward(retro, imagen)