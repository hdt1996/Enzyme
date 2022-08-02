#TEST
from front_end.css import *
from front_end.js import *
class HTML(CSS, JS):
    def __init__(self):
        self.doc_type = "<!DOCTYPE html>"
        self.html_format = {'head':[],'body':[],'script':[]}
        super().__init__(self)

    def buildDoc(self):
        return f"{'\n'.join(self.html_format['head'])}{'\n'.join(self.html_format['body'])}{'\n'.join(self.html_format['script'])}"
    
    def buildMainElements(self, main_tag:str, elements: list = []):
        self.html_format[main_tag]=[f"<{main_tag}>"]
        self.html_format[main_tag].extend(elements)
        self.html_format[main_tag].append(f"</{main_tag}>")
        return '\n'.join(self.html_format[main_tag])

    def buildElementGrid(self, row_col_grid: list =  []):
        #Examples:
        """
        Each cell assigned an id #TODO to be chosen
        Length of list is how many columns there are. We start from columns in our logic
        [3,3,3] means three columns with three rows each
        [[3,1],[3,1],[3,1]] means three columns with two columns each, first being three rows, second being 1 row
        [[[3,1],[3,1],[3,1]],[3,1],[3,1]]... This means three total columns
            First column has three sub columns, each sub column having 2 columns, first with 3 rows, second with 1 row
        3 rows, 2 columns, [3,2]
                                        [[1,3],[1,3],[1,3]]
        """

    def buildElement(self, properties: dict = {}, fetcher: str = '', innerText = ""):
        pass

    def assignAPI(self, api_endpoint: str, request_options: dict):
        pass