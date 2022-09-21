from .components.preprocess import *
from .components.preview import *
from .components.evaluation import *
class DataManager():
    def __init__(self, train_url: str = None, test_url: str = None, data_valid = None, metadata = None, label:str = None, 
                col_names: list = None, image_conform: dict = None, image_gen: dict = None, save_loc: os.PathLike = None):

        self.preprocessor = PreProcess(train_url = train_url, test_url = test_url, data_valid = data_valid, metadata=metadata, label=label, 
                                        col_names = col_names, image_conform=image_conform, image_gen = image_gen, save_loc = save_loc)
        self.previewer = Preview(metadata = metadata, save_loc = save_loc)
        self.evaluator = EvaluateKDS(labels = metadata.features['label'].names)
        self.train_df, self.train_label, self.test_df, self.test_label, self.data_valid = self.preprocessor.processSource()

    def cleanData(self):
        BATCH_SIZE = 32
        SHUFFLE_BUFFER_SIZE = 1000

        self.train_df = self.preprocessor.normalizeData(data = self.train_df)
        self.test_df = self.preprocessor.normalizeData(data = self.test_df)
        self.data_valid = self.preprocessor.normalizeData(data = self.data_valid)

        self.train_df = self.train_df.shuffle(SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
        self.data_valid = self.data_valid.batch(BATCH_SIZE)
        self.test_df = self.test_df.batch(BATCH_SIZE)

    def previewData(self, num_entries: int = 5):
        self.previewer.renderImages(data = self.train_df,num_entries = num_entries)
        self.previewer.renderImages(data = self.test_df,num_entries = num_entries)

    def predictTestData(self, model, num_entries: int = 5):
        self.evaluator.predictEntries(model = model, num_entries = num_entries, data = self.test_df)