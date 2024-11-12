from resources import logger
import json 
import asyncio



class Connection(): 
    def __init__(self, websocket) -> None:
        logger.log("NEXTJS Client connected", "Client Connection", "info")
        self.websocket = websocket
        self.commands = {}

    def init_experiment_manager(self, experiment_manager):
        self.experiment_manager = experiment_manager
        self.experiment_manager.register_nexjs_websocket(self.websocket)

    async def init_subscriber(self, subscriber): 
        self.subscriber = subscriber
        self.subscriber.add_subscriber_to_list(self.websocket)
        await self.subscriber.notify_user(self.websocket)

    async def handle_received_messages(self, message):
        command = json.loads(message)
        await self.parse_cmd(command)

    async def parse_cmd(self, cmd):        
        if not "cmd" in cmd: 
            raise Exception("Invalid JSON received")
        
        cmd_received, data = (cmd["cmd"], cmd["data"])
        logger.log(f"Parsing the following command: {cmd_received}",context="Client Connection", severity="info")

        if cmd_received in self.commands: 
            await self.commands[cmd_received](data)
        else:
            logger.log("Command not recognized", context="Client Connection", severity="warning")
    
    def register_commands(self, command_list): 
        for command in command_list: 
            key, value = command
            self.commands[key] = value

    def handle_disconnection(self): 
        logger.log("The client has been disconnected",context="Client Connection", severity="info")
        self.subscriber.unsubscribe(self.websocket)

class NextJSClientConnection(Connection): 
    def __init__(self, websocket) -> None:
        super().__init__(websocket)
        self.register_commands([
            ("start_experiment", self.start_experiment),
            ("stop_experiment", self.stop_experiment),
        ])

    async def listen_for_commands(self): 
        try: 
            while True:
                message = await self.websocket.recv()
                await self.handle_received_messages(message)
        except Exception as err: 
            logger.log("An error while listenning for commands: " + str(err), context="Client Connection", severity="error")
            self.handle_disconnection()

    async def start_experiment(self, data): 
        logger.log("Starting the experiment...",context="Python Spec Socket", severity="info")
        await self.experiment_manager.start_experiment()
    
    async def stop_experiment(self, data): 
        logger.log("Stopping the experiment...",context="Python Spec Socket", severity="info")
        await self.experiment_manager.stop_experiment()