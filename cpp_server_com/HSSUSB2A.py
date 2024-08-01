import json
from utils.json_handler import JSON_Handler
from utils.logger import log
class HSSUSB2A: 
    socket = None

    def __init__(self, nir_socket): 
        self.socket = nir_socket
        self.send_command({
            "cmd": "nir_status"
        })
        self.experiment_data = JSON_Handler()

    def set_nir_socket(self, nir_socket): 
        self.socket = nir_socket

    def send_command(self, command): 
        send_data = bytes(json.dumps(command), "utf-8")
        self.socket.send(send_data)
        
    def nir_status(self, data, *argv):
        log("NIR Status received", "info")
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