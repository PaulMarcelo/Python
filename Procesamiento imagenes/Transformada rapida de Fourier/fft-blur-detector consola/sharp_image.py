import base64

import cv2 as cv
import cv2
import numpy as np


def byte_to_image(string_byte):
    jpg_original = base64.b64decode(string_byte)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img


def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=1):
    blurred = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


# image = cv.imread('D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\\0.jpg')
encoded = base64.b64encode(
    open('D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\\0.jpg', "rb").read())
print("Input: " + str(encoded))
image = byte_to_image(encoded)
sharpened_image = unsharp_mask(image)
sharpened_image2 = unsharp_mask(sharpened_image)
img_as_string = cv2.imencode('.jpg', sharpened_image2)[1].tostring()

x = np.fromstring(sharpened_image2, dtype='uint8')

#decode the array into an image
img = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)

imagen_as_text = base64.b64encode(open(sharpened_image, "rb").read())
print("output: " + str(imagen_as_text))
imagen_result = byte_to_image(imagen_as_text)
cv2.imwrite('D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\sharp\sharpened-tv.jpg',
            imagen_result)
#
# cv.imwrite('D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\sharp\sharpened-tv.jpg',
#            sharpened_image2)
