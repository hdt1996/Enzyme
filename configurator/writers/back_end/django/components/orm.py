from ...utils.utils import StringModify
from .....modules.Utilities.py.util import *
from ..templates.orm import *

class DjangoORM():
    def __init__(self, crud_options: dict, table_name: str, crud: str):
        print('Initialized DjangoORM')
        self.tmp_query = ChoiceORM()
        self.orm_props = []
        self.crud = crud
        self.table_name = table_name
        self.crud_options = crud_options
        self.response_fields = self.crud_options['response_fields']
        self.query_fields = self.crud_options['query_fields'] if crud != 'POST' else {}
        self.limit_to_user = self.crud_options['limit_to_user'] 
        self.entry_limit = self.crud_options['entry_limit']
        self.expiration = self.crud_options['expiration']
        self.csrf = self.crud_options['csrf']
        self.auth_type = self.crud_options['auth_type']
        self.verify_fields = self.crud_options['verify_fields']
        self.unique = self.crud_options['unique']

    def addSelector(self, prop_selector: dict = None):
        lines = []
        custom_query = {}
        fixed_query = {}
        for qf in self.query_fields:
            if len(self.query_fields[qf]) == 0:
                custom_query[qf] = True
            else:
                fixed_query[qf] = self.query_fields[qf]

        if len(custom_query) > 0:
            var = self.getRequestData()[0].format(validateSelector = self.tmp_query.validateSelector[0].format(fixed_query = fixed_query))
        else:
            var = [self.getRequestData()[0].format(validateSelector = '')]
            var.append(inspect.cleandoc(\
                f"""
                
                selectors =  {prop_selector}
                sel_dict = {{}}
                """))
            var = '\n'.join(var)
        lines.append(StringModify.addTabs(txt = var, num_tabs = 1))
        return lines

    def checkCustomQuery(self):
        custom_query = False
        for i in self.query_fields:
            if self.query_fields[i] == {}:
                custom_query = True
                break
        return custom_query

    def createQuery(self):
        lines = []
        imps = []
        glbs, functs = [],[f"def {self.crud.lower()}(self, request):"]
        glbs.append(self.tmp_query.options[0])
        if self.limit_to_user:
            lines.append(f"{StringModify.addTabs(txt = self.tmp_query.queries['user'][0],num_tabs = 1)}")
        lines.extend(self.addResponseVar())
        if self.crud != 'POST':
            lines.extend(self.processVariableInputs() if self.checkCustomQuery() else self.processStaticInputs())
        else:
            lines.append(self.getRequestData()[0])
        imps.extend(self.getRequestData()[1])
        lines.append(self.serializeData())
        lines.extend(self.serIsValid())
        lines.extend(self.processUniqueOptions())
        lines.append(self.sendResponse())
        functs.append('\n'.join(lines))
        functs = '\n'.join(functs)
        return glbs, self.orm_props, functs, imps

    def processVariableInputs(self):
        lines = []
        if self.limit_to_user:
            user_select = "sel_dict['user'] = active_user"
        else:
            user_select = ''
        lines.extend(self.addSelector())
        selector_dict = str(buildDictBoolbyArr(arr = self.query_fields))
        selector_line = self.tmp_query.queries['custom_query'][0].format(table = self.table_name, fields = selector_dict, user_select = user_select)
        lines.append(StringModify.addTabs(txt = selector_line,num_tabs = 1))
        return lines

    def processStaticInputs(self):
        lines = []
        if self.limit_to_user:
            user_select = "sel_dict['user'] = active_user"
        else:
            user_select = ''
        selector_dict = self.query_fields
        lines.extend(self.addSelector(prop_selector = selector_dict))
        lines.append(StringModify.addTabs(txt = self.tmp_query.queries['fixed_query'][0].format(table = self.table_name, user_select = user_select),num_tabs = 1))
        return lines
