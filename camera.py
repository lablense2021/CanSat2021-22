import picamera
import time
import functions
import os
import threading
import logging_and_datasaving

class pi_camera():
    def __init__(self, resolution, pic_names, directory_name, timestamp_reference, log_function):
        self.log_function = log_function
        self.timestamp_reference=timestamp_reference
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.names = pic_names
        self.current_pic_number = 0
        self.type = pic_names[pic_names.index(".")+1:]
        self.directory_name = functions.search_for_directory(directory_name)
        os.makedir(self.directory_name)
        self.thread = threading.Thread(self.take_image)



    def take_image(self):
        while self.thread_on==True:
            name = self.directory_name+ "/"+ self.pic_names + str(self.current_pic_number) + "_" + time.time(self.timestamp_reference)
            self.current_pic_number += 1
            try:
                self.camera.capture(name , self.type )   
            except:
                with open(name +".txt" , "w") as text_file: 
                    text_file.write("An Error occurred")


    def start_imaging(self):
        self.log_function("imaging thread started")
        self.thread_on=True
        self.thread.start()
    
    def stop_thread(self):
        self.log_function("imaging thread stopped")
        self.thread_on==False
