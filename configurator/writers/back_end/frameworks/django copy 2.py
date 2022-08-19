from configurator.apis.Utilities.py.util import *
from configurator.apis.Utilities.py.file_manager import FileManager
from ..utils.regex import WriterRegex as WR, StringModify
from ..templates.django.models import *
from ..templates.django.settings import *
from ..templates.django.api import *
import os
FM = FileManager()

class DjangoTables():
    def __init__(self):
        self.dt_functions = ChoiceFunctions()
        self.dt_fields = ChoiceFields()
        self.dt_templates =\
        {
            'imports': ['from django.db import models'],
        }
        super().__init__()
    def modelImports(self):
        pass
    def modelClasses(self, table:str, field_dict: dict) -> list:
        properties, instance_methods, methods, imports = [], [], [], []
        commons = buildDictBoolbyArr(arr = ['char','text','int','float'])
        files = buildDictBoolbyArr(arr = ['img','file'])
        for field in field_dict:
            f_type =field_dict[field]['type']
            if f_type in commons:
                null = field_dict[field]['null']
                blank = field_dict[field]['blank']
                length = field_dict[field]['length']
                default= field_dict[field]['default']
                if isinstance(default, str):
                    default = f"'{default}'"
                pk = field_dict[field]['pk']
                inst_mths, imps = self.dt_functions.processCommonArgs(field = field, table = table, f_dict = field_dict[field])
                if len(inst_mths) > 0:
                    default = WR.matchCallFunction(declar = "def",txt = inst_mths['random'])
                instance_methods.extend(buildArrfromDict(data = inst_mths, kv = False))
                imports.extend(imps)
                properties.append(f"{field} = {self.dt_fields.fields[f_type].format(length = length, null = null, blank = blank, default = default, pk = pk)}")

            elif f_type in files:                
                null = field_dict[field]['null']
                blank = field_dict[field]['blank']
                mths, inst_mths, imps = self.dt_functions.processFileArgs(field = field, f_dict = field_dict[field])
                upload_to = field_dict[field]['upload_to']
                if len(inst_mths) > 0:
                    upload_to = WR.matchCallFunction(declar = "def",txt = inst_mths['upload_to'])
                methods.extend(mths)
                imports.extend(imps)
                instance_methods.extend(buildArrfromDict(data = inst_mths, kv = False))
                properties.append(f"{field} = {self.dt_fields.fields[f_type].format(null = null, blank = blank, upload_to = upload_to)}")
        return properties, instance_methods, methods, imports
        
    def modelFields(self):
        pass

    def processTables(self):
        oauth = self.server_settings["oauth"]
        app_dict = self.db_settings['tables']
        imp_template = list(self.dt_templates['imports'])
        prop_template = []
        if oauth:
            imp_template.append("from django.contrib.auth.models import User")
            prop_template.append("user = models.OneToOneField(User,on_delete=models.CASCADE)")
        for app in app_dict:
            txt = []
            models_py = os.path.join(self.app_locs[app],'models.py')
            imports = list(imp_template)
            classes = []
            for table in app_dict[app]:
                classes.append(f"class {table.capitalize()}(models.Model):")
                class_props = list(prop_template)
                props, inst_mths, mths, imps = self.modelClasses(table = table, field_dict = app_dict[app][table])
                class_props.extend(props)
                props = list(class_props)
                del class_props
                props= StringModify.addTabs(txt = '\n'.join(props), num_tabs = 1)
                inst_mths = '\n'.join(getDictUniques(dict_1 = buildDictBoolbyArr(inst_mths)))
                mths = '\n'.join(getDictUniques(dict_1 = buildDictBoolbyArr(mths)))
                imports.extend(imps)
                classes.append(inst_mths)
                classes.append(props)
                classes.append(mths)
                classes.append('\n')

            imports = getDictUniques(dict_1 = buildDictBoolbyArr(imports))
            txt.append('\n'.join(imports))
            txt.append('\n'.join(classes))
            txt = '\n\n'.join(txt)
            FM.writeText(file = models_py, text = txt, num_prefix = '_MODIFIED_', overwrite=True)


