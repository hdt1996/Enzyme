from .front_end.css import CSS
from .front_end.html import HTML
from configurator.apis.Utilities.dev import *
from configurator.apis.Utilities.file_manager import FileManager
import os

DEV = Development()
DEV.makeTestDir('EnzymeWriter')
if __name__ == 'configurator.writers.main' or __name__ == '__main__':

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
    FM = FileManager()
    html.html_format['body']['output'] = html.buildElementStr('body','',elements = html.buildDocJSON(data = TEST_DATA))
    test_inner = html.buildElementStr('div','',elements = ['.............'])
    html.html_format['head']['output'] = html.buildElementStr('head',elements = [test_inner])
    #html.html_format['scripts']['output'] = html.buildElementStr('scripts','',elements = [])
    doc = html.buildDoc()
    FM.writeText(file = os.path.join(DEV.proj_test_dir,'builder.html'), text = doc)