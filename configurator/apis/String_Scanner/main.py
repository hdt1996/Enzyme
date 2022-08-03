from .locals.globals_config import CATEG_MAP, MODE_MAP, CLI_ORDER
from ..Utilities.util import kwargsReturnValues, splitStringbyDelim
from ..Utilities.file_manager import FileManager
from ..Utilities.dev import Development
from ..Utilities.logger import Logger
from .modes.modes import Scan, Replace
import click, traceback

FS = FileManager()
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

@click.command()
@click.option("--keywords", multiple = True, default = []) #target for text or prepended phrases for finding type of data
@click.option("--location",type = str,required = True) #directory/filepath
@click.option("--debug",type=bool,default = True) #additional special cases #TODO for how to use
@click.option("--mode",type=str,default = "Scan") #to scan or replace match found inside str
@click.option("--category",type=str,default = "Universal") #to scan or replace match found inside str
@click.option("--custom_regex",type=str, default = "") #custom regex option to overwrite regexBuilder
@click.option("--file_type",type=str,default = '') #are we passing in a str or a file path
@click.option("--cases",type=str,default = '') #additional special cases #TODO for how to use
@click.option("--multiple",type=bool,default = False) #additional special cases #TODO for how to use
@click.option("--replace_all",type=bool,default = False) #additional special cases #TODO for how to use
@click.option("--repl_vals", multiple = True,default=[])  #target for text or prepended phrases for finding type of data
@click.option("--open_file", type = bool, default = False) #Set mode to open file and extract text. If false and looking at a file, only scan through filename
@click.option("--choose_group",type = str, default = '')  #Choose group in regex match results to get exact match
@click.option("--overwrite",type = bool, default = False) #Specific for overwriting files, only compatible with open_file option as True
@click.option("--rename",type = bool, default = False) #Specific for renaming files, only compatible with open_file option as False

# NOTE If rewrite and rename was desired, this main function should be called two times with Scan and Replace Mode in any order desired. Combining both Scan and Replace
# into one super module for the case above would decrease legibility. If a custom module was desired, there is a cases folder for custom cases for building new super'd classes.
def main(keywords:list,location:str,**kwargs:dict) -> None:
    try:
        original_location = str(location)
        var_names = splitStringbyDelim(CLI_ORDER,[','],[' '])
        category, mode, custom_regex, file_type, cases, multiple, \
            replace_all, repl_vals, open_file, choose_group, overwrite, rename =\
            kwargsReturnValues(kwargs = kwargs, var_names = var_names)

        if overwrite == True and open_file == False:
            raise ValueError('Overwrite CLI Argument cannot be True while open_file is False')
        LOGGER.debug_dict = kwargs
        LOGGER.addDebugVars(['original_src','location'],[original_location, location])
        regex_category = CATEG_MAP[category]()

        if choose_group != '':
            regex_category.choose_group = choose_group
        if len(keywords) != 0:
            regex_category.keywords = keywords
        if custom_regex != "":
            regex_category.custom_regex = custom_regex
        if len(repl_vals) != 0:
            regex_category.repl_vals = repl_vals
        
        if mode == 'Scan':
            parser = Scan(categ_attribs = regex_category.__dict__, multiple = multiple)
            reader = parser.scan
        elif mode == 'Replace':
            parser = Replace(categ_attribs = regex_category.__dict__, multiple = multiple, replace_all = replace_all, repl_vals = repl_vals)
            reader = parser.replace

        LOGGER.addDebugVars(['keywords','custom_regex','choose_group', 'repl_vals'], [parser.keywords, parser.custom_regex, parser.choose_group, parser.repl_vals])

        files = []
        files = FS.findFilesbyExt(location = location, file_type = file_type,open_file=open_file)
        LOGGER.addDebugVars(['files'],[files])

        if len(files) == 0:
            reader(txt_or_file = location)
            #LOGGER.logVars(debug = True,vars = debug_dict, isolate = ['location'])
        else:
            for file in files:
                extracted_text = FS.extractText(file = file)
                modified_text = reader(txt_or_file = extracted_text)
                FS.writeText(file = file, text = modified_text, overwrite=overwrite) #makes copy or overwrites based on overwrite CLI arg

    except BaseException:
        error_log = traceback.format_exc().split('File')
        LOGGER.traceRelevantErrors(error_log = error_log, script_loc =  __file__, latest = True)
        
if __name__ == '__main__' or __name__ == 'configurator.apis.String_Scanner.main':
    T= True
    if T:
        main(\
            [
                "--debug", True,
                "--keywords", "Hello",
                #"--keywords", '[\s\S]*', #for matching everything including new lines
                #"--keywords", r'NEW BALANCE ',
                #"--keywords", 'NOT TESTING',
                #"--keywords", r'logger',
                #"--keywords",r"datetime",
                "--location", DEV.proj_test_dir,#__file__,
                "--mode", 'Replace',
                "--category", "Universal",
                #"--custom_regex",r".*",
                "--file_type", '.txt',
                #"--cases","Capital One",
                "--multiple", True,
                "--replace_all", True,
                "--repl_vals","OVERRIDE",
                #"--repl_vals","TESTING",
                #"--repl_vals","test3",
                #"--repl_vals","test4",
                "--open_file", True,
                #"--choose_group", 2,
                "--overwrite", False

            ])
    else:
        main()
    
    #Example cmd shell usage with options/arguments
    #python -i main.py --location "C:\Users\hduon\Documents\Future_Projects-PsuedoCode\test files" --file_type ".txt" --category Balance --mode Replace --replace_all True --multiple True --debug True --repl_vals "rrrrrrrrr" --open_file True
