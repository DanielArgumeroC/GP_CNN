from skimage import io, transform, color
from pathlib import Path
import shutil

current_directory = Path.cwd()

def traer_imagen(imagen_name):
    # Construir la ruta completa al archivo de imagen
    image_path = current_directory / 'WebApp' / 'Server' / 'uploads' / imagen_name
    image = io.imread(image_path)
    image_resize = transform.resize(image, (144, 144))
    if image_resize.shape[2] == 4:
        image_resize = image_resize[:,:,:3]
    return image_resize

def traer_imagen_prueba(imagen_name):
    # Construir la ruta completa al archivo de imagen
    image_path = current_directory / 'CNN - Scripts' / 'datos_CNN' / imagen_name
    image = io.imread(image_path)
    image_resize = transform.resize(image, (144, 144))
    if image_resize.ndim == 2:
        image_resize = color.gray2rgb(image_resize)

    if image_resize.ndim == 3 and image_resize.shape[2] == 4:
        image_resize = image_resize[:,:,:3]
    
    return image_resize

def clasificar(imagen_name, clasificacion):
    carpeta = "Normal"
    path = current_directory / 'CNN - Scripts' / 'datos_CNN' / imagen_name
    if clasificacion == 1:
        carpeta = "Anormal"
    new_path = current_directory / 'CNN - Scripts' / 'clasificacion' / carpeta / imagen_name
    shutil.move(path, new_path)