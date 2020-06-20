from django.urls import path
from .views import *

urlpatterns = [
    path("isBlurFromImageFile/", is_blur_image_from_file, name="is_blur_image_from_file"),
    path("isBlurFromImageByte/", is_blur_image_from_byte, name="is_blur_image_from_byte"),
    path("sharpFromImageFile/", sharp_image_from_file, name="sharp_image_from_file"),
    path("sharpFromImageByte/", sharp_image_from_byte, name="sharp_image_from_byte"),
]
