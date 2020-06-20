## Código tomado de Detección de desenfoque con OpenCV por Adrian Rosebrock.
## Link: https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
## Instalar el paquete imutils=> pip install imutils.
## instalación openVC => http://acodigo.blogspot.com/2017/06/instalar-opencv-en-python.html
##Python Error:
##	Traceback (most recent call last):
##	  File   .... line 1, in <module>
##		import cv2
##	ModuleNotFoundError: No module named 'cv2'
##Solution:
##	cmd> pip install opencv-python
##
##Enviroment variable PC:
##Path=>	..\Python\Python38-32
##		..\Python\Python38-32\Scripts

from imutils import paths
import imutils
import argparse
import cv2


# Calcular la varianza del laplaciano, dada la imagen.
def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


# Se establece la ruta de la carpeta de imagenes.
# Se establece el umbral permitido.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", default="D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images")
ap.add_argument("-t", "--threshold", type=float, default=200.0)
args = vars(ap.parse_args())

# Recorrer la imagenes del la carpeta
# 1.- Se carga la imagen.
# 2.- Se convierte la imagen a escala de grises.
# 3.- Se calcula la medida de enfoque usando la varianza de laplaciano.
print("*********************CHECK IMAGE*************************************")
for imagePath in paths.list_images(args["images"]):
    image = cv2.imread(imagePath)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    round_fm = str(round(fm, 2))
    text = "Not Blurry"
    # Si la medida de enfoque es menor que el umbral, se considera borrosa
    if fm < args["threshold"]:
        text = "Blurry"
    print("Imagen:", imagePath, "=> Varianza:", round_fm, " =>", text)
print("*********************************************************************")
