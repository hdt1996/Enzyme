from genericpath import isfile
from msilib.schema import File
from configurator.apis.Utilities.py.util import *
from configurator.apis.Utilities.py.file_manager import FileManager
from ..utils.regex import WriterRegex
import os
FM = FileManager()

class DjangoModels(WriterRegex):
    def __init__(self):
        self.imports = []




class DjangoSettings(WriterRegex):
    def __init__(self):
        super().__init__()

    def setDatabase(self, txt: str):
        category, type = 'settings','db'
        engine = self.engines[self.db_settings['Engine']]
        name=self.db_settings['Name']
        user = self.db_settings['User']
        password = self.db_settings['Password']
        host = self.db_settings['Host']
        port = self.db_settings['PORT']   
        or_db_settings = self.matchDictVar(var_name = "DATABASES",txt = txt)
        db_temp = self.templates[category][type].format(dbengine = engine, dbname = name,dbuser = user, dbpassword = password, dbhost = host, dbport = port)
        txt =  txt.replace(or_db_settings,db_temp)
        return txt

    def setInstalledApps(self,txt: str, cors: bool = False, oauth: bool = False):
        category, type = 'settings','apps'
        match, curr_list = self.matchListVar(var_name = "INSTALLED_APPS",txt = txt)
        if match != False:
            app_list = self.templates[category][type]
            for app in self.app_locs:
                app_list.append(f"'{app}'")
            if cors:
                app_list.append(f"'corsheaders'")
            if oauth:
                app_list.append(f"'rest_framework'")
            app_str = ',\n\t'.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            txt = txt.replace(match[0],var_str)
            self.updateConf(curr_list= curr_list, app_list = app_list, category=category,type=type)
            return txt
        print('\nInstalled Apps ---------------FAILED MATCH\n')
        return txt

    def setMiddleWare(self,txt: str, cors: bool = False):
        category, type = 'settings','middleware'
        match, curr_list = self.matchListVar(var_name = "MIDDLEWARE",txt = txt)
        if match != False:
            app_list = self.templates[category][type]
            if cors:
                for index, app in enumerate(app_list):
                    if app == "'django.middleware.common.CommonMiddleware'":
                        app_list.insert(index, "'corsheaders.middleware.CorsMiddleware'")
                        break
            app_str = ',\n\t'.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            txt = txt.replace(match[0],var_str)
            self.updateConf(curr_list= curr_list, app_list = app_list, category=category,type=type)
            return txt
        print('\nMiddleware ---------------FAILED MATCH\n')
        return txt

    def setAllowHosts(self,txt: str, allowed_hosts: list):
        match, app_list = self.matchListVar(var_name = "ALLOWED_HOSTS",txt = txt)
        if match != False:
            for h in allowed_hosts:
                app_list.append(f"'{h}'")
            app_str = ','.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            txt = txt.replace(match[0],var_str)
            return txt
        print('\nAllowed Hosts ---------------FAILED MATCH\n')
        return txt

    def setStorage(self,txt: str, type: str):
        loc = self.server_settings['Storage'][type]['location'].replace('\\','/')
        url = self.server_settings['Storage'][type]['url']

        root_var = f"{type.upper()}_ROOT"
        url_var = f"{type.upper()}_URL"

        match = self.matchStrVar(var_name = root_var,txt = txt)
        if match != False:
            var_str = match[0].replace(f"'{match[1]}'",f"'{loc}'")
            txt = txt.replace(match[0],var_str)
        else:
            print('\nhandleStorage ROOT ---------------Made New Entry\n')
            txt = txt.split('\n')
            txt.append(f"{root_var} = '{loc}'")
            txt = '\n'.join(txt)

        match = self.matchStrVar(var_name = url_var,txt = txt)
        if match != False:
            var_str = match[0].replace(f"'{match[1]}'",f"'{url}'")
            txt = txt.replace(match[0],var_str)
        else:
            print('\nhandleStorage URL ---------------Made New Entry\n')
            txt = txt.split('\n')
            txt.append(f"{url_var} = '{url}'")
            txt = '\n'.join(txt)
        return txt

