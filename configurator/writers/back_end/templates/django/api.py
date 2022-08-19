import inspect
from ...utils.regex import StringModify

class ChoiceAPI():
    def __init__(self):
        print('Initialized ChoiceAPI')
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
                "from rest_framework.permissions import IsAuthenticated"
            ]
        }

        self.auth = \
        (inspect.cleandoc(
        """ 
            {csrf}
            class LoginView(APIView):
                serializer_class = UserSerializer
                permission_classes = (permissions.AllowAny,)
                def post(self,request):
                    username=request.data['username']
                    password=request.data['password']
            {session}
                    user_query=User.objects.filter(username=username)
                    if len(user_query) == 0:
                        return Response({{'Error': 'Invalid Credentials'}})
                    user = auth.authenticate(username=username, password=password)
                    if user is not None:
                        auth.login(request, user)
                        return Response({{'Success':'Authenticated'}})
                    else:
                        return Response({{'Error': 'Invalid Credentials'}})
        """),
        ["import django.contrib.auth as auth"])
        self.conditionals =\
            {
            'session':
                (inspect.cleandoc(
                """
                    if not request.session.exists(request.session.session_key):
                        request.session.create()
                """),[]),
            }

class ChoiceSerializer():
    def __init__(self):
        self.auth = \
        (inspect.cleandoc("""
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

class ChoiceORM():
    def __init__(self):
        self.globals = \
        {
            'queryOPs':
                (inspect.cleandoc(
                """
                    QUERY_OPTIONS = \\
                    {{
                        'greater':'__gt',
                        'greater-equal':'__gte',
                        'lesser':'__lt',
                        'lesser-equal':'__lte',
                    }}
                """),[]),
        }
        self.queries =\
        {
            'input':
                (inspect.cleandoc(
                """
                    if selectors == None:
                        return Response({{'Selector_Error':'No Search Parameters passed in'}})
                    allowed_fields = {fields}
            
                    sel_dict = {{}}
                    if isinstance(selectors, dict):
                        for field in selectors:
                            oper = selectors[field]['operation']
                            if oper in QUERY_OPTIONS:
                                sel_dict[f"{{field}}{{QUERY_OPTIONS[oper]}}"] = selectors[field]['value']
                            if field not in allowed_fields:
                                return Response({{'Selector_Error':'Unallowed field passed in'}})
                    else:
                        return Response({{'Selector_Error':f'{{type(selectors)}} is not allowed. Dict object only'}})
                    del selectors
                    table_query = {table}.objects.filter(**sel_dict)
                """),[]),
            'user':
                (inspect.cleandoc(
                """
                    table_query = {table}.objects.filter(user = request.user)
                """
                ),[]),
            'base':
                (inspect.cleandoc(
                """
                    sel_dict = {{}}
                    if isinstance(self.selectors, dict):
                        for field in self.selectors:
                            oper = self.selectors[field]['operation']
                            if oper in QUERY_OPTIONS:
                                sel_dict[f"{{field}}{{QUERY_OPTIONS[oper]}}"] = self.selectors[field]['value']
                    else:
                        return Response({{'Core_Logic_Error':f'{{type(self.selectors)}} is not allowed. Dict object only'}})
                    table_query = {table}.objects.filter(**sel_dict)
                """),[])
            } 
        self.vars =\
        {
            'selectors':
            {
                'GET':
                    (inspect.cleandoc(
                    """
                        "selectors =  request.GET.get('selector_value')"
                    """
                    ),[]),
                'DELETE':
                    (inspect.cleandoc(
                    """
                        "selectors =  request.data.get('selector_value')"
                    """
                    ),[]),
                'PUT':
                    (inspect.cleandoc(
                    """
                        "selectors =  request.data.get('selector_value')"
                    """
                    ),[]),
                'POST':
                    (inspect.cleandoc(
                    """
                        "selectors =  request.data.get('selector_value')"
                    """
                    ),[])
            }

        }
          