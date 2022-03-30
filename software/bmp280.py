import functions
import threading
import board
import adafruit_bmp280
import logging_and_datasaving
import time
import numpy as np


class bmp280():
    def __init__(self, data, timestamp_reference, log_function=print, decent_treshold=-5, acent_threshold=5):
        self.log_function = log_function
        self.timestamp_reference = timestamp_reference
        self.data = data
        self.data["bmp280"] = [[], [], [], []]
        self.data["bmp280_test"] = [[], [], [], []]
        self.decent_treshold = decent_treshold
        self.acent_threshold = acent_threshold
        try:
            i2c = board.I2C()
            self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
        except Exception as exception:
            self.log_function("bmp280: init failed: "+ str(type(exception))+ str(exception))
        self.thread = threading.Thread(target=lambda: self.data_capture("bmp280"))

    def calibrate_altitude(self):
        try:
            self.sensor.sea_level_pressure = functions.cut_time(self.sensor.pressure)
            self.log_function("bmp280: calibrate_altitude success")
        except Exception as exception:
            self.log_function("bmp280: calibrate_altitude failed "+ str(type(exception))+ str(exception))

    def read_data(self):
        try:
            temperature = functions.cut_time(self.sensor.temperature)
            pressure = functions.cut_time(self.sensor.pressure)
            altitude = functions.cut_time(self.sensor.altitude)
            data = [temperature, pressure, altitude]
        except Exception as exception:
            self.log_function("bmp280: read_data failed "+ str(type(exception))+ str(exception))
            data = ['E', 'E', 'E']
        self.log_function("bmp280 data read: " + str(data))
        return data

    def safe_data(self, data_entry):
        self.data[data_entry][0].append(self.read_data()[0])
        self.data[data_entry][1].append(self.read_data()[1])
        self.data[data_entry][2].append(self.read_data()[2])
        self.data[data_entry][3].append(functions.actime(self.timestamp_reference))

    def data_capture(self, data_entry):
        try:
            while self.capture_on == True:
                self.safe_data(data_entry)
                time.sleep(0.01)
        except Exception as exception:
            self.log_function("bmp280: data_capture failed: "+ str(type(exception))+ str(exception))

    def start_thread(self):
        try:
            self.capture_on = True
            self.thread.start()
            self.log_function("bmp280 thread started")
        except Exception as exception:
            self.log_function("bmp280: start_thread failed: "+ str(type(exception))+ str(exception))

    def stop_thread(self):
        try:
            self.capture_on = False
            while self.thread.is_alive():
                time.sleep(0.1)
            self.log_function("bmp280 thread stopped")
        except Exception as exception:
            self.log_function("bmp280: stop_thread failed: "+ str(type(exception))+ str(exception))

    def sensor_test(self):
        try:
            self.log_function("sensor test started")
            for i in range(20):
                self.safe_data("bmp280_test")
        except Exception as exception:
            self.log_function("bmp280: sensor_test failed: "+ str(type(exception))+ str(exception))

    def speed(self):
        try:
            time_pos_1 = functions.find_time(-2, self.data["bmp280"][3])
            time_1 = self.data["bmp280"][3][time_pos_1]
            time_2 = self.data["bmp280"][3][-1]
            timedif = time_2 - time_1

            alt_1 = self.data["bmp280"][2][time_pos_1]
            alt_2 = self.data["bmp280"][2][-1]
            altdif = alt_2 - alt_1

            v = altdif / timedif
        except:
            v = "NA"
        self.log_function("speed is: " + str(v))
        return v

    def check_if_down(self):
        speed = self.speed()
        try:
            if self.acent_threshold > speed > self.decent_treshold:
                bool = True
            else:
                bool = False
            self.log_function("down is: " + str(bool))
            return bool
        except:
            return "NA"

    def check_if_acent(self):
        speed = self.speed()
        try:
            if self.acent_threshold < speed:
                bool = True
            else:
                bool = False
            self.log_function("acent is: " + str(bool))
            return bool
        except:
            return "NA"

    def check_if_decent(self):
        speed = self.speed()
        try:
            if speed < self.decent_treshold:
                bool = True
            else:
                bool = False
            self.log_function("decent is: " + str(bool))
            return bool
        except:
            return "NA"
