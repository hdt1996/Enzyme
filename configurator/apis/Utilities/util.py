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

def listDictKeyUniques(dicts_in_array: list, target_key = str, sub_key = str) -> list:
    matches = []
    unique_map = {}
    for data in dicts_in_array:
        if isinstance(data[target_key], list):
            for match in data[target_key]:
                if isinstance(match, dict):
                    match_result = match[sub_key].lstrip()
                    if match_result == 'null':
                        continue
                    if unique_map.get(match_result) == None:
                        unique_map[match_result] = True
                        matches.append(match_result)
        else:
            matches.append(data[target_key][sub_key])
            
    return matches

