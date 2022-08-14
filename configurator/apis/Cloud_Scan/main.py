from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, pandas as pd
from ..Utilities.py.dev import Development
from ..Utilities.py.dataframes import DataFrames
from ..Utilities.py.util import *
from ..Utilities.py.psql import PSQL
import time

from .sites.sites import w3Schools



DEV = Development()
DEV.makeTestDir(proj_name = 'Cloud_Scan')

class WebExtractor():
    #Has useful methods for reading or clicking data with methods for catching dry selenium elements and iterating through them.
    def __init__(self, extract: bool = False, download: bool = False):
        self.extract = extract
        self.download = download
        self.active_url_num = None
        self.active_search_num = None
        self.DataFrame = DataFrames()
        self.unique_col_lists = {}
        self.psql = PSQL()
        self.site = w3Schools()

    def getDFfromTables(self, tag: str, df_title: str, url: str):
        js_str=\
        """
        let html_string_list = [];
        let data = document.querySelectorAll(arguments[0]);
        for(let table = 0; table < data.length; table++)
        {
            html_string_list.push(data[table].outerHTML)
        }
        return html_string_list
        """
        list_data = self.driver.execute_script(js_str, tag)
        for i in list_data:
            print(url)
            df_name = str(df_title)
            if df_name == 'CSS Units':
                print('Found')
            sub_df = pd.read_html(i)[0]
            sub_df = self.site.process_columns(sub_df = sub_df)
            sub_df['Section'] = df_name
            sub_df = self.site.setIndex(df = sub_df, df_name = df_name)
            
            if 'CSS' not in df_name.upper():
                df_name = 'CSS_Properties'

            self.psql.addDFToVarTable(df = sub_df, table = df_name,use_index=True)

    def printUniqueColumns(self, sub_uniques: dict, df_title: str):
            unique_len = len(self.unique_col_lists)
            if unique_len == 0:
                self.unique_col_lists[0] = sub_uniques
            else:
                if self.areKeysUniquetoDictVals(sub_uniques=sub_uniques) == False:
                    self.unique_col_lists[unique_len] = sub_uniques
            print('--------------------------------------UNIQUE--------------------',df_title,'\n')
            for i in self.unique_col_lists:
                print('Number ', i, '--------------',self.unique_col_lists[i])
                print('\n')
            print('\n.................................................................................................')

    def areKeysUniquetoDictVals(self, sub_uniques: dict = {}):
        found_difference = [False for i in self.unique_col_lists]
        for index, d in enumerate(self.unique_col_lists):
            for u in sub_uniques:
                if not u in self.unique_col_lists[d]:
                    found_difference[index]=True
                    break
        total_same = found_difference.count(False)
        if total_same > 0:
            return True
        return False

