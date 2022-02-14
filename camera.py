import picamera
import time
import functions
import os
import threading
import logging_and_datasaving

class pi_camera():
    def __init__(self, pic_names, directory_name, timestamp_reference, log_function=print):
        self.log_function = log_function
        self.timestamp_reference=timestamp_reference
        self.camera = picamera.PiCamera()
        #self.camera.resolution = resolution
        self.pic_names = pic_names
        self.current_pic_number = 0
        self.format = str(pic_names[pic_names.index(".")+1:])
        self.directory_name = functions.search_for_directory(directory_name)
        os.mkdir(self.directory_name)
        self.thread = threading.Thread(target=self.take_image)



    def take_image(self):
        while self.thread_on==True:
            name = self.directory_name+ "/"+ self.pic_names[:(self.pic_names.index("."))] + str(self.current_pic_number) + "_" + str(functions.actime(self.timestamp_reference))+"." +str(self.format)
            self.current_pic_number += 1
            try:
                self.camera.capture(name , self.format )  
                self.log_function("camera image taken")
            except:
                with open(name +".txt" , "w") as text_file: 
                    text_file.write("An Error occurred")
                self.log_function("camera image error ")



    def start_imaging(self):
        self.thread_on=True
        self.thread.start()
        self.log_function("imaging thread started")
    
    def stop_thread(self):
        self.thread_on=False
        while self.thread.is_alive():
            self.log_function("waiting for imaging_thread to stop")
            time.sleep(0.1)
        self.log_function("imaging thread stopped")

    def close(self):
        self.camera.close()
    
