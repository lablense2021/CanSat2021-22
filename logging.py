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
        self.time_marks[name]=functions.actime(self.starttime)
        self.create_entry("time mark created: " + name)

    def create_entry(self,entrytext, timein="NA"):
        
        if timein=="NA": #Falls keine Zeit angegeben ist wird functions.actime() vom start des loggings an verwendet
            time = functions.actime(self.starttime)
            entry="\n"+ "(" + str(time)+ ")" + entrytext


        if timein in self.time_marks:
            time = self.time_marks[timein]

            entry="\n"+ "(" + str(time)+" since " + timein +")" + entrytext 
        
        print(entry)
        self.current_log += entry
        with open(self.path, "w") as text_file: #speichern der änderung
            text_file.write(self.current_log)
    

if __name__== "__main__":
    log = log(functions.cut_time(time.time()), "logs.txt")

    time.sleep(3)
    log.create_entry("test entry")



