from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from .blur_image import file_to_image, byte_to_image, evaluate_image
from .sharp_image import sharp_image

THRESH_DEFAULT = 20
RADIO_DEFAULT = 60

FILE_PARAM = "file"
THRESH_PARAM = "thresh"
RADIO_PARAM = "radio"

DATA_PARAM_JSON = "data"
FILE_NAME_PARAM_JSON = "filename"
FILE_NAME_DEFAULT = "Archivo"


def exist_param_from_json(json_data, param):
    try:
        return json_data[param]
    except Exception:
        return False


def exist_param(request, param):
    try:
        return request.data[param]
    except MultiValueDictKeyError:
        return False


def evaluate_param(param, defaul_value):
    if not param:
        return defaul_value
    else:
        return int(param)


@api_view(["POST"])
def is_blur_image_from_file(request, format=None):
    file_param = exist_param(request, FILE_PARAM)
    if not file_param:
        return Response(FILE_PARAM + " no puede ser null", status=status.HTTP_400_BAD_REQUEST)

    try:
        thresh_param = exist_param(request, THRESH_PARAM)
        thresh_value = evaluate_param(thresh_param, THRESH_DEFAULT)
        radio_param = exist_param(request, RADIO_PARAM)
        radio_value = evaluate_param(radio_param, RADIO_DEFAULT)
    except Exception as ex:
        return Response("Error: " + str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    image = file_to_image(file_param)
    data = evaluate_image(image, file_param.name, radio_value, thresh_value)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def is_blur_image_from_byte(request):
    try:
        json_data = JSONParser().parse(request)
        array_byte_param = exist_param_from_json(json_data, DATA_PARAM_JSON)
        if not array_byte_param:
            return Response(DATA_PARAM_JSON + " no puede ser null", status=status.HTTP_400_BAD_REQUEST)
        thresh_param = exist_param_from_json(json_data, THRESH_PARAM)
        thresh_value = evaluate_param(thresh_param, THRESH_DEFAULT)
        radio_param = exist_param_from_json(json_data, RADIO_PARAM)
        radio_value = evaluate_param(radio_param, RADIO_DEFAULT)
        file_name_param = exist_param_from_json(json_data, FILE_NAME_PARAM_JSON)
        if not file_name_param:
            file_name_param = FILE_NAME_DEFAULT
    except Exception as ex:
        return Response("Error: " + str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    image = byte_to_image(array_byte_param)
    data = evaluate_image(image, file_name_param, radio_value, thresh_value)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def sharp_image_from_file(request, format=None):
    file_param = exist_param(request, FILE_PARAM)
    if not file_param:
        return Response(FILE_PARAM + " no puede ser null", status=status.HTTP_400_BAD_REQUEST)
    image = file_to_image(file_param)
    data = sharp_image(image, file_param.name)
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def sharp_image_from_byte(request):
    try:
        json_data = JSONParser().parse(request)
        array_byte_param = exist_param_from_json(json_data, DATA_PARAM_JSON)
        if not array_byte_param:
            return Response(DATA_PARAM_JSON + " no puede ser null", status=status.HTTP_400_BAD_REQUEST)
        file_name_param = exist_param_from_json(json_data, FILE_NAME_PARAM_JSON)
        if not file_name_param:
            file_name_param = FILE_NAME_DEFAULT
    except Exception as ex:
        return Response("Error: " + str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    image = byte_to_image(array_byte_param)
    data = sharp_image(image, file_name_param)
    return Response(data, status=status.HTTP_200_OK)
