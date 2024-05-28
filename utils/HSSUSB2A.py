

class HSSUSB2A: 
    socket = None
    is_nir_init = False

    def __init__(self, nir_socket): 
        self.socket = nir_socket

    def set_nir_socket(self, nir_socket): 
        self.socket = nir_socket

    def send_command(self, command): 
        self.socket.send(command)
        
    def nir_status(self, data, *argv):
        print("NIR Status received")
        self.is_nir_init = bool(data)

    def get_spectrometer_settings(self, data, *argv): 
        print("get_spectrometer_settings")

    def set_exposure_time(self, data, *argv): 
        print("set_exposure_time")

    def set_repeat_cout(self, data, *argv): 
        print("set_repeat_cout")

    def set_gain(self, data, *argv): 
        print("set_gain")