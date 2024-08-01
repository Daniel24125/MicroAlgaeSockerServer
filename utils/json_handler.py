import json 
from dotenv import load_dotenv
import os 

load_dotenv()

FILE_PATH = os.getenv("FILE_PATH")

class JSON_Handler: 
    updating_experiment = False
    experiment_data = None

    def __init__(self):
        self.read_experiment_data()

    def retrieve_experiment_data(self): 
        if not bool(self.experiment_data):
            self.read_experiment_data()
        return self.experiment_data 

    def read_experiment_data(self): 
        with open(FILE_PATH, 'r') as f:
            data = json.load(f)
            f.close()
            self.experiment_data = data

    def update_experiment_data(self, newData):
        self.experiment_data = {**self.experiment_data,**newData}

    def commit_experiment_changes(self): 
        if not self.updating_experiment:
            with open(FILE_PATH, "w") as f:
                self.updating_experiment = True
                json_object = json.dumps(self.experiment_data)
                f.write(json_object)
                self.updating_experiment = False


if __name__ == "__main__": 
    try: 
        file_handler = JSON_Handler()
        file_handler.update_experiment_data({
            "_id": "HELLO"
        })
        file_handler.commit_experiment_changes()
    except FileNotFoundError as err: 
        print("Error", err)
