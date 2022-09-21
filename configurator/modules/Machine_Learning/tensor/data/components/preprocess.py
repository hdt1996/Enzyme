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

class PreProcess():
    """
    RGB

        Data Types are VITAL
        If we have int types inside array, we can use standard (255, 255, 255) for white or (50, 100, 150) for some rgb color
        HOWEVER, if we have float types, we must use numbers between 0 and 1 such as (0,0,0) for black; (1,1,1) for white; (.5,.5,.5) for some rgb color
        This is why our data gets messed up if we use a cast to float and do not standardize the data by dividing it by 255
        If we have data that initially has 0-255 numbers and convert to float, these must be converted to 0-1 for rgb to be recognized
    
    
    """
    def __init__(self, **kwargs):
        pass


    def processSource(self):
        train_df, train_label, test_df, test_label, data_valid = None, None, None, None, None
        if isinstance(self.train_url,str) and validators.url(self.train_url):
            train_df = pd.read_csv(self.train_url,names = self.col_names, header = 0)
            train_label = train_df.pop(self.label)
        elif isinstance(self.train_url, pd.DataFrame):
            train_df = self.train_url
            last_col=list(train_df.columns).pop()
            train_label = train_df.pop(last_col)
        elif isinstance(self.train_url, tuple) and any(isinstance(i, np.ndarray) for i in self.train_url):
            train_df = self.train_url[0]
            train_label = self.train_url[1]
        elif isinstance(self.train_url, PrefetchDataset): 
            train_df = self.checkImageConform(data=self.train_url)

        if isinstance(self.test_url,str) and validators.url(self.test_url):
            test_df = pd.read_csv(self.test_url, names = self.col_names, header = 0)
            test_label = test_df.pop(self.label)
        elif isinstance(self.test_url, pd.DataFrame):
            test_df = self.test_url
            last_col=list(test_df.columns).pop()
            test_label = test_df.pop(last_col)
        elif isinstance(self.test_url, tuple) and any(isinstance(i, np.ndarray) for i in self.test_url):  
            test_df = self.test_url[0]
            test_label = self.test_url[1]
        elif isinstance(self.test_url, PrefetchDataset):
            test_df = self.checkImageConform(data=self.test_url)

        if self.data_valid:
            data_valid = self.data_valid.map(self.conformIMGSizePad)
        
        return train_df, train_label, test_df, test_label, data_valid

    def checkImageConform(self, data):
        if self.image_conform.get('padded') == False:
            fn = self.conformIMGSize
        else:
            fn = self.conformIMGSizePad

        if isinstance(data, PrefetchDataset):
            data = data.map(fn)
        elif isinstance(data, np.ndarray):
            np_array=[]
            for row in data:
                np_array.append(fn(img=row))
            data = np.array(object = np_array)
        return data

    def normalizeData(self, data):
        if self.image_conform != None:
            data = self.checkImageConform(data=data)
        else:
            data = data/255.0


        return data


    def conformIMGSize(self, img, label: str = None):
        """
        Reshape image to self.img_size
        """
        img = tf.cast(img, tf.float32)
        img = (img/255.0)
        img=tf.image.resize(images=img, size=(self.image_conform['size'], self.image_conform['size']),preserve_aspect_ratio=False)
        return img, label

    def conformIMGSizePad(self, img, label: str = None):
        """
        Reshape image to self.img_size
        """
        img = tf.cast(img, tf.float32)
        img = (img/255.0)
        #img = tf.image.convert_image_dtype(image=img,dtype=tf.float32) THIS IS SAME AS LAST TWO COMMANDS IN ONE
        img=tf.image.resize_with_pad(image=img, target_height=self.image_conform['size'], target_width= self.image_conform['size'])
        return img, label

    def generateImages(self, num_images: int = 1):
        img_generator=image.ImageDataGenerator(**self.image_gen)
        new_images=[]
        random_int = randrange(start= 0, stop = self.train_df.shape[0])
        img = self.train_df[random_int]
        img = image.image_utils.img_to_array(img = img)
        new_shape = [1]
        new_shape.extend(img.shape)
        img = img.reshape(tuple(new_shape))
        index = 0
        for batch in img_generator.flow(x = img, save_prefix='TD',save_format='.png'):
            PLT.graphImage(data = batch[0], show = True)
            index += 1
            if index > num_images:
                break
            new_images.append(batch[0])