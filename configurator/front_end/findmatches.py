import os
import re

TOTAL_PROPERTIES = 0
CATEG_MAP = {}
PROP_MAP={}
def buildClassNameMap(file_name:str):
    file_path = '/'.join(str(__file__).split('/')[:-1])
    txt = None
    global TOTAL_PROPERTIES, CATEG_MAP
    with open(os.path.join(file_path,file_name), mode='r') as f:
        txt = f.readlines()
        f.close()

    properties = {}
    found_class = None
    class_index = 0
    prop_index = 0
    for index, line in enumerate(txt):
        if len(line.split(';')) > 2:
            raise ValueError("CONTAINS MORE THAN ONE PROP")
        if len(re.findall("(\{)",line)) > 0:
            found_class = line.replace('{','')
            found_class = re.sub(r"  +",'',found_class).strip()
            if found_class not in CATEG_MAP:
                CATEG_MAP[found_class] = class_index
                properties[class_index] = set()
                class_index += 1
            continue
        cleaned_prop = re.sub(r"  +|\;",'',line).strip()
        if cleaned_prop == '' or cleaned_prop == '}':
            continue
        if cleaned_prop not in PROP_MAP:
            PROP_MAP[cleaned_prop] = prop_index
            prop_index+=1
        if cleaned_prop not in properties[CATEG_MAP[found_class]]:
            properties[CATEG_MAP[found_class]].add(PROP_MAP[cleaned_prop])
        
    return properties

def getIntersection(dict1, dict2):
    matches_dict = {}
    for d1 in dict1:
        if d1 in dict2:
            matches_dict[d1]=True

    return matches_dict


ClassPropsMULT = buildClassNameMap('App.css')
ClassPropsSingle = {}
MasterGroup = {} 



ClassPropsMULTCOPY = dict(ClassPropsMULT)

for cls in dict(ClassPropsMULTCOPY):
    current_props = ClassPropsMULTCOPY[cls]
    size = len(current_props)
    if size == 1:
        ClassPropsSingle[cls]=ClassPropsMULT.pop(cls)

ClassKeys = list(ClassPropsMULT.keys())
END = len(ClassKeys)

for index, cls in enumerate(ClassPropsMULT): #We have each class and props mapped to this CLassPropsMULT
    """Goal: Iterate each class and props to find similarities to other class's props"""
    current_class = cls
    current_props = ClassPropsMULT[cls] #set
    
    #Iterate thru each prop
    next_index = index+1
    if next_index == END:
        continue
    main_index = 0
    main_match = {}
    while next_index < END:
        sub_match = {"props":set(),"related_classes":set()}
        next_class = ClassKeys[next_index]
        next_props = ClassPropsMULT[next_class]
        intersection = current_props.intersection(next_props)
        if len(intersection) > 0:
            #print(f"\nCompare:\nCurrentClass:{current_class}\nTargetClass:{next_class}\nIntersection:{intersection}")
            sub_match["props"]=sub_match["props"].union(intersection)
            sub_match["related_classes"].add(next_class)
            sub_match["related_classes"].add(current_class)
            if f"group_{main_index}" not in main_match:
                main_match[f"group_{main_index}"] = sub_match
            found_match = False
            main_keys = list(main_match.keys())
            for i in main_keys:
                if sub_match["props"] == main_match[i]["props"]:
                    main_match[i]["related_classes"] = \
                        main_match[i]["related_classes"].union(sub_match["related_classes"])
                    found_match = True
                    break
            if not found_match:
                main_match[f"group_{len(main_keys)}"] = sub_match
        next_index+=1
    for i in main_match:
        print(main_match[i])
    
    

