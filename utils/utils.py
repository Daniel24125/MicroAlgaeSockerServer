from . import json_handler, logger
import json 

class SocketServer(): 
    def __init__(self): 
        self.experiment_data = json_handler.JSON_Handler()
        

    def handle_commands(self, data, client_socket): 
        if not len(data): 
            self.handle_client_disconnection(client_socket) 

        logger.log(f"Command received: {data}", "info")
        try: 
            cmd = json.loads(data)
            self.parse_cmd(cmd, client_socket)
        except ValueError as e: 
            logger.log("Error loading the json file. This probably occurs due to the first connection by the web client" + e,"error")

    
    def receive_cmd(self, data, client_socket):        
        if not len(data):  
            self.handle_client_disconnection(client_socket)
            
        logger.log(f"Command received: {data}")
        try: 
            cmd = json.loads(data)
            self.parse_cmd(cmd, client_socket)
        except ValueError as e: 
            logger.log("Error loading the json file.","error")


    def parse_cmd(self, cmd, client_socket, commands):        
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        
        cmd_received, data = (cmd["cmd"], cmd["data"])
        logger.log(f"Parsing the following command: {cmd_received}", "info")

        if cmd_received in commands: 
            commands[cmd_received](data, client_socket)
        else:
            logger.log("Command not recognized", "warning")
           
    def handle_client_disconnection(self, client_socket): 
        logger.log("The client has been disconnected")



class SubscriberClass(): 
    __subscriber_list = []

    def __init__(self, sio): 
        self.device_data = json_handler.JSON_Handler()
        self.sio = sio
        
      
    def add_subscriber_to_list(self, sid): 
        logger.log("[Subscriber] Adding client socket to the subscribers list", severity="info")
        self.__subscriber_list.append(sid)
        logger.log("[Subscriber] Number of subscribers: " + str(self.get_num_subscribers()), severity="info")


    def notify_subscribers(self): 
        if len(self.__subscriber_list) > 0: 
            logger.log("[Subscriber] Notifying all the subscribers", severity="info")
            for sid in self.__subscriber_list: 
                self.sio.emit('device_data_update',self.device_data.retrieve_data_from_file(), to=sid)

    def get_num_subscribers(self): 
        return len(self.__subscriber_list)

    def unsubscribe(self, sid): 
        logger.log("[Subscriber] Unsubscribing NextJS client SID...", severity="info")
        self.__subscriber_list.remove(sid)



if __name__ == "__main__": 
    sub = SubscriberClass()