class WebJavaScript():
    def __init__(self):
        self.js_functs ={'scanner':[]}
        with open(file = 'configurator\\apis\\Utilities\\js\\browser.js', mode = 'r') as js:
            self.js_functs['scanner'].append(js.read())
            js.close()

    def getParentandIndex(self, element):
        runtime_str = \
        """
            let element = arguments[0]
            return {"parent":element.parentNode,"index":Array.prototype.indexOf.call(element.parentNode.children,element)}
        """

        element_data = WebDriverWait(self.driver,40).until(lambda elem_data : self.driver.execute_script(runtime_str, element))
        return element_data

    def waitPopupTags(self, target: str = '', remove: bool = False):

        js_str = \
        """
            return document.querySelectorAll(arguments[0]).length
        """
        expiration = 1
        num_frames = 0
        while expiration > 0:
            cur_frame = self.driver.execute_script(js_str, target)
            if num_frames != cur_frame:
                expiration +=1.25
                num_frames = cur_frame
            if target == 'iframe' and remove:
                self.removeiFrames()
            print(expiration)
            time.sleep(1)
            expiration -= 1

    def scrolltoElement(self, element):
        js_str = \
        """
            let e = arguments[0];
            e.scrollIntoView();
            return true;
        """
        WebDriverWait(self.driver,60).until(lambda result: self.driver.execute_script(js_str, element))
    def getAllSis(self,parent_element):
        next_str = \
        """
            let par_children = arguments[0].children;
            let child_list = []
            for(let i = 0; i < par_children.length; i++)
            {
                child_list.push(par_children[i]);
            };
            return child_list
        """
        element_list = self.driver.execute_script(next_str, parent_element)
        return element_list

    def getNumChild(self,element):
        next_str = \
        """
            return arguments[0].children.length;
        """
        element_list = self.driver.execute_script(next_str, element)
        return element_list


    def getNextElement(self,element, curr_index: int):
        next_str = \
        """
            let element =  arguments[0];
            let index = arguments[1];
            let num_children;
            let par_children = element.parentNode.children;
            element = par_children[index + 1];
            return {'element': element}
        """
        next_element = self.driver.execute_script(next_str, element, curr_index)
        return next_element

    def getinnerHTML(self,element, get_parent: bool = False):
        next_str = \
        """
            let element =  arguments[0];
            let get_parent = arguments[1];
            if(get_parent === true)
            {
                return element.parentNode.innerHTML
            }
            return element.innerHTML;
        """
        next_element = self.driver.execute_script(next_str, element, get_parent)
        return next_element
    def removeiFrames(self):
        js_str = \
        """
        let iframes = document.querySelectorAll('iframe');
        for (let i = 0; i < iframes.length; i++) 
        {
            if (navigator.appName == 'Microsoft Internet Explorer') 
            {
                window.frames[i].document.execCommand('Stop');
            } 
            else 
            {
                try
                {
                    window.frames[i].stop()
                }
                catch
                {
                    console.log('Removed')
                }
                
            }
            iframes[i].remove();
        }
        if(document.querySelectorAll('iframe').length == 0)
        {
            return true
        }
        """
        WebDriverWait(self.driver,20).until(lambda results: self.driver.execute_script(js_str))

    def getSelected(self):
        js_str = \
        """
            return document.activeElement
        """
        self.driver.execute_script(js_str)
        print('FINED')
    def findActive(self):
        js_str = \
        """
            let actives = document.querySelectorAll('.active')
            return actives[actives.length-1]
        """
        return self.driver.execute_script(js_str)

    def isClickable(self, element):
        js_str = \
        """
        let e = arguments[0];
        if((e.getAttribute('onclick')!=null)||(e.getAttribute('href')!=null))
        {
            return true
        };
        return false;
        """
        return self.driver.execute_script(js_str, element)

