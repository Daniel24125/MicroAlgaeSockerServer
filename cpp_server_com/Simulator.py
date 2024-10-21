import json
from utils.experiment_handler import Experiment_Handler
from utils.logger import log
from . import experiment


class HSSUSB2A_Simulator: 
    config = {
        "integrationTime": 20000,
        "gain": 0
    }

    def __init__(self): 
        pass
    
    def get_spectrometer_settings(self, data, *argv): 
        log("Function called: get_spectrometer_settings", "HSSUSBA21_Simulator", "info")
        return self.config

    def register_command_socket(self, command_socket):
        self.command_socket = command_socket
        self.exp_instance.register_command_socket()

    def set_exposure_time(self, data, *argv): 
        log("Function called: set_exposure_time", "HSSUSBA21_Simulator", "info")
        self.set_config("integrationTime", data)

    def set_repeat_cout(self, data, *argv): 
        log("Function called: set_repeat_cout", "HSSUSBA21_Simulator", "info")

    def set_gain(self, data, *argv): 
        log("Function called: set_gain", "HSSUSBA21_Simulator", "info")
        self.set_config("gain", data)

    def set_config(self, param, value): 
        self.config = {
            **self.config, 
            param: value
        }