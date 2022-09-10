from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import tensorflow_probability as tfp
import pandas as pd
from ...Utilities.py.plotter import Plotter as Plot
import os
import numpy as np
PLT = Plot()

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
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None):
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
        if isinstance(train_url,str):
            self.train_df = pd.read_csv(train_url,names = col_names, header = 0)
            self.train_label = self.train_df.pop(label)
        elif isinstance(train_url, pd.DataFrame):
            self.train_df = train_url
        if isinstance(test_url,str):
            self.test_df = pd.read_csv(test_url, names = col_names, header = 0)
            self.test_label = self.test_df.pop(label)
        elif isinstance(test_url, pd.DataFrame):
            self.test_df = test_url
        if save_loc != None:
            self.save_loc = save_loc
            self.train_df.to_csv(os.path.join(save_loc, 'train_df.csv'))
            self.test_df.to_csv(os.path.join(save_loc, 'test_df.csv'))
            """ self.train_label.to_csv(os.path.join(save_loc, 'train_label.csv'))
            self.test_label.to_csv(os.path.join(save_loc, 'test_label.csv')) """
        self.model = None

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

    def genDataVisuals(self):
        PLT.plotHistogram(self.train_df, 'age',save_loc = os.path.join(self.save_loc,'histogram.png'))

        PLT.plotGroupMeans(col_names = ['sex'], output_col = 'survived', graph_type = 'barh',
                            dfs = [self.train_df, self.train_label],labels = ['',f"% survive"],
                            save_loc = os.path.join(self.save_loc,'group_means.png'))
    def processModel(self):
        self.prepareFeatures()
        self.estimateModel()



class LinearClassifier(TensorFlow): #Supervised
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)
        self.features = []
    def prepareFeatures(self):
        categories = []
        numericals = []
        for col in self.train_df.columns:
            val = self.train_df.loc[0][col]
            if isinstance(val,str) or np.issubdtype(type(val),np.integer):
                categories.append(col)
            else:
                numericals.append(col)
        for fname in categories:
            vocab = self.train_df[fname].unique()
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
        train_function = self.genInputFunction(feature_df = self.train_df, label_df = self.train_label)
        test_function = self.genInputFunction(feature_df = self.test_df, label_df = self.test_label, shuffle = False, epochs = 1)
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

    def inputForPrediction(self):
        for feature_col in self.train_df.columns:
            valid = True
            while valid:
                val = input(feature_col + ": ")
                if not val.isdigit():
                    valid = False

            self.predictions[feature_col] = [float(val)]

    def prepareFeatures(self):
        for col in self.train_df.columns:
            self.features.append(tf.feature_column.numeric_column(key = col))

    def estimateModel(self):
        estimator = tf.estimator.DNNClassifier(feature_columns=self.features, hidden_units=self.hidden_units, n_classes = len(self.label_classes))
        print(estimator)


        estimator.train(input_fn = lambda: self.inputFunction(feature_df = self.train_df, label_df = self.train_label, training = True),steps = 5000)
        test_results = estimator.evaluate(input_fn = lambda: self.inputFunction(feature_df = self.test_df, label_df = self.test_label, training = False))
        print(test_results)


        self.inputForPrediction()
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
    def prepareFeatures(self):
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
    """
    def __init__(self, train_url: str = None, test_url: str = None, label:str = None, save_loc: os.PathLike = None, col_names: list = None, options: dict = {}):
        super().__init__(train_url = train_url, test_url = test_url, label = label, save_loc = save_loc, col_names = col_names)