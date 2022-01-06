#import oled 
#import bmp280
#import IMU
#import camera
import functions
import logging_and_datasaving
import flight

import threading 
import time
import json 
import os 


startuptime=functions.cut_time(time.time())

log = logging_and_datasaving.log(startuptime, "log.txt")
time.sleep(2)
flight.flight(log)

