from configurator.apis.Utilities.py.file_manager import FileManager
import json
SA = FileManager()
CONFIG_MAP = None

with open("configurator/config/server_config.json") as config_file:
    CONFIG_MAP = json.loads(config_file.read())
    config_file.close()
SERVER_PATH = CONFIG_MAP['Server_Path']

class CSS():
    def __init__(self):
        pass
    def buildCSS(self, css_props:list=[]):
        pass

