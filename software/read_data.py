import os
import main
import time


def read(button, next_function, log_function=print, display_function=print):
    log_function("read_mode started")
    display_function("WLAN activated")
    os.system("sudo systemctl restart dnsmasq; sudo systemctl restart hostapd")
    while True:
        button_val = button.button_presscounter(2, 2)
        if button_val == 2:
            os.system("sudo systemctl stop hostapd; sudo systemctl stop dnsmasq")
            log_function("WLAN stopped")
            break

        elif button_val == 1:
            log_function("WLAN continued")
            break
        time.sleep(0.1)
    next_function()
