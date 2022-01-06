from time import sleep
import time
#import RPi.GPIO as gpio
import os

import pathlib




#Button
class Button():
    def __init__(self, button_pin):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        self.button_pin = button_pin
        gpio.setup(self.button_pin, gpio.IN)

    def button_presstime(self, cuttime):
        start = actime()
        endtime = start
        while (gpio.input(self.button_pin) == 1) and (endtime - start) < cuttime :
            endtime = actime()

        return endtime - start 

    def button_presscounter(self, ti, cutval):
        presscounter = 0
        prevpress = 0
        if gpio.input(self.button_pin) == 1:
            beginning = actime()
            while actime() - beginning < ti:
                pressed = gpio.input(self.button_pin)
                if prevpress != pressed and pressed == 1 :
                    presscounter += 1
                if presscounter >= cutval:
                    break
                prevpress = pressed
                sleep(0.1)
        return presscounter


#Time
def actime(starttime):
    actime= float(time.time()) - starttime
    return cut_time(actime)

def cut_time(ti):
    return float('{0:.3f}'.format(ti))



#Buzzer
class buzzer():
    def __init__(self, buzzer_pin):
        self.buzzer_pin = buzzer_pin 
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.buzzer_pin, gpio.IN)


    def buzzer(self, repetitions=5, duration=0.5):
        for i in range(repetitions):
            gpio.output(self.buzzer_pin , gpio.HIGH)
            sleep(duration)
            gpio.output(self.buzzer_pin, gpio.LOW)
            sleep(duration)


#OS
def shut_down(data, datapath):
    os.system("sudo shutdown ")


def search_for_filename(path):
    name = path[:path.index(".")]
    ending = path[path.index("."):]
    number= 0
    path = name+str(number)+ending
    while pathlib.Path(path).is_file():
        number += 1
        path = name+ str(number) + ending
    return path

def search_for_directory(directory_name):
    number = 0
    path = directory_name+str(number)
    while pathlib.Path(path).is_file():
        number += 1
        path = directory_name+ str(number)
    return path