from ...utils.utils import StringModify
from ....modules.Utilities.py.util import *
from .orm import *



class DjangoGET(DjangoORM):
    def __init__(self, crud_options: dict, table_name: str):
        self.crud = 'GET'
        super().__init__(crud_options = crud_options, table_name = table_name, crud = self.crud)
    def serializeData(self):
        temp_str = \
        inspect.cleandoc(
        f"""
            serialized_query = self.{self.crud}serializer_class(instance = table_query, many = True)
            response_data = []
            for entry in serialized_query.data:
                obj_dict = {{}}
                for key in response_fields:
                    obj_dict[key] = entry[key]
                response_data.append(obj_dict)
        """)
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)

    def getRequestData(self):
        return inspect.cleandoc(
        """
            if request.headers.get('selectors') == None:
                return Response('No headers')
            selectors =  json.loads(request.headers.get('selectors'))
            {validateSelector}
        """),['import json']

    def addResponseVar(self):
        return [StringModify.addTabs(txt = f"response_fields = {str(buildDictBoolbyArr(arr = self.response_fields))}",num_tabs= 1)]
    def serIsValid(self):
        return []

    def processUniqueOptions(self):
        return []

    def sendResponse(self):
        temp_str = \
        inspect.cleandoc(
        """
            return Response(response_data, status = status.HTTP_200_OK)
        """
        )
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)
class DjangoPOST(DjangoORM):
    def __init__(self, crud_options: dict, table_name: str):
        self.crud = 'POST'
        super().__init__(crud_options = crud_options, table_name = table_name, crud = self.crud)
    def serializeData(self):
        many = "True" if self.unique['entry_type'] == 'multiple' else "False"
        temp_str = inspect.cleandoc(f"serialized_data = self.{self.crud}serializer_class(data = req_body, many = {many})")
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)

    def getRequestData(self):
        return StringModify.addTabs(inspect.cleandoc("req_body = request.data"),1), []
    def addResponseVar(self):
        return []
    def serIsValid(self):
        temp_str = inspect.cleandoc(
        """
        if not serialized_data.is_valid():
            print(serialized_data.error_messages)
            return Response({{'{crud}_Error':'Input data is not valid'}}, status = status.HTTP_403_FORBIDDEN)
        """.format(crud = self.crud))
        return [StringModify.addTabs(txt = temp_str, num_tabs = 1)]

    def processUniqueOptions(self):
        mode = self.unique['mode']
        entry_type = self.unique['entry_type']
        backup = self.unique['backup']
        temp_str = []
        mode_str = []
        if mode == 'create' and entry_type == 'multiple':
            mode_str.append(StringModify.addTabs("data = list(serialized_data.data)",1))
            add_user = '' if not self.limit_to_user else "    obj_data['user'] = active_user"
            mode_str.append(StringModify.addTabs(inspect.cleandoc(
            f"""
            for obj in data:
                obj_data = dict(obj)
            {add_user}
                {self.table_name}.objects.create(**obj_data)
            """),1))
        elif mode == 'create' and entry_type == 'single':
            mode_str.append(StringModify.addTabs("data = dict(serialized_data.data)",1))
            if self.limit_to_user:
                mode_str.append(StringModify.addTabs("data['user'] = active_user",1))
            mode_str.append(StringModify.addTabs(inspect.cleandoc(
            f"""
            {self.table_name}.objects.create(**data)
            """),1))
        else:
            raise ValueError('Mode not accepted and/or entry_type is not correct')
            
        temp_str.extend(mode_str)
        return temp_str

    def sendResponse(self):
        temp_str = \
        inspect.cleandoc(
        """
            return Response(data, status = status.HTTP_200_OK)
        """
        )
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)

