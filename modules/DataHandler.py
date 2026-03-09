# ---- Python Modules ---- #
import pymongo
from pymongo.errors import DuplicateKeyError
import json
import os
from bson import ObjectId

# ---- Misc Variables ---- #

# ---- Initialising Variables ---- # 
config_path = "data/config.json"

class DataHandler():
    def __init__(self):
        self.currentData = []
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.collection = self.client["Tunneler"]
        self.db = self.collection["PlayerData"]
        self.db.create_index("username", unique=True)
        self.menuHandler = None

        self.db.insert_one({
            "test": "test"
        })
        print('i handle the data.')
        
    def setMenuHandler(self, MH):
        self.menuHandler = MH
    
    def formatPlayerData(self, username):
        return {
            "username": username,
            "currentLevel": "",
            "levelTimes": [],
        }
    
    def ensureUserConfig(self):
        if not os.path.exists(config_path):
            self.menuHandler.enableMenu("NewUser")
            return 
        
        with open(config_path, "r") as f:
            config = json.load(f)

        return config
    
    def setNewUserData(self, username):
        data = self.formatPlayerData(username)
        
        try:
            doc = self.db.insert_one(data)
        except DuplicateKeyError:
            return False
        
        self.currentData = data
        
        config = {
            "userID": str(doc.inserted_id),
        }

        # Ensure directory exists
        os.makedirs("data", exist_ok=True)

        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        print(f"Config created for user '{username}'")
        return True

    def saveData(self):
        self.db.update_one({ "_id": self.currentData._id }, self.currentData)
        print('Data has been saved.')
        
    def loadData(self):
        userConfig = self.ensureUserConfig()
        
        if userConfig:
            userData = self.db.find_one({ "_id": ObjectId(userConfig["userID"]) })
        
            if not userData:
                self.menuHandler.enableMenu("NewUser")
            else:
                self.currentData = userData
        
    def fetchData(self):
        return self.currentData
    