import os

from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import cv2
import numpy as np
import urllib.request as rq
import imutils

from fileuploadexample import settings
from .serializers import FileSerializer


def urlToImage(url):
    resp = rq.urlopen(url)
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def fileToImage(file):
    img = np.asarray(bytearray(file.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def check_image(image_path):
    image = urlToImage(image_path)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    round_fm = str(round(fm, 2))
    text = "Not Blurry"
    if fm < 200:
        text = "Blurry"
    print("Imagen:", image_path, "=> Varianza:", round_fm, " =>", text)


def check_image_file(file):
    image = fileToImage(file)
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return variance_of_laplacian(gray)


@api_view(["POST"])
# @parser_classes([JSONParser])
def polls_list(request, format=None):
    file_obj = request.data['file']
    if file_obj == '':
        return Response("File no puede ser null", status=status.HTTP_400_BAD_REQUEST)
    fm = check_image_file(file_obj)
    round_fm = str(round(fm, 2))
    text = "Not Blurry"
    if fm < 200:
        text = "Blurry"
    data = {"filename": file_obj.name, "varianza": round_fm, "results": text}
    return Response(data, status=status.HTTP_200_OK)


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']

        file_serializer = FileSerializer(data=request.data)

        # file_serializer = FileSerializer(data=request.data.get("file"))

        if file_serializer.is_valid():
            file_serializer.save()
            path_file = file_serializer.data["file"]
            image_path = "http://127.0.0.1:8000" + path_file
            check_image(image_path)
            # data_file = file_serializer.data["data"]
            # print(data_file)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #
        # file_upload_dir = os.path.join(settings.MEDIA_ROOT, 'media')
        # print(file_upload_dir)
        # if os.path.exists(file_upload_dir):
        #     print("Paso 1")
        #     import shutil
        #     shutil.rmtree(file_upload_dir)

