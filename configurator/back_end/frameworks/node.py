
from configurator.modules.Utilities.py.util import *
from configurator.modules.Utilities.py.file_manager import FileManager
from ..utils.utils import DjangoRegex
import os
FM = FileManager()

class Node(DjangoRegex):
    def __init__(self, server_name: str,  config_data: dict):
        self.server_name = server_name
        self.server_loc = config_data['Server_Locations'][self.server_name]
        self.app_locs = config_data['App_Locations'][self.server_name]
        self.server_settings = config_data['Server_Settings'][self.server_name]
        self.db_settings = config_data['Database_Settings'][self.server_name]
        self.api_settings = config_data['API_Settings'][self.server_name]
        self.be_root = config_data['Back_End_Path']
        self.it_root = config_data['Root_Path']
        super().__init__()

    def process(self):
        pass