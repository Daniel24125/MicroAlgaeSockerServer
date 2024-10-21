from utils.utils import SetInterval
from cpp_server_com import HSSUSB2A
from cpp_server_com.Simulator import HSSUSB2A_Simulator

class Experiment: 
    EXPERIMENT_STATE = "START"

    def __init__(self, data_handler) -> None:
        self.timer = SetInterval(self.send_experiment_data, 1)
        self.data_handler = data_handler
        self.device = HSSUSB2A_Simulator()

    def register_device(self, device_socket): 
        self.device = HSSUSB2A(device_socket)

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
        
    def send_experiment_data(self): 
        print("Experiment data sent")
        