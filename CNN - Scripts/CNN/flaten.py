class Flaten:
    def forward(self, imagen):
        self.estructura = imagen.shape
        return imagen.reshape(imagen.shape[0] * imagen.shape[1] * imagen.shape[2])
    
    def backward(self, error):
        return error.reshape(self.estructura)