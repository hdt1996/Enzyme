#TEST
import json 
from configurator.apis.Utilities.py.util import buildArrfromDict
COUNT = 0
class HTML():
    def __init__(self):
        self.doc_type = "<!DOCTYPE html>"
        self.html_format = {'html':{'output':'','mapping':[]}, 'head':{'output':'','mapping':[]},'body':{'output':'','mapping':[]},'scripts':{'output':'','mapping':[]}}
        self.main_tags=\
            {
                'head': True,
                'body': True,
                'scripts': True,
                'html': True
            }
        self.tag_map = \
            {
                'div': True,
                'tr': True,
                'li': True,
                'button': True,
                'ui': True,
                'li': True,
                'p': True,
                'span': True,
                'h1': True,
                'h2': True,
                'h3': True,
                'h4': True,
                'h5': True,
                'h6': True,
                'img': True,
                'video': True,
                'textarea': True,
                'input': True,
                'scripts': True
            }
        self.css_map = {} #TODO built by css module or import results/pickle of css builder method

    def buildDoc(self):
        html_element_build = []
        html_element_build.append(self.html_format['head']['output'])
        html_element_build.append(self.html_format['body']['output'])
        html_element_build.append(self.html_format['scripts']['output'])
        html_build = self.buildElementStr('html',elements = html_element_build)
        return html_build
        
    
    def buildElementStr(self, tag:str, prop_str: str = '', elements: list = [], rec_tabs: int = 1):
        nl = '\n'
        if self.main_tags.get(tag) == None:
            child = '\n\t'
            #child_tab = '\t'
            child_tab = []
            for num in range(rec_tabs):
                child_tab.append('\t')
            child_tab = ''.join(child_tab)
        else:
            child = ''
            child_tab = ''
        tag_build = [f"{nl+child_tab}<{tag} {prop_str}>{nl}"]
        for e in elements:
            tag_build.append(f"{nl+child}{e}{nl}")
        #tag_build.append('\n\n' if tag == 'html' else tab+nl)
        tag_build.append(f"{nl + child_tab}</{tag}>")
        return ''.join(tag_build)

    def buildBodyGrid(self, row_col_grid: list =  []):
        #Examples:
        """
        Each cell assigned an id #TODO to be chosen
        Grid: nested dictionary
        dictionary will be nested in alternating patterns of column and row starting with column
        At each level, dictionaries will have css and text keys to keep track of parent div props as well as child classes
        Structure:
        {
            layer_0:
            css: '',
            text: '',
            tag: '',
            properties: {},
            script: ''
            {
                col_0:
                {
                    css: '',
                    text: '',
                    tag: '',
                    properties: {},
                    script: ''
                    {
                        css: '',
                        text: '',
                        tag: '',
                        properties: {},
                        script: '',
                        row: 
                            { 
                                css: '',
                                text: '',
                                tag: '',
                                properties: {},
                                script: ''
                            }
                        css: '',
                        text: '',
                        tag: '',
                        properties: {},
                        script: ''
                        
                    }
                }
            }

        }

        """

        

    def buildElement(self, elem_type: str = None, prop_dict: dict = {}, css_list: dict = {}, fetcher: str = None, innerHTML: list = [], style: dict = [], rec_tabs: int = 1): 
        # For setting up element config. AKA element props, text, or css
        elem_props = []
        inner = []
        elem_build = []
        tab = ''
        if self.main_tags.get(elem_type) == None:
            tab = []
            for num in range(rec_tabs):
                tab.append('\t')
            tab = ''.join(tab)  
        if len(css_list) > 0:
            elem_props.append(f'classes = "{" ".join(css_list.keys())}"')

        if len(style) > 0:
            elem_props.append(f'style = "{" ".join(buildArrfromDict(data = style, item_type = str, item_delim= ":"))}"')
            
        for prop in prop_dict:
            elem_props.append(f"{prop} = {prop_dict[prop]}")
        if fetcher != None:
            elem_props.append(fetcher)
        elem_props = ' '.join(elem_props)
        if len(innerHTML) != 0:
            for i in innerHTML:
                inner.append(f"{tab}{i}")
        if self.tag_map.get(elem_type) == True:
            elem_build = self.buildElementStr(tag = elem_type, prop_str = elem_props, elements = inner, rec_tabs = rec_tabs) #time to build actual html tag
            return elem_build
        raise ValueError('Tag is not valid for buildElement method call')

    def recurseBuildJSON(self, data: any, n: int = 1) -> str:
        """
        Should be called to build large string of nested HTML elements
        """
        elem_list = []
        p_tag = data['tag']   
        p_props = data['properties']
        p_script = data['scripts']
        p_css = data['css']
        p_text = data['text']
        p_style = data['style']
        elem_list.append(p_text)


        if isinstance(data, dict) and data.get('type') == 'element':
            for key in data:
                if isinstance(data[key], dict) and data[key].get('type') == 'element':
                    ch_el_str = self.recurseBuildJSON(data[key], n = n + 1)
                    elem_list.append(ch_el_str)
        #should be string only if it reaches here
        build = self.buildElement(elem_type= p_tag, prop_dict = p_props, css_list = p_css, fetcher = p_script, innerHTML= elem_list, style = p_style, rec_tabs = n + 1)
        #print('Recursion Count: ', COUNT,'\n','build:\n',build)
        return build
        

        
    def buildDocJSON(self,data:str = ''):
        layer_build = []
        dict_data = json.loads(s = data, strict = False)
        for layer in dict_data:
            l_build = self.recurseBuildJSON(data = dict_data[layer])
            layer_build.append(l_build)
        return layer_build
        



    def assignAPI(self, api_endpoint: str, request_options: dict): #to be inherrited by JS
        pass
    def assignState(self, state_name: str, temp_or_persist: bool = True): #to be inherrited by JS
        pass