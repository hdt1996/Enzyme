def kwargsReturnValues(kwargs:dict,var_names: list) -> tuple:
    var_list = []
    for variable in var_names:
        if kwargs.get(variable) == None:
            if variable == '':
                raise ValueError(f'Check GLOBALS:\n\nEmpty key passed in.\nCheck that there are no duplicate commas or ending commas in global string')
            raise ValueError(f'Missing {variable} in Kwargs. Fix logic for handling passed in/default kwargs to CLI')
        else:
            var_list.append(kwargs[variable])
    return var_list

def splitStringbyDelim(src_string:str,sp_delim:list, cl_delim:list = [],replace:str = '') -> list:
    arr = []
    for sp in sp_delim:
        for item in src_string.split(sp):
            for cl in cl_delim:
                item = item.replace(cl,replace)
            arr.append(item)
    return arr

def buildArrfromDict(data: dict = {}, item_type : type = str, item_delim: str = ''):
    arr = []
    if item_type == str:
        for key in data:
            arr.append(f"{key}{item_delim}{data[key]} ;")
        return arr
    elif item_type == list:
        for key in data:
            arr.append([key,item_delim,data[key]])
        return arr