class DjangoSettings():
    def __init__(self):
        self.s_templates = ChoiceSettings()
        super().__init__()

    def setDatabase(self, txt: str):
        category, type = 'settings','database'
        engine = self.engines[self.db_settings['engine']]
        name=self.db_settings['name']
        user = self.db_settings['user']
        password = self.db_settings['password']
        host = self.db_settings['host']
        port = self.db_settings['port']   
        or_db_settings = self.s_templates.matchDBSetting(txt = txt)
        db_temp = self.s_templates.db.format(dbengine = engine, dbname = name,dbuser = user, dbpassword = password, dbhost = host, dbport = port)
        txt =  txt.replace(or_db_settings,db_temp)
        self.updateConf(curr_list = [or_db_settings], app_list = [db_temp], category = category, type = type)
        return txt

    def setInstalledApps(self,txt: str, cors: bool = False, oauth: bool = False):
        category, type = 'settings','apps'
        match, curr_list = WR.matchListVar(var_name = "INSTALLED_APPS",txt = txt)
        if match != False:
            app_list = self.s_templates.apps
            for app in self.app_locs:
                app_list.append(f"'{app}'")
            if cors:
                app_list.append(f"'corsheaders'")
            if oauth:
                app_list.append(f"'rest_framework'")
            app_str = ',\n    '.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            txt = txt.replace(match[0],var_str)
            self.updateConf(curr_list= curr_list, app_list = app_list, category=category,type=type)
            return txt
        raise ValueError('Failed Match for Settings - Installed Apps')

    def setMiddleWare(self,txt: str, cors: bool = False):
        category, type = 'settings','middleware'
        match, curr_list = WR.matchListVar(var_name = "MIDDLEWARE",txt = txt)
        if match != False:
            app_list = self.s_templates.middleware
            if cors:
                for index, app in enumerate(app_list):
                    if app == "'django.middleware.common.CommonMiddleware'":
                        app_list.insert(index, "'corsheaders.middleware.CorsMiddleware'")
                        break
            app_str = ',\n    '.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            txt = txt.replace(match[0],var_str)
            self.updateConf(curr_list= curr_list, app_list = app_list, category=category,type=type)
            return txt
        raise ValueError('Failed Match for Settings - Middleware')

    def setAllowHosts(self,txt: str, allowed_hosts: list):
        match, curr_list = WR.matchListVar(var_name = "ALLOWED_HOSTS",txt = txt)
        if match != False:
            app_list = []
            for h in allowed_hosts:
                app_list.append(f"'{h}'")
            app_str = ','.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            txt = txt.replace(match[0],var_str)
            return txt
        raise ValueError('Failed Match for Settings - Allowed Hosts')

    def setStorage(self,txt: str, type: str):
        loc = self.server_settings['storage'][type]['location'].replace('\\','/')
        url = self.server_settings['storage'][type]['url']
        root_var = f"{type.upper()}_ROOT"
        url_var = f"{type.upper()}_URL"
        match = WR.matchStrVar(var_name = root_var,txt = txt)
        if match != False:
            var_str = match[0].replace(f"'{match[1]}'",f"'{loc}'")
            txt = txt.replace(match[0],var_str)
        else:
            txt = txt.split('\n')
            txt.append(f"{root_var} = '{loc}'")
            txt = '\n'.join(txt)
        match = WR.matchStrVar(var_name = url_var,txt = txt)
        if match != False:
            var_str = match[0].replace(f"'{match[1]}'",f"'{url}'")
            txt = txt.replace(match[0],var_str)
        else:
            txt = txt.split('\n')
            txt.append(f"{url_var} = '{url}'")
            txt = '\n'.join(txt)
        return txt

    def setAuthentication(self, txt: str, oauth: bool, auth_type: str):
        if not oauth:
            return txt
        category, type = 'settings','oauth'
        auth_type = auth_type.split('|') if '|' in auth_type else auth_type
        match = self.s_templates.matchAuthSetting(txt = txt)
        oauth_template = self.s_templates.oauth
        permissions = ["\r    'rest_framework.permissions.IsAuthenticated'"]
        authentication = []
        if 'session' in auth_type:
            authentication.append("\r    'rest_framework.authentication.SessionAuthentication'")
        if 'token' in auth_type:
            authentication.append("'rest_framework.authentication.TokenAuthentication'")
        authentication = StringModify.addTabs(txt = ',\n'.join(authentication), num_tabs= 1)
        permissions = StringModify.addTabs(txt = ',\n'.join(permissions), num_tabs=1)
        oauth_template = oauth_template.format(permissions = permissions, authentication = authentication)
        if match != False:
            txt =  txt.replace(match,oauth_template)
            self.updateConf(curr_list = [match], app_list = [oauth_template], category = category, type = type)
        else:
            txt = txt.split('\n')
            txt.append(oauth_template)
            txt = '\n'.join(txt)
        return txt
