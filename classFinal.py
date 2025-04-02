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

class Period:
    def __init__(self, inputedTime):
        self.splitInput = self.num_word_spell_check(inputedTime.split(" "))
        self.spacelessInput = inputedTime.replace(" ","").lower()
        self.listInput = list(self.spacelessInput)
        self.hasPm = False
        self.hasPeriod = False
        self.time = None
        self.period = None
        self.toOrPastIndex = None
        self.hasPast = None
        
    def spell_check(str):
        spell = SpellChecker()
        for i,word in enumerate(str):
            if word not in spell:
                str[i] = spell.correction(word)
                
    def num_word_spell_check(str):
        spell = SpellChecker()
        for i,word in enumerate(str):
            if word not in spell:
                str[i] = spell.correction(word)
            if word == "quarter":
                str[i] = 15
            if word == "half":
                str[i] = 30
            try:
                str[i] = w2n.word_to_num(word)
            except:
                pass
        
    def num_time(self):
        if "period" in self.spacelessInput:
            self.hasPeriod = True
        if "pm" in self.spacelessInput:
            self.hasPm = True
        
        if self.hasPeriod:
            try:
                index = self.splitInput.index("period")
                self.period = int(self.splitInput[index + 1])
                return
            except:
                pass
        
        self.intList = [int(num) for num in self.listInput if num.isdigit()]
        self.periodInt = "".join(self.intList)
        if len(str(self.periodInt)) == (3 or 4):
            self.time = self.periodInt / 100
        elif len(str(self.periodInt)) == (1 or 2):
            self.time = self.periodInt

    def word_time(self):
        if "to" in self.splitInput:
            self.toOrPastIndex = self.splitInput.index("to")
            self.hasPast = True
        if "past" in self.splitInput:
            self.toOrPastIndex = self.splitInput.index("past")
            
        try:
            minutes = self.splitInput[self.toOrPastIndex - 1]
            hours = self.splitInput[self.toOrPastIndex + 1]
            self.time = hours + (2 * self.hasPast - 1) * minutes / 100
            return
        except:
            pass
        
        self.splitInput = [int(i) for i in self.splitInput if i.isdigit()]
class Time:
    def __init__(self):
        pass
    


def main():
    pass
if __name__ == "__main__":
    main()