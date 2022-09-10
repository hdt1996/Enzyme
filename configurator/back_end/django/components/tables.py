from msilib.schema import File
from ..templates.models import *
import os
from ....modules.Utilities.py.util import *
from ...utils.utils import DjangoRegex as DR
from ....modules.Utilities.py.file_manager import FileManager
FM = FileManager()

class DjangoTables():
    def __init__(self, server_oauth: bool, models_py: os.PathLike):
        print('Initialized DjangoTables')
        self.tmp_fields = FieldOptions()
        self.tmp_imports = ['from django.db import models']
        self.tables = []
        self.globals = []
        self.loc = models_py
        if server_oauth:
            self.tmp_imports.append("from django.contrib.auth.models import User")
        self.field_types =\
        {
            "commons":buildDictBoolbyArr(arr = ['char','text','int','float']),
            "files":buildDictBoolbyArr(arr = ['img','file'])
        }

    def prepareFields(self, tbl_name:str, table_dict: dict) -> list:
        field_imps, field_inst_mths, field_mths, field_props = [], [], [], []
        for field in table_dict:
            f_type =table_dict[field]['type']
            field_dict = table_dict[field]

            if f_type in self.field_types['commons']:
                imps, inst_mths, mths, prop = self.tmp_fields.processCommonFields(field_dict = field_dict, tbl_name = tbl_name, field=field, f_type= f_type)
            elif f_type in self.field_types['files']:              
                imps, inst_mths, mths, prop = self.tmp_fields.processFileFields(field_dict = field_dict, field=field, f_type = f_type)
            elif f_type == 'time':
                imps, inst_mths, mths, prop = self.tmp_fields.processTimeFields(field_dict = field_dict, field=field, f_type = f_type)
            elif f_type == 'fk':
                imps, inst_mths, mths, prop = self.tmp_fields.processFKFields(field_dict = field_dict, field=field, f_type = f_type)
            else:
                imps, inst_mths, mths, prop = self.tmp_fields.processSimpleFields(field_dict = field_dict, field=field, f_type = f_type)

            field_imps.extend(imps)
            field_inst_mths.extend(inst_mths)
            field_mths.extend(mths)
            field_props.append(prop)

        return field_imps, field_inst_mths, field_mths, field_props
        
    def prepTable(self, tbl_name: str, table_dict:dict):
        table = []

        imps, inst_mths, mths, props = self.prepareFields(tbl_name = tbl_name, table_dict = table_dict)
        inst_mths = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(inst_mths)))
        mths = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(mths)))
        self.tmp_imports.extend(imps)

        table.append(f"class {tbl_name.capitalize()}(models.Model):")
        table.append(inst_mths)
        table.append(StringModify.addTabs(txt = '\n'.join(props), num_tabs = 1))
        table.append(mths)
        table.append('\n')
        self.tables.append('\n'.join(table))


    def writeTables(self):
        model_imports = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.tmp_imports)))
        model_globals = '\n'.join(getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.globals)))
        models_txt = [model_imports, model_globals]
        models_txt.append('\n'.join(self.tables))
        models_txt = '\n'.join(models_txt)
        FM.writeText(file = self.loc,text = models_txt, overwrite=True)


