from time import sleep
import time
import RPi.GPIO as gpio
import threading
import os

import pathlib


# Button
class Button():
    def __init__(self, button_pin):
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        self.button_pin = button_pin
        gpio.setup(self.button_pin, gpio.IN)

    def button_presstime(self, cuttime):
        start = actime()
        endtime = start
        while (gpio.input(self.button_pin) == 1) and (endtime - start) < cuttime:
            endtime = actime()

        return endtime - start

    def button_presscounter(self, ti, cutval):
        presscounter = 0
        prevpress = 0
        if gpio.input(self.button_pin) == 1:
            beginning = cut_time(time.time())
            while cut_time(time.time()) - beginning < ti:
                pressed = gpio.input(self.button_pin)
                if prevpress != pressed and pressed == 1:
                    presscounter += 1
                if presscounter >= cutval:
                    break
                prevpress = pressed
                sleep(0.1)
        return presscounter


# Time
def actime(starttime):
    actime = float(time.time()) - starttime
    return cut_time(actime)


def cut_time(ti):
    return float('{0:.3f}'.format(ti))


# maths
def betrag(inp):
    return (inp ** 2) ** 0.5


# Buzzer
class signal():
    def __init__(self, buzzer_pins, log_function=print):
        self.log_function = log_function
        self.buzzer_pins = buzzer_pins
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        self.signal_thread_active = False
        for entry in self.buzzer_pins:
            gpio.setup(self.buzzer_pins[entry], gpio.OUT)
            gpio.output(self.buzzer_pins[entry], gpio.LOW)

    def signal(self, signal_types, repetitions=5, duration=0.5):

        #try:
        for i in range(repetitions):

                for entry in signal_types:
                    gpio.output(self.buzzer_pins[entry], gpio.HIGH)
                sleep(duration)
                for entry in signal_types:
                    gpio.output(self.buzzer_pins[entry], gpio.LOW)
                sleep(duration)
        #except:
            #self.log_function("something wrong with signal: ", str(signal_types), str(repetitions), str(duration),)

    def signal_thread_function(self, signal_types, repetitions=5, duration=0.5, ):
        while self.signal_thread_active == True:
            self.signal(signal_types, repetitions, duration)
            time.sleep(0.01)

    def start_thread(self, signal_types, repetitions=5, duration=0.5, ):
        self.thread = threading.Thread(
            target=lambda: self.signal_thread_function(signal_types, repetitions, duration, ))
        self.signal_thread_active = True
        self.thread.start()

    def stop_thread(self):
        self.signal_thread_active = False
        try:
            while self.thread.is_alive() == True:
                time.sleep(0.1)
        except:
            self.log_function("failed to stop, signal doesn´t exist")


def find_time(search, time):
    ac_pos = -1
    try:
        while time[ac_pos] - time[-1] > search:
            ac_pos -= 1
        if (time[-1] + search) - time[ac_pos + 1] > time[ac_pos] - (time[-1] + search):
            ac_pos += 1

        return ac_pos
    except IndexError:
        return False


# OS
def shut_down(log_function=print):
    log_function("shutdown called")
    # os.system("sudo shutdown now")


def search_for_filename(path):
    name = path[:path.index(".")]
    ending = path[path.index("."):]
    number = 0
    path = name + str(number)
    while len(list(pathlib.Path("./").glob(path+"*"))) != 0:
        number += 1
        path = name + str(number)
    return str(path+"_" + str(cut_time(time.time())) + ending)


def search_for_directory(directory_name):
    number = 0
    path = directory_name + str(number)
    while len(list(pathlib.Path("./").glob(path+"*"))) != 0:
        number += 1
        path = directory_name + str(number)
    return str(path + "_" + str(cut_time(time.time())))
