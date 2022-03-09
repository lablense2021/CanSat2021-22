from matplotlib.font_manager import json_dump, json_load
import functions
import time
import threading
import os
import pathlib
import json

import time
import board
import adafruit_lsm6ds.lsm6ds33
import adafruit_lis3mdl


class imu():
    def __init__(self, data, timestamp_reference, log_function=print):
        self.i2c = board.I2C()
        self.accel_gyro = adafruit_lsm6ds.lsm6ds33.LSM6DS33(self.i2c, 0x6a)
        self.magnetometer = adafruit_lis3mdl.LIS3MDL(self.i2c, 0x1c)
        self.timestamp_reference = timestamp_reference
        self.log_function = log_function
        self.data = data
        self.data["imu"] = [[], [], [], [], [], [], [], [], [], []]
        self.data["imu_test"] = [[], [], [], [], [], [], [], [], []]
        self.thread = threading.Thread(target=lambda: self.data_capture())
        self.calibration_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, ]

    def read_all(self):

        acceleration = self.accel_gyro.acceleration
        gyro = self.accel_gyro.gyro
        magnetic = self.magnetometer.magnetic
        data_raw = [acceleration, gyro, magnetic]
        data = []
        for i in range(len(data_raw)):

            for n in range(len(data_raw[i])):
                data.append(data_raw[i][n] - self.calibration_values[(i) * 3 + n])

        # self.log_function("imu data read"+ str(data))
        return data

    def safe_data(self, data_entry="imu"):
        read_data = self.read_all()
        for i in range(len(read_data)):
            self.data[data_entry][i].append(read_data[i])
        self.data[data_entry][9].append(functions.actime(self.timestamp_reference))

    def print_data(self, data):
        print(
            "Acceleration: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*data[0])
        )
        print("Gyro          X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*data[1]))
        print("Magnetic      X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*data[2]))
        print("")

    def calibrate(self, path):
        if pathlib.Path(path).is_file():
            self.calibration_values = json_load(path)["imu_calibration"]
        else:
            self.data["imu_calibration_values"] = [[], [], [], [], [], [], [], [], [], []]
            for i in range(10000):
                self.safe_data("imu_calibration_values")

            for n in range(len(self.calibration_values)):
                print(n)
                if n < 6:
                    sum = 0
                    for i in self.data["imu_calibration_values"][n]:
                        sum += i
                    if n == 2:
                        self.calibration_values[n] = (sum / len(self.data["imu_calibration_values"][n])) - 9.81
                    else:
                        self.calibration_values[n] = sum / len(self.data["imu_calibration_values"][n])

            json_dump({"imu_calibration": self.calibration_values}, path)
            self.log_function("imu calibration done. values: " + str(self.calibration_values))

    # Thread
    def start_thread(self):
        self.capture_on = True
        self.thread.start()
        self.log_function("imu capture thread started")

    def data_capture(self, data_entry="imu"):
        while self.capture_on == True:
            self.safe_data("imu")
            time.sleep(0.0001)

    def stop_thread(self):
        self.capture_on = False
        self.log_function("imu capture thread stopped")