class DjangoAPISerializer(ChoiceSerializer):
    def __init__(self, oauth: bool, table: str):
        self.classes = []
        self.ser_call = ''
        if oauth:
            self.classes.append(self.auth[0])
        self.table = table
        self.props = []
        self.lines = []
        self.ser_txt = []
        super().__init__()
        
    def apiSerializers(self, api_dict: dict):

        table = api_dict['table']
        trgt_fields = tuple(api_dict['fields'])
        validate = api_dict['validate']
        imps = '\n'.join(self.imports)
        class_dec = f"class {table}Serializer(ModelSerializer):"
        ser_call = WR.matchCallFunction('class',txt = class_dec)
        s_class = [class_dec]
        s_class.append(StringModify.addTabs(txt = self.meta[validate][0].format(table = table, fields = trgt_fields),num_tabs = 1))
        return '\n'.join(s_class), imps, ser_call
    def createSerializer(self):






class DjangoAPI():
    def __init__(self):
        self.v_templates = ChoiceAPI()
        self.ser_templates = ChoiceSerializer()
        super().__init__()

    def checkCSRF(self, app_csrf: bool, api_dict: dict):
        if not app_csrf:
            return []
        crud = api_dict['crud']
        csrf = api_dict['csrf']
        if csrf == 'ensure':
            decorator = f'@method_decorator(ensure_csrf_cookie, name = "{crud}")'
        else:
            decorator = f'@method_decorator(csrf_{csrf}, name = "{crud}")'
        return [decorator]

    def checkAuth(self, app_oauth: bool, auth_required: str|list):
        props = []
        if app_oauth:
            if auth_required:
                props.append(f"    permission_classes = (permissions.IsAuthenticated,)")
            else:
                props.append(f"    permission_classes = (permissions.AllowAny,)")
        return props

    def processAPIs(self):
        for app in self.api_settings:
            app_imps = list(self.v_templates.imports)
            app_ser_class, app_class, app_globals, views_txt, ser_txt = [],[],[],[], []
            app_oauth = self.api_settings[app]['oauth']
            app_auth_type = self.api_settings[app]['auth_type']
            app_auth_type = app_auth_type.split('|') if '|' in app_auth_type else app_auth_type
            app_csrf = self.api_settings[app]['csrf']
            if app_csrf:
                app_imps.append("from django.utils.decorators import method_decorator")
                app_imps.append("from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt")
            if app_oauth:
                login_api = self.v_templates.auth[0]
                if 'token' in app_auth_type:
                    app_imps.append("from rest_framework.authtoken.models import Token")
                if 'session' in app_auth_type:
                    sess_cond= StringModify.addTabs(txt = self.v_templates.conditionals['session'][0], num_tabs = 2)
                    app_imps.append('\n'.join(self.v_templates.conditionals['session'][1]))
                    app_class.append(login_api.format(session = sess_cond, csrf = '@method_decorator(csrf_exempt,name="post")' if app_csrf else ''))
                else:
                    app_class.append(login_api.format(session = ''))
                app_imps.append("import django.contrib.auth as auth")
                app_imps.append("from rest_framework import status, permissions")
                app_imps.append("from rest_framework.permissions import IsAuthenticated")
                app_ser_class.append(self.ser_templates.auth[0])
            views_py = os.path.join(self.app_locs[app],'views.py')
            serializer_py = os.path.join(self.app_locs[app],'serializer.py')
            views_dict = self.api_settings[app]['apis']
            for api in views_dict:
                app_props = []
                auth_required = views_dict[api]['auth_required']
                app_class.extend(self.checkCSRF(app_csrf = app_csrf, api_dict= views_dict[api]))
                app_class.append(f"class {api.capitalize()}(APIView):")
                ser_class, ser_imps, ser_call= self.apiSerializers(api_dict = views_dict[api])
                ser_txt.append(ser_imps)
                ser_txt.extend(app_ser_class)
                ser_txt.append(ser_class)
                imps, glbs, props, functs = self.apiFunctions(api_dict = views_dict[api])
                app_props.append(f"    serializer_class = {ser_call}")
                app_props.extend(self.checkAuth(app_oauth = app_oauth, auth_required = auth_required))
                app_props.extend(props)
                app_globals.extend(glbs)
                functs = StringModify.addTabs(txt = '\n'.join(functs), num_tabs = 1)
                app_class.extend(app_props)
                app_class.append(functs)
                app_class.append('\n')
                app_imps.extend(imps)
            ser_txt = getDictUniques(dict_1 = buildDictBoolbyArr(ser_txt))
            app_imps = getDictUniques(dict_1 = buildDictBoolbyArr(app_imps))
            app_globals = getDictUniques(dict_1 = buildDictBoolbyArr(app_globals))
            views_txt.append('\n'.join(app_imps))
            views_txt.append('\n'.join(app_globals))
            views_txt.append('\n'.join(app_class))
            views_txt = '\n\n'.join(views_txt)
            FM.writeText(file = serializer_py, text = '\n'.join(ser_txt), overwrite=True)
            FM.writeText(file = views_py, text = views_txt, overwrite= True)

    def apiSerializers(self, api_dict: dict):

        table = api_dict['table']
        trgt_fields = tuple(api_dict['fields'])
        validate = api_dict['validate']
        imps = '\n'.join(self.ser_templates.imports)
        class_dec = f"class {table}Serializer(ModelSerializer):"
        ser_call = WR.matchCallFunction('class',txt = class_dec)
        s_class = [class_dec]
        s_class.append(StringModify.addTabs(txt = self.ser_templates.meta[validate][0].format(table = table, fields = trgt_fields),num_tabs = 1))
        return '\n'.join(s_class), imps, ser_call

    def apiFunctions(self, api_dict: dict):
        glbs, props, imps, all_functs = [], [], [], []
        crud = api_dict['crud']   
        table = api_dict['table']
        fields = api_dict['fields']
        selectors = api_dict['selector']
        selector_values = api_dict['selector_value']
        selector_by_input = api_dict['selector_by_input']

        for c in crud:
            orm = DjangoORM(by_input = selector_by_input, selectors = selectors, selector_values = selector_values,table=table, crud = c)
            g, p, f  = orm.createQuery()
            glbs.extend(g)
            props.extend(p)
            all_functs.append(f)
        props = getDictUniques(dict_1 = buildDictBoolbyArr(props))
        return imps, glbs, props, all_functs

