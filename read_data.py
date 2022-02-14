import os
import main
import time


def read( button, next_function, log_function=print, display_function=print):
    log_function("read_mode started")
    display_function("WLAN activated")
    os.system("sudo systemctl restart dnsmasq; sudo systemctl restart hostapd")
    while True:
        if button.button_presscounter(2,2)==2:
             break
        time.sleep(0.1)
    next_function()
    
    
