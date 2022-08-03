from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class TensorFlow():
    """ 
    Basics:
        
        Machine Learning: Using one or multiple inputs (feature data) to find rules that we would use to make predictions for labels
        Neural Network: Machine Learning but using multiple layers to transform data before translating to new rules and prediction

    Types of Machine Learning:
        Unsupervised: We have both features (input) and labels (output). Compare results of machining learning to expected label output.
            Make changes to fundamental algorithm to get closer to expected prediction value
            Con: REQUIRES LOT of DATA to be more accurate
            Pro: Extremely accurate with a lot of data

        Supervised: Only features, have models come up with predicted output (labels) for us. 
            Example: 
                Clustering data points:Create best estimated groupings from feature data.
                Predict next feature's group based.

        Reinforcement: No data. What we have: Agent, Environment, Reward
                Example:
                    Get to the flag:
                    Agent is the player. Environment is the setting. 
                    Reward is point system to show that the agent is getting closer to the end goal.
                    Agent objective: Gain as much reward/points as possible.

        Tensors:
            Partially defined computation that will eventually produce a value
            Is a vector generalized to higher dimensions
            Data point that have multiple dimensions [x] - 1 Dimension or Scalar; [x,y] - 2 Dimensions; [x,y,z] - 3 Dimensions

            Usage: Tensors created. Store partially defined computations in the graph. Later, when graph ran and session is running, tensors are executed and results will be outputed.

        DataType:
            typical data types
            RANK: 0: scalar or one value; 1: 1-D Vector i.e. [1,2,3], 2: 2-D Vector i.e. [[1,2,3],[1,2,3]], etc...
            Shape: How many items in each dimension or how many items inside each nested array i.e. [[1,2],[1,2]] --> This gives us shape of [2,2] or [2 items index 0 AKA first dimension, 2 items index 1 AKA second dimension]
                Example: [  [   ['A','B'],['A','B']   ],[    ['A','B'],['A','B']    ],[   ['A','B'],['A','B']     ]     ]
                    This list has 3 sublists, each sublist has 2 sublists, and each sublist has 2 sublists, hence (3,2,2) for shape

        Variable Types:
            Variable: May Change
            Constant, Placeholder, SparseTensor NO CHANGE or immutable (can copy though)

        Session:
            To evaluate tensors
     """
    def __init__(self, feat_names:list = [], label_names:list = []):
        self.features = feat_names #input values
        self.labels = label_names #output values
        self.data_types = \
        {
            'string':tf.string,
            'int':tf.int16,
            'float16':tf.float16,
            'float32':tf.float32,
            'float64':tf.float64,
        }

    def createTensor(self, type: str, init_value : list|str, rank:int = 0):
        if rank == 0:
            for dtype in [dict, list, set, tuple]:
                if isinstance(init_value, dtype):
                    raise ValueError('Passed in Wrong Datatype for Scalar. Should not be datatype with dunder len() method')
            tf_var = tf.Variable(initial_value = init_value, dtype= self.data_types[type])
        elif rank > 0:
            if not isinstance(init_value, list):
                raise ValueError('Passed in wrong datatype for vector')
            tf_var = tf.Variable(initial_value = init_value, dtype= self.data_types[type])
            print('\n\n',tf.rank(tf_var),'\n',tf_var.shape)
            if tf.rank(tf_var) != rank:
                raise ValueError('Deepest nested length should match Rank')
        else:
            raise ValueError('Rank should be INT value')
        return tf_var

    def reshapeTensor(self, tvar: tf.Variable, new_shape: list = []):
        total_elems = 1
        for s in tvar.shape:
            total_elems = total_elems * s
        new_elems = 1
        for s in new_shape:
            new_elems = new_elems * s
        if new_elems != total_elems:
            raise ValueError(f'Total elements between old and new shapes do not match:\nOriginal:{total_elems}\nNew:{new_elems}')
        tf.reshape(tvar, new_shape)
        return tvar

class DataFrames(TensorFlow):
    #TODO allow multiple dataframes to be pulled and concated per arguments
    def __init__(self, feat_names:list = [], labels:list = []):
        self.df = None
        super().__init__(feat_names = feat_names ,label_names = labels)
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

DF_OBJECT = DataFrames(labels = [],feat_names = [])
