from dataclasses import dataclass
import imu
import functions

class reaction_wheel():
    def __init__(self, get_data_function, safe_data_function ,timestamp_reference, log_function=print):
        self.log_function= log_function
        self.timestamp_reference=timestamp_reference
        self.get_data_function=get_data_function


    