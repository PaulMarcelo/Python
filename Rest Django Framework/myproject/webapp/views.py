from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import employees
from .serializers import EmployessSerializer


class emplyeeList(APIView):
    parser_class = (FileUploadParser,)

    def get(self, request):
        employees1 = employees.objects.all()
        seializer = EmployessSerializer(employees1, many=True)
        return Response(seializer.data)

    def put(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        print("File Name:")
        mymodel.my_file_field.save(f.name, f, save=True)
        return Response(status=status.HTTP_201_CREATED)