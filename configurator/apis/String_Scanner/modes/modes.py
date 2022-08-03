import re
from ...Utilities.logger import Logger
from ...Utilities.file_manager import FileManager
from ...Utilities.dev import Development
FS = FileManager()
DEV = Development()
DEV.makeTestDir('String_Scanner')
DEV.makeTestDir('String_Scanner/Test_Scans')
LOGGER = Logger()

class StringParser():
    def __init__(self):
        self.actions=\
        {
            'Scan':self.scan,
            'Replace':self.replace
        }
    def parse(self,txt: str, file: str):
        return self.actions[self.mode](txt = txt, file = file)

    def scan(self, txt: str) -> dict:
        simple_string = str(txt)
        match = self.evaluateMultiple(search_str= simple_string, keywords = self.keywords) 
        return {'match':match, 'source':simple_string}
    def replace(self, txt: str, file: str) -> dict:
        extracted_text = str(txt)
        match = self.evaluateMultiple(search_str= extracted_text, keywords = self.keywords)  
        text_modified = self.evaluateReplace(search_str = extracted_text, matches = match)  
        if txt == text_modified:
            return {'match':match, 'source':txt}
        FS.writeText(file = file, text = text_modified, overwrite=self.overwrite)
        return {'match':match, 'source':txt, 'modified':text_modified}

    def process_files(self, txt_or_path: str) -> dict:
        files = FS.findFilesbyExt(location = txt_or_path, file_type = self.file_type, open_file=self.open_file)
        processed_data = []
        if len(files) == 0: #means We received a string a not a directory/filepath
            processed_data.append(self.parse(txt = txt_or_path))
        else:
            for file in files:
                extracted_text = FS.extractText(file = file,open_file = self.open_file)
                modified_text= self.parse(txt = extracted_text,file = file)
                processed_data.append(modified_text)
        return processed_data

class RegexMatch(StringParser):
    def __init__(self,custom_regex: str, multiple : bool, choose_group: str):
        self.custom_regex = custom_regex
        self.multiple = multiple
        self.choose_group = choose_group
        super().__init__()

    def evaluateMultiple(self, search_str:str, keywords: list = []) -> list:
        if self.multiple == False:
            return self.getFirstMatch(search_str = search_str, keywords = keywords)
        else:
            return self.getAllMatches(search_str = search_str, keywords = keywords)

    def getAllMatches(self, search_str: str, keywords: list = []) -> list:
        match_list = []
        for kw in keywords:
            comb_regex = self.buildRegex(keyword = kw, custom_regex = self.custom_regex) 
            matches = re.findall(pattern = comb_regex,string = search_str) #returns list with inner tuples for found_groupings
            #... Logic to parse through match results
            if len(matches) == 1:
                match_result = self.isolateMatch(matches[0],keyword = kw, choose_group = self.choose_group)
                if match_result != None:
                    match_list.append(match_result)
            elif len(matches) > 1:
                match_result = self.checkDuplicates(matches = self.isolateMatches(matches,keyword = kw, choose_group = self.choose_group))
                filtered_result = []
                for mr in match_result:
                    if mr != None:
                        filtered_result.append(mr)

                #Extend with multiple dictionarys [{'match':val},{'match':val},{'match':val},{'match':val},{'match':val}]
                match_list.extend(filtered_result) #TODO check duplicates too
        return match_list
            
    def getFirstMatch(self, search_str:str, keywords: list = []) -> list:
        """
        Return list of all matches. Each match should be isolated string and not contain groups.
        Returned list will be evaluated for length in next step.
        """
        for kw in keywords:
            comb_regex = self.buildRegex(keyword = kw, custom_regex = self.custom_regex) 
            matches = re.findall(pattern = comb_regex,string = search_str) #returns list with inner tuples for found_groupings
            #... Logic to parse through match results
            if len(matches) == 1:
                match_result = self.isolateMatch(matches[0],keyword = kw, choose_group = self.choose_group)
                if match_result == None:
                    match_result = []
                else:
                    match_result = [match_result]
                return match_result
            elif len(matches) > 1:
                match_result = self.checkDuplicates(matches = self.isolateMatches(matches,keyword = kw, choose_group = self.choose_group))
                filtered_result = []
                for mr in match_result:
                    if mr != None:
                        filtered_result.append(mr)
                return filtered_result
        return [] #Implied no matches here after iterating through all of keywords

    def checkDuplicates(self, matches: list) -> list:
        if len(matches) == 0: 
            return []
        uniques = {matches[0]['match']:True}
        unique_matches = [matches[0]]
        for match_dict in matches:
            if match_dict['match'] not in uniques:
                uniques[match_dict['match']]=True
                unique_matches.append(match_dict)
        return unique_matches
            
    def isolateMatch(self,match: any, keyword:str = '', choose_group:str = '') -> str:
        match_dict = {}
        group_index = 0
        if choose_group != '':
            group_index = int(choose_group)
        if isinstance(match,tuple) or isinstance(match,list):
            match = match[group_index] #first index of tuple is the whole match
        elif isinstance(match,str):
            pass 
        match_dict['match'] = match
        return match_dict

    def evaluateReplace(self,match:str,search_str:str):
        return search_str

    def isolateMatches(self,matches:list = [], keyword: str = '', choose_group: str= '') -> list:
        """
        Args:
            matches variable will be list with either strings or tuple
        """
        new_matches = []
        for match in matches:
            match_result = self.isolateMatch(match = match, keyword = keyword, choose_group = choose_group)
            if match_result != None:
                new_matches.append(match_result)
        return new_matches

    def buildRegex(self,keyword:str,custom_regex: str) -> str:
        # logic to allow custom regex patterns per particular case i.e. if scanning pdf documents for different financial documents, each vendor has different format hence -> custom regex patterns
        #print(f"({keyword}{custom_regex})")
        comb_regex = f"({keyword}{custom_regex})"
        return comb_regex
        

