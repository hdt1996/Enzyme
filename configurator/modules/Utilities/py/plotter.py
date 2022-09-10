
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

class Plotter():
    def __init__(self):
        self.df_plots = \
            {
                'bar': True,
                'barh': True,
                'hist':True,
                'box':True,
                'kde':True,
                'density': True, #Same as kde
                'area': True,
                'scatter': True,
                'hexbin': True,
                'pie': True

            }
    def regLinear(self, x: list, y: list, axis: list = [], point_color:str = 'b-', save_loc: os.PathLike = None):
        #axis: [xbeginning, xend, ybeginning, yend]
        plt.plot(x, y, 'ro')
        plt.axis(axis)
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x,y,1))(np.unique(x)))
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()


    def plotHistogram(self, df: pd.DataFrame, column: str, bins: int = 100, save_loc: os.PathLike = None):
        df[column].hist(bins = bins)
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()

    def setLabels(self,plot: plt.plot, labels:list):
        if labels[0]:
            plot.set_xlabel(labels[0])
        if labels[1]:
            plot.set_ylabel(labels[1])
        return plot


    def plotColCounts(self,df: pd.DataFrame, col_names: str, graph_type:str = 'scatter', labels:list = [None, None], save_loc: os.PathLike = None, axis_range = [None,None]):
        if not graph_type in self.df_plots:
            raise ValueError ('Please choose one of graphs defined in self.df_plots')
        plot = df[col_names].value_counts().plot(kind = graph_type, xlim = axis_range[0], ylim = axis_range[1])
        plot = self.setLabels(plot = plot, labels = labels)
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()

    def plotGroupMeans(self,  col_names: str|list, output_col: str, graph_type: str = 'scatter', dfs: list = [],  axis: int = 1, 
                        labels: list = [None,None], save_loc: os.PathLike = None, axis_range = [None,None]):
        if not graph_type in self.df_plots:
            raise ValueError ('Please choose one of graphs defined in self.df_plots')
        plot = pd.concat(dfs, axis = axis).groupby(col_names)[output_col].mean().plot(kind = graph_type, xlim = axis_range[0], ylim = axis_range[1])
        plot = self.setLabels(plot = plot, labels = labels)
        if save_loc != None:
            plt.savefig(save_loc)
        plt.clf()