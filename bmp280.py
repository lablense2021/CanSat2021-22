import functions
import threading
import board
import adafruit_bmp280
import logging_and_datasaving

class bmp280():
    def __init__(self, data,  timestamp_reference,  log_function=print):
        self.log_function =log_function
        self.timestamp_reference= timestamp_reference
        self.data = data
        self.data["bmp280"] = []
        self.data["bmp280_test"] = []
        try:
            i2c = board.I2C()
            self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
        except:
            self.log_function("Error occurred in I2C config")
        self.thread=threading.Thread(target=lambda: self.safe_data("bmp280"))

        
    def read_data(self):
        try:
            temperature = self.sensor.temperature
            pressure = self.sensor.pressure
            altitude = self.sensor.altitude
            data = [temperature, pressure, altitude]
        except:
            data="ErrorOccured"
        self.log_function("bmp280 data read: " + str(data))
        return data

    def safe_data(self, data_entry):
        self.data[data_entry].append([self.read_data(), functions.actime(self.timestamp_reference)])

    def data_capture(self):
        while self.capture_on==True:
            self.safe_data()

    def start_thread(self):
        self.capture_on=True
        self.thread.start()

    def stop_thread(self):
        self.capture_on=False

    def sensor_test(self):
        self.log_function("sensor test started")
        for i in range(20):
            self.safe_data("bmp280_test")




        



    





        