import json 
from .env_handler import load_env
import datetime 
import os 
from .logger import log

FILE_PATH = load_env("FILE_PATH")
BACKUP_FILE_PATH = load_env("BACKUP_FILE_PATH")

class JSON_Handler: 
    updating_experiment = False
    experiment_data = None
    command_socket = None

    def __init__(self):
        self.read_experiment_data()

    def register_command_socket(self, socket):
        self.command_socket = socket

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
        log("\n[Experimental Data Handler] Sending updated data to the command socket\n", "info")
        self.command_socket.send(bytes(json.dumps({
            "cmd": "status_update", 
            "data": self.experiment_data
        }),encoding="utf-8"))


    def commit_experiment_changes(self): 
        if not self.updating_experiment:
            self.backup_experiment_data()
            self.updating_experiment = True
            self.save_data_to_file(self.experiment_data)
            self.updating_experiment = False
        else: 
            log("[Experimental Data Handler] File is currently being updated...", "warning")

    def backup_experiment_data(self): 
        log("\n[Experimental Data Handler] Backing up experiment data...\n", "info")
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
        with open(path_to_file, "w") as f:
            json_object = json.dumps(data)
            f.write(json_object)
            f.close()

if __name__ == "__main__": 
    try: 
        file_handler = JSON_Handler()
       
    except FileNotFoundError as err: 
        log("Error", "error")
