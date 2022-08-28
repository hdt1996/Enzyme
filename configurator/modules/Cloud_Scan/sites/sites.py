from ...Utilities.py.dataframes import DataFrames
from ...Utilities.py.util import buildDictBoolbyArr
import pandas as pd
import re
DF = DataFrames()

class w3Schools():
    def __init__(self):
        self.cols_drop = \
            ['Try it','Demo','Play it']
        self.ctxt_remove = \
            'Try it'
        self.cn_remove=\
            '/value'
        self.cint_rename = \
            {
                2: {0:'Value',1:'Description'},
            }
        self.indices =\
            [
                'Selector','Element','Value','Font_Family','Function','Px','Unit','Property','Char','Section'
            ]
        self.tables = \
            [
                'CSS Animatable',
                'CSS Browser Support',
                'CSS Default Values',
                'CSS Entities',
                'CSS Fallback Fonts',
                'CSS Functions',
                'CSS PX-EM Converter',
                'CSS Reference',
                'CSS Reference Aural',
                'CSS Selectors',
                'CSS Units',
                'CSS_Properties'
            ]


    def assignBrowsers(self, col_name):
        browsers = ['Chrome','Edge','FireFox','Safari','Opera']
        return browsers[int(col_name.split(':')[1])- 1]


    def cleanCapitalize(self, col_name):
        new_name = re.split('[- ]',col_name)
        for index, word in enumerate(new_name):
            new_name[index] = word.capitalize()
        return '_'.join(new_name)

    def checkColNames(self, df: pd.DataFrame):
        df_col_len = len(df.columns)
        if DF.allIntColumns(df):
            df = df.rename(columns = self.cint_rename[df_col_len])
            return df
        for col in df.columns:
            if 'Unnamed:' in col:
                new_name = self.assignBrowsers(col_name = col)
            elif 'Property Value' in col:
                new_name = 'Value'
            elif 'Property/Value' in col:
                new_name = 'Value'
            elif 'Font format' in col:
                new_name = 'Value'
            elif 'Font descriptor' in col:
                new_name = 'Property'
            elif 'Values' in col:
                new_name = 'Value'
            elif 'Filter' in col:
                new_name = 'Value'
            elif 'Result' in col:
                new_name = 'Property'
            elif 'Entity Number' in col:
                new_name = 'Value'
            elif 'Length Unit' in col:
                new_name = 'Unit'
            elif 'Default CSS Value' in col:
                new_name = 'Value'
            elif 'CSS Entity' in col:
                new_name = 'Value'
            else:
                new_name = self.cleanCapitalize(col_name = col)
            df = df.rename(columns = {col:new_name})
        return df

    def setIndex(self,df: pd.DataFrame, df_name):
        unique_cols = buildDictBoolbyArr(arr = df.columns)
        if 'CSS' not in df_name.upper():
            df = df.set_index('Section')
            return df
        for index in self.indices:
            if index in unique_cols:
                df = df.set_index(index)
                return df

    def process_columns(self, sub_df: pd.DataFrame):
        sub_df = DF.removeColumns(df = sub_df, col_to_remove=self.cols_drop)
        sub_df = DF.changeColDtype(df = sub_df, types = 'string')
        sub_df = DF.removeTextByCol(df = sub_df, texts = self.ctxt_remove)
        sub_df = self.checkColNames(df = sub_df)
        return sub_df

