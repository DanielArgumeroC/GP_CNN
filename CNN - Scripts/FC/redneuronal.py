import numpy as np
import sigmoide

class redneuronal:
    def __init__(self, entrada, ocultos, ocultos2, salida, aprendizaje):
        self.entrada = entrada
        self.ocultos = ocultos
        self.ocultos2 = ocultos2
        self.salida = salida
        self.apredizaje = aprendizaje

        self.pesos1 = np.random.randn(entrada, ocultos)
        self.bias1 = np.zeros((1, ocultos))

        self.pesos2 = np.random.randn(ocultos, ocultos2)
        self.bias2 = np.zeros((1, ocultos2))

        self.pesos3 = np.random.randn(ocultos2, salida)
        self.bias3 = np.zeros((1, salida))

    def forward(self, entradas, salida):
        print(entradas.shape)
        salida = np.array(salida)
        self.x = np.reshape(entradas, 1016064)
        self.hidden_1 = np.dot(entradas, self.pesos1) + self.bias1
        self.hidden_1_activation = sigmoide.sigmoid(self.hidden_1)
        
        self.hidden_2 = np.dot(self.hidden_1_activation, self.pesos2) + self.bias2
        self.hidden_2_activation = sigmoide.sigmoid(self.hidden_2)

        self.hidden_3 = np.dot(self.hidden_2_activation, self.pesos3) + self.bias3
        self.hidden_3_activation = sigmoide.sigmoid(self.hidden_3)

        self.error = sigmoide.binary_crossentropy(salida, self.hidden_3_activation)
        print(self.hidden_3_activation)
        print("error "+str(self.error))
        print("salida esperada" + str(salida))
    
    def forwardClasifica(self, entradas):
        self.x = np.reshape(entradas, (1, 1016064))
        self.hidden_1 = np.dot(entradas, self.pesos1) + self.bias1
        self.hidden_1_activation = sigmoide.sigmoid(self.hidden_1)
        
        self.hidden_2 = np.dot(self.hidden_1_activation, self.pesos2) + self.bias2
        self.hidden_2_activation = sigmoide.sigmoid(self.hidden_2)

        self.hidden_3 = np.dot(self.hidden_2_activation, self.pesos3) + self.bias3
        self.hidden_3_activation = sigmoide.sigmoid(self.hidden_3)
        return(self.hidden_3_activation)
    
    def backward(self, objetivo):

        output_error = objetivo - self.hidden_3_activation
        hidden_3_delta = output_error * sigmoide.sigmoid_derivative(self.hidden_3)

        hidden_2_error = hidden_3_delta.dot(self.pesos3.T)
        hidden_2_delta = hidden_2_error * sigmoide.sigmoid_derivative(self.hidden_2)
        
        hidden_1_error = hidden_2_delta.dot(self.pesos2.T)
        hidden_1_delta = hidden_1_error * sigmoide.sigmoid_derivative(self.hidden_1)

        return hidden_1_delta.dot(self.pesos1.T) * 5

   