from ..templates.settings import *
from ...utils.utils import DjangoRegex as DR, StringModify
import os
from .....modules.Utilities.py.file_manager import FileManager
FM = FileManager()

class DjangoSettings():
    def __init__(self,server_settings:dict, db_settings: dict, app_locations: dict, loc: os.PathLike, txt:str):
        print('Initialized DjangoSettings')
        self.temp = ChoiceSettings()
        self.setting_apps = list(self.temp.installed_apps)
        self.setting_middleware = list(self.temp.middleware)
        self.loc = loc
        self.app_locations = app_locations

        self.setting_txt = txt
        self.server_cors = server_settings['cors']
        self.allowed_hosts = server_settings['allowed_hosts']
        self.server_oauth = server_settings['oauth']
        self.server_auth_type = server_settings['auth_type']
        self.server_storage = server_settings['storage']
        self.db_config = \
        {
            "dbengine":db_settings['engine'],
            "dbname":db_settings['name'],
            "dbuser":db_settings['user'],
            "dbpassword":db_settings['password'],
            "dbhost":db_settings['host'],
            "dbport":db_settings['port']
        }
        if self.server_cors:
            self.setting_apps.append(f"'corsheaders'")
            for index, app in enumerate(self.setting_middleware):
                if app == "'django.middleware.common.CommonMiddleware'":
                    self.setting_middleware.insert(index, "'corsheaders.middleware.CorsMiddleware'")
                    break
        if self.server_oauth:
            self.setting_apps.append(f"'rest_framework'")


    def setDatabase(self):
        category, type = 'settings','database'
        or_db_settings = DR.matchDBSetting(txt = self.setting_txt)
        if or_db_settings != False:
            db_temp = self.temp.databases.format(**self.db_config)
            self.setting_txt =  self.setting_txt.replace(or_db_settings,db_temp)
            #self.updateConf(curr_list = [or_db_settings], app_list = [db_temp], category = category, type = type)
        else:
            raise ValueError('Failed Match for Settings - Database Config')
    def setInstalledApps(self):
        category, type = 'settings','apps'
        match, curr_list = DR.matchListVar(var_name = "INSTALLED_APPS",txt = self.setting_txt)
        if match != False:
            for app in self.app_locations:
                self.setting_apps.append(f"'{app}'")
            app_str = ',\n    '.join(self.setting_apps)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            self.setting_txt = self.setting_txt.replace(match[0],var_str)
            #self.updateConf(curr_list= curr_list, app_list = self.setting_apps, category=category,type=type)
        else:
            raise ValueError('Failed Match for Settings - Installed Apps')

    def setMiddleWare(self):
        category, type = 'settings','middleware'
        match, curr_list = DR.matchListVar(var_name = "MIDDLEWARE",txt = self.setting_txt)
        if match != False:
            app_str = ',\n    '.join(self.setting_middleware)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            self.setting_txt = self.setting_txt.replace(match[0],var_str)
            #self.updateConf(curr_list= curr_list, app_list = self.setting_middleware, category=category,type=type)
        else:
            raise ValueError('Failed Match for Settings - Middleware')

    def setAllowHosts(self):
        match, curr_list = DR.matchListVar(var_name = "ALLOWED_HOSTS",txt = self.setting_txt)
        if match != False:
            app_list = []
            for h in self.allowed_hosts:
                app_list.append(f"'{h}'")
            app_str = ','.join(app_list)
            var_str = match[0].replace(f"[{match[1]}]",f"[{app_str}]")
            self.setting_txt = self.setting_txt.replace(match[0],var_str)
            return self.setting_txt
        raise ValueError('Failed Match for Settings - Allowed Hosts')

    def setStorage(self, type: str):
        loc = self.server_storage[type]['location'].replace('\\','/')
        url = self.server_storage[type]['url']
        root_var = f"{type.upper()}_ROOT"
        url_var = f"{type.upper()}_URL"
        match = DR.matchStrVar(var_name = root_var,txt = self.setting_txt)
        if match != False:
            var_str = match[0].replace(f"'{match[1]}'",f"'{loc}'")
            self.setting_txt = self.setting_txt.replace(match[0],var_str)
        else:
            self.setting_txt = self.setting_txt.split('\n')
            self.setting_txt.append(f"{root_var} = '{loc}'")
            self.setting_txt = '\n'.join(self.setting_txt)
        match = DR.matchStrVar(var_name = url_var,txt = self.setting_txt)
        if match != False:
            var_str = match[0].replace(f"'{match[1]}'",f"'{url}'")
            self.setting_txt = self.setting_txt.replace(match[0],var_str)
        else:
            self.setting_txt = self.setting_txt.split('\n')
            self.setting_txt.append(f"{url_var} = '{url}'")
            self.setting_txt = '\n'.join(self.setting_txt)

    def setAuthentication(self):
        if not self.server_oauth:
            return self.setting_txt
        category, type = 'settings','oauth'
        auth_type = self.server_auth_type.split('|') if '|' in self.server_auth_type else self.server_auth_type
        match = DR.matchAuthSetting(txt = self.setting_txt)
        permissions = ["\r    'rest_framework.permissions.IsAuthenticated'"]
        authentication = []
        if 'session' in auth_type:
            authentication.append("\r    'rest_framework.authentication.SessionAuthentication'")
        if 'token' in auth_type:
            authentication.append("'rest_framework.authentication.TokenAuthentication'")
        authentication = StringModify.addTabs(txt = ',\n'.join(authentication), num_tabs= 1)
        permissions = StringModify.addTabs(txt = ',\n'.join(permissions), num_tabs=1)
        oauth_template = self.temp.rest_framework.format(permissions = permissions, authentication = authentication)
        if match != False:
            self.setting_txt =  self.setting_txt.replace(match,oauth_template)
        else:
            self.setting_txt = self.setting_txt.split('\n')
            self.setting_txt.append(oauth_template)
            self.setting_txt = '\n'.join(self.setting_txt)

    def writeSettings(self):
        FM.writeText(file = self.loc, text = self.setting_txt, overwrite=True)