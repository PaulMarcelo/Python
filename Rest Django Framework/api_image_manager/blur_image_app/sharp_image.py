import os

import numpy as np
import cv2
import base64

from api_image_manager.settings import MEDIA_ROOT


def sharpen_image_with_unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred_image = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened_image = float(amount + 1) * image - float(amount) * blurred_image
    sharpened_image = np.maximum(sharpened_image, np.zeros(sharpened_image.shape))
    sharpened_image = np.minimum(sharpened_image, 255 * np.ones(sharpened_image.shape))
    sharpened_image = sharpened_image.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred_image) < threshold
        np.copyto(sharpened_image, image, where=low_contrast_mask)
    return sharpened_image


def sharp_image(image, file_name_param):
    index_cart = file_name_param.find(".")
    if index_cart < 0:
        ext = 'jpg'
    else:
        ext = file_name_param.split(".")[-1]
    output_filepath = MEDIA_ROOT + "." + ext
    sharpened_image_unsharp = sharpen_image_with_unsharp_mask(image)
    cv2.imwrite(output_filepath, sharpened_image_unsharp)
    encoded = base64.b64encode(open(output_filepath, "rb").read())
    os.remove(output_filepath)
    return {"filename": file_name_param, "data": encoded}
