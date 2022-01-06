import picamera
import time
import functions
import os
import threading
import logging_and_datasaving

class pi_camera():
    def __init__(self, resolution, pic_names, directory_name, log):
        self.log = log
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.names = pic_names
        self.current_pic_number = 0
        self.type = pic_names[pic_names.index(".")+1:]
        self.directory_name = functions.search_for_directory(directory_name)
        os.makedir(self.directory_name)
        self.thread = threading.Thread(self.take_images)



    def take_image(self):
        while self.thread_on==True:
            name = self.directory_name+ "/"+ self.pic_names + str(self.current_pic_number) + "_" + self.log.get_time_passed("startflighttime")
            self.camera.capture(name , self.type )
            self.current_pic_number += 1


    def start_imaging(self):
        self.log.create_entry("imaging thread started", "startflighttime")
        self.thread_on=True
        self.thread.start()
    
    def stop_thread(self):
        self.log.create_entry("imaging thraed stopped", "startflighttime")
        self.thread_on==False