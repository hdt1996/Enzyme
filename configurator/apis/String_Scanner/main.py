from multiprocessing.sharedctypes import Value
from .locals.globals_config import CATEG_MAP, CLI_ORDER
from ..Utilities.util import kwargsReturnValues, splitStringbyDelim
from ..Utilities.dev import Development
from ..Utilities.logger import Logger
from .modes.modes import Scan, Replace
from ..Utilities.dataframes import DataFrames
import click, traceback
import os
import pandas as pd

DEV = Development()
DEV.makeTestDir('String_Scanner')
DEV.makeTestDir('String_Scanner/Test_Scans')
LOGGER = Logger()


"""
Author: Hung Tran

Summary:
    Goal of this utility is to find text matches from any giving string or extracted text of files within a directory.
    Matches are found using combined regex formats, dynamically adjusted per the keywords sent in and custom category classes with their own unique formats.
    There are primarily two different modes or actions to take with the results of the match using: Scan or Replace
    Scan will only give us the results of the match. Replace will give us the results of the match while replacing the match with empty for now. #TODO replace with format/word of our choosing.
    Other optional arguments will change functionality of operation. Detais listed below in CLI Args.

CLI Args:
    Keywords: List, List of target words to search in text. First argument for building regex with customized formats
    Location: String, text string, filepath, or directory. All text based on extension argument will be extracted for text
    Debug: Bool, debug mode will disable/enable loggers placed inside main.py
    Mode: String, Choose different modes - Scan, Replace, etc.
    Category: String, Choose one of pre-made categories for searching, i.e. Balance, SSN, Date, etc.
    Custom_Regex: Raw String, Use your own regex to overwrite category or General Regex in Universal category class (when no category is specified)
    File_Type: String, Extension type used to find files within location
    Cases: String, Very optional. In the event clients want to build their own custom classes #TODO not implemented yet
    Multiple: Bool, True or False to set return values for scan/replace to all matches or single match
    Replace All: Bool, Have program replace all instances per match found or replace one by one per match found
    Repl_Vals: List, Maps Match to Replacement. Ex. First match from first keyword/regex combination is replaced with first repl_value...
    Open_File: Bool, if file is active file, open to extract text
    Choose_Group: Str, represents group number in regex match of string
    Overwrite: Bool, chooses whether to overwrite text with replacements or make a copy in same directory with _COPY suffix

Return: None
"""

