import os
from datetime import datetime
from ..Utilities.file_manager import FileManager
FS = FileManager()

class Logger():
    def __init__(self):
        self.debug_dict = {}
    def logVars(self,debug:bool = True, custom:str = '',isolate: list = []) -> None:
        if debug:
            vars = self.debug_dict
            var_log = []
            vars_length = len(vars)
            for index, var in enumerate(vars):
                if len(isolate) >=1 and not var in isolate:
                    continue
                if index == vars_length - 1:
                    var_log.append(f"\r{var} ------------- Type: {type(vars[var])} ---------------------- Value:----------------\n{vars[var]}")
                    break
                var_log.append(f"\r{var} ------------- Type: {type(vars[var])} ---------------------- Value:----------------\n{vars[var]}")
            var_log = '\n'.join(var_log)
            print(\
            f"""
            \r\n------------DEBUG LOGS-------------Time: {datetime.now()}\n
            {var_log}
            {custom}

            """)
    def addDebugVars(self, var_list:list = [], var_values = []):
        if len(var_list) != len(var_values):
            raise ValueError("List arguments passed in must match. Variable Names --> Variable Values")
        for index, name in enumerate(var_list):
            self.debug_dict[name]=var_values[index]

    def traceRelevantErrors(self,error_log:list,script_loc:os.PathLike,latest = False):
        new_error_log = []
        proj_files_dict = FS.findFilesbyExt(file_type = '.py',location = script_loc.replace('main.py',''), dict_keys=True)
        for error_file in error_log:
            file_name = os.path.join(error_file.split(", line")[0].replace(' ','').replace('"',''))
            if file_name.upper() in proj_files_dict:
                new_error_log.append(error_file)
        if latest:
            print('\nMy Error\n')
            print(new_error_log.pop())
        else:
            print('\nMy Error\n')
            print('\n'.join(new_error_log))


