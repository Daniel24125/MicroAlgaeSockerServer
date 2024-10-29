from utils.utils import SetInterval
from cpp_server_com import HSSUSB2A
from cpp_server_com.Simulator import HSSUSB2A_Simulator
import asyncio

class Experiment: 
    EXPERIMENT_STATE = "START"
   
    def __init__(self, subscriber) -> None:
        self.device = HSSUSB2A_Simulator()
        self.subscriber = subscriber
        self.timer = SetInterval(self.device.update_experimental_data, 1)

    def register_device(self, device_socket): 
        self.device = HSSUSB2A(device_socket)

    def set_state(self, state): 
        self.EXPERIMENT_STATE = state
    
    def start_experiment(self): 
        self.set_state("START")
        self.device.data_handler.send_data_via_socket()
        # self.timer.start()

    def stop_experiment(self): 
        self.set_state("STOP")
        self.timer.stop()

    def pause_experiment(self): 
        self.set_state("PAUSE")
        self.timer.stop()

    def resume_experiment(self): 
        self.set_state("RESUME")
        self.timer.start()
        
    

