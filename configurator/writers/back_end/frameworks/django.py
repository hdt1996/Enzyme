from configurator.apis.Utilities.py.util import *
from configurator.apis.Utilities.py.file_manager import FileManager
from ..utils.regex import WriterRegex as WR, StringModify
from ..templates.django.models import *
from ..templates.django.settings import *
from ..templates.django.api import *
import os
FM = FileManager()

class DjangoTables(ChoiceTableFunctions,ChoiceTableFields):
    def __init__(self, server_oauth: bool, loc: os.PathLike):
        print('Initialized DjangoTables')
        super().__init__()
        self.imports = \
            {
                'user':"from django.contrib.auth.models import User"
            }
        self.table_props = []
        self.table_imports = ['from django.db import models']
        self.table_classes = []
        self.table_globals = []
        self.field_props = []
        self.field_imports = []
        self.field_methods = []
        self.field_inst_methods = []
        self.loc = loc
        if server_oauth:
            self.table_imports.append(self.imports['user'])
            self.table_props.append(inspect.cleandoc(f"user = {self.fields['user']}"))
        self.field_types =\
        {
            "commons":buildDictBoolbyArr(arr = ['char','text','int','float']),
            "files":buildDictBoolbyArr(arr = ['img','file'])
        }

    def processCommonFields(self, field_dict: dict, table:str, field:str, f_type: str):
        null = field_dict['null']
        blank = field_dict['blank']
        length = field_dict['length']
        default= field_dict['default']
        if isinstance(default, str):
            default = f"'{default}'"
        pk = field_dict['pk']
        inst_mths, imps = self.processCommonArgs(field = field, table = table, f_dict = field_dict)
        if len(inst_mths) > 0:
            default = WR.matchCallFunction(declar = "def",txt = inst_mths['random'])
        self.field_inst_methods.extend(buildArrfromDict(data = inst_mths, kv = False))
        self.field_imports.extend(imps)
        self.field_props.append(f"{field} = {self.fields[f_type].format(length = length, null = null, blank = blank, default = default, pk = pk)}")

    def processFileFields(self, field_dict: dict, field:str, f_type: str = None):
        null = field_dict['null']
        blank = field_dict['blank']
        mths, inst_mths, imps = self.processFileArgs(field = field, f_dict = field_dict)
        upload_to = field_dict['upload_to']
        if len(inst_mths) > 0:
            upload_to = WR.matchCallFunction(declar = "def",txt = inst_mths['upload_to'])
        self.field_methods.extend(mths)
        self.field_imports.extend(imps)
        self.field_inst_methods.extend(buildArrfromDict(data = inst_mths, kv = False))
        self.field_props.append(f"{field} = {self.fields[f_type].format(null = null, blank = blank, upload_to = upload_to)}")
        
    def prepareFields(self, table:str, table_dict: dict) -> list:
        for field in table_dict:
            f_type =table_dict[field]['type']
            if f_type in self.field_types['commons']:
                field_dict = table_dict[field]
                self.processCommonFields(field_dict = field_dict, table = table, field=field, f_type= f_type)

            elif f_type in self.field_types['files']:
                field_dict = table_dict[field]                
                self.processFileFields(field_dict = field_dict, field=field, f_type = f_type)
        return self.field_props, self.field_inst_methods, self.field_methods, self.field_imports
        
    def prepareTables(self, table: str, table_dict:dict):
        self.table_classes.append(f"class {table.capitalize()}(models.Model):")
        t_props = list(self.table_props)
        prps, inst_mths, mths, imps = self.prepareFields(table = table, table_dict = table_dict)
        t_props.extend(prps)
        t_props = StringModify.addTabs(txt = '\n'.join(t_props), num_tabs = 1)
        inst_mths = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(inst_mths)))
        mths = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(mths)))
        self.table_imports.extend(imps)
        self.table_classes.append(inst_mths)
        self.table_classes.append(t_props)
        self.table_classes.append(mths)
        self.table_classes.append('\n')

    def writeTables(self):
        self.table_imports = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.table_imports))
        self.table_globals = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.table_globals))
        table_txt = ['\n'.join(self.table_imports),'\n'.join(self.table_globals),'\n'.join(self.table_classes)]
        table_txt = '\n\n'.join(table_txt)
        FM.writeText(file = self.loc,text = table_txt, overwrite=True)


