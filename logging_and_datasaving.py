import time

from matplotlib.font_manager import json_dump 
import functions
import threading
import json

"""
class time_mark(): #Zeitmarken von denen an die zeit gemessen werden kann
            def __init__(self, log):
                self.time = functions.actime(log.starttime)
                self.log= log
                log.create_entry("time mark created: " + str(self))"""


class log():
    def __init__(self, starttime, filename):
        self.starttime=starttime
        self.path=functions.search_for_filename(filename)
        self.current_log=""
        self.time_marks={"log_start":self.starttime}
        self.create_entry("starttime: "+ str(self.starttime))
        self.create_entry("log_started")


    def time_mark(self, name):
        self.time_marks[name]=functions.cut_time(time.time())
        self.create_entry("time mark created: " + name)

    def get_time_passed(self, timein="log_start"):
       
        timeout = functions.actime(self.time_marks[timein])
        return timeout


    def create_entry(self,entrytext, timemark="log_start"):
        
        entry="\n"+ "(" + str(self.get_time_passed(timemark)) + " since " + str(timemark) + ")" + str(entrytext)
        
        print(entry)
        self.current_log += entry
        with open(self.path, "w") as text_file: #speichern der änderung
            text_file.write(self.current_log)
    

class flight_data_dictionnary():
    def __init__(self, filename, timestamp_reference, logging_function=print):
        self.path = functions.search_for_filename(filename)
        self.logging_function= logging_function
        self.logging_function("created flight_data_dictionnary")
        self.timestamp_reference=timestamp_reference
        self.data = {"info_about_dictionnary(time since timestamp) ":str(functions.actime(self.timestamp_reference))}
        self.savingthread=threading.Thread(target=self.data_saving)

    def save_data(self):
        self.logging_function("data saved", "starttimeflight")
        json_dump(self.data, self.path)

    def data_saving(self):
        while self.saving==True:
            self.save_data()
            time.sleep(5)
    
    def start_data_saving(self):
        self.logging_function("started data saving","starttimeflight")
        self.saving=True
        self.savingthread.start()
        

    def stop_data_saving(self):
        self.logging_function("stopped data saving","starttimeflight")
        self.saving=False



    

    


    



if __name__== "__main__":
    log = log(functions.cut_time(time.time()), "logs.txt")

    time.sleep(3)
    log.create_entry("test entry")



