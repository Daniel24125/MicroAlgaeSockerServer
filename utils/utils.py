from . import json_handler, logger
import json 
from threading import Thread

class SocketServer(): 
    def __init__(self): 
        self.experiment_data = json_handler.JSON_Handler()
        
    
    def receive_cmd(self, data, client_socket):        
        try: 
            if len(data) > 0:  
                
                logger.log(f"Command received: {data}", context="Socket Server Parent Class")
                cmd = json.loads(data)
                self.parse_cmd(cmd, client_socket)
        except ValueError as e: 
            logger.log("Error loading the json file: " + str(e),context="Socket Server Parent Class",severity="error")


    def parse_cmd(self, cmd, client_socket, commands):        
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        
        cmd_received, data = (cmd["cmd"], cmd["data"])
        logger.log(f"Parsing the following command: {cmd_received}",context="Socket Server Parent Class", severity="info")

        if cmd_received in commands: 
            commands[cmd_received](data, client_socket)
        else:
            logger.log("Command not recognized", context="Socket Server Parent Class", severity="warning")
           
    def handle_client_disconnection(self, client_socket): 
        logger.log("The client has been disconnected",context="Socket Server Parent Class")



class SubscriberClass(): 
    __subscriber_list = []

    def __init__(self, sio): 
        self.device_data = json_handler.JSON_Handler()
        self.sio = sio
        
    def add_subscriber_to_list(self, sid): 
        logger.log("Adding client socket to the subscribers list", context="Subscriber", severity="info")
        self.__subscriber_list.append(sid)
        logger.log("Number of subscribers: " + str(self.get_num_subscribers()), context="Subscriber", severity="info")

    async def notify_user(self, sid): 
        await self.sio.emit('device_update', self.device_data.retrieve_data_from_file(), to=sid)

    async def notify_subscribers(self): 
        if len(self.__subscriber_list) > 0: 
            logger.log("Notifying all the subscribers", context="Subscriber", severity="info")
            for sid in self.__subscriber_list: 
                await self.notify_user(sid)

    def get_num_subscribers(self): 
        return len(self.__subscriber_list)

    def unsubscribe(self, sid): 
        logger.log("Unsubscribing NextJS client SID...", context="Subscriber", severity="info")
        self.__subscriber_list.remove(sid)



if __name__ == "__main__": 
    sub = SubscriberClass()
