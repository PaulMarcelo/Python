import imutils
import numpy as np
import cv2
import base64


def byte_to_image(string_byte):
    jpg_original = base64.b64decode(string_byte)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img


def file_to_image(file):
    img = np.asarray(bytearray(file.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def resize_gray_image(image):
    orig_resize = imutils.resize(image, width=500)
    gray = cv2.cvtColor(orig_resize, cv2.COLOR_BGR2GRAY)
    return gray


def detect_blur_fft(image, size, thresh):
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


def evaluate_image(image, file_name_param, radio_value, thresh_value):
    image = resize_gray_image(image)
    (mean, blurry) = detect_blur_fft(image, radio_value, thresh_value)
    return {"filename": file_name_param, "value": mean, "isblur": blurry}
