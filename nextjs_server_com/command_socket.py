
import sys
import os
import socket
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger
HOST = env_handler.load_env("CPP_HOST")
PORT = int(env_handler.load_env("CPP_PORT"))

class CommandSocket: 
    notify = None
    
    def __init__(self): 
        try:
            self.connect_to_spec_socket()
            self.send_command_to_spec_server({
                "cmd": "identification",
                "data": "next"
            })

        except Exception as err: 
            logger.log(f"An error occured {err}", context="Command Socket", severity="error")

    async def init_notifier(self, notifier): 
        self.notify = notifier
     
    def connect_to_spec_socket(self): 
        try: 
            logger.log("Trying to connect to the server on port " + str(PORT),context="Command Socket", severity="info")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.settimeout(2)
            logger.log("Connection made",context="Command Socket", severity="info")
            self.socket = s
        except Exception as err: 
            self.handle_disconnection()

    def get_spec_socket(self): 
        return self.socket
    
    async def wait_for_commands(self): 
        logger.log("Listenning for commands",context="Command Socket", severity="info")
        while True:
            try:
                received_data = self.socket.recv(1024)
                print("AFTER socket.recv")
            except socket.timeout as e:
                err = e.args[0]
                if err == 'timed out':
                    continue
                else: 
                    logger.log("Error while receiving data: " + str(e),context="Command Socket", severity="error")
                    continue
            except socket.error as e:
                logger.log("A socket error occured: " + str(e),context="Command Socket", severity="error")
            else: 
                if len(received_data) == 0: 
                    self.handle_disconnection()
                else: 
                    cmd, data =  self.extract_command(received_data)
                    logger.log("Command received from the Python Spec Socket server: " + str(cmd),context="Command Socket", severity="info")
                    logger.log("Data: " + str(data),context="Command Socket", severity="info")
                    if self.notify:
                        await self.notify()

    def handle_disconnection(self): 
        logger.log("Disconnected from the spec server",context="Command Socket", severity="warning")
        self.connect_to_spec_socket()

    def extract_command(self, data):
        logger.log("Parsing the command " + str(data),context="Command Socket", severity="info")
        loaded_data = json.loads(str(data.decode("utf-8")))
        return (loaded_data["cmd"], loaded_data["data"] if bool(loaded_data["data"]) else "")
    
    def send_command_to_spec_server(self, msg): 
        logger.log("Sending command to the Python Spec Socket",context="Command Socket", severity="info")
        self.socket.send(bytes(json.dumps(msg), encoding="utf-8"))

    def disconnect(self): 
        logger.log("Closing the command socket connection...",context="Command Socket", severity="info")
       

if __name__ == "__main__": 
    cmd = CommandSocket()
