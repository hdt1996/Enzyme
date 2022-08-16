from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .models import *
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import django.contrib.auth as auth
from .serializer import CSSPropSerializer
class GetCSSProps(APIView):
    serializer = CSSPropSerializer
    def get(self, request):
        props = CssProperties.objects.all()
        serial_data = self.serializer(props, many = True)
        return Response(serial_data.data, status = status.HTTP_200_OK)




