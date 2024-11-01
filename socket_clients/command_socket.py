
import sys
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from resources import env_handler, logger, utils
from cpp_server_com.experiment import Experiment
HOST = env_handler.load_env("CPP_HOST")
PORT = int(env_handler.load_env("CPP_PORT"))

class NextJSSocket: 
    
    def __init__(self): 
        try:
            self.subscriber = utils.SubscriberClass()   
            self.init_experiment_manager()
        except Exception as err: 
            logger.log(f"An error occured {err}", context="NextJS Socket", severity="error")

    def init_experiment_manager(self): 
        self.experiment_manager = Experiment(self.subscriber)
     
    def init_client(self, socket): 
        logger.log("Command Client connected",context="Python Spec Socket", severity="info")
        self.subscriber.add_subscriber_to_list(socket)
        self.subscriber.notify_user(socket)

    def parse_cmd(self, received_data): 
        commands = {
            "notify_subscribers": self.notify_subscribers
        }
        try: 
            cmd, data =  self.extract_command(received_data)
            logger.log("Command received from the Python Spec Socket server: " + str(cmd),context="Command Socket", severity="info")
            if cmd in commands: 
                commands[cmd]()
            else: 
                raise Exception("Command not found")
        
        except Exception as err:
            logger.log("An error occured while trying to parse the data received: " + str(err),context="Command Socket", severity="error")
            logger.log("Data: " + str(received_data.decode("utf-8")) ,context="Command Socket", severity="error")
             

    def notify_subscribers(self, *argv): 
        self.subscriber.notify_subscribers()

    ############## UTILS

   
    def extract_command(self, data):
        logger.log("Parsing the command " + str(data),context="Command Socket", severity="info")
        loaded_data = json.loads(str(data.decode("utf-8")))
        if not "cmd" in loaded_data: 
            raise Exception("Invalid JSON received")
        return (loaded_data["cmd"], loaded_data["data"] if hasattr(loaded_data, "data") else "")
    
    def send_command_to_spec_server(self, msg): 
        logger.log("Sending command to the Python Spec Socket",context="Command Socket", severity="info")
        self.socket.send(bytes(json.dumps(msg), encoding="utf-8"))

    def disconnect(self): 
        logger.log("Closing the command socket connection...",context="Command Socket", severity="info")
       

if __name__ == "__main__": 
    cmd = CommandSocket()