class DjangoPUT(DjangoORM):
    def __init__(self, crud_options: dict, table_name: str):
        self.crud = 'PUT'
        super().__init__(crud_options = crud_options, table_name = table_name, crud = self.crud)
    def serializeData(self):
        many = "True" if self.unique['mode'] == 'var_update' else "False"
        temp_str = inspect.cleandoc(f"serialized_data = self.{self.crud}serializer_class(data = req_body, many = {many})")
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)
    def getRequestData(self):
        return inspect.cleandoc(
        """
            req_body = request.data
            selectors =  json.loads(request.headers.get('selectors'))
            {validateSelector}
        """),['import json']
    def addResponseVar(self):
        return []
    def serIsValid(self):
        temp_str = inspect.cleandoc(
        """
        if not serialized_data.is_valid():
            return Response({{'{crud}_Error':'Input data is not valid'}}, status = status.HTTP_403_FORBIDDEN)
        """.format(crud = self.crud))
        return [StringModify.addTabs(txt = temp_str, num_tabs = 1)]

    def processUniqueOptions(self):
        mode = self.unique['mode']
        entry_type = self.unique['entry_type']
        backup = self.unique['backup']
        temp_str = []
        mode_str = []
        if mode == 'var_update':
            mode_str.append(StringModify.addTabs(inspect.cleandoc(
            """
            if len(data) != len(table_query):
                return Response({{'{crud}_Error':'Number of updates must match number of found items in database. Correct your selector'}}, status = status.HTTP_403_FORBIDDEN)
            id_list = []
            for entry in table_query:
                id_list.append(entry.id)
            for index, obj in enumerate(data):
                {table}.objects.filter(id = id_list[index]).update(**data[obj])

            """).format(crud = self.crud, table = self.table_name),1))
        elif mode == 'update' and entry_type == 'multiple':
            mode_str.append(StringModify.addTabs("data = dict(serialized_data.data)",1))
            mode_str.append(StringModify.addTabs(inspect.cleandoc(
            f"""
            table_query.update(**data)
            """),1))

        elif mode == 'update' and entry_type == 'single':
            mode_str.append(StringModify.addTabs("data = dict(serialized_data.data)",1))
            mode_str.append(StringModify.addTabs(inspect.cleandoc(
            """
            if len(table_query) > 1:
                return Response({{'{crud}_Error':'Mode - Single - was specified. Query resulted in many entries. Update was halted.'}}, status = status.HTTP_403_FORBIDDEN)
            table_query.update(**data)
            """).format(crud = self.crud),1))
            
        temp_str.extend(mode_str)
        return temp_str


    def sendResponse(self):
        temp_str = \
        inspect.cleandoc(
        """
            return Response(data, status = status.HTTP_200_OK)
        """
        )
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)
class DjangoDEL(DjangoORM):
    def __init__(self, crud_options: dict, table_name: str):
        self.crud = 'DELETE'
        super().__init__(crud_options = crud_options, table_name = table_name, crud = self.crud)
    def serializeData(self):
        return ''
    def getRequestData(self):
        return inspect.cleandoc(
        """
            selectors =  json.loads(request.headers.get('selectors'))
            {validateSelector}
        """),['import json']
    def addResponseVar(self):
        return []
    def serIsValid(self):
        return []

    def processUniqueOptions(self):
        mode = self.unique['mode']
        entry_type = self.unique['entry_type']
        backup = self.unique['backup']
        temp_str = inspect.cleandoc(
        """
            table_query.delete()
        """)
        return [StringModify.addTabs(txt = temp_str, num_tabs= 1)]
    def sendResponse(self):
        temp_str = \
        inspect.cleandoc(
        """
            return Response({'DELETE':'Success'}, status = status.HTTP_200_OK)
        """
        )
        return StringModify.addTabs(txt = temp_str, num_tabs = 1)
class DjangoCRUD():
    def __init__(self):
        super().__init__()
        self.table_name = None
        self.crud_inst = None

    def setCRUD(self, crud:str, crud_options:dict, table_name: str):
        if crud == 'GET':
            self.crud_inst = DjangoGET(crud_options = crud_options, table_name = table_name)
        elif crud == 'POST':
            self.crud_inst = DjangoPOST(crud_options = crud_options, table_name = table_name)
        elif crud == 'PUT':
            self.crud_inst = DjangoPUT(crud_options = crud_options, table_name = table_name)
        elif crud == 'DELETE':
            self.crud_inst = DjangoDEL(crud_options = crud_options, table_name = table_name)
        
    def createMethod(self,crud:str, crud_options:dict, table_name: str):
        self.setCRUD(crud = crud, crud_options=crud_options, table_name= table_name)
        g, p, m, i = self.crud_inst.createQuery()
        return g, p, m, i


