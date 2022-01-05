from time import sleep
import time
#import RPi.GPIO as gpio
import os

import pathlib



#GPIO setup
def gpio_setup():

    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)

    BUZZER = 23
    gpio.setup(BUZZER, gpio.OUT)

    BUTTON = 6
    gpio.setup(BUTTON, gpio.IN)




#Button
def button_presstime(cuttime, button_pin):
    start = actime()
    endtime = start

    while (gpio.input(button_pin) == 1) and (endtime - start) < cuttime :
        endtime = actime()

    return endtime - start 

def button_presscounter(ti, cutval, button_pin):
    presscounter = 0
    prevpress = 0
    if gpio.input(button_pin) == 1:
        beginning = actime()
        while actime() - beginning < ti:
            pressed = gpio.input(button_pin)
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
def buzzer(repetitions=5, duration=0.5):
    for i in range(repetitions):
        gpio.output(BUZZER, gpio.HIGH)
        sleep(duration)
        gpio.output(BUZZER, gpio.LOW)
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