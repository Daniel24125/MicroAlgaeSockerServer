from . import json_handler, logger
import json 
from threading import Thread

class SocketServer(): 
    def __init__(self): 
        self.experiment_data = json_handler.JSON_Handler()
        
    
    def receive_cmd(self, data, client_socket):        
        try: 
            if len(data) > 0:  
                
                logger.log(f"Command received: {data}")
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

    async def notify_subscribers(self): 
        logger.log("[Subscriber] Subscribers " + str(self.get_num_subscribers()), severity="info")

        if len(self.__subscriber_list) > 0: 

            logger.log("[Subscriber] Notifying all the subscribers", severity="info")
            for sid in self.__subscriber_list: 
                print("NOTIFY SUBS", self.sio)
                await self.sio.emit('test', self.device_data.retrieve_data_from_file())

    def get_num_subscribers(self): 
        return len(self.__subscriber_list)

    def unsubscribe(self, sid): 
        logger.log("[Subscriber] Unsubscribing NextJS client SID...", severity="info")
        self.__subscriber_list.remove(sid)



class ReturnableThread(Thread):
    # This class is a subclass of Thread that allows the thread to return a value.
    def __init__(self, target):
        Thread.__init__(self)
        self.target = target
        self.result = None
    
    def run(self) -> None:
        self.result = self.target()

if __name__ == "__main__": 
    sub = SubscriberClass()
