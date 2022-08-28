import inspect

class ChoiceSerializer():
    def __init__(self):
        self.auth = \
        (inspect.cleandoc(
        """
            class UserSerializer(ModelSerializer):
                class Meta:
                    model = User
                    fields = '__all__'
        """),[])


        self.imports =\
        {
            'from rest_framework.serializers import ModelSerializer',
            'from rest_framework import serializers',
            'from .models import *'
        }
        self.meta =\
        {
            'include':
            (inspect.cleandoc(
            """
                class Meta:
                    model = {table}
                    fields = {fields}
            """),[]),
            'exclude':
            (inspect.cleandoc(
            """
                class Meta:
                    model = {table}
                    exclude = {fields}
            """),[]),
        }