class DjangoORM(ChoiceORM):
    def __init__(self, table:str, by_input: bool, selectors: list, selector_values: list, crud: str):
        self.table = table
        self.by_input = by_input
        self.selectors = selectors
        self.selector_values = selector_values
        self.crud = crud
        self.props = []
        self.lines = []
        super().__init__()

    def addSelector(self, crud: str = None, by_input: bool = False, selector: dict = None):
        lines = []
        if by_input:
            var = self.vars['selectors'][crud][0]
        else:
            var = f"selectors =  {selector}"
        lines.append(StringModify.addTabs(txt = var, num_tabs = 1))
        return lines

    def createQuery(self):
        glbs, functs = [],[f"def {self.crud.lower()}(self, request):"]
        if self.by_input or self.selector_values:
            glbs.append(self.globals['queryOPs'][0])
        if self.by_input:
            self.processVariableInputs()
        else:
            self.processStaticInputs()
        functs.append('\n'.join(self.lines))
        functs = '\n'.join(functs)
        return glbs, self.props, functs
    def processVariableInputs(self):
        self.lines.extend(self.addSelector(crud = self.crud, by_input = self.by_input))
        selector_dict = str(buildDictBoolbyArr(arr = self.selectors))
        selector_line = self.queries['input'][0].format(table = self.table, fields = selector_dict)
        self.lines.append(StringModify.addTabs(txt = selector_line,num_tabs = 1))

    def processStaticInputs(self):
        if len(self.selectors) == 1 and self.selectors[0] == 'user': 
            self.lines.append(StringModify.addTabs(txt = self.queries['user'][0].format(table = self.table),num_tabs = 1))
        else:
            selector_dict = buildDictfromArrs(key_arr = self.selectors, value_arr = self.selector_values)
            self.props.extend(self.addSelector(by_input= self.by_input, selector = selector_dict))
            self.lines.append(StringModify.addTabs(txt = self.queries['base'][0].format(table = self.table),num_tabs = 1))

