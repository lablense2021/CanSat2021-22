from dataclasses import dataclass
import imu
import functions

import time
import RPi.GPIO as GPIO
import numpy as np
import threading


class motor():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        self.motor = GPIO.PWM(13, 50)  # frequency=50Hz

    def rot_right(self, speed):
        GPIO.output(6, GPIO.LOW)
        GPIO.output(5, GPIO.HIGH)

        self.motor.start(speed)

    def rot_left(self, speed):
        GPIO.output(5, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        self.motor.start(speed)

    def rot(self, speed):
        if speed < 0:
            self.rot_right(functions.betrag(speed))

        elif speed > 0:
            self.rot_left(functions.betrag(speed))

        else:
            self.motor.start(0)

    def close_pwm(self):
        self.motor.stop()


class reaction_wheel():
    def __init__(self, current_speed, log_function=print):
        self.log_function = log_function
        self.current_speed = current_speed
        self.motor = motor()
        self.thread = threading.Thread(target=self.control)
        self.thread_on = False

    def control(self):
        val = 0
        while self.thread_on == True:
            correction_val = 0
            try:
                read_val = float(self.current_speed())
            except Exception as exception:
                self.log_function("reaction wheel: read current speed failed " + str(type(exception)) + str(exception))
                read_val = 0

            #print(read_val)

            if functions.betrag(read_val) > 0.1:
                correction_val = (functions.betrag(read_val) / read_val) * ((functions.betrag(read_val) ** 3) + 1)

            val += correction_val
            if val > 100.0:
                val = 100
            elif val < -100.0:
                val = -100

            self.motor.rot(val)
            time.sleep(0.001)

    def start_thread(self):
        self.thread_on = True
        self.thread.start()
        self.log_function("reaction wheel started")

    def stop_thread(self):
        self.thread_on = False
        while self.thread.is_alive():
            print("waiting for reaction_wheel to stop")
            time.sleep(0.1)
        self.motor.rot(0)
        self.log_function("reaction wheel stopped")

    def close(self):
        self.motor.close_pwm()
