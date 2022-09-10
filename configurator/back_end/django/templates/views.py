import inspect
from ...utils.utils import StringModify
from ....modules.Utilities.py.util import *
from ...utils.utils import DjangoRegex as DR
from ....modules.Utilities.py.file_manager import FileManager
FM = FileManager()


class ViewOptions():
    def __init__(self):
        print('Initialized ChoiceViews')
        self.imports = \
        {
            "default":
            [
                'from rest_framework.response import Response',
                'from rest_framework.views import APIView',
                'from .models import *',
                'from .serializer import *'
            ],
            "csrf":
            [
                "from django.utils.decorators import method_decorator",
                "from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt"
            ],
            "oauth":
            [
                "import django.contrib.auth as auth",
                "from rest_framework import status, permissions",
            ]
        }

        self.auth = \
        (inspect.cleandoc(
        """ 
            class LoginView(APIView):
                serializer_class = UserSerializer
                permission_classes = (permissions.AllowAny,)
                def post(self,request):
                    serialized_login = self.serializer_class(data = request.data, many = False)
                    if not serialized_login.is_valid():
                        return Response({{'Error': 'Invalid Credentials'}}, status = status.HTTP_403_FORBIDDEN)
                    username=serialized_login.data.get('username')
                    password=serialized_login.data.get('password')
            {session}
                    user_query=User.objects.filter(username=username)
                    if len(user_query) == 0:
                        return Response({{'Error': 'Invalid Credentials'}}, status = status.HTTP_403_FORBIDDEN)
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return Response({{'Success':'Authenticated'}}, status = status.HTTP_200_OK)
                    else:
                        return Response({{'Error': 'Invalid Credentials'}}, status = status.HTTP_403_FORBIDDEN)

        """),
        ["import django.contrib.auth as auth"])
        self.conds =\
            {
            'session':
                (inspect.cleandoc(
                """
                    if not request.session.exists(request.session.session_key):
                        request.session.create()
                """),[]),
            }









