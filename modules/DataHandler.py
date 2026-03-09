# ---- Python Modules ---- #
import pymongo

# ---- Misc Variables ---- #

# ---- Initialising Variables ---- # 


class DataHandler():
    def __init__(self):
        self.currentData = []
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["Tunneler"]
        print('i handle the data.')
        
    def saveData(self):
        print("data saved")
        
    def loadData(self):
        print("data load") # set data to current data
        
    def fetchData(self):
        return self.currentData