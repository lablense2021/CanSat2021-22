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
            signals.signal(("buzzer", "vibration"), 1, 0.25, )
            menu.change_menu_option(1)

        if presses == 2:
            display.stop_scroll()
            signals.signal(("buzzer", "vibration"), 1, 1, )
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
    camera.start_imaging()
    imu.start_thread()

    display.start_scroll("Waiting for acent!")

    while bmp280.check_if_acent() != True:
        time.sleep(0.0001)
        print("Waiting on acent")


    log.create_entry("now acent", "starttimeflight")



    while bmp280.check_if_decent() != True:
       print("waiting on decent")
    signals.start_thread(("buzzer", "vibration"), 1, 2, )
    reac.start_thread()
    log.create_entry("Now falling", "starttimeflight")
    display.start_scroll("Falling")

    #time.sleep(20)
    while bmp280.check_if_down() != True and button.button_presscounter(3, 2) != 3:
        print("falling")
        time.sleep(0.1)

    camera.stop_thread()
    bmp280.stop_thread()
    reac.stop_thread()
    imu.stop_thread()
    camera.close()
    reac.close()
    data.stop_data_saving()

    log.create_entry("waiting to be found", "starttimeflight")
    display.start_scroll("waiting to be found")

    while button.button_presscounter(2, 2) != 2:
        time.sleep(0.05)

    log.create_entry("found", "starttimeflight")
    display.show_text("Found!!!")
    signals.stop_thread()
    button_open_menu()


if __name__ == "__main__":
    startuptime = functions.cut_time(time.time())

    log = logging_and_datasaving.log(startuptime, "log.txt")
    log.create_entry("main started")
    button = functions.Button(16)
    signals = functions.signal({"buzzer": 1, "vibration": 7})
    signals.signal(("buzzer", "vibration"), 1, 2)
    display = oled.oled(log.create_entry)

    # defining of menu
    options = ["Flight Control Software", "Access CanSat through WLAN", "Shutdown CanSat"]
    when_called = [flight, lambda: read_data.read(button, button_open_menu, log.create_entry, display.start_scroll),
                   functions.shut_down]

    menu = menu(options, when_called, log.create_entry, display.start_scroll)
    button_open_menu()
