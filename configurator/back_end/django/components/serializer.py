from ...utils.utils import StringModify
from ....modules.Utilities.py.util import *
from ..templates.orm import *
from ..templates.serializer import *
from ...utils.utils import DjangoRegex as DR, StringModify
from ....modules.Utilities.py.file_manager import FileManager
FM = FileManager()

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
        
    def setAttribs(self, api_dict: dict, table: str, crud: str, api_name:str):
        self.fields = api_dict['response_fields']
        self.verify_fields = api_dict['verify_fields']
        self.table_name = table
        self.crud = crud
        self.api_name = api_name

    def prepareSerializer(self, api_dict: dict, table: str, crud: str, api_name:str):
        self.setAttribs(api_dict = api_dict, table = table, crud = crud, api_name = api_name)
        imps = '\n'.join(self.imports)
        s_class = [f"class {self.api_name}{self.crud}Serializer(ModelSerializer):"]
        ser_call = DR.matchCallFunction('class',txt = s_class[0])
        m_class = StringModify.addTabs(txt = self.meta[self.verify_fields][0].format(table = self.table_name, fields = tuple(self.fields)),num_tabs = 1)
        s_class.append(m_class)
        self.ser_classes.extend(s_class)
        self.ser_imports.append(imps)
        return ser_call

    def writeSerializer(self):
        self.ser_imports = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.ser_imports))
        ser_text = '\n'.join(['\n'.join(self.ser_imports),'\n'.join(self.ser_classes)])
        FM.writeText(file = self.loc, text = ser_text, overwrite=True)