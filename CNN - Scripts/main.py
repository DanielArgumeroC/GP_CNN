import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_directory = Path.cwd()

ruta = current_directory / 'CNN - Scripts'

sys.path.append(str(ruta / 'fc'))
sys.path.append(str(ruta / 'cnn'))
sys.path.append(str(ruta / 'manejo_archivos'))

from cnn import estructura
from fc import redneuronal
from manejo_archivos import gestion_imagenes, datos_filtros

name = '1713127076312imagecropped-3072-1728-1318408.png'

def escribir():
    datos_filtros.escribir_filtros(cnn.c1.filtros, 1)
    datos_filtros.escribir_filtros(cnn.c2.filtros, 2)
    datos_filtros.escribir_filtros(cnn.c3.filtros, 3)

def leer():
    cnn.c1.filtros = datos_filtros.leer_filtros(cnn.c1.filtros, 1)
    cnn.c2.filtros = datos_filtros.leer_filtros(cnn.c2.filtros, 2)
    cnn.c3.filtros = datos_filtros.leer_filtros(cnn.c3.filtros, 3)

def entrenar(inicio):
    mapa = datos_filtros.map()
    for i in range(1000):
        cont = -1
        for clave in mapa:
            cont+=1
            print("ronda " + str(cont))
            if cont > inicio -1:
                image = gestion_imagenes.traer_imagen_prueba(str(clave)+".pgm")
                datos = cnn.forward(image)
                dato = rn.forward(datos, 1)
                print(dato)
                delta = rn.backward(1)
                delta = np.array(delta)
                cnn.backward(delta, image)
                escribir()

def clasificar():
    mapa = datos_filtros.map()
    acierto = 0
    fallo = 0
    for clave in mapa:
        image = gestion_imagenes.traer_imagen_prueba(str(clave)+".pgm")
        datos = cnn.forward(image)
        dato = rn.forward(datos, 1)
        print(dato)
        
        print(dato/100)
        dato = round(dato[0][0])

        if dato == mapa[clave]: acierto+=1
        else: fallo+=1

        gestion_imagenes.clasificar(clave, dato)
        print("aciertos: "+str(acierto))
        print("fallos: "+str(fallo))
    print("aciertos: "+str(acierto))
    print("fallos: "+str(fallo))

def clasificarImagen(image):
    datos = cnn.forward(image)
    dato = rn.forwardClasifica(datos)
    print("dato devuelto", dato[0][0])

    return dato[0][0]*100
    
if __name__ == '__main__':
    cnn = estructura.estructura()
    l = 0.5
    rn = redneuronal.redneuronal(64*126*126, 64, 64, 1, l)

    leer()
    #name es el nombre de la imagen guardada 
    image = gestion_imagenes.traer_imagen(name)
    respuesta = clasificarImagen(image)
    print(respuesta)