class Scan(RegexMatch): #has Category properties Category.__dict__
    def __init__(self,categ_attribs:dict, multiple: bool, open_file: bool, file_type: str):
        print('\n\n Init Scan')
        self.mode = 'Scan'
        self.categ_attribs = categ_attribs # to store for debugging
        self.keywords = categ_attribs['keywords']
        self.custom_regex = categ_attribs['custom_regex']
        self.open_file = open_file
        self.file_type = file_type
        RegexMatch.__init__(self,custom_regex = categ_attribs['custom_regex'],  multiple = multiple, choose_group = categ_attribs['choose_group'])
        
        """ 
        #Parent function only returns same string. Since this is scan. We do not override.
        def evaluateReplace(self, amtches: list, search_str:str) 
            pass

        #Parent function does not map keyword to match. Needed for replace module to correctly map replacements. Not overriden for Scan mode.
        def isolateMatch(self,match: any, keyword:str = '', choose_group:str = '') -> str: 
            ...
        """

class Replace(RegexMatch):
    do_multiple = False
    def __init__(self,categ_attribs:dict, multiple: bool, replace_all: bool, repl_vals: list, open_file: bool, overwrite: bool, file_type: str):
        print('\n\n Init Replace')
        self.mode =  'Replace'
        self.categ_attribs = categ_attribs # to store for debugging
        self.keywords = categ_attribs['keywords']
        self.custom_regex = categ_attribs['custom_regex']
        self.replace_all = replace_all
        self.repl_vals = repl_vals
        self.repl_map = {}
        self.open_file = open_file
        self.overwrite = overwrite
        self.file_type = file_type
        for index, keyw in enumerate(self.keywords):
            try:
                self.repl_map[keyw]= self.repl_vals[index]
            except:
                self.repl_map[keyw]= ''
        RegexMatch.__init__(self,custom_regex = categ_attribs['custom_regex'], multiple = multiple, choose_group = categ_attribs['choose_group'])

    def evaluateReplace(self,matches:list,search_str:str):
        replace_count = 1
        if self.replace_all == True:
            replace_count = -1
        for mtch in matches:
            search_str = search_str.replace(mtch['match'],mtch['replace'],replace_count)
        return search_str

    def isolateMatch(self,match: any, keyword:str = '', choose_group: str = '') -> str:
        match_dict = {}
        group_index = 0
        if choose_group != '':
            group_index = int(choose_group)
        if isinstance(match,tuple) or isinstance(match,list):
            match = match[group_index] #first index of tuple is the whole match
        elif isinstance(match,str):
            if match == '':
                return
        else:
            return
        match_dict['match'] = match
        match_dict['replace'] = self.repl_map[keyword]
        return match_dict
