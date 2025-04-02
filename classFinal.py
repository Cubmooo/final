import pandas as pd
import datetime
from spellchecker import SpellChecker
from word2number import w2n
import re

class Teacher:
    def __innit__(self):
            self.location = None
            self.className = None
            self.classCode = None
            self.day = None
            self.time = None
        
    def add(self, name):
        name = name.replace(" ","")
        teacherList=[]
        teachers = open("final/teachers.txt", "r")
        for i in teachers:
            teacherList.append(i.split(" ",1)[0])

        spell = SpellChecker(language = None)
        spell.word_frequency.load_words(teacherList)
        
        name = spell.correction(name)
        if name == None:
            self.name = name
            return 0
        
        with open("final/teachers.txt") as gh:
            nameIndex = dict([line.strip().split(" ",1) for line in gh])
        name = nameIndex[name]
        self.name = name
        
    def get_time(self):
        bellTimes={
        "Before School" : [00.00,8.40],
        "Morning Tutor":[8.40,8.50],
        "Period 1" : [8.50,9.40],
        "Period 2" : [9.40,10.30],
        "Period 3" : [10.50,11.40],
        "Period 4" : [11.40,12.30],
        "ETT" : [12.30,13.00],
        "Lunch" : [13.00,13.50],
        "Period 5" : [13.50,14.40],
        "Period 6" : [14.40,15.30],
        "After School" : [15.30,24.00],                 
        }
        
        currentDateAndTime = datetime.datetime.now()
        self.day = currentDateAndTime.strftime("%d/%m/%Y")
        time = currentDateAndTime.strftime("%H.%M")
        
        for period,times in bellTimes.items():
            if times[0] <= float(time) < times[1]:
                self.time = period
                
        schoolCalender = pd.read_csv('final/school_calender.csv')
        for _,row in schoolCalender.iterrows():
            if row["start_date"] == self.day:
                self.day = row["name"][5:]
    
        
    def current_position(self):
        timetable = pd.read_csv(self.name)
        if self.day != "No School" and self.time not in ["Before School", "After School"]:
            try:
                periodIloc = timetable.index[timetable.iloc[:,0] == self.time][0]
            except:
                return
            dayIloc = timetable.columns.get_loc(self.day)
            teacherDetails = timetable.iloc[periodIloc:periodIloc+3,dayIloc].tolist()
        
            self.className = teacherDetails[0]
            self.classCode = teacherDetails[1]
            self.location = teacherDetails[2]
def main():
    pass
if __name__ == "__main__":
    main()