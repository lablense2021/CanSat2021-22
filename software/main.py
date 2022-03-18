import oled
import bmp280
import imu
import camera
import functions
import logging_and_datasaving
import reaction_wheel_control

import read_data

import threading
import time
import json
import os
import oled


class menu():
    def __init__(self, options, when_called, log_function,
                 display_function=print):  # display_function specifies the funtion which shows the options
        self.log_function = log_function
        self.display_function = display_function
        self.pos = 0
        self.options = options
        self.when_called = when_called
        self.log_function("menu created")

    def show_option(self):
        self.display_function(str(self.options[self.pos]))

    def change_menu_option(self, hops=1):
        self.pos = (self.pos + hops) % len(self.options)
        self.show_option()
        self.log_function("changed menu option to" + str(self.options[self.pos]))

    def choose_option(self):
        self.when_called[self.pos]()


def button_open_menu():
    log.create_entry("menu opened with option " + str(menu.options[menu.pos]))
    menu.show_option()
    while True:
        presses = button.button_presscounter(1, 2)
        if presses == 1:
            signals.signal(1, 0.5, "buzzer", "vibration")
            menu.change_menu_option(1)

        if presses == 2:
            display.stop_scroll()
            signals.signal(1, 2, "buzzer", "vibration")
            menu.choose_option()
            break
        time.sleep(0.1)


def flight():
    # init
    import bmp280
    import camera
    import imu
    display.show_text("On Flight!")
    log.time_mark("starttimeflight")
    log.create_entry("flight function started")
    data = logging_and_datasaving.flight_data_dictionnary(("flightdata.json"), (log.time_marks["log_start"]),
                                                          (lambda x: log.create_entry(x, "starttimeflight")))
    data.start_data_saving()
    bmp280 = bmp280.bmp280(data.data, log.time_marks["starttimeflight"],
                           lambda entry: log.create_entry(entry, "starttimeflight"))
    bmp280.calibrate_altitude()
    camera = camera.pi_camera("img.png", "images", log.time_marks["starttimeflight"],
                              lambda entry: log.create_entry(entry, "starttimeflight"))
    imu = imu.imu(data.data, log.time_marks["starttimeflight"],
                  lambda entry: log.create_entry(entry, "starttimeflight"))
    imu.calibrate("calibration.json")
    reac = reaction_wheel_control.reaction_wheel(lambda: data.data["imu"][5][-1],
                                                 lambda entry: log.create_entry(entry, "starttimeflight"))
    bmp280.start_thread()
    """while bmp280.check_if_acent() != True:
        print("Waiting on acent")main.py
    
    while bmp280.check_if_decent() != True:
       print("waiting on decent")"""

    camera.start_imaging()
    imu.start_thread()
    reac.start_thread()

    log.create_entry("Now falling", "starttimeflight")
    display.start_scroll("Falling")
    while bmp280.check_if_down() != True or button.button_presscounter(3, 2) != True:
        print("falling")
        time.sleep(0.1)

    camera.stop_thread()
    bmp280.stop_thread()
    reac.stop_thread()
    imu.stop_thread()
    camera.close()

    data.stop_data_saving()
    display.close_oled()

    button_open_menu()


if __name__ == "__main__":
    startuptime = functions.cut_time(time.time())

    log = logging_and_datasaving.log(startuptime, "log.txt")
    log.create_entry("main started")
    button = functions.Button(16)
    signals = functions.signal({"buzzer": 1, "vibration": 7})

    display = oled.oled()

    # defining of menu
    options = ["Flight Control Software", "Acces CanSat through WLAN", "Shutdown CanSat"]
    when_called = [flight, lambda: read_data.read(button, button_open_menu, log.create_entry, display.start_scroll),
                   functions.shut_down]

    menu = menu(options, when_called, log.create_entry, display.start_scroll)
    button_open_menu()