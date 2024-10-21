import json
from utils.experiment_handler import Experiment_Handler
from utils.logger import log
class HSSUSB2A: 
    socket = None
    def __init__(self, device_socket): 
        self.device_socket = device_socket
        self.experiment_data = Experiment_Handler()


    def set_device_socket(self, device_socket): 
       self.device_socket = device_socket


    def send_command(self, command): 
        send_data = bytes(json.dumps(command), "utf-8")
        self.device_socket.send(send_data)
        

    def device_status(self, data, *argv):
        log("NIR Status received", context="HSSUSB2A",severity="info")
        deviceState =  True if data == "True" else False
        self.experiment_data.update_experiment_data({
            "isDeviceConnected": deviceState
        }, True)


    def get_spectrometer_settings(self, data, *argv): 
        print("get_spectrometer_settings")

    def set_exposure_time(self, data, *argv): 
        print("set_exposure_time")

    def set_repeat_cout(self, data, *argv): 
        print("set_repeat_cout")

    def set_gain(self, data, *argv): 
        print("set_gain")