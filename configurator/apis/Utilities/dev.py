TEST_LOC = 'C:\\Users\\hduon\\Documents\\Tests'
import os

class Development():
    def __init__(self):
        self.proj_test_dir = None
        self.debug = True
    def makeTestDir(self, proj_name: str = None):
        if proj_name != None:
            self.proj_test_dir = os.path.join(TEST_LOC, proj_name)
            os.makedirs(self.proj_test_dir,exist_ok = True)
        
