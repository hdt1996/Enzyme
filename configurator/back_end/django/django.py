from configurator.modules.Utilities.py.util import *
from configurator.modules.Utilities.py.file_manager import FileManager
from ..utils.utils import DjangoRegex as DR, StringModify
import os, shutil as sh
FM = FileManager()
from .components.settings import *
from .components.views import *
from .components.tables import *



class DjangoConfig():
    def __init__(self):
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



class DjangoWriter():
    def __init__(self, server_name: str, config_data: dict):
        print('Initialized DjangoWriter')        
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

    def processSettings(self):
        settings_py = os.path.join(self.server_loc,'settings.py')
        txt = FM.extractText(file = settings_py, open_file = True)
        dj_settings = DjangoSettings(server_settings = self.server_settings, db_settings = self.db_settings, 
                                    app_locations = self.app_locs, loc = settings_py, txt = txt)
        dj_settings.setInstalledApps()
        dj_settings.setDatabase()
        dj_settings.setMiddleWare()
        dj_settings.setAllowHosts()
        for st in self.server_settings['storage']:
            dj_settings.setStorage(type = st)
        dj_settings.setAuthentication()
        dj_settings.writeSettings()

    def processViews(self):
        for app in self.api_settings:
            app_oauth = self.api_settings[app]['oauth']
            app_auth_type = self.api_settings[app]['auth_type']
            app_auth_type = app_auth_type.split('|') if '|' in app_auth_type else app_auth_type
            app_csrf = self.api_settings[app]['csrf']
            views_dict = self.api_settings[app]['apis']
            ser_py = os.path.join(self.app_locs[app],'serializer.py')
            view_py = os.path.join(self.app_locs[app],'views.py')
            urls_py = os.path.join(self.app_locs[app],'urls.py')
            dj_views = DjangoViews(app_oauth = app_oauth, app_auth_type=app_auth_type,app_csrf = app_csrf, view_loc = view_py, ser_loc = ser_py, url_loc = urls_py)
            for api in views_dict:
                dj_views.prepAPI(api_dict = views_dict[api], api_name = api)
            dj_views.SERIALIZER.writeSerializer()
            dj_views.URLS.writeURLs()
            dj_views.writeViews()

    def processModels(self):
        for app in self.app_locs:
            models_py = os.path.join(self.app_locs[app],'models.py')
            dj_table = DjangoTables(server_oauth = self.server_settings["oauth"], models_py = models_py)
            for table in self.db_settings['tables'][app]:
                table_dict = self.db_settings['tables'][app][table]
                dj_table.prepTable(tbl_name = table, table_dict= table_dict)
            dj_table.writeTables()

    def processContainer(self):
        port = self.server_settings["port"] #For Docker-Compose/NGINX to Use
        containers = self.server_settings["containers"] #Not required for django but is for NGINX deployment


    def processAPIs(self):
        curr_util_dir = './configurator/modules'
        new_util_dir = os.path.join(self.be_root,'modules')
        FM.copyDir(src = curr_util_dir, dst = new_util_dir)

    def process(self):
        for i in [mro for mro in str(DjangoWriter.__mro__).split(',')]:
            print(i)
        self.processSettings()
        self.processModels()
        self.processAPIs()
        self.processViews()