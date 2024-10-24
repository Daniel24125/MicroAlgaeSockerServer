from utils.utils import SetInterval
from cpp_server_com import HSSUSB2A
from cpp_server_com.Simulator import HSSUSB2A_Simulator

class Experiment: 
    EXPERIMENT_STATE = "START"
   
    def __init__(self) -> None:
        self.device = HSSUSB2A_Simulator()
        self.timer = SetInterval(self.device.update_experimental_data, 1)

    def register_device(self, device_socket): 
        self.device = HSSUSB2A(device_socket)

    def register_command_socket(self, command_socket): 
        self.device.register_command_socket(command_socket)

    def set_state(self, state): 
        self.EXPERIMENT_STATE = state
    
    def start_experiment(self): 
        self.set_state("START")
        self.timer.start()

    def stop_experiment(self): 
        self.set_state("STOP")
        self.timer.stop()

    def pause_experiment(self): 
        self.set_state("PAUSE")
        self.timer.stop()

    def resume_experiment(self): 
        self.set_state("RESUME")
        self.timer.start()
        
    

