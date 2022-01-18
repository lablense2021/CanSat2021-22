import os
import main


def read( button, next_function, log_function=print ):
    log_function("read_mode started")
    os.system("sudo systemctl restart dnsmasq; sudo systemctl restart hostapd")
    while True:
        if button.button_presscounter(2,2):
             break
    next_function()
    
    