class DjangoWriter(DjangoSettings, DjangoTables, DjangoAPI):
    def __init__(self, server_name: str, config_data: dict):
        self.server_name = server_name
        self.engines=\
            {
                'postgres':'django.db.backends.postgresql_psycopg2'
            }

        self.server_loc = config_data['Server_Locations'][self.server_name]
        self.app_locs = config_data['App_Locations'][self.server_name]
        self.server_settings = config_data['Server_Settings'][self.server_name]
        self.db_settings = config_data['Database_Settings'][self.server_name]
        self.api_settings = config_data['API_Settings'][self.server_name]
        self.be_root = config_data['Back_End_Path']
        self.it_root = config_data['Root_Path']
        self.conf = {}
        self.conf['settings'] = self.setUpConf(loc = os.path.join(self.server_loc,'settings.py'),subcategory=['middleware','apps','database','oauth'])
        self.conf['tables'] = {}

        for app in self.app_locs:
            loc = os.path.join(self.app_locs[app],'models.py')
            if not os.path.isfile(loc):
                raise ValueError(f'FATAL ERROR: models.py in {app} folder does not exist!')
            self.conf['tables'][app] = self.setUpConf(loc = loc,
            subcategory=[table for table in self.db_settings['tables'][app]])

        with open(file = self.conf['settings']['loc'], mode = 'r', encoding = 'utf-8-sig') as s:
            txt = str(s.read())
            self.conf['settings']['text'] = txt
            s.close()
        super().__init__()

    def setUpConf(self, loc: os.PathLike, subcategory: list):
        conf_dict = \
        {
            'loc':loc,
            'text':None,
        }
        for subc in subcategory:
            conf_dict[subc] = {'removed':[],'added':[]}
        return conf_dict

    def updateConf(self, curr_list: list, app_list: list, category: str, type: str):
        app_uniques = buildDictBoolbyArr(arr = app_list)
        cur_uniques = buildDictBoolbyArr(arr = curr_list)
        self.conf[category][type]['added'] = getDictDiffArr(dict_1 = cur_uniques, dict_2 = app_uniques)
        self.conf[category][type]['removed'] = getDictDiffArr(dict_2 = cur_uniques, dict_1 = app_uniques)

    def processSettings(self):
        settings_py = self.conf['settings']['loc']
        txt = str(self.conf['settings']['text'])
        cors = self.server_settings["cors"]
        oauth = self.server_settings["oauth"]
        auth_type = self.server_settings["auth_type"]
        allowed_hosts = self.server_settings["allowed_hosts"]
        
        txt = self.setInstalledApps(txt = txt, cors = cors, oauth = oauth)
        txt = self.setDatabase(txt = txt)
        txt = self.setMiddleWare(txt = txt, cors = cors)
        txt = self.setAllowHosts(txt = txt, allowed_hosts=allowed_hosts)
        for st in self.server_settings['storage']:
            txt = self.setStorage(txt = txt, type = st)
        txt = self.setAuthentication(txt = txt, oauth = oauth, auth_type = auth_type)
        FM.writeText(file = settings_py,text = txt, num_prefix="_COPY_", overwrite= True)

    def processContainer(self):
        port = self.server_settings["port"] #For Docker-Compose/NGINX to Use
        containers = self.server_settings["containers"] #Not required for django but is for NGINX deployment

    def process(self):
        print(DjangoWriter.__mro__)
        self.processSettings()
        self.processTables()
        self.processAPIs()