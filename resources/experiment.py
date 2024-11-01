from resources.utils import SetInterval
from cpp_server_com import HSSUSB2A
from cpp_server_com.Simulator import HSSUSB2A_Simulator

class Experiment: 
    EXPERIMENT_STATE = "START"
   
    def __init__(self) -> None:
        self.device = HSSUSB2A_Simulator()
        self.timer = SetInterval(self.device.update_experimental_data, 1)

    def register_device(self, device_socket): 
        self.device = HSSUSB2A(device_socket)

    def register_nexjs_websocket(self, websocket): 
        self.device.register_nexjs_websocket(websocket)

    def set_state(self, state): 
        self.EXPERIMENT_STATE = state
    
    async def start_experiment(self): 
        print("Experiment starte")
        self.set_state("START")
        await self.timer.start()

    async def stop_experiment(self): 
        self.set_state("STOP")
        self.timer.stop()

    async def pause_experiment(self): 
        self.set_state("PAUSE")
        self.timer.stop()

    async def resume_experiment(self): 
        self.set_state("RESUME")
        await self.timer.start()
        
    

