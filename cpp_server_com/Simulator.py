from resources.data_handler import Data_Handler
from resources.logger import log
import random
import asyncio


class HSSUSB2A_Simulator: 
    config = {
        "integrationTime": 20000,
        "gain": 0
    }
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

    def __init__(self): 
        self.data_handler = Data_Handler()

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
        

    def register_command_socket(self, command_socket): 
        self.data_handler.register_command_socket(command_socket)    

    def update_param(self, param, value): 
        if param in self.EXPERIMENT_DATA: 
            self.EXPERIMENT_DATA[param].append(value)

    def get_spectrometer_settings(self, data, *argv): 
        log("Function called: get_spectrometer_settings", "HSSUSBA21_Simulator", "info")
        return self.config

    def get_random_value(self, min, max): 
        return min + random.random()*(max-min)
    
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