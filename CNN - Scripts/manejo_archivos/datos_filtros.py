from io import open
from pathlib import Path

current_directory = Path.cwd()

def map():
    data_path = current_directory / 'CNN - Scripts' / 'datos_CNN' / 'info.txt'
    archivo = open(str(data_path), "r")

    texto = archivo.readlines()

    archivo.close()
    datos = {}

    for lines in texto:
        fracmentos = lines.strip().split(" ")
        valor = [1]
        if fracmentos[1].startswith("N"): valor = [0]
        datos[fracmentos[0]] = valor

    return datos

def escribir_filtros(filtros, numero):
    data_path = current_directory / 'CNN - Scripts' / 'filtros'
    with open(data_path / f'filtros{numero}.txt', "w") as archivo:
        escribir = ""
        for i in range(filtros.shape[0]):
            escribir += "X\n"
            for j in range(filtros.shape[1]):
                escribir += "Y\n"
                for k in range(filtros.shape[2]):
                    escribir += "Z\n"
                    for l in range(filtros.shape[3]):
                        escribir+= str(filtros[i][j][k][l]) + ' '
                    escribir +="\n"
                escribir +="\n"
        archivo.write(escribir)
            
def leer_filtros(matriz, numero):
    data_path = current_directory / 'CNN - Scripts' / 'filtros'
    with open(data_path / f'filtros{numero}.txt', "r") as archivo:
        contadorY = -1
        profundidad = -1
        contadorX = -1
        for line in archivo.readlines():
            frat = line.strip().split(" ")
            filtro = 0
            for tui in frat:
                if tui == 'X':
                    contadorY = -1
                    contadorX += 1
                elif tui == 'Y':
                    contadorY += 1
                elif tui == 'Z':
                    profundidad += 1
                elif tui == '':
                    profundidad = -1
                    continue
                else:
                    matriz[contadorX][contadorY][profundidad][filtro] = float(tui)
                    filtro += 1
        archivo.close
        return matriz
