import inspect
from ...utils.regex import StringModify
class ChoiceTableFunctions():
    def __init__(self):
        super().__init__()
        self.file = \
            {
                'servable': (inspect.cleandoc(
                """
                def {field}ToUrl(self):
                    try:
                        url=str(self.{field}.url)
                    except:
                        url=None
                    return url
                """),[]),
                'upload_to':
                {
                    'user': (inspect.cleandoc(
                    """
                    def {field}ToUserDir(instance, file: str):
                        return f'{upload_to}/{{instance.user.id}}_{{instance.user.username}}/{{file}}'
                    """),[]),
                    None: (inspect.cleandoc(
                    """
                    def {field}toCustomDir(instance, file: str):
                        return f'{upload_to}/{{file}}'
                    """),[])
                },
                'max_size': (inspect.cleandoc(
                """
                def validate{field}Size(self,value):
                    filesize= value.size
                    max_size = {max_size}
                    if filesize > max_size:
                        raise ValidationError(f"The maximum size of uploading to {field} is {{max_size/10**6}} mb.")
                    else:
                        return value
                """),['from django.core.exceptions import ValidationError'])
            }
        self.display = \
            {
            'identifier': (inspect.cleandoc(
            """
                def __str__(self):
                    return str({field_names})
            """),[])
            }
        self.defaults = \
            {
                'char': (inspect.cleandoc(
                """
                def gen{field}Code(length: int = {length}):
                    length = {length}
                    while True:
                        unique_code = ''.join(random.choices(string.ascii_uppercase,k=length))
                        if {table}.objects.filter({field}=unique_code).count() == 0:
                            return unique_code
                """),['import random','import string']),
                'int': (inspect.cleandoc(
                """
                def gen{field}Code(length: int = {length}):
                    while True:
                        unique_code = ''.join(random.choices(random.randint(0,9),k=length))
                        if {table}.objects.filter({field}=unique_code).count() == 0:
                            return unique_code
                """),[])
            }

    def processFileArgs(self, field:str, f_dict: dict):
        servable = f_dict['servable']
        max_size = f_dict['max_size']
        upload_to = f_dict['upload_to']
        structure = f_dict['structure']
        methods, instance_methods, imports = [],{},[]
        if servable:
            methods.append(StringModify.addTabs(txt = self.file['servable'][0].format(field = field),num_tabs = 1))
            imports.extend(self.file['servable'][1])
        if max_size:
            if max_size.endswith('mb'):
                max_size = float(max_size.split('mb')[0]) * 10**6
            elif max_size.endswith('kb'):
                max_size = float(max_size.split('kb')[0])
            else:
                raise ValueError('Size type is not specified. Correct front-end input~')
            methods.append(StringModify.addTabs(txt = self.file['max_size'][0].format(field = field, max_size = max_size), num_tabs=1))
            imports.extend(self.file['max_size'][1])
        if upload_to and structure:
            instance_methods['upload_to'] = StringModify.addTabs(txt = self.file['upload_to'][structure][0].format(field = field, upload_to = upload_to),num_tabs = 1)
            imports.extend(self.file['upload_to'][structure][1])
        return methods, instance_methods, imports

    def processCommonArgs(self, field:str, table:str, f_dict:dict):
        random = f_dict['random']
        f_type = f_dict['type']
        length = f_dict['length']
        instance_methods, imports = {},[]
        if random:
            instance_methods['random'] = StringModify.addTabs(txt = self.defaults[f_type][0].format(field = field, table = table, length = length),num_tabs = 1)
            imports.extend(self.defaults[f_type][1])
        return instance_methods, imports

class ChoiceTableFields():
    def __init__(self):
        print('Initialized ChoiceTableFields')
        self.fields = \
            {
                'char':"models.CharField(max_length={length},null={null},blank={blank},default={default}, primary_key = {pk})", #add function for generating uniques
                'text':"models.TextField(max_length={length},null={null},blank={blank},default={default}, primary_key = {pk})",
                'int':"models.IntegerField(max_digits={length},null={null},blank={blank},default={default}, primary_key = {pk})",
                'float':"models.FloatField(max_digits={length},null={null},blank={blank},default={default}, primary_key = {pk})",
                'bool':"models.BooleanField(default={default},null={null},blank={blank})",
                'img':"models.ImageField(null={null}, blank={blank}, upload_to={upload_to})", #add function to check filesize per kwa and where to upload by structure per kwa
                "fk":"models.ForeignKey({attached},on_delete=models.{on_delete},blank={blank},null={null})",
                "time":"models.DateTimeField(auto_now_add={on_update}, auto_now={on_created})",
                'file':"models.FileField(null={null}, blank={blank}, upload_to={upload_to})", #add function to check filesize per kwa and where to upload by structure per kwa
                'json':"models.JSONField(default = {default})",
                "user":"models.OneToOneField(User,on_delete=models.CASCADE)"
            }
            