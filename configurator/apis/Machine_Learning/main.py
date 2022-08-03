from data.data import *
from tensor.tensor import *
from sysadmin.sysadmin import *
import shutil as sh
SA = SystemAdmin()
DF_UTIL = DataFrames()

def main(features: list, labels: list, col_names: list, train_url: str, eval_url: str):
    tensor_obj = TensorFlow(feat_names = features, label_names = labels)
    if train_url != None and eval_url != None:  
        train_df, eval_df = pd.read_csv(train_url), pd.read_csv(eval_url)
        train_df.to_csv(os.path.join(TEST_LOC,f"traindf.csv"))
        eval_df.to_csv(os.path.join(TEST_LOC,f"evaldf.csv"))
        y_train=train_df.pop('survived')
        y_eval=eval_df.pop('survived')
        y_train.to_csv(os.path.join(TEST_LOC,f"ytrain.csv"))
        y_eval.to_csv(os.path.join(TEST_LOC,f"yeval.csv"))
        for i in range(len(train_df)):
            print(train_df.loc[i],y_train.loc[i]) #prints row and corresponding output in train series data (Indices match)
        print(train_df.describe()) #gives us stat data
        print(train_df.shape) #Tells us how many rows and columns in (row, column)
        DF_UTIL.makeGraphs(train_df, 'age',save_loc = os.path.join(TEST_LOC,'graphs.png'), graph_type='Histogram')
    SRS_LIST = DF_UTIL.buildSeriesList(nested_list = [[40,50,45],[70,90,50],[99,70,50]], col_names = col_names)
    #print(SRS_LIST)
    DF_UTIL.buildDF(SRS_LIST, col_names)
    DF_UTIL.addRow([2,4,4])
    df = DF_UTIL.df
    tvar = tensor_obj.createTensor('string',[[['A','B'],['A','B']],[['A','B'],['A','B']],[['A','B'],['A','B']]],3)
    tvar = tensor_obj.reshapeTensor(tvar = tvar, new_shape = [4,3,1])
    #pl = Plotter()
    #pl.regLinear(x=[1,2,2.5,3,4],y=[1,4,7,9,15], axis = [0,6,0,16])


DEBUG = True
if DEBUG:
    if __name__ == '__main__':
        main(features = [0,2], labels = [1], col_names = ['Midterm 1','Midterm 2','Final'], 
        train_url = "https://storage.googleapis.com/tf-datasets/titanic/train.csv",
        eval_url = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv")
