import re

class WriterRegex():
    def matchListVar(self,var_name: str, txt: str):
        match = re.findall("({var_name}[ ]*\=[ ]*\[([ a-zA-Z\'\.\n\,\_\d\n\t]*[ ]*)\])".format(var_name = var_name),txt)
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
                app_list.append(f"\n    {app}")
            else:
                app_list.append(app)
        return match, app_list

    def matchStrVar(self,var_name, txt: str):
        match = re.findall("""({var_name}[ ]*\=[ ]*[\"\']([ \:\d\_a-zA-Z\'\.\n\t\,\/]*)[ ]*[\"\'])""".format(var_name = var_name),txt)
        if len(match) > 0:
            match = match[0]
        else: 
            return False
        return match

    def matchCallFunction(self,declar:str, txt:str):
        match = re.findall("""({declar} ([a-zA-Z\_\d]*)(\(([a-zA-Z\_\d\t\: ]+\,?)*\)))""".format(declar = declar),txt)
        if len(match) > 0:
            match = match[0][1]
        else: 
            return False
        return match

class StringModify():
    def addTabs(txt: str, num_tabs: int = 2):
        tabs = ''.join(['    ' for i in range(num_tabs)])
        new_text = []
        for line in txt.split('\n'):
            new_text.append(f"{tabs}{line}")
        return '\n'.join(new_text)
