from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os, pandas as pd
from ..Utilities.dev import Development
from ..Utilities.file_manager import FileManager
import time

DEV = Development()
DEV.makeTestDir(proj_name = 'Cloud_Scan')

class WebExtractor():
    #Has useful methods for reading or clicking data with methods for catching dry selenium elements and iterating through them.
    def __init__(self, extract: bool = False, download: bool = False):
        self.extract = extract
        self.download = download
        self.configs = \
            {
                'Sign In': 
                    {'ignore':{'style': True, 'iframe': True, 'script': True, 'path': True,'svg': True, 'text':True, 'svg':True, 'form':True,'dialog':True},
                    'prop_trgs':{'aria-label': True, 'value': True},
                    'filt_trgs': {'input': True, 'a': True}}
            }

class WebNavigator(WebExtractor):
    # For navigating web using combination of selenium python functions and javascript. Clicking and waiting.
    def __init__(self, urls: list, click_targets: list, extract: bool, download: bool, 
                driver_options: Options = Options(),  driver_loc: os.PathLike = None):
        if driver_loc == None:
            raise ValueError('Please pass in location of your webdriver for chrome.')
        self.urls = urls
        self.click_targets = click_targets
        self.driver = webdriver.Chrome(executable_path = driver_loc, options = driver_options)
        super().__init__(extract = extract, download = download)

    def navigateURLS(self, wait: bool = False):
        index = 0
        for url in self.urls:
            self.driver.get(url)
            if wait:
                self.awaitPageLoad(target = self.click_targets[index])
            #time.sleep(20)
            index +=1

    def awaitPageLoad(self, target: str):
        body_elements = self.driver.find_elements(by=By.TAG_NAME, value = 'body')
        print(body_elements[0].tag_name)
        matches = self.findByBruteRec(body_elements, target = target)
        if len(matches) == 1:
            return matches
        elif len(matches) > 1:
            print(matches)
            raise ValueError('Too many matches. Try different target or use xpath instead')
        else:
            print('No Matches: ',matches)

    def findEfficiient(self, elements: list, target: str, 
                        choose_config: str = 'Sign In',
                        prop_attribs: list = ['aria-label', 'value'],
                        n: int = 0):
        pass
    def findByBruteRec(self, elements: list, target: str, 
                        choose_config: str = 'Sign In',
                        prop_attribs: list = ['aria-label', 'value'],
                        n: int = 0):
        match_vals = []

        if isinstance(elements, list):
            for i, child in enumerate(elements):
                if child.tag_name in self.configs[choose_config]['ignore']:
                    continue
                if n == 1 or n ==2:
                    print(n, f" {child.tag_name} ---- id: {child.get_attribute('id')} ------- class: {child.get_attribute('class')}")
                sub_child = child.find_elements(by = By.XPATH, value = './/*')
                if child.tag_name in self.configs[choose_config]['filt_trgs']:
                    if child.text == target:
                        return match_vals.append('element: ',child)
                    for prop in self.configs[choose_config]['prop_trgs']:
                        if child.get_attribute(prop) == target:
                            return match_vals.append('element: ',child)
                    
                if len(sub_child) > 0:
                    match_vals.extend(self.findByBruteRec(elements = sub_child, target = target, n= n + 1))
                

        return match_vals



#'--disable-gpu'
def main(driver_config: list = [], urls: str = ['https://google.com','https://facebook.com'], click_targets: list = ['Sign In'], 
        extract: bool = False, download = False):
    """
    Summary: Goal of this program is to navigate multiple urls and find targets per click_target/ other optional arguments and perform actions of extract or download.
    If multiple urls are passed in, the click_targets list argument should have lists within matching the number of urls since each site have different setups/parameters.
    Method is build in to parse through all html elements until chosen element with text is found.
    """
    options = Options()
    for option in driver_config:
        options.add_argument(option)

    navigator = WebNavigator(driver_options = options, driver_loc = "C:\\Users\\hduon\\Documents\\Enzyme\\configurator\\apis\\Cloud_Scan\\src\\chromedriver.exe",
    urls = urls, click_targets = click_targets, extract = extract, download = download)

    navigator.navigateURLS(wait = True)
    navigator.driver.close()
    

if __name__ == '__main__' or __name__ == 'configurator.apis.Cloud_Scan.main':
    main()