import functions
import time
import threading

import time
import board
import adafruit_lsm6ds.lsm6ds33 
import adafruit_lis3mdl 

class imu():
    def __init__(self, data, timestamp_reference,  log_function=print):
        self.i2c = board.I2C() 
        self.accel_gyro = adafruit_lsm6ds.lsm6ds33.LSM6DS33(self.i2c, 0x6a)
        self.magnetometer = adafruit_lis3mdl.LIS3MDL(self.i2c, 0x1c)
        self.timestamp_reference=timestamp_reference
        self.log_function=log_function
        self.data = data
        self.data["imu"]=[[],[],[],[],[],[],[],[],[]]
        self.data["imu_test"]=[[],[],[],[],[],[],[],[],[]]
        self.thread=threading.Thread(target=self.data_capture("imu"))
        

    def read_all(self):
        
        acceleration = self.accel_gyro.acceleration
        gyro = self.accel_gyro.gyro
        magnetic = self.magnetometer.magnetic
        data=[acceleration, gyro, magnetic]
        #self.log_function("imu data read"+ str(data))
        return data


    def safe_data(self,data_entry):
        self.data[data_entry][0].append(self.read_all()[0][0])
        self.data[data_entry][1].append(self.read_all()[0][1])
        self.data[data_entry][2].append(self.read_all()[0][2])
        self.data[data_entry][3].append(self.read_all()[1][0])
        self.data[data_entry][4].append(self.read_all()[1][1])
        self.data[data_entry][5].append(self.read_all()[1][2])
        self.data[data_entry][6].append(self.read_all()[2][0])
        self.data[data_entry][7].append(self.read_all()[2][1])
        self.data[data_entry][8].append(self.read_all()[2][2])
        self.data[data_entry][9].append(functions.actime(self.timestamp_reference))


    def print_data(self, data):
            print(
                "Acceleration: X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} m/s^2".format(*data[0])
            )
            print("Gyro          X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} rad/s".format(*data[1]))
            print("Magnetic      X:{0:7.2f}, Y:{1:7.2f}, Z:{2:7.2f} uT".format(*data[2]))
            print("")
            
    #Thread
    def start_thread(self):
        self.capture_on=True
        self.thread.start()
        self.log_function("imu capture thread started")

    def data_capture(self,data_entry):
        while self.capture_on==True:
            self.safe_data(data_entry)
            time.sleep(0.1)

   

    def stop_thread(self):
        self.capture_on=False
        self.log_function("imu capture thread stopped")