class DjangoSettings(ChoiceSettings):
    def __init__(self):
        print('Initialized DjangoSettings')
        super().__init__()

    def setDatabase(self, txt: str):
        category, type = 'settings','database'
        engine = self.engines[self.db_settings['engine']]
        name=self.db_settings['name']
        user = self.db_settings['user']
        password = self.db_settings['password']
        host = self.db_settings['host']
        port = self.db_settings['port']   
        or_db_settings = self.matchDBSetting(txt = txt)
        db_temp = self.databases.format(dbengine = engine, dbname = name,dbuser = user, dbpassword = password, dbhost = host, dbport = port)
        txt =  txt.replace(or_db_settings,db_temp)
        self.updateConf(curr_list = [or_db_settings], app_list = [db_temp], category = category, type = type)
        return txt

    def setInstalledApps(self,txt: str, cors: bool = False, oauth: bool = False):
        category, type = 'settings','apps'
        match, curr_list = WR.matchListVar(var_name = "INSTALLED_APPS",txt = txt)
        if match != False:
            app_list = list(self.installed_apps)
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
            app_list = self.middleware
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
        match = self.matchAuthSetting(txt = txt)
        oauth_template = self.rest_framework
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

class DjangoSerializer(ChoiceSerializer):
    def __init__(self, app_oauth: bool, loc: str):
        print('Initialized DjangoSerializer')
        super().__init__()
        self.ser_classes = []
        self.ser_imports = []
        self.ser_call = ''
        self.ser_props = []
        self.loc = loc

        if app_oauth:
            self.ser_classes.append(self.auth[0])
        
    def prepareSerializer(self, api_dict: dict):
        table = api_dict['table']
        fields = tuple(api_dict['fields'])
        validate = api_dict['validate']
        imps = '\n'.join(self.imports)
        s_class = [f"class {table}Serializer(ModelSerializer):"]
        self.ser_call = WR.matchCallFunction('class',txt = s_class[0])
        m_class = StringModify.addTabs(txt = self.meta[validate][0].format(table = table, fields = fields),num_tabs = 1)
        s_class.append(m_class)
        self.ser_classes.extend(s_class)
        self.ser_imports.append(imps)
    def writeSerializer(self):
        self.ser_imports = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.ser_imports))
        ser_text = '\n'.join(['\n'.join(self.ser_imports),'\n'.join(self.ser_classes)])
        FM.writeText(file = self.loc, text = ser_text, overwrite=True)


class DjangoViews(ChoiceAPI):
    def __init__(self, app_oauth: bool, app_csrf: bool, app_auth_type: bool, loc: os.PathLike):
        print('Initialized DjangoViews')
        super().__init__()
        self.app_csrf = app_csrf
        self.app_auth_type = app_auth_type
        self.app_oauth = app_oauth
        self.view_class = []
        self.view_globals = []
        self.loc = loc

        self.view_imports = self.imports['default']
        if app_csrf:
            self.view_imports.extend(self.imports['csrf'])
        if app_oauth:
            self.processAuthType()
            self.view_imports.extend(self.imports['oauth'])

    def checkViewAuth(self, auth_required: str|list):
        props = []
        if self.app_oauth:
            if auth_required:
                props.append(f"    permission_classes = (permissions.IsAuthenticated,)")
            else:
                props.append(f"    permission_classes = (permissions.AllowAny,)")
        return props

    def processAuthType(self):
        login_api = self.auth[0]
        if 'token' in self.app_auth_type:
            self.view_imports.append("from rest_framework.authtoken.models import Token")
        if 'session' in self.app_auth_type:
            sess_cond= StringModify.addTabs(txt = self.conditionals['session'][0], num_tabs = 2)
            self.view_imports.append('\n'.join(self.conditionals['session'][1]))
            self.view_class.append(login_api.format(session = sess_cond, csrf = '@method_decorator(csrf_exempt,name="post")' if self.app_csrf else ''))
        else:
            self.view_class.append(login_api.format(session = '', csrf = ''))

    def checkCSRF(self, api_csrf: bool, api_crud: str):
        if not self.app_csrf:
            return []
        if api_csrf == 'ensure':
            decorator = f'@method_decorator(ensure_csrf_cookie, name = "{api_crud}")'
        else:
            decorator = f'@method_decorator(csrf_{api_csrf}, name = "{api_crud}")'
        return [decorator]

    def prepFunctions(self, api_dict: dict):
        glbs, props, imps, functs = [], [], [], []
        crud = api_dict['crud']  
        fields = api_dict['fields']

        dj_orm = DjangoORM(api_dict = api_dict)
        for c in crud:
            dj_orm.setAttribs(crud = c)
            g, p, f  = dj_orm.createQuery()
            glbs.extend(g)
            props.extend(p)
            functs.append(f)
        props = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(props))
        functs = StringModify.addTabs(txt = '\n'.join(functs), num_tabs = 1)
        return imps, glbs, props, functs

    def prepareViews(self, api_dict: dict, api_name: str, ser_call: str):
        api_props = []
        api_crud = api_dict['crud']
        api_csrf = api_dict['csrf']
        auth_required = api_dict['auth_required']
        self.view_class.extend(self.checkCSRF(api_crud = api_crud, api_csrf = api_csrf))
        self.view_class.append(f"class {api_name.capitalize()}(APIView):")
        imps, glbs, props, functs = self.prepFunctions(api_dict = api_dict)
        api_props.append(f"    serializer_class = {ser_call}")
        api_props.extend(self.checkViewAuth(auth_required = auth_required))
        api_props.extend(props)
        self.view_globals.extend(glbs)
        self.view_class.extend(api_props)
        self.view_class.append(functs)
        self.view_class.append('\n')
        self.view_imports.extend(imps)

    def writeViews(self):
        self.view_imports = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.view_imports))
        self.view_globals = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.view_globals))
        views_txt = ['\n'.join(self.view_imports),'\n'.join(self.view_globals),'\n'.join(self.view_class)]
        views_txt = '\n\n'.join(views_txt)
        FM.writeText(file = self.loc,text = views_txt, overwrite=True)


