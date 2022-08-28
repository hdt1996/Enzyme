import inspect
from ...utils.utils import StringModify
from .....modules.Utilities.py.util import *
from ...utils.utils import DjangoRegex as DR

class FieldFunctions():
    def __init__(self):
        super().__init__()
        self.nums = \
        {
            'length': (inspect.cleandoc(
            """
                def validate{field}Length(self, length: int = {length}):
                    if len(str(self.{field})) > length:
                        return False
                    else:
                        return True
            """),[])
        }
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
        self.dunders = \
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

    def processCommonArgs(self, field:str, tbl_name:str, f_dict:dict):
        random = f_dict['random']
        f_type = f_dict['type']
        length = f_dict['length']
        methods, instance_methods, imports = [],{},[]
        if random:
            instance_methods['random'] = StringModify.addTabs(txt = self.defaults[f_type][0].format(field = field, table = tbl_name, length = length),num_tabs = 1)
            imports.extend(self.defaults[f_type][1])
        if f_type in ['float','int']:
            methods.append( StringModify.addTabs(txt = self.nums['length'][0].format(field = field, table = tbl_name, length = length),num_tabs = 1))
        return methods, instance_methods, imports

class FieldOptions():
    def __init__(self):
        print('Initialized ChoiceTableFields')
        self.functions = FieldFunctions()
        self.fields = \
            {
                'char':"models.CharField(max_length={length}, null={null}, blank={blank}, default={default}, primary_key = {pk})", #add function for generating uniques
                'text':"models.TextField(max_length={length}, null={null}, blank={blank}, default={default}, primary_key = {pk})",
                'int':"models.IntegerField(null={null}, blank={blank}, default={default}, primary_key = {pk})",
                'float':"models.FloatField(null={null}, blank={blank}, default={default}, primary_key = {pk})",
                'bool':"models.BooleanField(default={default}, null={null}, blank={blank})",
                'img':"models.ImageField(null={null}, blank={blank}, upload_to={upload_to})", #add function to check filesize per kwa and where to upload by structure per kwa
                "fk":"models.ForeignKey({attached}, on_delete=models.{on_delete}, blank={blank}, null={null} {to_field})",
                "time":"models.DateTimeField(auto_now_add={on_created}, auto_now={on_update})",
                'file':"models.FileField(null={null}, blank={blank}, upload_to={upload_to})", #add function to check filesize per kwa and where to upload by structure per kwa
                'json':"models.JSONField(default = {default}, null={null}, blank={blank})",
                "O2O":"models.OneToOneField({attached}, on_delete=models.{on_delete})",
                "M2M":"models.ManyToManyField('{attached}', through='{through_class}', related_name='{related_name}')"
            }
        #Example:
        """
        Tables: ['Harley Davidson','Indian','Dealership']
        Dealership sells both bikes and both bikes exist in many other dealerships, hence M2M.

        Class...
        indian = Dealership.objects.create(name = 'Specials')
        harley = Harley.objects.create(name = 'street glide')

        For M2M to work with through model, we need MEMBERSHIP CLASS that is FKeyed to both.
        class Dealershp:
            indian = models.ForeignKey('indian', related_name = 'dealerships', on_delete = models.SET_NULL, null = True)

            ## HOW TO DO CHOICES ##
            LOW = 0
            NORMAL = 1
            HIGH = 2
            CHOICES = (
                (LOW, 'Low'),
                (NORMAL, 'Normal'),
                (HIGH, 'High'),)
            connecting_field = models...(choices = CHOICES, default = HIGH)
            #PIZZA EXAMPLE: models.ManyToManyField('Topping', through='ToppingAmount', related_name='pizzas')
        """
    def processCommonFields(self, field_dict: dict, tbl_name:str, field:str, f_type: str):
        null = field_dict['null']
        blank = field_dict['blank']
        length = field_dict['length']
        default= field_dict['default']
        pk = field_dict['pk']

        if isinstance(default, str):
            default = f"'{default}'"
        
        if (pk and null) or (pk and blank):
            raise ValueError('Primary Key must not be blank or null. Please fix your configuration.')

        mths, inst_mths, imps = self.functions.processCommonArgs(field = field, tbl_name = tbl_name, f_dict = field_dict)
        if len(inst_mths) > 0:
            default = DR.matchCallFunction(declar = "def",txt = inst_mths['random'])

        inst_mths = buildArrfromDict(data = inst_mths, kv = False)
        prop = f"{field} = {self.fields[f_type].format(length = length, null = null, blank = blank, default = default, pk = pk)}"

        return imps, inst_mths, mths, prop

    def processFileFields(self, field_dict: dict, field:str, f_type: str):
        null = field_dict['null']
        blank = field_dict['blank']
        mths, inst_mths, imps = self.functions.processFileArgs(field = field, f_dict = field_dict)
        upload_to = field_dict['upload_to']
        if len(inst_mths) > 0:
            upload_to = DR.matchCallFunction(declar = "def",txt = inst_mths['upload_to'])
        inst_mths = buildArrfromDict(data = inst_mths, kv = False)
        prop = f"{field} = {self.fields[f_type].format(null = null, blank = blank, upload_to = upload_to)}"

        return imps, inst_mths, mths, prop

    def processTimeFields(self, field_dict: dict, field:str, f_type: str):
        created = field_dict['auto_now_add']
        updated = field_dict['auto_now']
        imps, inst_mths, mths = [], [], []
        if created and updated:
            raise ValueError('Created and Updated options together cannot be used. Choose only one.')
        prop = f"{field} = {self.fields[f_type].format(on_created = created, on_update = updated)}"

        return imps, inst_mths, mths, prop
    def processSimpleFields(self, field_dict: dict, field:str, f_type: str):
        null = field_dict['null']
        blank = field_dict['blank']
        default = field_dict['default']
        imps, inst_mths, mths = [], [], []
        prop = f"{field} = {self.fields[f_type].format(default = default, null = null, blank = blank)}"
        return imps, inst_mths, mths, prop

    def processFKFields(self, field_dict: dict, field:str, f_type: str):
        null = field_dict['null']
        blank = field_dict['blank']
        on_delete = field_dict['on_delete'].upper()
        attached = field_dict['attached']
        to_field = field_dict['to_field']
        imps, inst_mths, mths = [], [], []
        if to_field == None:
            to_field = ''
        elif isinstance(to_field, str) and to_field != '':
            to_field = f", to_field = '{to_field}'"

        else:
            raise ValueError('Please pass in string with nonblank value for Foreign Key "to_field" option')
        prop = f"{field} = {self.fields[f_type].format(null = null, blank = blank, attached = attached, to_field = to_field, on_delete = on_delete)}"
        return imps, inst_mths, mths, prop

