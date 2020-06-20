import base64
from io import BytesIO
import io

import cv2 as cv
import numpy as np
import scipy
from PIL import Image

input_filepath = 'D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\\0.jpg'
output1_filepath = 'D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\sharp\cat_sharpened_filter.jpg'
output2_filepath = 'D:\Python\Procesamiento imagenes\Laplaciano\BlurDetectionOpenvc\images\sharp\cat_sharpened_unmask.jpg'


def stringToRGB(base64_string):
    nparr = np.frombuffer(base64.b64decode(base64_string), np.uint8)
    return cv.imdecode(nparr, cv.IMREAD_ANYCOLOR)

    # imgdata = base64.b64decode(base64_string)
    # image = Image.open(io.BytesIO(imgdata))
    # return cv.cvtColor(np.array(image), cv.COLOR_BGR2RGB)


def byte_to_image(string_byte):
    jpg_original = base64.b64decode(string_byte)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv.imdecode(jpg_as_np, flags=1)
    return img


# Sharpens the image using Laplacian Filter.
def sharpen_image_with_kernel(image):
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv.filter2D(image, -1, sharpen_kernel)


# Sharpens the image using Unsharp Mark.
# Unsharp Mark is more robust to noise, because It first removes noise.
# Also, You can control the amount of sharpness.
def sharpen_image_with_unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred_image = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened_image = float(amount + 1) * image - float(amount) * blurred_image
    sharpened_image = np.maximum(sharpened_image, np.zeros(sharpened_image.shape))
    sharpened_image = np.minimum(sharpened_image, 255 * np.ones(sharpened_image.shape))
    sharpened_image = sharpened_image.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred_image) < threshold
        np.copyto(sharpened_image, image, where=low_contrast_mask)
    return sharpened_image


# image = cv.imread(input_filepath)
encoded = base64.b64encode(open(input_filepath, "rb").read())
print("Input: " + str(encoded))
image = byte_to_image(encoded)

# sharpened_image_kernel = sharpen_image_with_kernel(image)
sharpened_image_unsharp = sharpen_image_with_unsharp_mask(image)

# cv.imwrite(output1_filepath, sharpened_image_kernel)
# cv.imwrite(output2_filepath, sharpened_image_unsharp)

# encoded = base64.b64encode(open(output2_filepath, "rb").read())

image = cv.imread(input_filepath)
# pil_img = Image.fromarray(image.astype(np.uint8))

pil_img = Image.fromarray(image)
pil_img.save(output1_filepath)
# buff = BytesIO()
# pil_img.save(buff, format="PNG")
# new_image_string = base64.b64encode(buff.getvalue())


# print("Input: " + str(new_image_string))
# jpg_original = base64.b64decode(new_image_string)
# image = stringToRGB(new_image_string)
# cv.imshow('i', pil_img)
# cv.waitKey(0)
# cv.destroyWindow('i')
# cv.imwrite(output1_filepath, image)
