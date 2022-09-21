import tensorflow as tf
from tensorflow.python.data.ops.dataset_ops import PrefetchDataset, MapDataset
import pandas as pd
import numpy as np
import os
import validators
from keras.preprocessing import image
from random import randrange
from .....Utilities.py.plotter import Plotter as Plot
PLT = Plot()

class Preview():
    def __init__(self, metadata = None, save_loc: os.PathLike = None, **kwargs):
        self.metadata = metadata
        self.save_loc = save_loc

    def renderImages(self, data, num_entries: int = 10):
        if isinstance(data, MapDataset):
            fn = self.metadata.features['label'].int2str
            for img, label in data.take(num_entries):
                plt_title = fn(label)
                #print('New Shape: ',img.shape)
                PLT.graphImage(data=img,title=plt_title,show=True)
        elif isinstance(data, np.ndarray):
            for i in data[:num_entries]:
                PLT.graphImage(data=i, show = True)

    def renderDFAnalytics(self, df_1: pd.DataFrame, df_2: pd.DataFrame):
        PLT.plotHistogram(df_1, 'age',save_loc = os.path.join(self.save_loc,'histogram.png'))

        PLT.plotGroupMeans(col_names = ['sex'], output_col = 'survived', graph_type = 'barh',
                            dfs = [df_1, df_2],labels = ['',f"% survive"],
                            save_loc = os.path.join(self.save_loc,'group_means.png'))