class MainProcessor():
    def __init__(self, modes, categories, dataframe, location, kwargs: dict):

        self.debug, self.custom_regex, self.multiple, self.replace_all, self.export, self.export_loc, \
        self.unique, self.keywords, self.repl_vals, self.choose_group, self.overwrite, self.rename,\
        self.df_index, self.df_col_names, self.file_type, self.open_file, self.df_mult_override=\
        kwargsReturnValues(kwargs = kwargs, var_names = splitStringbyDelim(CLI_ORDER,[', ']))

        self.modes = modes
        self.location = location
        self.categories = categories
        self.regex_category = None
        self.dataframe = dataframe

        if self.dataframe and (len(self.df_col_names) == 0):
            raise ValueError('Dataframe option is chosen, but no df_col_names or df_index provided. Please supply both.')
        if self.dataframe and self.multiple and not self.df_mult_override:
            raise ValueError('Multiple and DataFrame option together not allowed. If you want all matches to be mapped to single entry, please add df_mult_override option to CLI.')

        self.df_map = {}
        self.scan_data = []
        self.DataFrame = DataFrames(df_index= self.df_index, df_col_names= self.df_col_names)

    def processCategory(self, mode: str, col_index: int):
        self.scan_data = self.parser.process_files(txt_or_path= self.location, file_type= self.file_type, open_file = self.open_file)
        if self.export:
            self.parser.exportResults(processed_data = self.scan_data, export_loc = self.export_loc, unique = self.unique)
        if self.dataframe and mode == 'Scan':
            for data in self.scan_data:
                if isinstance(data['results'], list):
                    for match_results in data['results']:
                        self.DataFrame.col_dict[self.df_col_names[col_index]].append(match_results['match'])
                else:
                    self.DataFrame.col_dict[self.df_col_names[col_index]].append(data['results']['match'])
        #LOGGER.debug_dict = {}
        #LOGGER.addArrDBVars(arr = self.scan_data)
        #LOGGER.logVars(save = True,to_terminal = False, title = f"_{mode}_")

    def processModes(self):
        for mode in self.modes:
            if mode == 'Scan':
                for categ_index, category in enumerate(self.categories):
                    self.regex_category = CATEG_MAP[category](choose_group = self.choose_group, keywords = self.keywords, custom_regex = self.custom_regex)
                    self.parser = Scan(categ_attribs = self.regex_category.__dict__, multiple = self.multiple)
                    self.processCategory(col_index = categ_index, mode = mode)
                if len(self.DataFrame.col_dict) != 0:
                    self.DataFrame.buildDFbyDict()
                    print(self.DataFrame.df)

            elif mode == 'Replace':
                for categ_index, category in enumerate(self.categories):
                    self.regex_category = CATEG_MAP[category](choose_group = self.choose_group, keywords = self.keywords, custom_regex = self.custom_regex)
                    self.parser = Replace(categ_attribs = self.regex_category.__dict__, multiple = self.multiple, replace_all = self.replace_all, 
                    repl_vals = self.repl_vals, overwrite=self.overwrite)
                    self.processCategory(col_index = categ_index, mode = mode)
            else:
                raise ValueError(f'Mode does not exist. Please change to one of the following\n------1)\nScan\n2)\nReplace\n3)\nScan&Replace')

@click.command()
@click.option("--keywords", multiple = True, default = []) #Target for text searches or prepended phrases for finding specific type of data AKA account balances, statement dates, etc.
@click.option("--location",type = str,required = True) #Text argument that can be simple string, file, or directory.
                                                        #Passing in directory leads to search of all files by file_type argument.
                                                        #If open_file is false, only the file names will be parsed.
@click.option("--debug",type=bool,default = True) #Choose whether to log functions. If true, saves log to designed log folder.
@click.option("--modes",multiple = True, default = ["Scan"]) #Scan Mode... Replace Mode... Rename/Reformat in planning...
@click.option("--categories", multiple = True, default = ["Universal"]) #Choose category class that contains pre-designed keywords and regex formats. Default is Universal with empty properties.
@click.option("--custom_regex",type=str, default = "") #Custom regex option to overwrite regexBuilder
@click.option("--file_type", multiple = True, default = ['']) #Extension for FileManager search utility. Can choose any extension as long as encodings are available.
@click.option("--multiple",type=bool,default = False) #During parse, end match process when first match is found, or keep going to get all of them when multiple is true.
@click.option("--replace_all",type=bool,default = False) #Designate whether to replace all items or single item per match found (count = -1 for all in str.replace())
@click.option("--repl_vals", multiple = True,default=[])  #Target for text or prepended phrases for finding type of data
@click.option("--open_file", type = bool, default = False) #Set mode to open file and extract text. If false and looking at a file, only scan through filename
@click.option("--choose_group",type = str, default = '')  #Choose group in regex match results to get exact match
@click.option("--overwrite",type = bool, default = False) #Specific for overwriting files, only compatible with open_file option as True
@click.option("--rename",type = bool, default = False) #Specific for Scan Mode: renaming files, only compatible with open_file option as False
@click.option("--export",type = bool, default = False) #Specific for Scan Mode: export matches
@click.option("--export_loc",type = str, default = '') #Specific for Scan Mode: export location of matches. Can end in any extension desired... .py .txt etc.
@click.option("--unique", type = bool, default = False) #Specific for Scan Mode: modifies export of matches to have only unique entries

