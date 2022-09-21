from ..Utilities.py.dataframes import *
from ..Utilities.py.file_manager import *
from ..Utilities.py.dev import *
from .tensor.tensor import *
SA = FileManager()
DF = DataFrames()
PLT = Plot()
DEV = Development()
import tensorflow_datasets as tfds
from keras.datasets import imdb
from keras.preprocessing import sequence


DEV.makeTestDir(proj_name = 'Tensor')
#plt.imshow(train_df.loc['[0, 0]':'[0, 27]'].to_numpy())
def main(model: str, src_type: str = 'Custom', train_src = None, test_src = None, module_opts: str = None, label: str = None, col_names: list = None, options: dict = {}):
    data_src = \
        {
            'train_url': None,
            'test_url': None,
            'metadata': None,
            'data_valid': None,
        }
    if src_type == 'TFDS':
        tfds_src = tfds.load(**module_opts)
        data_src['train_url'],data_src['data_valid'],data_src['test_url'] = tfds_src[0]
        data_src['metadata'] = tfds_src[1]

    else:
        data_src['train_url']=train_src
        data_src['test_url']=test_src

    if model == 'LinearBinary':
        tensor_obj = LinearClassifier(train_url = train_src, test_url = test_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'LinearVariable':
        tensor_obj = LinearVariable(train_url = train_src, test_url = test_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'DeepNeuralNetwork':
        tensor_obj = DeepNeuralNetwork(train_url = train_src, test_url = test_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'Hidden_Markov':
        tensor_obj = Hidden_Markov(train_url = train_src, test_url = test_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'DeeperNeuralNetwork':
        tensor_obj = DeeperNeuralNetwork(train_url = train_src, test_url = test_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'ConvNeuralNetwork':
        tensor_obj = ConvNeuralNetwork(**data_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    elif model == 'RecurNeuralNetwork':
        tensor_obj = RecurrentNeuralNetworks(**data_src, train_url = train_src, test_url = test_src, label = label, save_loc = DEV.proj_test_dir, col_names = col_names, options = options)
    tensor_obj.processModel()

DEBUG = True
if DEBUG:
    """ 
        main(label = 'survived', 
        train_url = "https://storage.googleapis.com/tf-datasets/titanic/train.csv",
        test_url = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv") 
    """

    """ 
        main(
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
        }) 
    """

    """ 
        main(   
        model = 'Hidden_Markov',
        label = 'Species', 
        train_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv",
        test_url = "https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv",
        col_names = ['SepalLength','SepalWidth','PetalLength','PetalWidth','Species'],
        options = \
        {
            'hidden_units':[30,10],
            'steps': 7
        }) 
    """
    
    """
        train_data, test_data =  tf.keras.datasets.fashion_mnist.load_data()
        main(   
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
        })
    """

    """
        train_data, test_data =  tf.keras.datasets.cifar10.load_data()
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
        })
    """
    
    """ ConvNeuralNetwork with PreTrain
        main(   
            model = 'ConvNeuralNetwork',
            src_type = 'TFDS',
            label = None, 
            col_names = None,
            module_opts=\
            {
                'name':'cats_vs_dogs',
                'split':['train[:80%]','train[80%:90%]','train[90%:]'],
                'with_info':True,
                'as_supervised':True
            },
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
    """
    main(   
        model = 'ConvNeuralNetwork',
        src_type = 'TFDS',
        label = None, 
        col_names = None,
        module_opts=\
        {
            'name':'cats_vs_dogs',
            'split':['train[:80%]','train[80%:90%]','train[90%:]'],
            'with_info':True,
            'as_supervised':True
        },
        options = \
        {
            'hidden_layers':
            [
                {'type':'PreTrain',"src_name":"MobileNetV2", 'input_shape':(160,160,3), 'include_top': False, 'weights':'imagenet'},
                {'type':'GlobalAveragePooling2D'},
                {'type':'Dense','neurons':1, 'activation':'0 to 1'},
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

    """
        VOCAB_SIZE=88584
        MAXLEN=250
        train_data, test_data =   imdb.load_data(num_words = VOCAB_SIZE)
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
                },
                'image_conform':
                {
                    'size':160,
                    'padded':True
                }
            })
    """
