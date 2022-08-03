import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class Graphs(): #to many args in matplotlib, #TODO add to this class to manage graphs
    def __init__(self):
        pass


class DataFrames():
    #TODO allow multiple dataframes to be pulled and concated per arguments
    def __init__(self):
        self.df = None
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
    def addRow(self, data: list):
        self.df.loc[len(self.df.index)] = data
    def buildDF(self, data:list = [], columns: list= [], index:list = []):
        if len(index) != 0 and len(index) == len(data):
            self.df = pd.DataFrame(data = data, columns = columns,index = index)
        else:
            self.df = pd.DataFrame(data = data, columns = columns)
    def stats(self, df: pd.DataFrame):
        return  df.describe()

    def plotHistogram(self, df: pd.DataFrame, column: str, graph_type:str, bins: int = 100, save_loc: os.PathLike = None):
        df[column].hist(bins = bins)
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()
    def plotCounts(self,
        df: pd.DataFrame, col_names: str, graph_type:str, bins: int = 100, labels:list = [None, None], save_loc: os.PathLike = None):
        plot = df[col_names].value_counts().plot(kind = graph_type)
        if labels[0]:
            plot.set_xlabel(labels[0])
        if labels[1]:
            plot.set_ylabel(labels[1])
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()

    def plotDistribution(self, col_names: str, output_col: str, objs: list = [], operation: str = "mean", axis: int = 1, 
                        labels: list = [None,None], save_loc: os.PathLike = None):
        concat_df = pd.concat(objs, axis = axis).groupby(col_names)[output_col]
        if operation == "mean":
            concat_df = concat_df.mean()
        self.plotCounts(df = concat_df, labels = labels)

class Plotter():
    def __init__(self):
        pass
    def regLinear(self, x: list, y: list, axis: list = [], point_color:str = 'b-', save_loc: os.PathLike = None):
        #axis: [xbeginning, xend, ybeginning, yend]
        plt.plot(x, y, 'ro')
        plt.axis(axis)
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x,y,1))(np.unique(x)))
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()




