import re

class WriterRegex():
    def matchListVar(self,var_name: str, txt: str):
        match = re.findall("({var_name}[ ]*\=[ ]*\[([ a-zA-Z\'\.\n\,]*[ ]*)\])".format(var_name = var_name),txt)
        if len(match) > 0:
            match = match[0]
        else:
            return False
        app_list = []
        for index, app in enumerate(match[1].split(',')):
            app = re.sub('[\n ]*','',app)
            if app == '':
                continue
            if index == 0:
                app_list.append(f"\n\t{app}")
            else:
                app_list.append(app)
        return match, app_list

    def matchStrVar(self,var_name, txt: str):
        match = re.findall("""({var_name}[ ]*\=[ ]*[\"\']([ a-zA-Z\'\.\n\,\/]*[ ]*)[\"\'])""".format(var_name = var_name),txt)
        if len(match) > 0:
            match = match[0]
        else: 
            return False
        return match

    def matchDictVar(self,var_name:str, txt:str):
        match = re.findall("""({var_name}[ ]*\=[ ]*\{{([ a-zA-Z\'\.\n\,\/\:\{{\d\_\#]*[ ]*\}})[\n ]*\}})""".format(var_name = var_name),txt)
        if len(match) > 0:
            match = match[0][0]
        else: 
            return False
        return match