class DjangoORM(ChoiceORM):
    def __init__(self, api_dict: dict):
        print('Initialized DjangoORM')
        super().__init__()
        self.props = []
        self.lines = []
        self.crud = None 
        self.table = api_dict['table']
        self.selectors = api_dict['selector']
        self.selector_values = api_dict['selector_value']
        self.by_input = api_dict['selector_by_input']


    def addSelector(self, by_input: bool = False, prop_selector: dict = None):
        lines = []
        if by_input:
            var = self.vars['selectors'][self.crud][0]
        else:
            var = f"selectors =  {prop_selector}"
        lines.append(StringModify.addTabs(txt = var, num_tabs = 1))
        return lines

    def setAttribs(self, crud: str):
        self.props = []
        self.lines = []
        self.crud = crud

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
        self.lines.extend(self.addSelector(by_input = self.by_input))
        selector_dict = str(buildDictBoolbyArr(arr = self.selectors))
        selector_line = self.queries['input'][0].format(table = self.table, fields = selector_dict)
        self.lines.append(StringModify.addTabs(txt = selector_line,num_tabs = 1))

    def processStaticInputs(self):
        if len(self.selectors) == 1 and self.selectors[0] == 'user': 
            self.lines.append(StringModify.addTabs(txt = self.queries['user'][0].format(table = self.table),num_tabs = 1))
        else:
            selector_dict = buildDictfromArrs(key_arr = self.selectors, value_arr = self.selector_values)
            self.props.extend(self.addSelector(by_input= self.by_input, prop_selector = selector_dict))
            self.lines.append(StringModify.addTabs(txt = self.queries['base'][0].format(table = self.table),num_tabs = 1))

class DjangoWriter(DjangoSettings):
    def __init__(self, server_name: str, config_data: dict):
        print('Initialized DjangoWriter')        
        super().__init__()
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

    def processAPIs(self):
        for app in self.api_settings:
            app_oauth = self.api_settings[app]['oauth']
            app_auth_type = self.api_settings[app]['auth_type']
            app_auth_type = app_auth_type.split('|') if '|' in app_auth_type else app_auth_type
            app_csrf = self.api_settings[app]['csrf']
            views_dict = self.api_settings[app]['apis']
            ser_py = os.path.join(self.app_locs[app],'serializer.py')
            view_py = os.path.join(self.app_locs[app],'views.py')
            dj_ser = DjangoSerializer(app_oauth = app_oauth, loc = ser_py)
            dj_views = DjangoViews(app_oauth = app_oauth, app_auth_type=app_auth_type,app_csrf = app_csrf, loc = view_py)
            for api in views_dict:
                dj_ser.prepareSerializer(api_dict = views_dict[api])
                dj_views.prepareViews(api_dict = views_dict[api], api_name = api, ser_call = dj_ser.ser_call)
            dj_ser.writeSerializer()
            dj_views.writeViews()

    def processModels(self):
        for app in self.app_locs:
            models_py = os.path.join(self.app_locs[app],'models.py')
            dj_table = DjangoTables(server_oauth = self.server_settings["oauth"], loc = models_py)
            for table in self.db_settings['tables'][app]:
                table_dict = self.db_settings['tables'][app][table]
                dj_table.prepareTables(table = table, table_dict= table_dict)

            dj_table.writeTables()

    def processContainer(self):
        port = self.server_settings["port"] #For Docker-Compose/NGINX to Use
        containers = self.server_settings["containers"] #Not required for django but is for NGINX deployment

    def process(self):
        for i in [mro for mro in str(DjangoWriter.__mro__).split(',')]:
            print(i)
        self.processSettings()
        self.processModels()
        self.processAPIs()