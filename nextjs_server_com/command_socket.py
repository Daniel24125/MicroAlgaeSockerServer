
import sys
import os
import socket
import json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils import env_handler, logger
HOST = env_handler.load_env("CPP_HOST")
PORT = int(env_handler.load_env("CPP_PORT"))
import time
class CommandSocket: 
    
    def __init__(self, notify): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                logger.log("[Command Socket] Trying to connect to the server on port " + str(PORT), severity="info")
                s.connect((HOST, PORT))
                logger.log("[Command Socket] Connection made", severity="info")

                self.socket = s
                self.notify = notify
                time.sleep(3)
                self.send_command_to_spec_server({
                    "cmd": "identification",
                    "data": "next"
                })

            except Exception as err: 
                logger.log(f"[Command Socket] An error occured {err}", severity="error")
    
   
    def get_spec_socket(self): 
        return self.socket
    
    async def wait_for_commands(self): 
        while True:
            logger.log("[Command Socket] Listenning for commands", severity="info")
            received_data = self.socket.recv(1024)
            cmd, data =  self.parse_command(received_data)
            logger.log("[Command Socket] Command received from the Python Spec Socket server: " + str(cmd), severity="info")
            logger.log("[Command Socket] Data: " + str(data), severity="info")
            await self.notify()

            

    def parse_command(self, data):
        logger.log("[Command Socket] Parsing the command " + str(data), severity="info")
        loaded_data = json.loads(str(data.decode("utf-8")))
        return (loaded_data["cmd"], loaded_data["data"] if bool(loaded_data["data"]) else "")
    
    def send_command_to_spec_server(self, msg): 
        logger.log("[Command Socket] Sending command to the Python Spec Socket", severity="info")
        self.socket.send(bytes(json.dumps(msg), encoding="utf-8"))

    def disconnect(self): 
        logger.log("[Command Socket] Closing the command socket connection...", severity="info")
       

if __name__ == "__main__": 
    cmd = CommandSocket()
