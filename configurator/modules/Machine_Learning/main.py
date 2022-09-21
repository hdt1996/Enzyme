from ..Utilities.py.dataframes import *
from ..Utilities.py.file_manager import *
from ..Utilities.py.dev import *
from .tensor.tensor import *
SA = FileManager()
DF = DataFrames()
PLT = Plot()
DEV = Development()
import tensorflow_datasets as tfds
DEV.makeTestDir(proj_name = 'Tensor')
#plt.imshow(train_df.loc['[0, 0]':'[0, 27]'].to_numpy())
def main(model: str, train_url: str = None, test_url: str = None, label: str = None, col_names: list = None, options: dict = {}, data_valid= None, metadata = None):
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
    elif model == 'ConvNeuralNetwork':
        tensor_obj = ConvNeuralNetwork(train_url = train_url, test_url = test_url, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options, metadata= metadata, data_valid = data_valid)
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
    #train_data, test_data =  tf.keras.datasets.fashion_mnist.load_data()
    """main(   
        model = 'DeeperNeuralNetwork',
        label = None, 
        train_url = train_data,
        test_url = test_data,
        col_names = None,
        options = \
        {
            'hidden_layers':
            [
                {'type':'Flat','input_shape':(28,28)},
                {'type':'Dense','neurons':128, 'activation':'0 or More'},
                {'type':'Dense','neurons':10 , 'activation': 'Sum to 1'},
            ],
            'label_classes':['T-Shirt','Trouser','Pull-overs','Dress','Coat','Sandal','Shirt','Sneaker','Bag','Ankle Boots'],
            'epochs':5,
            'loss':'sparse_categorical_crossentropy',
            'optimizer':'adam',
            'metrics':['accuracy'],
            'batch_size':64,
            'DNN_type': 'Sequential'
        })"""

    """train_data, test_data =  tf.keras.datasets.cifar10.load_data()
    main(   
        model = 'ConvNeuralNetwork',
        label = None, 
        train_url = train_data,
        test_url = test_data,
        col_names = None,
        options = \
        {
            'hidden_layers':
            [
                {'type':'Conv2D', 'filters':32, 'size':(3,3), 'input_shape':(32,32,3), 'activation':'0 or More'},
                {'type':'MaxPooling2D', 'size':(2,2)},
                {'type':'Conv2D', 'filters':64, 'size':(3,3), 'activation':'0 or More'},
                {'type':'MaxPooling2D', 'size':(2,2)},
                {'type':'Conv2D', 'filters':64, 'size':(3,3), 'activation':'0 or More'},
                {'type':'Flat'},
                {'type':'Dense','neurons':64, 'activation':'0 or More'},
                {'type':'Dense','neurons':10}
            ],
            'label_classes':['Airplane','Automobile','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck'],
            'epochs':1,
            'loss':'sparse_categorical_crossentropy',
            'optimizer':'adam',
            'metrics':['accuracy'],
            'batch_size':128,
            'DNN_type': 'Sequential',
            'image_gen':
            {
                "rotation_range":40, 
                "width_shift_range":0.2, 
                "height_shift_range":0.2, 
                "shear_range":0.2,
                "zoom_range":0.2, 
                "horizontal_flip": True, 
                "fill_mode":"nearest"
            }
        })"""
    (train_data, data_valid, test_data), metadata = tfds.load('cats_vs_dogs',split=['train[:80%]','train[80%:90%]','train[90%:]'], with_info=True, as_supervised=True)
    main(   
        model = 'ConvNeuralNetwork',
        label = None, 
        train_url = train_data,
        test_url = test_data,
        data_valid = data_valid,
        metadata=metadata,
        col_names = None,
        options = \
        {
            'hidden_layers':
            [
                {'type':'Conv2D', 'filters':32, 'size':(3,3), 'input_shape':(32,32,3), 'activation':'0 or More'},
                {'type':'MaxPooling2D', 'size':(2,2)},
                {'type':'Conv2D', 'filters':64, 'size':(3,3), 'activation':'0 or More'},
                {'type':'MaxPooling2D', 'size':(2,2)},
                {'type':'Conv2D', 'filters':64, 'size':(3,3), 'activation':'0 or More'},
                {'type':'Flat'},
                {'type':'Dense','neurons':64, 'activation':'0 or More'},
                {'type':'Dense','neurons':10}
            ],
            'label_classes':['Airplane','Automobile','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck'],
            'epochs':1,
            'loss':'sparse_categorical_crossentropy',
            'optimizer':'adam',
            'metrics':['accuracy'],
            'batch_size':128,
            'DNN_type': 'Sequential',
            'image_gen':
            {
                "rotation_range":40, 
                "width_shift_range":0.2, 
                "height_shift_range":0.2, 
                "shear_range":0.2,
                "zoom_range":0.2, 
                "horizontal_flip": True, 
                "fill_mode":"nearest"
            },
            'image_conform':
            {
                'size':160,
                'padded':True
            }
        })