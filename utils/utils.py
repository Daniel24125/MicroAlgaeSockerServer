from . import data_handler, logger
import json 
import threading
import time 
import hashlib
import base64

class SetInterval: 
    def __init__(self, func, sec, func_args=None): 
        self.func = func
        self.sec = sec
        self.STOP_TIMER = False
    
    def func_wrapper(self): 
        while self.STOP_TIMER: 
            self.func()    
            time.sleep(self.sec)
    
    def start(self): 
        if not self.STOP_TIMER: 
            self.STOP_TIMER = True
            t = threading.Thread(target=self.func_wrapper)
            t.start()

    def stop(self): 
        self.STOP_TIMER = False

class SocketServer(): 
    def __init__(self): 
        pass        
    def websocket_handshake(self,data, client_socket):
        try: 

            request_headers = {}
            for line in data.decode("utf-8").split('\r\n')[1:]:
                line = line.strip()
                if not line:
                    break
                header, value = line.split(': ')
                request_headers[header.lower()] = value.strip()

            sec_websocket_key = request_headers['sec-websocket-key']
            key_concat = sec_websocket_key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            sha1_hash = hashlib.sha1(key_concat.encode('utf-8')).digest()
            sec_websocket_accept = base64.b64encode(sha1_hash).decode('utf-8')

            response = f"HTTP/1.1 101 Switching Protocols\r\n" \
                    f"Upgrade: websocket\r\n" \
                    f"Connection: Upgrade\r\n" \
                    f"Sec-WebSocket-Accept: {sec_websocket_accept}\r\n" \
                    f"\r\n"
            client_socket.sendall(response.encode('utf-8'))
        except Exception as err: 
            print(err)

    def receive_cmd(self, data, client_socket):        
        try: 
            if len(data) > 0:  
                self.parse_connection_data(data, client_socket)     
        except ValueError as e: 
            logger.log("Error loading the json file: " + str(e),context="Socket Server Parent Class",severity="error")
          
    def parse_connection_data(self, data, client_socket): 
        is_handshake_data = data.find(b"GET") >= 0
        if is_handshake_data: 
            self.websocket_handshake(data, client_socket)
        else:
            cmd = json.loads(data)
            self.parse_cmd(cmd, client_socket)

    def parse_cmd(self, cmd, client_socket, commands):        
        if not "cmd" in cmd or not "origin" in cmd: 
            raise Exception("Invalid JSON received")
        
        cmd_received, data, origin = (cmd["cmd"], cmd["data"], cmd["origin"])
        logger.log(f"Parsing the following command: {cmd_received}",context="Socket Server Parent Class", severity="info")

        if cmd_received in commands: 
            commands[cmd_received](data, client_socket)
        else:
            logger.log("Command not recognized", context="Socket Server Parent Class", severity="warning")
           
    def handle_client_disconnection(self, client_socket): 
        logger.log("The client has been disconnected",context="Socket Server Parent Class")

class SubscriberClass(): 
    def __init__(self): 
        self.__subscriber_list = []
        self.device_data = data_handler.Data_Handler()
        
    def add_subscriber_to_list(self, socket): 
        logger.log("Adding client socket to the subscribers list", context="Subscriber", severity="info")
        self.__subscriber_list.append(socket)
        logger.log("Number of subscribers: " + str(self.get_num_subscribers()), context="Subscriber", severity="info")

    def notify_user(self, socket): 
        socket.send(bytes(json.dumps(self.device_data.retrieve_data_from_file()),encoding="utf-8"))

    def notify_subscribers(self): 
        if len(self.__subscriber_list) > 0: 
            logger.log("Notifying all the subscribers", context="Subscriber", severity="info")
            for s in self.__subscriber_list: 
                self.notify_user(s)

    def get_num_subscribers(self): 
        return len(self.__subscriber_list)

    def unsubscribe(self, socket): 
        logger.log("Unsubscribing NextJS client...", context="Subscriber", severity="info")
        self.__subscriber_list.remove(socket)
        



if __name__ == "__main__": 
    sub = SubscriberClass()