class DjangoWriter(DjangoSettings):
    def __init__(self, server_name: str, config_data: dict):
        self.server_name = server_name
        self.engines=\
            {
                'postgres':'django.db.backends.postgresql_psycopg2'
            }
        self.templates = \
        {
            'settings':
            {
                "db":
                """\
                \rDATABASES = {{\
                    \r\t'default': {{\
                        \r\t\t'ENGINE': '{dbengine}',\
                        \r\t\t'NAME': '{dbname}',\
                        \r\t\t'USER': '{dbuser}',\
                        \r\t\t'PASSWORD': '{dbpassword}',\
                        \r\t\t'HOST': '{dbhost}',\
                        \r\t\t'PORT': '{dbport}',\
                    \r\t}}\
                \r}}\
                """,
                "apps":
                [
                    "\n\t'django.contrib.admin'",
                    "'django.contrib.auth'",
                    "'django.contrib.contenttypes'",
                    "'django.contrib.sessions'",
                    "'django.contrib.messages'",
                    "'django.contrib.staticfiles'",
                ],
                "middleware":
                [
                    "\n\t'django.middleware.security.SecurityMiddleware'",
                    "'django.contrib.sessions.middleware.SessionMiddleware'",
                    "'django.middleware.common.CommonMiddleware'",
                    "'django.middleware.csrf.CsrfViewMiddleware'",
                    "'django.contrib.auth.middleware.AuthenticationMiddleware'",
                    "'django.contrib.messages.middleware.MessageMiddleware'",
                    "'django.middleware.clickjacking.XFrameOptionsMiddleware'",
                ]
            }
        }
        self.server_loc = config_data['Servers'][self.server_name]
        self.app_locs = config_data['Apps'][self.server_name]
        self.server_settings = config_data['Back_End_Settings'][self.server_name]
        self.db_settings = config_data['Database_Settings'][self.server_name]
        self.api_settings = config_data['API_Settings'][self.server_name]
        self.be_root = config_data['Back_End_Path']
        self.it_root = config_data['Root_Path']
        self.conf = {}
        self.conf['settings'] = self.setUpConf(loc = os.path.join(self.server_loc,'settings.py'),subcategory=['middleware','apps'])
        self.conf['tables'] = {}

        for app in self.app_locs:
            loc = os.path.join(self.app_locs[app],'models.py')
            if not os.path.isfile(loc):
                raise ValueError(f'FATAL ERROR: models.py in {app} folder does not exist!')
            self.conf['tables'][app] = self.setUpConf(loc = loc,
            subcategory=[table for table in self.db_settings['tables'][app]])

        with open(file = self.conf['settings']['loc'], mode = 'r') as s:
            self.conf['settings']['text'] = s.read()
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
        cors = self.server_settings["Cors"]
        oauth = self.server_settings["OAUTH"]
        allowed_hosts = self.server_settings["Allowed_Hosts"]
        
        txt = self.setInstalledApps(txt = txt, cors = cors, oauth = oauth)
        txt = self.setDatabase(txt = txt)
        txt = self.setMiddleWare(txt = txt, cors = cors)
        txt = self.setAllowHosts(txt = txt, allowed_hosts=allowed_hosts)
        for st in self.server_settings['Storage']:
            txt = self.setStorage(txt = txt, type = st)
        FM.writeText(file = settings_py,text = txt, num_prefix="_COPY_")

    def processContainer(self):
        port = self.server_settings["PORT"] #For Docker-Compose/NGINX to Use
        containers = self.server_settings["Containerization"] #Not required for django but is for NGINX deployment

    def processTables(self):
        for t in self.db_settings['tables']:
            models_py = self.conf['tables'][t]['loc']
            print(models_py)

    def process(self):
        self.processSettings()
        self.processTables()