
import sys
import os
import json
import time
import socket
import select


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from resources import env_handler, logger, utils
from socket_clients.command_socket import NextJSSocket

HOST = env_handler.load_env("CPP_HOST") 
PORT = int(env_handler.load_env("CPP_PORT"))

class SpecServerSocket(utils.SocketServer): 
    device_socket = None
    simulation_mode = True

    def __init__(self, ): 
        super().__init__()
        self.nexjs_client_handler = NextJSSocket()

    def init_socket(self, port=PORT): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.server_socket.bind((HOST, port))
        self.server_socket.listen()
        logger.log(f"Server listenning on port {port}", context="Python Spec Socket", severity="info")

    def listen_for_connections(self): 
        while True: 
            read_socket, _ , exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_socket: 
                try: 
                    if notified_socket == self.server_socket: 
                        client_socket, client_address = self.server_socket.accept()
                        logger.log(f"A client has connected with the following address: {client_address}",context="Python Spec Socket",severity="default")
                        self.handle_data_reception(client_socket)
                    else: 
                        self.handle_data_reception(notified_socket)

                except ConnectionResetError as e: 
                    self.handle_client_disconnection(notified_socket)
                except Exception as err: 
                    
                    logger.log(f"An error occured: {str(err)}",context="Python Spec Socket",severity="error")   
    
    def handle_data_reception(self, client_socket):
        logger.log("Waiting for Commands", context="Python Spec Socket",severity="default")
        try: 
            data = client_socket.recv(1024)
        except socket.timeout as e:
            err = e.args[0]
            if err != 'timed out':
                logger.log("Error while receiving data: " + str(e),context="Python Spec Socket", severity="error")
        except socket.error as e:
            self.handle_client_disconnection(client_socket)
        else: 
            if len(data) == 0: 
                   self.handle_client_disconnection(client_socket)
            else: 
                self.receive_cmd(data, client_socket)

    def parse_cmd(self, cmd, client_socket):
        commands = {
            "identification": self.identification,
            "device_status": self.device_status, 
            "start_experiment": self.start_experiment, 
            "stop_experiment": self.stop_experiment
        }
        super().parse_cmd(cmd, client_socket, commands)

    # ------------- Available spectrometer commands -----------------
    def identification(self, data, client_socket, *argv):
        if data == "nir": 
            self.nir_spec_init(client_socket)
        elif data == "next": 
            self.nexjs_client_handler.init_client(client_socket)
        else: 
            raise Exception("Unauthorized connection.")
        self.sockets_list.append(client_socket)

    def nir_spec_init(self, socket): 
        logger.log("Initializing the Spectrometer instance...",context="Python Spec Socket", severity="info")
        self.device_socket = socket

    def device_status(self, data, socket): 
        logger.log("Updating spec status...",context="Python Spec Socket", severity="info")
        self.nexjs_client_handler.subscriber.notify_subscribers()

    def start_experiment(self, data, socket): 
        logger.log("Starting the experiment...",context="Python Spec Socket", severity="info")
        self.experiment_manager.start_experiment()
    
    def stop_experiment(self, data, socket): 
        logger.log("Stopping the experiment...",context="Python Spec Socket", severity="info")
        self.experiment_manager.stop_experiment()
         
    # ------------- Utils methods -----------------
    def handle_client_disconnection(self, client_socket): 
        super().handle_client_disconnection(client_socket)
        if client_socket == self.device_socket: 
            self.reset_socket()
        self.sockets_list.remove(client_socket)

    def reset_socket(self):
        self.device_socket = None
        self.spec.set_device_socket(None)
        self.simulation_mode = True
      

    def send_client_commands(self, msg): 
        if hasattr(self, "nextjs_socket"):
            self.nextjs_socket.send(bytes(json.dumps(msg),encoding="utf-8"))
        else:
            logger.log("Command socket client not available!", context="Python Spec Socket", severity="info")
    
    def send_spectrometer_command(self, cmd): 
        if hasattr(self, "device_socket"):
            self.device_socket.send(bytes(json.dumps(cmd),encoding="utf-8"))










