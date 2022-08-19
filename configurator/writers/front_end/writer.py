from .css import CSS
from .html import HTML
from configurator.apis.Utilities.py.dev import *
from configurator.apis.Utilities.py.file_manager import FileManager
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
            "css": {"test_class1":true,"YT_TRSF_2":true},
            "text": "L1",
            "tag": "div",
            "properties": {},
            "scripts": "",
            "api_type":"",
            "style":{"height":"5px"},
            "0":
            {
                "type": "element",
                "css": {"test_class1":true,"YT_TRSF_2":true},
                "text": "L2",
                "tag": "div",
                "properties": {},
                "scripts": "",
                "api_type":"",
                "style":{"height":"5px"},
                "0":
                {
                    "type": "element",
                    "css": {"test_class1":true,"YT_TRSF_2":true},
                    "text": "L3",
                    "tag": "div",
                    "properties": {},
                    "scripts": "",
                    "api_type":"",
                    "style":{"height":"5px"},
                    "0":
                    {
                        "type": "element",
                        "css": {"test_class1":true,"YT_TRSF_2":true},
                        "text": "L4",
                        "tag": "div",
                        "properties": {},
                        "scripts": "",
                        "api_type":"",
                        "style":{"height":"5px"},
                        "0": 
                        { 
                            "type": "element",
                            "css": {"test_class1":true,"YT_TRSF_2":true},
                            "text": "TARGET",
                            "tag": "div",
                            "properties": {},
                            "scripts": "",
                            "api_type":"",
                            "style":{"height":"5px"},
                            "0": 
                            { 
                                "type": "element",
                                "css": {"test_class1":true,"YT_TRSF_2":true},
                                "text": "TARGET",
                                "tag": "div",
                                "properties": {},
                                "scripts": "",
                                "api_type":"",
                                "style":{"height":"5px"},
                                "0": 
                                { 
                                    "type": "element",
                                    "css": {"test_class1":true,"YT_TRSF_2":true},
                                    "text": "DDEEEEEPPP_____TARGET",
                                    "tag": "div",
                                    "properties": {},
                                    "scripts": "",
                                    "api_type":"",
                                    "style":{"height":"5px"}
                                }
                            }
                        }
                    }
                }
            },
            "1":
            {
                "type": "element",
                "css": {"test_class1":true,"YT_TRSF_2":true},
                "text": "L2",
                "tag": "div",
                "properties": {},
                "scripts": "",
                "api_type":"",
                "style":{"height":"5px"},
                "0":
                {
                    "type": "element",
                    "css": {"test_class1":true,"YT_TRSF_2":true},
                    "text": "L3",
                    "tag": "div",
                    "properties": {},
                    "scripts": "",
                    "api_type":"",
                    "style":{"height":"5px"},
                    "0":
                    {
                        "type": "element",
                        "css": {"test_class1":true,"YT_TRSF_2":true},
                        "text": "L4",
                        "tag": "div",
                        "properties": {},
                        "scripts": "",
                        "api_type":"",
                        "style":{"height":"5px"},
                        "0": 
                        { 
                            "type": "element",
                            "css": {"test_class1":true,"YT_TRSF_2":true},
                            "text": "L5",
                            "tag": "div",
                            "properties": {},
                            "scripts": "",
                            "api_type":"",
                            "style":{"height":"5px"}
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