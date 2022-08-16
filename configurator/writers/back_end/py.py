from distutils.command.build import build
import json
import os

from ...apis.Utilities.py.file_manager import FileManager
from ...apis.Utilities.py.dev import Development
from .frameworks.django import DjangoWriter
from .frameworks.node import Node
from .frameworks.proxy import Proxy

DEV = Development()
FM = FileManager()


class WebServerWriter():
    def __init__(self, config_loc: os.PathLike):
        with open(file = config_loc,mode = 'r') as f:
            txt = f.read()
            self.config_data = json.loads(s = txt)
            f.close()
        self.be_settings = self.config_data['Back_End_Settings']
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

def main(config_loc: os.PathLike = "C:\\Users\\hduon\\Documents\\Enzyme\\conf\\server_config.json"):
    writer = WebServerWriter(config_loc=config_loc)
    writer.processBackEnds()

main()
