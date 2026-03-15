# ---- Python Modules ---- #
import pymongo
from pymongo.errors import DuplicateKeyError
import json
import os
from bson import ObjectId

# ---- Misc Variables ---- #

# ---- Initialising Variables ---- # 
config_path = "data/config.json"
settings_path = "data/settings.json"
mongoDbUri = "mongodb://localhost:27017/" ## add to env 

class DataHandler():
    def __init__(self):
        self.currentData = []
        # initialises the database client connection
        self.client = pymongo.MongoClient(mongoDbUri)
        self.database = self.client["Tunneler"]
        self.db = self.database["PlayerData"]
        # makes sure that the username is always something unique
        self.db.create_index("username", unique=True)
        self.menuHandler = None
        
    def setMenuHandler(self, MH):
        self.menuHandler = MH
    
    def formatPlayerData(self, username):
        return {
            "username": username,
            "currentLevel": "CH1/LV1",
            "levelTimes": {},
        }
    
    def ensureUserConfig(self): # checks for a local config file for the users uuid
        if not os.path.exists(config_path):
            self.menuHandler.enableMenu("NewUser")
            return {}
        
        with open(config_path, "r") as f:
            config = json.load(f)

        return config
    
    def saveSettings(self, settings):
        os.makedirs("data", exist_ok=True)

        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)

        print("Saved the data ",)
    
    def setNewUserData(self, username): # creates new user data if none can be found
        data = self.formatPlayerData(username)
        
        try:
            doc = self.db.insert_one(data)
        except DuplicateKeyError: # if data cant be inserted due to the duplicated username itll return false and ask again
            return False
        
        self.currentData = data
        
        # writes the data to the config file to be used when people load up
        config = {
            "userID": str(doc.inserted_id),
        }

        # Ensure directory exists
        os.makedirs("data", exist_ok=True)

        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        print(f"Config created for user '{username}'")
        return True

    def saveData(self): # save user data 
        self.db.update_one({"_id": self.currentData["_id"]}, {"$set": self.currentData })
        print('Data has been saved.')
        
    def loadData(self): # loads user data if it can find config. if it cant itll send the user to the new user screen
        userConfig = self.ensureUserConfig()
        
        if userConfig:
            userData = self.db.find_one({ "_id": ObjectId(userConfig["userID"]) })
        
            if not userData:
                self.menuHandler.enableMenu("NewUser")
            else:
                self.currentData = userData
              
    # ---- Encapsulation ----- #

    def fetchSettings(self):
        if not os.path.exists(settings_path):
            return {"volume": 1.0, "brightness": 1.0}  # defaults

        with open(settings_path, "r") as f:
            data = json.load(f)

        # Extract only the settings you care about
        return {
            "volume": data.get("volume", 1.0),
            "brightness": data.get("brightness", 1.0)
        }
    
    def fetchLevelTime(self, id):
        return self.currentData["levelTimes"].get(id)
    
    def fetchCurrentLevel(self):
        return self.currentData["currentLevel"]
    
    def fetchAllUsers(self):
        return self.db.find()
              
    def fetchData(self):
        return self.currentData
    
    def setCurrentLevel(self, currentLevel):
        self.currentData["currentLevel"] = currentLevel
        
    def setLevelSpeed(self, id, time):
        self.currentData["levelTimes"][id] = time