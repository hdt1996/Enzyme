from .components.preprocess import *
from .components.preanalyze import *
from .components.postanalyze import *
class DataManager(PreProcess, PreAnalyze, PostAnalyze):
    def __init__(self, train_url: str = None, test_url: str = None, data_valid = None, metadata = None, label:str = None, 
                col_names: list = None, image_conform: dict = None, image_gen: dict = None, save_loc: os.PathLike = None):
        super().__init__(train_url = train_url, test_url = test_url, data_valid = data_valid, metadata=metadata, 
                        label=label, col_names = col_names, image_conform=image_conform, image_gen = image_gen, save_loc = save_loc)
        self.train_url = train_url
        self.test_url = test_url
        self.data_valid = data_valid
        self.metadata=metadata
        self.col_names = col_names
        self.image_conform = image_conform
        self.image_gen = image_gen
        self.label = label

        self.train_df, self.train_label, self.test_df, self.test_label, self.data_valid = self.processSource()

    def cleanData(self):
        BATCH_SIZE = 32
        SHUFFLE_BUFFER_SIZE = 1000



        self.train_df = self.normalizeData(data = self.train_df)
        self.test_df = self.normalizeData(data = self.test_df)
        self.data_valid = self.normalizeData(data = self.data_valid)

        self.train_df = self.train_df.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
        self.data_valid = self.data_valid.batch(BATCH_SIZE)
        self.test_df = self.test_df.batch(BATCH_SIZE)