class WebNavigator(WebExtractor, WebJavaScript):
    # For navigating web using combination of selenium python functions and javascript. Clicking and waiting.
    def __init__(self, urls: list, start_tag: str, text_targets: list,tag_targets: list, prop_targets: list, \
                extract: bool, download: bool, iter_sis: bool, mode: str = 'Match', driver_options: Options = Options(),  \
                driver_loc: os.PathLike = None):
        if driver_loc == None:
            raise ValueError('Please pass in location of your webdriver for chrome.')
        self.mode = mode
        self.urls = urls
        self.text_targets = text_targets
        self.driver = webdriver.Chrome(executable_path = driver_loc, options = driver_options)
        self.prop_targets = prop_targets
        self.start_tag = start_tag
        self.tag_targets = tag_targets
        self.iter_sis = iter_sis
        self.processed_urls = {}
        self.ignore=\
            {
                'BR':True,
                'HR':True,
                'SPACER':True
            }

        WebExtractor.__init__(self,extract = extract, download = download)
        WebJavaScript.__init__(self)
        
    def getScanJS(self, mode: str= 'match', xpath: str = 'null', exc_txt_trgt = None):
        run_str = \
        '''
            let trgt_element = arguments[0];
            console.log('Selenium Arg passed Element -----------------------',trgt_element,'.........................................')
            let selenium = new Selenium({txt_trgt:TYA_TXT_TRGT, props_trgts:TYA_PROP_TRGT, tags_trgts:TYA_TAG_TRGT, action: 'TYA_ACTION', xpath: TYA_XPATH, element: trgt_element});
            selenium.processAction({selector: 'TYA_START'});
            if(selenium.MATCH.length > 0 && selenium.action === 'match')
            {
                return selenium.MATCH
            };
            if(selenium.HTML_MAPPING !== {} && selenium.action === 'grid')
            {
                return selenium.HTML_MAPPING
            };
            console.log("RESULTS: -----------------",selenium.action, selenium.xpath);
            if(selenium.EL_BY_XPATH !== null && selenium.action === 'xpath')
            {
                return selenium.EL_BY_XPATH
            };
            if(selenium.EL_BY_EL !== null && selenium.action === 'element')
            {
                return selenium.EL_BY_EL
            };
        '''
        s_js_str = list(self.js_functs['scanner'])
        s_js_str.append(run_str)

        if mode == 'match':
            if self.active_url_num != None and self.active_search_num != None:
                if exc_txt_trgt != None:
                    txt_target = exc_txt_trgt
                else:
                    txt_target = f"""'{self.text_targets[self.active_url_num].split(";")[self.active_search_num]}'"""
                tag_target = self.tag_targets[self.active_url_num].split(";")[self.active_search_num].split('|')
                prop_target = self.prop_targets[self.active_url_num].split(';')[self.active_search_num].split('|')
            else:
                raise ValueError ('You selected match mode, but url_num and self.active_search_num are missing their values.\nPlease re-instantiate Selenium class with right arguments for init.')
        if mode == 'xpath':
            txt_target, tag_target, prop_target = 'null',[],[]
        if mode == 'element':
            txt_target, tag_target, prop_target= 'null',[],[]

        s_js_str = \
            '\n'.join(s_js_str)\
            .replace("TYA_START",self.start_tag)\
            .replace("TYA_TXT_TRGT",txt_target)\
            .replace("TYA_PROP_TRGT",str(prop_target))\
            .replace("TYA_TAG_TRGT",str(tag_target))\
            .replace("TYA_ACTION",mode)\
            .replace("TYA_XPATH",str(xpath))\
            .replace('export','')

        return s_js_str
    
    def navigateURLS(self, wait: bool = False):
        for index, url in enumerate(self.urls):
            self.driver.get(url)
            self.active_url_num = index
            self.awaitPageLoad()

    def findByTextHTML(self, exc_txt_trgt: str = None, expir: int = 3):
        while True:
            try:
                self.driver.delete_all_cookies()
                runtime_str =  self.getScanJS(exc_txt_trgt= f"'{exc_txt_trgt}'" if isinstance(exc_txt_trgt,str) else exc_txt_trgt, mode = 'match') 
                matches = self.driver.execute_script(runtime_str, None)
                if len(matches) != 0:
                    return self.evaluateMatches(matches)
            except:
                pass
       


    def findByXpathHTML(self, xpath:list = 'null', expir: int = 3):
        while True:
            try:
                self.driver.delete_all_cookies()
                runtime_str =  self.getScanJS(xpath = xpath, mode = 'xpath') 
                matches = self.driver.execute_script(runtime_str, None)
                if matches != None:
                    return matches
            except:
                pass

    def findByElementHTML(self, element, expir: int = 3):
        while True:
            try:
                self.driver.delete_all_cookies()
                runtime_str =  self.getScanJS(mode = 'element') 
                matches = self.driver.execute_script(runtime_str, element)
                if matches != None:
                    return matches
            except:
                pass

    def evaluateMatches(self, el_list):
        for i in el_list:
            if i['element'].text != '':
                return i
        raise ValueError('Your search lead to finding of elements that are not interactible. Please refine your search in main args.')

    def recurseSisLinks(self, c_grid: list, start_index: int, end_index: int, active: bool = False, home_url: str = None, last_url: str = None):
        print('Started')
        child_grid = list(c_grid)
        el_txt = None

        if home_url == None:
            home_url = self.driver.current_url
        if last_url == None:
            last_url = self.driver.current_url

        for i in range(start_index, end_index):
            print('RECURS-----------',i,'-------------Remaining: ',end_index - i)
            self.findByTextHTML(exc_txt_trgt='Log in')
            sub_c_grid = self.findByElementHTML(element = self.findActive())['xpath']
            sub_c_grid.pop()
            child_grid.append(i)

            if not active:
                self.driver.get(home_url)
                print('LOADED HOME')
            else:
                self.driver.get(last_url)
                print('LOADED LAST URL')
            el_data = self.findByXpathHTML(xpath = child_grid)
            el = el_data['element']
            el_tag = el.tag_name.upper()
            el_txt = el.text
            el_num_child = self.getNumChild(el)

            print(child_grid, el_txt if el_num_child == 0 else 'Many Texts with Children')

            child_grid.pop()

            if active and self.isClickable(element = el) == False:
                continue

            if el_tag in self.ignore:
                continue

            self.scrolltoElement(element = el)

            if self.isClickable(element = el):
                parel_innerHTML = el_data['par_innerHTML'].replace(' class="active"','')
                el_outerHTML = el.get_attribute('outerHTML')
                el_link =  el.get_attribute('href')
                if el_link != None and el_link not in self.processed_urls:
                    el.click()
                else:
                    print('Already processed. Skipped')
                    continue
                active_el_data = self.findByElementHTML(element = self.findActive())
                paractive_innerHTML = active_el_data['par_innerHTML'].replace(' class="active"','')
                active_outerHTML = active_el_data['outerHTML'].replace(' class="active"','')
                if active_outerHTML != el_outerHTML:
                    if parel_innerHTML != paractive_innerHTML:
                        self.iterSisLinks(match_result = active_el_data)
                        self.driver.get(home_url)
                        print('LOADED BACK TO HOME: ',home_url,'...')
                        continue
                self.findByTextHTML(exc_txt_trgt='Log in')
                self.getDFfromTables(tag = 'table', df_title = el_txt, url = self.driver.current_url)
                last_url = self.driver.current_url
                self.processed_urls[last_url] = True

            elif el_num_child > 0:
                self.driver.get(last_url)
                if len(sub_c_grid) ==len(child_grid):
                    sub_c_grid = list(child_grid)
                    sub_c_grid.append(i)
                self.findByTextHTML(exc_txt_trgt='Log in')
                self.recurseSisLinks(c_grid = sub_c_grid , start_index = 0, end_index = el_num_child, active = True, last_url = last_url, home_url=home_url)
            else:
                continue
        print('Finished')   

    def iterSisLinks(self, match_result = None):
        print('\n Called \n')
        #FIND MATCH AND GET THE XPATH TO USE in Selenium JS Class
        if match_result == None:
            match_result = self.findByTextHTML()
        #NOTE This result MUST be 100% pinpointing to element. This means using more specific property attributes, text, and/or tags in main.py args to isolate.
        el = match_result['element']
        el_xpath = match_result['xpath']
        
        el_data = self.getParentandIndex(el)
        el_index = el_data['index']
        num_par_children = self.getNumChild(el_data['parent'])
        el_xpath.pop()
        self.recurseSisLinks(c_grid = el_xpath, start_index = el_index, end_index = num_par_children)
        print('DONE WITH ITERSIS CALL')

    def awaitPageLoad(self):
        txt_targets = self.text_targets[self.active_url_num].split(";")
        for search_num, trgt_text in enumerate(txt_targets):
            trgt_text =  trgt_text.lstrip()
            if self.iter_sis:
                self.active_search_num = search_num
                self.iterSisLinks()


