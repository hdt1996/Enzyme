#from writers.front_end.css import CSS
from writers.front_end.html import HTML
from utils.sysadmin.sysadmin import SystemAdmin
import os
import json
TEST_LOC = "C:/Users/hduon/Documents/API_Utilities/test files"
TEST_ARG = \
{ #Layer: type Dictionary
    '0':{},
    '1':{},
    '2':{}
}


TEST_DATA = \
"""
{
    "layer_0":
    {
        "type": "element",
        "css": [],
        "text": "L1",
        "tag": "div",
        "properties": {},
        "scripts": "",
        "api_type":"",
        "col_0":
        {
            "type": "element",
            "css": [],
            "text": "L2",
            "tag": "div",
            "properties": {},
            "scripts": "",
            "api_type":"",
            "row_0":
            {
                "type": "element",
                "css": [],
                "text": "L3",
                "tag": "div",
                "properties": {},
                "scripts": "",
                "api_type":"",
                "col_0":
                {
                    "type": "element",
                    "css": [],
                    "text": "L4",
                    "tag": "div",
                    "properties": {},
                    "scripts": "",
                    "api_type":"",
                    "row_0": 
                    { 
                        "type": "element",
                        "css": [],
                        "text": "TARGET",
                        "tag": "div",
                        "properties": {},
                        "scripts": "",
                        "api_type":"",
                        "row_0": 
                        { 
                            "type": "element",
                            "css": [],
                            "text": "TARGET",
                            "tag": "div",
                            "properties": {},
                            "scripts": "",
                            "api_type":"",
                            "row_0": 
                            { 
                                "type": "element",
                                "css": [],
                                "text": "DDEEEEEPPP_____TARGET",
                                "tag": "div",
                                "properties": {},
                                "scripts": "",
                                "api_type":""
                            }
                        }
                    }
                }
            }
        },
        "col_1":
        {
            "type": "element",
            "css": [],
            "text": "L2",
            "tag": "div",
            "properties": {},
            "scripts": "",
            "api_type":"",
            "row_0":
            {
                "type": "element",
                "css": [],
                "text": "L3",
                "tag": "div",
                "properties": {},
                "scripts": "",
                "api_type":"",
                "col_0":
                {
                    "type": "element",
                    "css": [],
                    "text": "L4",
                    "tag": "div",
                    "properties": {},
                    "scripts": "",
                    "api_type":"",
                    "row_0": 
                    { 
                        "type": "element",
                        "css": [],
                        "text": "L5",
                        "tag": "div",
                        "properties": {},
                        "scripts": "",
                        "api_type":""
                    }
                }
            }
        }
        
    }
}
"""
html = HTML()
SA = SystemAdmin()
html.html_format['body']['output'] = html.buildElementStr('body','',elements = html.buildDocJSON(data = TEST_DATA))
print(html.html_format['body']['output'])
test_inner = html.buildElementStr('div','',elements = ['.............'])
html.html_format['head']['output'] = html.buildElementStr('head',elements = [test_inner])
#html.html_format['scripts']['output'] = html.buildElementStr('scripts','',elements = [])
doc = html.buildDoc()
#print(doc)
SA.writeText(file = os.path.join(TEST_LOC,'builder.html'), text = doc)
#data = json.loads(TEST_DATA, strict = False)
#print(data)

#SA = SystemAdmin()
#
#print(doc)


""" head_elems = []
elem = html.buildElement(elem_type = 'div', prop_dict = {'aria-label': 'Test', 'alt_img':'Test2'}, innerText = 'HELLO WORLD', fetcher = 'onClick = "fetchBackend()"')
head_elems.append(elem)
head_elems.append(elem)
html.html_format['head']['output'] = html.buildElementStr('head','',elements = head_elems)
html.html_format['body']['output'] = html.buildElementStr('body','',elements = head_elems)
html.html_format['scripts']['output'] = html.buildElementStr('scripts','',elements = head_elems)
doc = html.buildDoc()
SA.writeText(file = os.path.join(TEST_LOC,'builder.html'), text = '')
 """