from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import cv2
from imutils import paths
import argparse

@api_view(["POST"])
def IdealWeight(heightdata):
    checkImage()
    try:
        height = json.loads(heightdata.body)
        weight = str(height * 10)
        return JsonResponse("Ideal weight should be: " + weight + " kg", safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_Bad_REQUEST)


def checkImage():
    images = "D:\Python\BlurDetectionOpenvc\images"
    threshold = 100.0
    print("*********************CHECK IMAGE*************************************")
    for imagePath in paths.list_images(images):
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fm = variance_of_laplacian(gray)
        round_fm = str(round(fm, 2))
        text = "Not Blurry"
        if fm < threshold:
            text = "Blurry"
        print("Imagen:", imagePath, "=> Varianza:", round_fm, " =>", text)
    print("*********************************************************************")


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()
