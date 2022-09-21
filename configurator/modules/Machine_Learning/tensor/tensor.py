from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.python.data.ops.dataset_ops import PrefetchDataset, MapDataset

from tensorflow import keras
import pandas as pd
from ...Utilities.py.plotter import Plotter as Plot
from ...Utilities.py.dataframes import DataFrames

import os
import numpy as np

from .data.data import DataManager

PLT = Plot()
DF = DataFrames()

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
            Constant, 
            Placeholder, 
            SparseTensor NO CHANGE or immutable (can copy though)

        Session:
            To evaluate tensors
     """
    def __init__(self, train_url: str = None, test_url: str = None, data_valid = None, metadata = None, label:str = None, 
                col_names: list = None, image_conform: dict = None, image_gen: dict = None, save_loc: os.PathLike = None):
        self.data_types = \
        {
            'string':tf.string,
            'int16':tf.int16,
            'int32': tf.int32,
            'int64':tf.int64,
            'float16':tf.float16,
            'float32':tf.float32,
            'float64':tf.float64,
        }
        self.DM= DataManager(train_url = train_url, test_url = test_url, data_valid = data_valid, metadata=metadata, 
                                    label=label, col_names = col_names, image_conform=image_conform, image_gen = image_gen, save_loc = save_loc)

    def isolateNPValue(self, nparray: np.ndarray):
        if not isinstance(nparray, np.ndarray):
            return nparray
        nparray=list(nparray.flatten())
        if len(nparray) == 1:
            nparray = nparray[0]
        return nparray


    def createTensor(self, d_type: str, init_value : list|str, rank:int = 0) -> dict:
        if not isinstance(rank, int):
            raise ValueError('Rank should be INT value')
        if rank == 0 and type(d_type) in [list, dict, tuple, set]:
            raise ValueError('Passed in Wrong Datatype for Scalar. Should not be datatype with dunder len() method')
        if rank > 0 and not isinstance(init_value, list):
            raise ValueError('Passed in wrong datatype for vector')
        tf_dict = {}
        var = tf.Variable(initial_value = init_value, dtype= self.data_types[d_type])
        shape = tuple(var.shape)
        tf_dict['var'] = var
        tf_dict['rank'] = f"Nested Levels: {int(tf.rank(var))}"
        tf_dict['shape'] = shape
        return tf_dict

    def reshapeTensor(self, tf_dict: dict, new_shape: list = []) -> dict:
        var = tf_dict['var']
        total_elems = 1
        for s in var.shape:
            total_elems = total_elems * s
        new_elems = 1
        for s in new_shape:
            new_elems = new_elems * s
        if new_elems != total_elems:
            raise ValueError(f'Total elements between old and new shapes do not match:\nOriginal:{total_elems}\nNew:{new_elems}')
        var = tf.reshape(var, new_shape)
        tf_dict['var'] = var
        tf_dict['shape'] = tuple(var.shape)
        tf_dict['rank'] = f"Nested Levels: {int(tf.rank(var))}"
        return tf_dict



    def conformIMGSize(self, img, label):
        """
        Reshape image to self.img_size
        """
        img = tf.cast(img, tf.float32)
        img = (img/255.0)
        img=tf.image.resize(images=img, size=(self.image_conform['size'], self.image_conform['size']),preserve_aspect_ratio=False)
        return img, label

    def conformIMGSizePad(self, img, label):
        """
        Reshape image to self.img_size
        """
        img = tf.cast(img, tf.float32)
        img = (img/255.0)
        #img = tf.image.convert_image_dtype(image=img,dtype=tf.float32) THIS IS SAME AS LAST TWO COMMANDS IN ONE
        img=tf.image.resize_with_pad(image=img, target_height=self.image_conform['size'], target_width= self.image_conform['size'])
        return img, label

    def processModel(self):
        self.processData()
        self.estimateModel()


class LinearClassifier(TensorFlow): #Supervised
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)
        self.features = []
    def processData(self):
        categories = []
        numericals = []
        for col in self.DM.train_df.columns:
            val = self.DM.train_df.loc[0][col]
            if isinstance(val,str) or np.issubdtype(type(val),np.integer):
                categories.append(col)
            else:
                numericals.append(col)
        for fname in categories:
            vocab = self.DM.train_df[fname].unique()
            self.features.append(tf.feature_column.categorical_column_with_vocabulary_list(key = fname, vocabulary_list = vocab))
        for fname in numericals:
            self.features.append(tf.feature_column.numeric_column(key = fname, dtype = tf.float32))

    def genInputFunction(self,feature_df: pd.DataFrame, label_df: pd.DataFrame, epochs: int = 10, shuffle: int = 1000, batch_size: int = 32):
        def inputFunction() -> tf.data.Dataset:
            data_obj = tf.data.Dataset.from_tensor_slices((dict(feature_df),label_df))
            if isinstance(shuffle, int) and shuffle > 0:
                data_obj = data_obj.shuffle(shuffle)
            data_obj = data_obj.batch(batch_size).repeat(epochs) # Split dataset into batches of speciifed size. Repeat for number of epochs
            return data_obj
        return inputFunction

    def estimateModel(self):
        train_function = self.genInputFunction(feature_df = self.DM.train_df, label_df = self.DM.train_label)
        test_function = self.genInputFunction(feature_df = self.DM.test_df, label_df = self.DM.test_label, shuffle = False, epochs = 1)
        estimator = tf.estimator.LinearClassifier(feature_columns = self.features)
        estimator.train(train_function)
        test_results = estimator.evaluate(test_function)
        predictions = estimator.predict(test_function)
        print(test_results['accuracy'])


class LinearVariable(TensorFlow):
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)


class DeepNeuralNetwork(TensorFlow): #Supervised

    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)
        self.features = []
        self.hidden_units = options['hidden_units']
        self.label_classes = options['label_classes']
        self.steps = options['steps']
        self.predictions = {}
    def inputFunction(self,feature_df: pd.DataFrame, label_df: pd.DataFrame, training: bool = True, shuffle: int = 1000, batch_size: int = 256):
        data_obj = tf.data.Dataset.from_tensor_slices((dict(feature_df),label_df))
        if training:
            data_obj = data_obj.shuffle(shuffle).repeat()
        return data_obj.batch(batch_size)

    def inputPredictFunction(self, feature_df: pd.DataFrame, batch_size: int = 256):
        return tf.data.Dataset.from_tensor_slices(dict(feature_df)).batch(batch_size)

    def toPredictPrompt(self):
        for feature_col in self.DM.train_df.columns:
            valid = True
            while valid:
                val = input(feature_col + ": ")
                if not val.isdigit():
                    valid = False

            self.predictions[feature_col] = [float(val)]

    def processData(self):
        for col in self.DM.train_df.columns:
            self.features.append(tf.feature_column.numeric_column(key = col))

    def estimateModel(self):
        estimator = tf.estimator.DNNClassifier(feature_columns=self.features, hidden_units=self.hidden_units, n_classes = len(self.label_classes))
        print(estimator)


        estimator.train(input_fn = lambda: self.inputFunction(feature_df = self.DM.train_df, label_df = self.DM.train_label, training = True),steps = 5000)
        test_results = estimator.evaluate(input_fn = lambda: self.inputFunction(feature_df = self.DM.test_df, label_df = self.DM.test_label, training = False))
        print(test_results)


        self.toPredictPrompt()
        predictions = estimator.predict(input_fn = lambda: self.inputPredictFunction(self.predictions))
        for item in predictions:
            class_id = item['class_ids'][0]
            probability = item['probabilities']
            print(f"Prediction is {self.label_classes[class_id]} with {100*probability}%")

class Clusters(TensorFlow): #Unsupervised
    """
    Summary:
        Uses K-Means Clustering to find groupings among data points. We do not have any labels, so the algorithm will find related groups (categorical) for us.
        Required: Need to know how many centroids (K value) is.
    Definitions:
        K Centroid: Triangles: Where different clusters currently exist
            1) Randomly pick assign K centroids in scatter of data
                ex. K = 3 for three K clusters (placed randomly)
            2) Each point is measured in distance to each K Cluster via Euclidian or Manhattan distance
            3) Groups assigned to cluster by distance using the closest one
            4) Move centroid to center of grouped data points via center mass
            5) Repeat 2 and 3 to reassign groups via closest centroid

    """
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)
        self.features = []

class Hidden_Markov(TensorFlow):
    """
    Summary:
        Goal: Predict future events based on past events.
        Uses probability distribution. States are events such as hot and cold day. Each state contains transition probabilities..
            ex. For a cold day, there is a 30% of hot day next day and 70% of cold day next day
            ex. For a hot day, there is a 20% of cold day next day and 80% of continued hot day next day.
        Observations are stats:
            ex. For hot day:
                Mean temperature: 20
                Min: 20
                Max: 25
    """
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)
        self.features = []
        self.tfd = tfp.distributions
        self.init_dist = self.tfd.Categorical(probs = [.8,.2])
        self.trans_dist = self.tfd.Categorical(probs = [[.5,.5],[.2,.8]])
        self.obs_dist = self.tfd.Normal(loc = [0.,15.], scale=[5.,10.]) #loc is mean for states (hot and cold) | scale is standard deviation for states (hot and cold)
        self.steps = options['steps'] #How many days to predict for or how many cycles to run through probability model
    def processData(self):
        pass
        print('Done...')
    def estimateModel(self):
        model = self.tfd.HiddenMarkovModel(initial_distribution = self.init_dist, transition_distribution = self.trans_dist, observation_distribution = self.obs_dist, num_steps = self.steps)
        mean = model.mean() #Gives us list
        #Meaning by index: 0 -> Starting temperature | 1 -> Next Day Temp | 2...
        print(mean)
        print('Done...')


class DeeperNeuralNetwork(TensorFlow):
    """
        Definitions
        Bias: (B)
            CONSTANT for bias (Like Y intercepts for y = mx + b). One for each layer. Exists in previous layer to the layer it affects. Connected to each neuron in next layer (Complies with Densely Connected)
            TAKES NO INPUT --> Trainable parameter in neural network. Weights are automatically assigned 1.
            Bias not connected to other biases!
        Input Layer: (I)
            One input neuron needed for each piece of information i.e. one input neuron for each pixel for 20x20 or 400 pixel image
        Hidden Layer: (H)
            Hidden because we do not observe this. We pass information from input layer and get output from output layer. We do not see what happens in hidden layer.
            Input neurons will be connected to one of these hidden neurons or ALL of them for Densely Connected Neural Network
            Connections between input and hidden neurons are called weights (Numbers between 0 and 1 to assign weights; these will be modified through training)
        Output Layer: (O)
            Each output neuron will have value between 0 and 1 inclusively. If closer to 0, output will be 0. If closer to 1, output will be 1.
            For multiple labels to determine, each output neuron will be part of probability distribution summing to 1.

        Activation Function: (A)
            Converts numbers that do not conform
            Options:
                Relu (Rectified Linear Unit)
                    - Any values less than 0, set Y to 0
                    - Any values greater than 0, leave alone
                Tanh (Hyperbolic Tangent):
                    - Squishes values between -1 to 1
                    - The more negative, closer to -1
                    - The more positive, closer to +1
                Sigmoid:
                    - Squish values between 0 and 1
                    - Any negative numbers, place closer to 0
                    - Any positive numbers, place closer to 1
                    - 1/(1 + e^-z)

        Loss Function: (L)
            Compares network output vs expected output (Actual vs Expected)
            Example: for (2,2,2) (x,y,z) We expect to get Red (0), but got 0.7 -> Loss = .7
            Options:
                - Mean Squared Error
                - Mean Absolute Error
                - Hinge Loss
            Goal:
                Choose best loss function and inside the results of this loss function, find the global minimum.
                Use gradient descent algorithm to determine which direction of modifying bias/weights to achieve loss minimum.
                Use backpropagation to move backwards in network and update weights/biases to achieve direction per gradient descent.

        Optimizer:
            Choose algorithm and performs back propagation in neural network to update weights/biases
            Options:
                Gradient Descent
                Stochastic Gradient Descent
                Mini-Batch Gradient Descent
                Momentum
                Nesterov Accelerated Gradient
                Atom

        Example:
            Predict colors -----> Red or Blue (0 or 1)
            Inputs: X, Y, Z
            Activiation: Using Sigmoid
        (Ix)

            (A)->(H1)

        (Iy)            (A)->(O1)
            (A)->(H2)

        (Iz)

            (Bh)

        (Bi)

        Calculation of H1:
            A sigmoid(Ix*Wx + Iy*Wy + Iz*Wz + Bi) = H1
        Calculation of H2:
            A sigmoid(Ix*Wx + Iy*Wy + Iz*Wz + Bi) = H2
        Calculation of O1:
            A sigmoid(H1*Wh1+H2*Wh2 + Bh= O1)

        Process (Example for Fashion Items)
            1) Pre-Process Data: Since data are comprised of 8-bit integers (grayscale), we divide by 255 to get value between 0 and 1 (Our requirement)
            2) Defining model Architecture:
               
                Activation Function Options:
                    a) relu - Rectify Linear Unit
                    b) sigmoid
                    c) tan h
                    b) softmax - Make sure all values of neurons add up to 1 and between 0 and 1
                Definitions:
                    Flatten: keras.layers.Flatten(input_shape=tuple)
                             Matrix data (pixels) flattened to single list (28x28 to 784)
                    Dense:   Dense keras.layers.Dense(num_neurons, activation = '')
                            Neurons in previous later connected to every Neuron in this layer
                Architecture Types
                    Sequential - (keras.Sequential(kera.layers) 
                        Simple neural network moving from left to right (input -> hidden layers -> output)

                    1)  Input layer - Flatten
                    2)  1st Hidden Layer - Dense with activation
                    ... More Hidden Layers
                    3)  Last Hidden Layer - Dense with activation
                        Since last just before output, number of neurons (num_neurons) needs to match number of potential outputs
                    
                    Convoluted (More complicated, allows bidirectional neural network movement)
            3) Compiling Model
                    optimizer: algorithm for gradient-descent
                    loss function: Calculating diff between actual vs predicted
                        Options:
                            spare_categorical_crossentropy
                            mean_squared_error
                            mean_absolute_error
                            research others...
                    metric: Output to see from neural network
            4) Training/Fitting Model (Creating Prediction Regression)
                    args: Train Data Set (Pre-processed) and Train Label Set (Most Likely Unmodified)
                          Epochs: How many times sample data is funnel through (too much means overfitting)
                          TODO: Create module that evaluates accuracy of variety of models with varying inputs
                          Take a look at other arguments such as activation, optimizer, loss, batch size (Not used yet), etc.


    """
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)
        self.features = []
        self.hidden_layers = options['hidden_layers']
        # Hidden Layer Structure
        """
        {
            Dense: [Number of Neurons, Activation Fn Name],
            Flatten: [Shape to Match Data]
        }
        """
        self.label_classes = options['label_classes']
        self.epochs = options['epochs']
        self.predictions = {}
        self.optimizer = options['optimizer']
        self.loss = options['loss']
        self.metrics = options['metrics']
        self.batch_size = options['batch_size']
        self.layer_options =\
        {
            'Dense':{"neurons":int, "activation":str},
            'Flat':{"input_shape":tuple},
        }
        self.activation_options=\
        {
            '0 or More': 'relu', #Used for setting negative values to zero and leaving positive alone
            'Sum to 1': 'softmax', #Used for probability distribution where all neurons sum to one/ All values nonnegative
            '0 to 1': 'sigmoid', #Used to squish values between zero and one
            '-1 to 1': 'tanh' #Used to squish values between -1 and 1
        }
        self.dnn_type = options['DNN_type']
        self.predictions = []

    def processData(self):

        self.DM.train_df = self.DM.train_df / 255.0
        self.DM.test_df = self.DM.test_df / 255.0


    def processHiddenLayers(self,layer_choice: dict) -> keras.layers:
        layer_type = layer_choice['type']
        for key in self.layer_options[layer_type]:
            if not key in layer_choice:
                raise KeyError (f"You are missing {key} in your layer inputs")
        if layer_type == 'Flat':
            input_shape = layer_choice['input_shape']
            layer_item = keras.layers.Flatten(input_shape = input_shape)
        elif layer_type == 'Dense':
            neurons = layer_choice['neurons']
            activation = self.activation_options[layer_choice['activation']]
            layer_item = keras.layers.Dense(units=neurons, activation=activation)
        return layer_item

    def prepareModel(self):
        #Define the architecture
        if self.dnn_type == 'Sequential':
            model = keras.Sequential([self.processHiddenLayers(layer_choice = choice) for choice in self.hidden_layers])
        return model

    def estimateModel(self):
        model = self.prepareModel()
        model.compile(optimizer=self.optimizer, loss = self.loss, metrics= self.metrics)
        model.fit(self.DM.train_df, self.DM.train_label, epochs = self.epochs, batch_size = self.batch_size)

        test_loss, test_acc = model.evaluate(self.DM.test_df, self.DM.test_label, verbose = 1) #Verbose - are we looking at output or not (How much printed to console)
        print('Test Accuracy: ', test_acc)
        predictions = model.predict(self.DM.test_df) #Gives us probability distribution of items on output layer

        self.toPredictPrompt()
        for requested in self.predictions:
            requested = int(requested)
            prediction=model.predict(self.DM.test_df[requested])
            pred_val = self.label_classes[np.argmax(prediction)] #np.argmax Gives us maximum value
            act_val = self.label_classes[self.DM.test_label[requested]]
            print('Prediction is :',pred_val)
            print('Actual Result is :', act_val)
            PLT.graphImage(data = self.DM.test_df[requested], show = True)

    def toPredictPrompt(self):
        valid = False
        while not valid:
            val = input("Which entry do you want to predict?: ")
            if val.isdigit():
                self.predictions.append(val)
            proceed = input("Keep choosing? [Y/N]: ")
            if proceed == "N":
                valid = True
            
class ConvNeuralNetwork(TensorFlow):
    """ 
    Difference between Dense and Convolution:
        Dense searches in globally in images for patterns
            Will not be able to detect local patterns/features in different part of image
            Requirements: Symmetric images preferred
        Convolution takes care of this by searching for local features throughout the image!
            Look for local patterns; i.e. it knows what an individual ear of a cat looks like
            Find all identifiable images and determine combination that makes up specific classifications
            Outputs feature_maps
        General Idea:
            Runs filters over image (sample in different areas) ->create output feature map that quantifies
            presence of filters patterns at different locations
                Will run many filters over images at a time to give many different feature maps to describe presence of features
                1) First Conv Layer: Run simple filter such as straight layer
                2) Next Layers: Take previous map from previous layer and look for curves/edges
    
    Image data - 3 Dimensional
        1st Dimension: Width
        2nd Dimension: Height
        3rd Dimension: Color Layers
            1st Layer, Red Values
            2nd Layer, Green Values
            3rd Layer, Blue Values
            AKA Color Layers for (RGB)

        Process:
            1) Place filter over image with variable size and type
            2) Find features in image that closely match filter
                - Conv Layer will output feature map
                - Section of image will be dot product multipled against feature map
                    Original Image       Filters
                        x o o o o        o o x       o o o 
                        o x o o o        o o x       x x x 
                        o o x o o        o o x       o o o 
                        o o o x o
                        o o o o x   
                    Vector Dot Product = |A||B|*cosine(theta) 
                    Multiply magnitude of all dimensions with matching counter part
                                      c  c  c  c     c  c  c  c
                    Ex.          r   [1, 2, 3, 4]   [1, 2, 3, 4]   
                                 r   [1, 2, 3, 4]   [1, 2, 3, 4]
                                 r   [1, 2, 3, 4]   [1, 2, 3, 4]
                                 r   [1, 2, 3, 4]   [1, 2, 3, 4]
            2b) Padding:
                Make sure that output feature map from original image is same dimensions
                Our output feature map is 3x3 while original is 5x5. Solution -> Adding padding to rows and columns of original image
                    Add extra rows and columns
                    Goal: We want pixels in center and not in the edges
                    Allows us to build output map that is same size as input
                    Allows us to see features on the edge of images as well
                Stride: How much we move sample box (Can have box move by one or two or whatever)
            3) Pooling:
                Next Convolution Layer:
                Take output feature maps from previous layer
                Pick up combinations of lines and edges to find curves and other patterns
                Go from small features and groups of pixels to building up to more abstract patterns

                3 Types: Pooling: 
                    Taking specific values from sample of output feature map to reduce dimensionality
                    Get smaller chunk of output feature map and find min to map to new but smaller feature map
                    Goal: Tell us of CHOSEN (below) presence of a feature in local area
                Min: 
                Max
                Average
                General pooling size: 2x2 with stride of 1 or 2


    """
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}, metadata = None, data_valid = None):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names, metadata = metadata, data_valid = data_valid, 
                            image_conform = options['image_conform'], image_gen = options['image_gen'])
        self.hidden_layers = options['hidden_layers']
        self.input_size = None #How many filters we will have
        self.filters = None #How many filters; def: some pattern of pixels such as straight line in bitmap
                            #Usually use x32 filters up to x64
                            #Filter is trainiable parameter, amount of filters and what they are as training
        self.sample_size = None #Sample size of filters, How big our filter is i.e. 3x3
        self.label_classes = options['label_classes']
        self.epochs = options['epochs']
        self.predictions = {}
        self.optimizer = options['optimizer']
        self.loss = options['loss']
        self.metrics = options['metrics']
        self.batch_size = options['batch_size']
        self.dnn_type = options['DNN_type']
        self.layer_options =\
        {
            'Dense':{"neurons":int},#"activation":str},
            'Flat':{}, #"input_shape":tuple},
            'Conv2D':{"filters":int, "size":tuple, "activation":str}, #"input_shape": tuple}
            'MaxPooling2D':{"size":tuple}
        }
        self.activation_options=\
        {
            '0 or More': 'relu', #Used for setting negative values to zero and leaving positive alone
            'Sum to 1': 'softmax', #Used for probability distribution where all neurons sum to one/ All values nonnegative
            '0 to 1': 'sigmoid', #Used to squish values between zero and one
            '-1 to 1': 'tanh' #Used to squish values between -1 and 1
        }

        self.predictions = []


    def processData(self):
        self.DM.cleanData()
        self.DM.renderImages(num_entries = 15)
        print('Done')

    


    def processHiddenLayers(self,layer_choice: dict) -> keras.layers:
        layer_type = layer_choice['type']
        for key in self.layer_options[layer_type]:
            if not key in layer_choice:
                raise KeyError (f"You are missing {key} in your layer inputs")
            if not isinstance(layer_choice[key],self.layer_options[layer_type][key]):
                raise TypeError (f"Please correct type for {key} to {self.layer_options[layer_type][key]}")
        if layer_type == 'Flat':
            kwargs={}
            if layer_choice.get('input_shape'):
                kwargs['input_shape']= layer_choice['input_shape']
            layer_item = keras.layers.Flatten(**kwargs)
        elif layer_type == 'Dense':
            kwargs={}
            neurons = layer_choice['neurons']
            if layer_choice.get('activation'):
                kwargs['activation']=self.activation_options[layer_choice['activation']]
            layer_item = keras.layers.Dense(units=neurons, **kwargs)
        elif layer_type == 'Conv2D':
            kwargs={}
            if layer_choice.get('input_shape'):
                kwargs['input_shape'] = layer_choice['input_shape']
            filters = layer_choice['filters']
            size = layer_choice['size']
            activation = self.activation_options[layer_choice['activation']]
            layer_item = keras.layers.Conv2D(filters=filters, kernel_size=size, activation=activation, **kwargs)
        elif layer_type == 'MaxPooling2D':
            size = layer_choice['size']
            layer_item = keras.layers.MaxPooling2D(pool_size= size)
        return layer_item

    def prepareModel(self):
        #Define the architecture
        if self.dnn_type == 'Sequential':
            model = keras.Sequential([self.processHiddenLayers(layer_choice = choice) for choice in self.hidden_layers])
            print(model.summary())
        return model

    def estimateModel(self):
        model = self.prepareModel()
        model.compile(optimizer=self.optimizer, loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics= self.metrics)
        model.fit(self.DM.train_df, self.DM.train_label, epochs = self.epochs, batch_size = self.batch_size, validation_data=(self.DM.test_df, self.DM.test_label))

        test_loss, test_acc = model.evaluate(self.DM.test_df, self.DM.test_label, verbose = 2) #Verbose - are we looking at output or not (How much printed to console)
        print('Test Accuracy: ', test_acc)
        predictions = model.predict(self.DM.test_df) #Gives us probability distribution of items on output layer
        self.generateImages(num_images = 20)
        self.toPredictPrompt()
        for requested in self.predictions:
            requested = int(requested)
            #Since images have multiple layers (for color - red green blue)
            #image data will be stored as multiple np arrays
            #All need to be housed within one np array for model to predict properly
            #Will use np.expand_dims to place all nested_arrays within one large np_array
            raw_data = self.DM.test_df[requested]
            img_array = np.expand_dims(raw_data,0)
            label_index = self.isolateNPValue(nparray=self.DM.test_label[requested])
            prediction=model.predict(img_array)
            pred_val = self.label_classes[np.argmax(prediction)] #np.argmax Gives us maximum value
            act_val = self.label_classes[label_index]
            print('Prediction is :',pred_val)
            print('Actual Result is :', act_val)
            PLT.graphImage(data = raw_data, show = True)

    def toPredictPrompt(self):
        valid = False
        while not valid:
            val = input("Which entry do you want to predict?: ")
            if val.isdigit():
                self.predictions.append(val)
            proceed = input("Keep choosing? [Y/N]: ")
            if proceed == "N":
                valid = True

