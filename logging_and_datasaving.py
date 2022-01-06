import time 

import functions

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
        self.time_marks={}
        self.create_entry("starttime: "+ str(self.starttime))
        self.create_entry("log_started")

    def time_mark(self, name):
        self.time_marks[name]=functions.cut_time(time.time())
        self.create_entry("time mark created: " + name)

    def get_time_passed(self, timein="log_start"):
       
        if timein in self.time_marks:
            time = functions.actime(self.time_marks[timein])

        else : #Falls keine Zeit angegeben ist wird functions.actime() vom start des loggings an verwendet
            time = functions.actime(self.starttime)
        
        return time


    def create_entry(self,entrytext, timemark="log_start"):
        
        entry="\n"+ "(" + str(self.get_time_passed(timemark)) + " since " + timemark + ")" + entrytext 
        
        print(entry)
        self.current_log += entry
        with open(self.path, "w") as text_file: #speichern der änderung
            text_file.write(self.current_log)
    

class flight_data_dictionnary():
    def __init__(self, filename, log):
        self.path = functions.search_for_filename(filename)
        self.log = log 
        self.log.create_entry("created flight_data_dictionnary")
        self.data = {"info_about_dictionnary "+ str(log.get_time_passed())}

    def create_data_class(self, name):
        self.data[name]=[]
        



if __name__== "__main__":
    log = log(functions.cut_time(time.time()), "logs.txt")

    time.sleep(3)
    log.create_entry("test entry")



