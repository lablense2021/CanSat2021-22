import time
import RPi.GPIO as GPIO
import numpy as np

import imu
import functions

#class reaction_wheel():

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

p = GPIO.PWM(13, 50)  # frequency=50Hz


def rot_right(pwm):
   
    GPIO.output(6, GPIO.LOW)
    GPIO.output(5, GPIO.HIGH)
   
    p.start(pwm)
    

def rot_left(pwm):
  
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    p.start(pwm)

def betrag(inp):
    return (inp**2)**0.5


def rot(val):
    if val<0:
        rot_right(betrag(val))

    elif val>0:
        rot_left(betrag(val))

    else:
        p.start(0)
    

data={}

imu = imu.imu(data, functions.cut_time(time.time()))

def run():
    val=0
    imu.safe_data()
    failure_sum=0
    imu.safe_data()
    for i in range(4000):
        read = imu.read_all()
        read_val = read[1][2]
        failure_sum += read_val
        
    failure= failure_sum/4000
    print("failure: " + str(failure))
    time.sleep(2)
    
    read_vals=0
    for i in range(5000):
        correction_val=0
        read = imu.read_all()
        u_read_val = read[1][2]
        read_val = u_read_val-failure
        imu.safe_data()
        print(read_val)
        read_vals += read_val
       
        
        if betrag(read_val)>0.25:
            correction_val=(betrag(read_val)/read_val)*(5+betrag(read_val)*5)
            print(correction_val)

        
        val = val + correction_val
        if val>99.9999:
            val=100
        

       
            
        print(val)
        rot(val)    
        
        
    
    

    read_vals=read_vals/5000
    print("Read_vals")
    print(read_vals)
        
        

run()

