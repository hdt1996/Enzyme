import os
from .util import *

class FileManager():
    def __init__(self):
        print('\n\n Init FileManager')

    def findFilesbyExt(self,file_type:str = '.txt', location: str = os.PathLike, dict_keys: bool = False, open_file: bool = False) -> list:
        if file_type != None:
            if (not os.path.isdir(location)) and (not os.path.isfile(location)):
                if open_file == True:
                    raise ValueError('Error with core logic. Not able to find files. Submitting for bugfix...')
                return []
            file_list = []
            for file in os.scandir(location):
                f_path = file.path
                if os.path.isfile(f_path) and f_path.endswith(file_type):
                    file_list.append(f_path)
                elif os.path.isdir(f_path):
                    file_list.extend(self.findFilesbyExt(file_type = file_type, location = f_path))
            if dict_keys:
                dict_obj = {}
                for f in file_list:
                    dict_obj[f.upper()] = True
                file_list = dict_obj
            return file_list

    def extractText(self,file: os.PathLike, open_file: bool = False) -> str:
        if open_file == True:
            with open(file = file, mode = 'r') as f:
                txt = ''.join(f.readlines())
                f.close()
                return txt
        else:
            return file

    def writeText(self,file: os.PathLike, text:str = '', overwrite: bool = False) -> str:
        file_split = file.split('.')
        new_name = f"{file_split[0]}_COPY"
        ext = file_split[1]
        lines = text.split("\\n', '")
        lines[0] = lines[0].replace("['",'')
        lines[len(lines)-1]= lines[len(lines)-1].replace("']",'')
        if overwrite == False:
            with open(file = f"{new_name}.{ext}", mode = 'w') as f:
                f.writelines(text)
                f.close()
                return text
        else:
            with open(file = file, mode = 'w') as f:
                f.writelines(text)
                f.close()
                return text

