#import oled 
#import bmp280
#import IMU
#import camera
import functions
import logging
import flight

import threading 
import time
import json 
import os 


startuptime=functions.cut_time(time.time())

log = logging.log(startuptime, "log.txt")
time.sleep(2)
flight.flight(log)