#'--disable-gpu' #'https://www.w3schools.com/css/css3_backgrounds.asp' #"CSS Advanced Background Properties"

def main(driver_config: list = ['--start-maximized','--window-size=1920,1080','disable-infobars','--disable-extensions','--no-sandbox','--disable-blink-features=AutomationControlled',
'--disable-application-cache','--disable-gpu','--disable-dev-shm-usage','--ignore-certificate-errors','log-level=3'], urls: str = ['https://www.w3schools.com/css/css3_borders.asp','https://facebook.com'], 
    text_targets: list = ['CSS References', 'Log In'],
    prop_targets: list = ["text","text|innerHTML|aria-label"],tag_targets: list = ["H2|A|DIV","BUTTON"],
    extract: bool = False, download = False, iter_sis: bool = True,
    mode: str = 'xpath'):
    """
    Summary: Utility for parsing through html elements to extract information from websites using Selenium.

    Args:

        urls: List of urls to load. 

        text_targets: List of target values to search for. #NOTE multiple target values for one url can be used by delimiting with ";"
        #NOTE We use ";" as delimiter because it doesn't confict with typical text content on sites.
            Example: 
                urls:  ['google.com', 'facebook.com']
                text_targets: ['Sign in;Next', 'Log in; Submit']
            Meaning:
                Google page: Search for "Sign in" and then "Next"
                Facebook: Search for "Login" and then "Submit"
        tag_targets: List of tags to validate text we are searching for...
            Example: 
                urls: ['google.com', 'facebook.com']
                text_targets: ['Sign in;Next', 'Log in; Submit']
                tag_targets: ['A SPAN','SPAN A'] #NOTE these must be upper cased. A means <a></a>.. SPAN means <span></span>
            Meaning:
                Google page: Search for "Sign in".
                    ---> If "Sign in" and element tag is "a", proceed to other target "Next"
                    ---> If "Next" and element tag is "span", search complete
                Facebook: Search for "Login" and then "Submit"
        prop_targets: List of element properties to match against our text_targets
            Example:
                urls: ['google.com', 'facebook.com']
                text_targets: ['Sign in;Next', 'Log in; Submit']
                tag_targets: ['A SPAN','SPAN A'] #NOTE these must be upper cased. A means <a></a>.. SPAN means <span></span>
                prop_targets: ["text|aria-label;aria-label","alt_text innerHTML"] #NOTE Bar means or for Searching through both properties searching
                #NOTE: Use bar for searching for multiple attributes for one search i.e. 'Sign In' if more than one element leads to same output.
                    #Example: Multiple Sign in Buttons. No consequence of clicking any one of them.
            Meaning:
                Google Page:
                    Searching for "Sign In" --> Only look for "Sign In" inside text element property AKA element.innerTEXT OR aria-label
                    Searching for "Next" --> Only look for "Next" inside aria-label element property AKA element.getAttribute('aria-label')
                Facebook:
                    Same process except the element attributes would come from the second item or index 1 of prop_targets list
        extract: Bool. Get data from html and parse to DataFrame or another data format
        download: Bool. Download files and call methods to handle downloading single or multiple files depending on vendor site limitations.
    """
    options = Options()
    for option in driver_config:
        options.add_argument(option)

    navigator = WebNavigator(driver_options = options, start_tag = 'body',
        driver_loc = "C:\\Users\\hduon\\Documents\\Enzyme\\configurator\\apis\\Cloud_Scan\\src\\chromedriver.exe",
        urls = urls, text_targets = text_targets,tag_targets = tag_targets, \
        prop_targets = prop_targets, extract = extract, download = download, iter_sis = iter_sis, mode = mode)

    navigator.navigateURLS(wait = True)
    navigator.driver.close()
    

if __name__ == '__main__' or __name__ == 'configurator.apis.Cloud_Scan.main':
    main()