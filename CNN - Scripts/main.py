import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_directory = Path.cwd()

ruta = current_directory

sys.path.append(str(ruta))
sys.path.append(str(ruta / 'manejo_archivos'))
sys.path.append(str(ruta / 'fc'))
sys.path.append(str(ruta / 'CNN'))

# Get the path of the "uploads" folder
uploads_folder = current_directory.parent / 'WebApp' / 'Server' / 'uploads'
# Obtener la lista de archivos en la carpeta
files = [f for f in uploads_folder.iterdir() if f.is_file()]


first_file = files[0]
name = first_file.name

from CNN import estructura
from FC import redneuronal
from manejo_archivos import gestion_imagenes, datos_filtros
import threading
import multiprocessing


def escribir():
    datos_filtros.escribir_filtros(CNN.c1.filtros, 1)
    datos_filtros.escribir_filtros(CNN.c2.filtros, 2)
    datos_filtros.escribir_filtros(CNN.c3.filtros, 3)

def leer():
    CNN.c1.filtros = datos_filtros.leer_filtros(CNN.c1.filtros, 1)
    CNN.c2.filtros = datos_filtros.leer_filtros(CNN.c2.filtros, 2)
    CNN.c3.filtros = datos_filtros.leer_filtros(CNN.c3.filtros, 3)

def entrenar(inicio):
    mapa = datos_filtros.map()
    for i in range(1000):
        cont = -1
        for clave in mapa:
            cont+=1
            print("ronda " + str(cont))
            if cont > inicio -1:
                image = gestion_imagenes.traer_imagen_prueba(str(clave)+".pgm")
                datos = CNN.forward(image)
                dato = rn.forward(datos, 1)
                print(dato)
                delta = rn.backward(1)
                delta = np.array(delta)
                CNN.backward(delta, image)
                escribir()

def clasificar():
    mapa = datos_filtros.map()
    acierto = 0
    fallo = 0
    for clave in mapa:
        image = gestion_imagenes.traer_imagen_prueba(str(clave)+".pgm")
        datos = CNN.forward(image)
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
    datos = CNN.forward(image)
    dato = rn.forwardClasifica(datos)
    print("dato devuelto", dato[0][0])

    return dato[0][0]*100

CNN = estructura.estructura()

rn = None

def process_image():
    global rn
    l = 0.5
    rn = redneuronal.redneuronal(64*126*126, 64, 64, 1, l)
    
    leer()
    #name es el nombre de la imagen guardada 
    image = gestion_imagenes.traer_imagen(name)

    respuesta = clasificarImagen(image)
    return respuesta

if __name__ == '__main__':
    process_image()

