import picamera
import time
import functions
import os
import threading
import logging_and_datasaving


class pi_camera():
    def __init__(self, pic_names, directory_name, timestamp_reference, log_function=print):
        self.log_function = log_function
        self.timestamp_reference = timestamp_reference
        try:
            self.camera = picamera.PiCamera()
            # self.camera.resolution = resolution
        except Exception as exception:
            self.log_function("camera init failed: " + str(type(exception)) + str(exception))
        self.pic_names = pic_names
        self.current_pic_number = 0
        self.format = str(pic_names[pic_names.index(".") + 1:])
        self.directory_name = functions.search_for_directory(directory_name)
        os.mkdir(self.directory_name)
        log_function("image directory created: " + str(self.directory_name))
        self.thread = threading.Thread(target=self.take_image)

    def take_image(self):
        while self.thread_on:
            name = self.directory_name + "/" + self.pic_names[:(self.pic_names.index("."))] + str(
                self.current_pic_number) + "_" + str(functions.actime(self.timestamp_reference)) + "." + str(
                self.format)
            self.current_pic_number += 1
            try:
                self.camera.capture(name, self.format)
                self.log_function("camera image taken")
            except Exception as exception:
                with open(name + ".txt", "w") as text_file:
                    text_file.write("An Error occurred")
                self.log_function("take_image failed: " + str(type(exception)) + str(exception))
            time.sleep(0.05)

    def start_imaging(self):
        try:
            self.thread_on = True
            self.thread.start()
            self.log_function("imaging thread started")
        except Exception as exception:
            self.log_function("start_imaging failed: " +str(type(exception)) + str(exception))


    def stop_thread(self):
        try:
            self.thread_on = False
            start_time = functions.cut_time(time.time())
            while self.thread.is_alive() and functions.cut_time(time.time()) - start_time < 10:
                self.log_function("waiting for imaging_thread to stop")
                time.sleep(0.1)
            self.log_function("imaging thread stopped")
        except Exception as exception:
            self.log_function("stop_thread failed: " + str(type(exception)) + str(exception))

    def close(self):
        try:
            self.camera.close()
        except Exception as exception:
            self.log_function("close camera failed: " + str(type(exception)) + str(exception))




