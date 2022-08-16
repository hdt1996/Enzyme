#to turn python object into JSON format
from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers
from rest_framework import serializers
from .models import *

class CSSPropSerializer(ModelSerializer):
    class Meta:
        model = CssProperties
        fields='__all__'