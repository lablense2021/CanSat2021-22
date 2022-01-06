#import oled 
#import bmp280
#import IMU
#import camera
import functions
import logging


import threading 
import time
import json 
import os 




    
def flight(log):
    log.time_mark("starttimeflight")
    log.create_entry("flight function started")
    time.sleep(3)
    log.create_entry("after 3 seconds flight", "starttimeflight")
    


#setup objects

    

    
