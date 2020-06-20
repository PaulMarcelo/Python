from rest_framework import serializers
from .models import employees


class EmployessSerializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        #        fields = ('firsname', 'lastname')
        fields = '__all__'
