import json
import pymongo.errors 
from .env_handler import load_env
import datetime 
import os 
from .logger import log
import pymongo


FILE_PATH = load_env("FILE_PATH")
BACKUP_FILE_PATH = load_env("BACKUP_FILE_PATH")
MONGODB_URI = load_env("MONGODB_URI")

class Data_Handler: 
    updating_experiment = False
    
    def __init__(self):
        self.experiment_data = None
        self.command_socket = None
        # self.init_db()
        self.read_experiment_data()

    ################ MONGO DB METHODS
    def init_db(self):
        try:
            log("Initiating DB","Experimental Data Handler", "warning")
            client = pymongo.MongoClient(MONGODB_URI)
            self.db = client["experimental_data"]
            self.exp_data_col = self.db["experiment"]
        except pymongo.errors.ConnectionFailure as err: 
            log("An error occured while connecting to the db: " + str(err), "Experimental Data Handler", "error")

    def save_to_db(self):
        try:
            self.exp_data_col.insert_one(self.experiment_data)
        except pymongo.errors.DuplicateKeyError as err:
            log("The record already exists: " + str(err), "Experimental Data Handler", "error")
            
    def get_exp_data(self): 
        data = self.exp_data_col.find()
        for exp in data: 
            print(exp)
    
    
    def retrieve_experiment_data(self): 
        if not bool(self.experiment_data):
            self.read_experiment_data()
        return self.experiment_data 

    def read_experiment_data(self, path_to_file = FILE_PATH): 
        data = self.retrieve_data_from_file(path_to_file)
        self.experiment_data = data

    def update_experiment_data(self, newData, commit_changes = False):
        self.experiment_data = {**self.experiment_data,**newData}
        if commit_changes: self.commit_experiment_changes()
        if self.command_socket: self.send_data_via_socket()

    def send_data_via_socket(self): 
        log("Sending updated data to the command socket\n","Experimental Data Handler", "info")
        if hasattr(self, "command_socket"):
            self.command_socket.send(bytes(json.dumps({"cmd": "notify_subscribers"}),encoding="utf-8"))


    def commit_experiment_changes(self): 
        if not self.updating_experiment:
            # self.backup_experiment_data()
            self.save_data_to_file(self.experiment_data)
        else: 
            log("File is currently being updated...","Experimental Data Handler", "warning")

    def backup_experiment_data(self): 
        log("\nBacking up experiment data...\n","Experimental Data Handler", "info")
        data = self.retrieve_data_from_file(FILE_PATH)
        backup_path = self.get_backup_path()
        self.save_data_to_file(data, backup_path)

    # UTILS 
    def get_backup_path(self): 
        current_date = str(datetime.datetime.now())
        backup_path = os.path.join(BACKUP_FILE_PATH.replace("/", "\\"), current_date)
        backup_path = backup_path.split(".")[0].replace(":", "_")
        os.mkdir(backup_path)
        return os.path.join(backup_path,"experiment.json")

    def retrieve_data_from_file(self, path_to_file = FILE_PATH):
        with open(path_to_file, 'r') as f:
            data = json.load(f)
            f.close()
            return data

    def save_data_to_file(self, data, path_to_file = FILE_PATH):
        self.updating_experiment = True
        with open(path_to_file, "w") as f:

            json_object = json.dumps(data)
            f.write(json_object)
            f.close()
        self.updating_experiment = False

    #COMMAND SOCKET    

    def register_command_socket(self, socket):
        self.command_socket = socket

    def unregister_command_socket(self):
        self.command_socket = None