import oled 
import bmp280
import IMU
import camera
import functions
import logging_and_datasaving

import read_data

import threading 
import time
import json 
import os 
import oled

class menu():
    def __init__(self, options, when_called, log_function, display_function=print): #display_function specifies the funtion which shows the options 
        self.log_function=log_function
        self.display_function=display_function
        self.pos=0
        self.options=options
        self.when_called=when_called
        self.display_function(str(self.options[self.pos]))
        self.log_function("menu created")


    def change_menu_option(self, hops=1): 
        self.pos=(self.pos+hops)%len(self.options)
        self.display_function(str(self.options[self.pos]))
        self.log_function("changed menu option to" + str(self.options[self.pos]))

    def choose_option(self):
        print(self.pos)
        self.when_called[self.pos]()
        

def button_open_menu():
    log.create_entry("menu opened with option " + str(menu.options[menu.pos]))
    while True:
        presses = button.button_presscounter(1, 2)
        if presses==1:
            menu.change_menu_option(1)

        if presses==2:
            menu.choose_option()
            break


def flight():
    import bmp280
    import camera
    log.time_mark("starttimeflight")
    log.create_entry("flight function started")
    data = logging_and_datasaving.flight_data_dictionnary(("flightdata.json"), (log.time_marks["log_start"]) ,(lambda x: log.create_entry(x, "starttimeflight" )))
    data.start_data_saving()
    bmp280 = bmp280.bmp280(data.data, log.time_marks["starttimeflight"], lambda entry : log.create_entry(entry, "starttimeflight"))
    #camera = camera.pi_camera()
    

    bmp280.sensor_test()
    data.stop_data_saving()
    print(data.data)
    button_open_menu()


    



if __name__ == "__main__":
    startuptime=functions.cut_time(time.time())

    log = logging_and_datasaving.log(startuptime, "log.txt")
    log.create_entry("main started")
    button = functions.Button(16)
    display = oled.oled()


    #defining of menu 
    options = ["Flight Control Software", "Acces CanSat through WLAN", "Shutdown CanSat"]
    when_called= [flight, lambda: read_data.read(button, button_open_menu, log.create_entry), functions.shut_down]
    
    menu = menu(options, when_called, log.create_entry, display.show_text)
    button_open_menu()
    
    



    
    
    

   




