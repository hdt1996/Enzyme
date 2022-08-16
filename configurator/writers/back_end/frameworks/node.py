from msilib.schema import File
from configurator.apis.Utilities.py.util import *
from configurator.apis.Utilities.py.file_manager import FileManager
from ..utils.regex import WriterRegex
import os
FM = FileManager()

class Node(WriterRegex):
    def __init__(self, server_name: str,  config_data: dict):
        self.server_name = server_name
        self.server_loc = config_data['Servers'][self.server_name]
        self.app_locs = config_data['Apps'][self.server_name]
        self.server_settings = config_data['Back_End_Settings'][self.server_name]
        self.db_settings = config_data['Database_Settings'][self.server_name]
        self.api_settings = config_data['API_Settings'][self.server_name]
        self.be_root = config_data['Back_End_Path']
        self.it_root = config_data['Root_Path']
        super().__init__()

    def process(self):
        pass