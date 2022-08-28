import pandas as pd
from ...Utilities.py.util import buildDictBoolbyArr

class DataFrames():
    #TODO allow multiple dataframes to be pulled and concated per arguments
    def __init__(self, df_col_names = [], df_index = ''):
        self.df = pd.DataFrame()
        self.col_dict = {}
        self.df_index = df_index
        if self.df_index != '':
            if not self.df_index in df_col_names:
                raise ValueError('Make sure self.df_index is one of the column names.')
        for col in df_col_names:
            self.col_dict[col] = []
        if len(df_col_names) != len(self.col_dict):
            raise ValueError('Column_Name list error. One of them are duplicates. Please make each unique.')

    def combine(self, col_to_join: str, main_df: pd.DataFrame, new_df: pd.DateOffset, join_type: str = 'outer'):
        main_df = main_df.merge(right = new_df, how = join_type, on = col_to_join)
        return main_df

    def getDatabyURL(self,url):
        if url == None:
            return pd.DataFrame()
        return pd.read_csv(url)

    def buildSeriesList(self, nested_list:list, col_names: list):
        result_list = []
        for s_list in nested_list:
            result_list.append(pd.Series(data = s_list, index = col_names))
        return result_list

    def addColumn(self, df: pd.DataFrame, data: list, col_name: str):
        # Data parameter must be list and must match length of dataframe
        df[col_name] = data
        return df

    def removeColumns(self, df: pd.DataFrame, col_to_remove: list):
        df_uniques = buildDictBoolbyArr(df.columns)
        for ctr in col_to_remove:
            if ctr in df_uniques:
                df = df.drop(columns = ctr)
        return df

    def changeColDtype(self, df: pd.DataFrame, types: list|str = 'string'):
        if isinstance(types, str):
            for col in df.columns:
                df[col]=df[col].astype(dtype = types)
        elif isinstance(types, list):
            for index, col in enumerate(df.columns):
                df[col]=df[col].astype(dtype = types[index])
        return df

    def removeTextByCol(self,df: pd.DataFrame, texts: list|str):
        if isinstance(texts, str):
            for col in df.columns:
                df[col] = df[col].str.replace(texts,'')
        elif isinstance(texts, list):
           for index, col in enumerate(df.columns):
                df[col] = df[col].str.replace(texts[index],'')
        return df

    def addRow(self, data: list):
        self.df.loc[len(self.df.index)] = data

    def buildDFbyList(self, data:list = [], columns: list= [], index:list = []):
        if len(index) != 0 and len(index) == len(data):
            self.df = pd.DataFrame(data = data, columns = columns,index = index)
        else:
            self.df = pd.DataFrame(data = data, columns = columns)

    def stats(self, df: pd.DataFrame):
        return  df.describe()

    def buildDFbyDict(self):
        max_length = None
        for file in self.col_dict:
            arr =  self.col_dict[file]
            if max_length == None:
                max_length = len(arr)
                continue
            if len(arr) != max_length:
                raise ValueError(f'Array length -- {len(arr)} -- within {file} does not match current len -- {max_length} --.\nCheck that CLI arg check_multiple = False')
        if self.df_index == '':
            self.df = pd.DataFrame(data =  self.col_dict)
        else:
            self.df = pd.DataFrame(data =  self.col_dict).set_index(self.df_index)
        return self.df

    def allIntColumns(self, df: pd.DataFrame):
        for col in df.columns:
            if not isinstance(col, int):
                return False
        return True


