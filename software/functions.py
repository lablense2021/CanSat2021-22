from time import sleep
import time
import RPi.GPIO as gpio
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
        for entry in self.buzzer_pins:
            gpio.setup(self.buzzer_pins[entry], gpio.OUT)
            gpio.output(self.buzzer_pins[entry], gpio.LOW)

    def signal(self, repetitions=5, duration=0.5, *argv):
        try:
            for i in range(repetitions):

                for entry in argv:
                    gpio.output(self.buzzer_pins[entry], gpio.HIGH)
                sleep(duration)
                for entry in argv:
                    gpio.output(self.buzzer_pins[entry], gpio.LOW)
                sleep(duration)
        except:
            self.log_function("something wrong with signal")


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
    path = name + str(number) + ending
    while pathlib.Path(path).is_file():
        number += 1
        path = name + str(number) + "_" + str(cut_time(time.time())) + ending
    return path


def search_for_directory(directory_name):
    number = 0
    path = directory_name + str(number)
    while pathlib.Path(path).is_dir():
        number += 1
        path = directory_name + str(number) + "_" + str(cut_time(time.time()))
    return path