#_---------------------------------------------------DATAFRAME NOTES ____________________________________________________________________#
@click.option("--dataframe", type = bool, default = False) #Allows taking matches and placing them into dataframe for database use. Requiries df_* CLI args below
@click.option("--df_col_names", multiple = True, default = []) #Set column names for each match in order of list passed in
@click.option("--df_index", type = str, default = '') #Set index/identifier for dataframe. Useful for comparing data from database or mapping column values to file_number.. etc.
@click.option("--df_mult_override", type = bool, default = False) #Set index/identifier for dataframe. Useful for comparing data from database or mapping column values to file_number.. etc.
#NOTE
# Dataframes usually only have one datatype in there, not an object with length such as list or JSON. IF this is what you need, set multiple to False to only find first match.

# ALSO, make sure there are no keywords set. For database solutions, I recommend using the native category classes. If modification is needed. You make changes there!

# The most important reason for using the default classes is to allow recursion of the keyword and custom_regex arguments. If keyword or custom_regex arguments are passed
# the keywords and custom_regex will not change.

# If rewrite and rename was desired, this main function should be called two times with Scan and Replace Mode in any order desired. Combining both Scan and Replace
# into one super module for the case above would decrease legibility. If a custom module was desired, there is a cases folder for custom cases for building new super'd classes.
def main(modes: list, categories: list, location:str, dataframe: bool, **kwargs:dict) -> None:
    try:
        main_processor = MainProcessor(modes = modes, categories = categories, location = location, dataframe = dataframe, kwargs = kwargs)
        if main_processor.overwrite == True and main_processor.open_file == False:
            raise ValueError('Overwrite CLI Argument cannot be True while open_file is False')
        main_processor.processModes()
    except BaseException:
        error_log = traceback.format_exc()
        LOGGER.traceRelevantErrors(error_log = error_log.split('File "'), script_loc =  DEV.proj_dir, latest = False)
        
if __name__ == '__main__' or __name__ == 'configurator.apis.String_Scanner.main':
    T= True
    if T:
        main(\
            [
                "--debug", True,
                #"--keywords", "HELLO",
                #"--keywords", '[\s\S]*', #for matching everything including new lines
                #"--keywords", r'NEW BALANCE ',
                #"--keywords", 'NOT TESTING',
                #"--keywords", r'logger',
                #"--keywords",r"",
                "--location", os.path.join(DEV.proj_test_dir),#,"encodings.txt"),#__file__,
                #"--location", "C:\\Users\\hduon\\Documents\\Tests\\String_Scanner\\Test_Scans\\Admin_RESULTS_1_RESULTS_1.css",
                "--modes", 'Scan',
                #"--modes", 'Replace',
                "--categories", "CSS",
                "--categories", "Balance",
                "--categories", "CSS",
                "--categories", "Balance",
                "--categories", "CSS",
                "--categories", "Balance",
                "--categories", "CSS",
                "--categories", "Balance",
                #"--custom_regex",r".*",
                "--file_type", '.css',
                #"--file_type", '.scss',
                #"--multiple", True,
                #"--replace_all", True,
                #"--repl_vals","OVERRIDE",
                #"--repl_vals","TESTING",
                #"--repl_vals","test3",
                #"--repl_vals","test4",
                "--open_file", True,
                #"--choose_group", 2,
                #"--overwrite", False,
                #"--export", True,
                #"--export_loc", DEV.proj_test_dir,
                #"--unique", False,
                "--dataframe", True,
                "--df_col_names", "CSS",
                "--df_col_names", "Balance",
                "--df_col_names", "Test_0",
                "--df_col_names", "Test_1",
                "--df_col_names", "Test_2",
                "--df_col_names", "Test_3",
                "--df_col_names", "Test_4",
                "--df_col_names", "Test_5",
                "--df_index", "Balance"

            ])
    else:
        main()
    
    #Example cmd shell usage with options/arguments
    #python -i main.py --location "C:\Users\hduon\Documents\Future_Projects-PsuedoCode\test files" --file_type ".txt" --category Balance --mode Replace --replace_all True --multiple True --debug True --repl_vals "rrrrrrrrr" --open_file True
