import numpy as np
import argparse
import imutils
from imutils import paths
import cv2
import urllib
from urllib import request

# grab the dimensions of the image and use the dimensions to
# derive the center (x, y)-coordinates
# compute the FFT to find the frequency transform, then shift
# the zero frequency component (i.e., DC component located at
# the top-left corner) to the center where it will be more
# easy to analyze
# zero-out the center of the FFT shift (i.e., remove low
# frequencies), apply the inverse shift such that the DC
# component once again becomes the top-left, and then apply
# the inverse FFT
# compute the magnitude spectrum of the reconstructed image,
# then compute the mean of the magnitude values
# the image will be considered "blurry" if the mean value of the
# magnitudes is less than the threshold value

def detect_blur_fft(image, size=60, thresh=10):
    (h, w) = image.shape
    (cX, cY) = (int(w / 2.0), int(h / 2.0))
    fft = np.fft.fft2(image)
    fft_shift = np.fft.fftshift(fft)
    fft_shift[cY - size:cY + size, cX - size:cX + size] = 0
    fft_shift = np.fft.ifftshift(fft_shift)
    recon = np.fft.ifft2(fft_shift)
    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)
    return mean, mean <= thresh


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str,
                default="D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images")
ap.add_argument("-t", "--thresh", type=int, default=20)
args = vars(ap.parse_args())

print("*********************CHECK IMAGE*************************************")
for imagePath in paths.list_images(args["images"]):
    orig = cv2.imread(imagePath)
    orig = imutils.resize(orig, width=500)
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    (mean, blurry) = detect_blur_fft(gray, size=60, thresh=args["thresh"])
    print("[INFO] Imagen:", imagePath, " => MVM-FFT: ", mean, " => ", ("Blurry" if blurry else "Not Blurry "))
print("*********************************************************************")
