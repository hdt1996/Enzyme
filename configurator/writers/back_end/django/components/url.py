from ..templates.url import *
from .....modules.Utilities.py.util import *
import inspect
from .....modules.Utilities.py.file_manager import FileManager
FM = FileManager()

class DjangoURLS():
    def __init__(self, app_oauth: bool, loc: str):
        self.loc = loc
        self.tmp_url = URLOptions()
        self.app_oauth = app_oauth
        self.url_imports = self.tmp_url.imports['default']
        self.url_patterns = []

    def prepURLs(self, url: str, api_name: str):
        self.url_patterns.append(f"    path('{url}',{api_name}.as_view())")

    def writeURLs(self):
        url_imports = getArrUniquesByDict(dict_1 = buildDictBoolbyArr(self.url_imports))
        url_patterns = inspect.cleandoc(
        """
            urlpatterns = \\
            [
            {url_list}
            ]
        """).format(url_list = ',\n'.join(self.url_patterns))
        url_text = '\n'.join(['\n'.join(url_imports),url_patterns])
        FM.writeText(file = self.loc, text = url_text, overwrite=True)