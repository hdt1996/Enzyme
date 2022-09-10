from ..Utilities.py.dataframes import *
from ..Utilities.py.file_manager import *
from ..Utilities.py.dev import *
from .tensor.tensor import *
import numpy as np
import shutil as sh
SA = FileManager()
DF = DataFrames()
PLT = Plot()
DEV = Development()
DEV.makeTestDir(proj_name = 'Tensor')

def main(model: str, train_url: str = None, test_url: str = None, label: str = None, col_names: list = None, options: dict = {}):
    if model == 'LinearBinary':
        tensor_obj = LinearClassifier(train_url = train_url, test_url = test_url, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'LinearVariable':
        tensor_obj = LinearVariable(train_url = train_url, test_url = test_url, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'DeepNeuralNetwork':
        tensor_obj = DeepNeuralNetwork(train_url = train_url, test_url = test_url, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'Hidden_Markov':
        tensor_obj = Hidden_Markov(train_url = train_url, test_url = test_url, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'DeeperNeuralNetwork':
        tensor_obj = DeeperNeuralNetwork(train_url = train_url, test_url = test_url, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    tensor_obj.processModel()

DEBUG = True
if DEBUG:
    """ main(label = 'survived', 
    train_url = "https://storage.googleapis.com/tf-datasets/titanic/train.csv",
    test_url = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv") """

    """ main(
        model = 'DeepNeuralNetwork',
        label = 'Species', 
        train_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv",
        test_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv",
        col_names = ['SepalLength','SepalWidth','PetalLength','PetalWidth','Species'],
        options = \
        {
            'hidden_units':[30,10],
            'label_classes':['Setosa','Versicolor','Virginica'],
            'steps': 5000
        }) """

    """ main(   
        model = 'Hidden_Markov',
        label = 'Species', 
        train_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv",
        test_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv",
        col_names = ['SepalLength','SepalWidth','PetalLength','PetalWidth','Species'],
        options = \
        {
            'hidden_units':[30,10],
            'steps': 7
        }) """
    train_data, test_data =  tf.keras.datasets.fashion_mnist.load_data()
    train_df = DF.buildDFbyNumpy(data = train_data[0])
    train_label = DF.buildDFbyNumpy(data = train_data[1])
    test_df = DF.buildDFbyNumpy(data = test_data[0])
    test_label = DF.buildDFbyNumpy(data = test_data[1])
    main(   
        model = 'DeeperNeuralNetwork',
        label = None, 
        train_url = pd.DataFrame(),
        test_url = pd.DataFrame(),
        col_names = None,
        options = \
        {
            'hidden_units':[30,10],
            'steps': 7
        })
