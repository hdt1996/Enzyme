import json
import os

from ..modules.Utilities.py.file_manager import FileManager
from ..modules.Utilities.py.dev import Development
from .django.django import DjangoWriter
from .frameworks.node import Node
from .frameworks.proxy import Proxy

DEV = Development()
FM = FileManager()


class WebServerWriter():
    def __init__(self, config_loc: os.PathLike):
        print('Initialized WebServerWriter')
        with open(file = config_loc,mode = 'r') as f:
            txt = f.read()
            self.config_data = json.loads(s = txt)
            f.close()
        self.be_settings = self.config_data['Server_Settings']
        self.parser = None
        
    def processBackEnds(self):
        for server in self.be_settings:
            framework = self.be_settings[server]['framework']
            if framework == 'python django':
                self.parser = DjangoWriter(server_name = server, config_data = self.config_data)
            elif framework == 'node express':
                self.parser = Node(server_name = server, config_data = self.config_data)
            else:
                continue
            self.parser.process()

    def processProxy(self):
        self.parser = Proxy(config_data = self.config_data)

def main(config_loc: os.PathLike = "./conf/server_config.json"):
    writer = WebServerWriter(config_loc=config_loc)
    writer.processBackEnds()

main()
