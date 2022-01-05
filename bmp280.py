import functions
import threading
#import board
#import adafruit_bmp280
import logging

class bmp280():
    def __init__(self, pin, log, data):
        self.pin = pin
        self.log =log
        self.data = data
        
        i2c = board.I2C()
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        
    def read_data(self):
        temperature = sensor.temperature
        pressure = sensor.pressure
        altitude = sensor.altitude
        data = [temperature, pressure, altitude]
        self.log.create_entry("bmp280 data read: " + str(data))
        return data

    #def safe_data:

        



    





        