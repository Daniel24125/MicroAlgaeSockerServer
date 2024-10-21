from utils.utils import SetInterval
from cpp_server_com import HSSUSB2A
from cpp_server_com.Simulator import HSSUSB2A_Simulator
import random

class Experiment: 
    EXPERIMENT_STATE = "START"
    EXPERIMENT_DATA = {
        "dissolvedCO2": [],
        "dissolvedO2": [],
        "glucose": [],
        "od": [],
        "temperature": [],
        "ph": [],
        "lightIntensity": [],
        "urea": [],
        "ortofosfate": [],
        "totalCellCount": []
    }

    def __init__(self, data_handler) -> None:
        self.timer = SetInterval(self.update_experimental_data, 1)
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
        
    def update_experimental_data(self): 
        self.update_param("dissolvedCO2", self.get_random_value(1, 10))
        self.update_param("dissolvedO2", self.get_random_value(1, 10))
        self.update_param("glucose", self.get_random_value(10, 100))
        self.update_param("od", self.get_random_value(0.1, 0.6))
        self.update_param("temperature", self.get_random_value(35, 37))
        self.update_param("ph", self.get_random_value(5, 7))
        self.update_param("lightIntensity", self.get_random_value(1, 10))
        self.update_param("urea", self.get_random_value(1, 10))
        self.update_param("ortofosfate", self.get_random_value(1, 10))
        self.update_param("totalCellCount", self.get_random_value(10, 1000))
        self.data_handler.update_experiment_data({
            "data": self.EXPERIMENT_DATA
        })
        
    def update_param(self, param, value): 
        if hasattr(self.EXPERIMENT_DATA, param): 
            self.EXPERIMENT_DATA[param].append(value)

    def get_random_value(self, min, max): 
        return min + random.random()*(max-min)
    