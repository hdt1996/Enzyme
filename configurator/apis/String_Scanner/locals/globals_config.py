from ..categories.categories import *
from ..modes.modes import *

CATEG_MAP = \
{
    'Balance':Balance,
    'Name':Name,
    'Date':Date,
    'SSN':SSN,
    'Address':Address,
    'CreditCards':CreditCards,
    'Property_IDs':Property_IDs,
    'File_Numbers':File_Numbers,
    'Universal':Universal,
    'CSS':CSS
}
MODE_MAP = \
{
    'Scan':Scan,
    'Replace':Replace
}

CLI_ORDER = "debug, custom_regex, multiple, replace_all, export, export_loc, unique, keywords, repl_vals, choose_group, overwrite, rename, df_index, df_col_names, file_type, open_file, df_mult_override"

#"debug, custom_regex, multiple, replace_all, export, export_loc, unique, keywords, repl_vals, choose_group, overwrite, rename, df_index, df_col_names"


