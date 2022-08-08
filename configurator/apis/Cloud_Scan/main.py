from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, pandas as pd
from ..Utilities.py.dev import Development
import time

DEV = Development()
DEV.makeTestDir(proj_name = 'Cloud_Scan')

class WebExtractor():
    #Has useful methods for reading or clicking data with methods for catching dry selenium elements and iterating through them.
    def __init__(self, extract: bool = False, download: bool = False):
        self.extract = extract
        self.download = download


class WebJavaScript():
    def __init__(self):
        self.js_functs ={'scanner':[]}
        with open(file = 'configurator\\apis\\Utilities\\js\\browser.js', mode = 'r') as js:
            self.js_functs['scanner'].append(js.read())
            js.close()

    def getElementData(self, element):
        runtime_str = \
        """
            let element = arguments[0]
            return {"parent":element.parentNode, "num_children":element.children.length ,"index":Array.prototype.indexOf.call(element.parentNode.children,element)}
        """

        element_data = WebDriverWait(self.driver,40).until(lambda elem_data : self.driver.execute_script(runtime_str, element))
        return element_data

    def waitPopupTags(self, target = ''):

        js_str = \
        """
            return document.querySelectorAll(arguments[0]).length
        """
        expiration = 1
        num_frames = 0
        while expiration > 0:
            cur_frame = self.driver.execute_script(js_str, target)
            if num_frames != cur_frame:
                expiration +=1
                num_frames = cur_frame
            print(expiration)
            time.sleep(1)
            expiration -= 1
        print('Done')

    def waitInteractible(self, element):
        js_str = \
        """
            let e = arguments[0];
            e.scrollIntoView();
            return true;
            if((e.getAttribute('onclick')!=null)||(e.getAttribute('href')!=null))
            {
                
                return true
            }
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

    def removeiFrames(self):
        js_str = \
        """
        let iframes = document.querySelectorAll('iframe');
        for (let i = 0; i < iframes.length; i++) 
        {
            iframes[i].parentNode.removeChild(iframes[i]);
        }
        if(document.querySelectorAll('iframe').length == 0)
        {
            return true
        }
        """
        WebDriverWait(self.driver,20).until(lambda results: self.driver.execute_script(js_str))



class WebNavigator(WebExtractor, WebJavaScript):
    # For navigating web using combination of selenium python functions and javascript. Clicking and waiting.
    def __init__(self, urls: list, start_tag: str, text_targets: list, stop_targets: list, tag_targets: list, prop_targets: list, \
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
        self.stop_targets = stop_targets
        self.iter_sis = iter_sis
        self.ignore=\
            {
                'BR':True,
                'HR':True,
                'SPACER':True
            }
        WebExtractor.__init__(self,extract = extract, download = download)
        WebJavaScript.__init__(self)
        


    def getScanJS(self,url_num: int = None, search_num: int = None, mode: str= 'match', xpath: str = 'null'):

        run_str = \
        '''
            let selenium = new Selenium({target:'TYA_TXT_TRGT', props:TYA_PROP_TRGT, target_tags:TYA_TAG_TRGT, action: 'TYA_ACTION', xpath: TYA_XPATH});
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
        '''
        s_js_str = list(self.js_functs['scanner'])
        s_js_str.append(run_str)
        if mode == 'match':
            if url_num != None and search_num != None:
                txt_target = self.text_targets[url_num].split(";")[search_num]
                tag_target = self.tag_targets[url_num].split(";")[search_num].split('|')
                stop_target = self.stop_targets[url_num].split(";")[search_num].split('|')
                prop_target = self.prop_targets[url_num].split(';')[search_num].split('|')
            else:
                raise ValueError ('You selected match mode, but url_num and search_num are missing their values.\nPlease re-instantiate Selenium class with right arguments for init.')
        elif mode == 'xpath':
            txt_target, tag_target, stop_target, prop_target = '',[],[],[]
        s_js_str = \
            '\n'.join(s_js_str)\
            .replace("TYA_START",self.start_tag)\
            .replace("TYA_TXT_TRGT",txt_target)\
            .replace("TYA_PROP_TRGT",str(prop_target))\
            .replace("TYA_TAG_TRGT",str(tag_target))\
            .replace("TYA_ACTION",mode)\
            .replace("TYA_XPATH",str(xpath))\
            .replace("TYA_STOP_TRGT",str(stop_target))\
            .replace('export','')

        return s_js_str
    
    def navigateURLS(self, wait: bool = False):
        for index, url in enumerate(self.urls):
            self.driver.get(url)
            if wait:
                self.awaitPageLoad(url_num = index)

    def scanHTML(self, js_str):
        return WebDriverWait(self.driver, 300).until(lambda element: self.driver.execute_script(js_str))

    def iterSisLinks(self, url_num: int, search_num: int):
        self.waitPopupTags(target="iframe")
        self.removeiFrames()
        runtime_str =  self.getScanJS(url_num = url_num, search_num = search_num, mode = 'match')
        #FIND MATCH AND GET THE XPATH TO USE in Selenium JS Class
        match_result = self.scanHTML(runtime_str)
        #NOTE This result MUST be 100% pinpointing to element. This means using more specific property attributes, text, and/or tags in main.py args to isolate.
        el = match_result[0]['element']
        el_xpath = match_result[0]['xpath']
        el_data = self.getElementData(el)
        el_index = el_data['index']
        par_children = self.getElementData(el_data['parent'])['num_children']
        par_xpath = list(el_xpath) #copy
        par_xpath.pop() #remove last item in array to represent parent node
        c_grid = list(el_xpath)
        for i in range(el_index, par_children):
            runtime_str =  self.getScanJS(mode = 'xpath', xpath = c_grid)            
            el_data= self.scanHTML(runtime_str)
            el = el_data['element']
            el_xpath = el_data['xpath']
            el_tag = el.tag_name.upper()

            print('Gen XPath: ',el_xpath,'------- Current XPath: ',c_grid,'\nText: ',el.text,'\nTag: ',el.tag_name)
            c_lkey = c_grid.pop()
            c_grid.append(c_lkey + 1)
            if el_tag in self.ignore:
                continue
            self.waitInteractible(element = el)
            el.click()
            self.waitPopupTags(target="iframe")
            self.removeiFrames()



    def awaitPageLoad(self, url_num: int = 0):
        txt_targets = self.text_targets[url_num].split(";")
        for search_num, trgt_text in enumerate(txt_targets):
            trgt_text =  trgt_text.lstrip()
            if self.iter_sis:
                self.iterSisLinks(url_num = url_num, search_num = search_num)
            else:
                runtime_str =  self.getScanJS(url_num = url_num, search_num = search_num)
                match_result = WebDriverWait(self.driver, 90).until(lambda element: self.driver.execute_script(runtime_str))[0]
                element = match_result['element']
                grid = match_result['xpath']
                element.click()
                WebDriverWait(self.driver, 90).until(lambda element: self.driver.execute_script(self.js_functs['wait_refresh']))
                print('Finished wait load')


#'--disable-gpu' #'https://www.w3schools.com/css/css3_backgrounds.asp' #"CSS Advanced Background Properties"

def main(driver_config: list = [], urls: str = ['https://www.w3schools.com/css/css3_backgrounds.asp','https://facebook.com'], 
    text_targets: list = ['CSS Rounded Corners', 'Log In'], stop_targets: list = ['CSS Response'],
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
        urls = urls, text_targets = text_targets, stop_targets = stop_targets, tag_targets = tag_targets, \
        prop_targets = prop_targets, extract = extract, download = download, iter_sis = iter_sis, mode = mode)

    navigator.navigateURLS(wait = True)
    navigator.driver.close()
    

if __name__ == '__main__' or __name__ == 'configurator.apis.Cloud_Scan.main':
    main()