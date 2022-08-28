from .....modules.Utilities.py.file_manager import FileManager
from ..components.crud import *
from .serializer import *
from ..templates.views import *
from .url import *
import os
FM = FileManager()

class DjangoViews():
    def __init__(self, app_oauth: bool, app_csrf: bool, app_auth_type: bool, view_loc: os.PathLike, ser_loc: os.PathLike, url_loc: os.PathLike):
        print('Initialized DjangoViews')

        self.apis = []
        self.app_oauth = app_oauth
        self.view_class = []
        self.view_globals = []
        self.view_loc = view_loc
        self.tmp_views = ViewOptions()
        self.SERIALIZER = DjangoSerializer(app_oauth = app_oauth, loc = ser_loc)
        self.URLS = DjangoURLS(app_oauth = app_oauth, loc = url_loc)
        self.METHODS = ViewMethods(ser_instance=self.SERIALIZER, tmp_instance = self.tmp_views, app_csrf = app_csrf)

        self.view_imports = self.tmp_views.imports['default']
        if app_csrf:
            self.view_imports.extend(self.tmp_views.imports['csrf'])
        if app_oauth:
            imps, api = self.METHODS.addLoginAPI(app_csrf= app_csrf, app_auth_type = app_auth_type)
            self.view_imports.extend(imps)
            self.apis.append(api)
            self.view_imports.extend(self.tmp_views.imports['oauth'])

    def checkViewAuth(self, auth_required: str|list):
        props = []
        if self.app_oauth:
            if auth_required:
                props.append(f"    permission_classes = (permissions.IsAuthenticated,)")
            else:
                props.append(f"    permission_classes = (permissions.AllowAny,)")
        return props

    def prepAPI(self, api_dict: dict, api_name: str):
        api = [f"class {api_name}(APIView):"]
        auth_required = api_dict['auth_required']
        url = api_dict['url']
        self.URLS.prepURLs(url = url, api_name = api_name)
        imps, glbs, props, methods, srs = self.METHODS.prepMethods(api_dict = api_dict, api_name = api_name)
        self.view_imports.extend(imps)
        self.view_globals.extend(glbs)
        api_props = [StringModify.addTabs(txt = f"{crud}serializer_class = {srs[crud]}",num_tabs = 1) for crud in srs]
        api_props.extend(self.checkViewAuth(auth_required = auth_required))
        api_props.extend(props)
        api.extend(api_props)
        api.append(methods)
        api.append('\n')
        api = '\n'.join(api)
        self.apis.append(api)

    def writeViews(self):
        self.view_imports = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.view_imports)))
        self.view_globals = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.view_globals)))
        views_txt = [self.view_imports,self.view_globals]
        views_txt.append('\n'.join(self.apis))
        views_txt = '\n'.join(views_txt)
        FM.writeText(file = self.view_loc,text = views_txt, overwrite=True)


class ViewMethods():
    def __init__(self, ser_instance: DjangoSerializer, tmp_instance: ViewOptions, app_csrf: bool):
        self.methods = []
        self.imports = []
        self.globals = []
        self.SERIALIZER = ser_instance
        self.tmp_views = tmp_instance
        self.CRUD = DjangoCRUD()
        self.app_csrf = app_csrf

    def prepMethods(self, api_dict: dict, api_name: str):
        view_glbs, view_prps, view_imps, view_srs ,view_methods= [], [], [], {}, []
       
        for crud in ['GET','POST','PUT','DELETE']:     
            if not crud in api_dict:
                continue
            view_srs[crud]= self.SERIALIZER.prepareSerializer(api_dict = api_dict[crud], table = api_dict['table'], crud = crud, api_name = api_name)
            g, p, m, i= self.CRUD.createMethod(crud = crud, crud_options = api_dict[crud], table_name = api_dict['table'])
            view_glbs.extend(g)
            view_prps.extend(p)
            view_imps.extend(i)
            method = []
            method.append('\n'.join(self.checkCSRF(api_crud = crud, api_csrf = api_dict[crud]['csrf']  )))
            method.append(m)
            method = '\n'.join(method)
            view_methods.append(method)

        view_prps = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(view_prps))
        view_methods = StringModify.addTabs(txt = '\n'.join(view_methods), num_tabs = 1)
        return view_imps, view_glbs, view_prps, view_methods, view_srs
        
    def checkCSRF(self, api_csrf: str, api_crud: str):
        if not self.app_csrf:
            return []
        if api_csrf == 'ensure':
            decorator = f'@method_decorator(ensure_csrf_cookie, name = "{api_crud.lower()}")'
        elif api_csrf == 'exempt':
            decorator = f'@method_decorator(csrf_exempt,name="{api_crud.lower()}")'
        else:
            decorator = f'@method_decorator(csrf_protect, name = "{api_crud.lower()}")'
        return [decorator]


    def addLoginAPI(self, app_csrf: bool, app_auth_type: str):
        imps = []
        funct = self.tmp_views.auth[0].format(session = self.checkSession(auth_type = app_auth_type))
        api = ['\n'.join(self.checkCSRF(api_csrf = 'ensure', api_crud = 'POST')) if app_csrf else '', funct]
        if 'token' in app_auth_type:
            imps.append("from rest_framework.authtoken.models import Token")
        api = '\n'.join(api)
        return imps, api

    def checkSession(self, auth_type: str):
        if 'session' in auth_type:
            sess_cond= StringModify.addTabs(txt = self.tmp_views.conds['session'][0], num_tabs = 2)
        else:
            sess_cond = ''
        return sess_cond
        