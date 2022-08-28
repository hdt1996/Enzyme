class URLOptions():
    def __init__(self):
        self.imports = \
        {
            "default":
            [
                'from django.urls import path, include',
                'from .views import *'
            ]
        }