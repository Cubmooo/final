import pandas as pd
import datetime
from spellchecker import SpellChecker
from word2number import w2n
import re

class Teacher:
    def __init__(self):
        self.location = None
        self.className = None
        self.classCode = None
        self.day = None
        self.time = None
        self.name = None
        
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
            return
        
        with open("final/teachers.txt") as gh:
            nameIndex = dict([line.strip().split(" ",1) for line in gh])
        name = nameIndex[name]
        self.name = name
    
    def get_current_time(self):
        currentDateAndTime = datetime.datetime.now()
        self.day = currentDateAndTime.strftime("%d/%m/%Y")
        self.dayTime = currentDateAndTime.strftime("%H.%M")
        print(self.day)
        self.get_time()
        
    def add_dayTime(self, dayTime):
        self.dayTime = dayTime
        
    def add_day(self, day):
        self.day = day
           
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
        
        for period,times in bellTimes.items():
            if times[0] <= float(self.dayTime) < times[1]:
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
    def __init__(self):
        self.hasPm = False
        self.hasPeriod = False
        self.time = None
        self.period = None
        self.toOrPastIndex = None
        self.hasTo = False
    
    def add(self, inputedTime):
        self.splitInput = self.num_word_spell_check(inputedTime.split())
        self.splitInput = [word.lower() if type(word) == str else word
                           for word in self.splitInput]
        self.spacelessInput = inputedTime.replace(" ","")
        self.listInput = list(self.spacelessInput)
                
    def num_word_spell_check(self, str):
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
        return str
        
    def num_time(self):
        if "period" in self.splitInput:
            self.hasPeriod = True
        if "pm" in self.splitInput:
            self.hasPm = True
        
        if self.hasPeriod:
            try:
                index = self.splitInput.index("period")
                self.period = int(self.splitInput[index + 1])
                print(self.period)
                return
            except:
                pass
        
        self.intList = [int(num) for num in self.listInput if num.isdigit()]
        self.periodInt = "".join(map(str, self.intList))
        self.periodInt = int(self.periodInt) if self.periodInt else None
        if self.periodInt == None:
            return
        if len(str(self.periodInt)) in [3, 4]:
            self.time = self.periodInt / 100
        elif len(str(self.periodInt)) in [1, 2]:
            self.time = self.periodInt

    def word_time(self):      
        if "to" in self.splitInput:
            self.toOrPastIndex = self.splitInput.index("to")
            self.hasTo = True
        if "past" in self.splitInput:
            self.toOrPastIndex = self.splitInput.index("past")
            
        try:
            minutes = self.splitInput[self.toOrPastIndex - 1]
            hours = self.splitInput[self.toOrPastIndex + 1]
            offset = (-2 * self.hasTo + 1) * minutes - 40 * self.hasTo
            self.time = hours + offset / 100
            return
        except:
            pass
        
        self.splitInput = [int(i) for i in self.splitInput if str(i).isdigit()]
        i = 0
        try:
            while i < len(self.splitInput) - 1:
                if self.splitInput[i] >= 10:
                    self.splitInput[i] += self.splitInput[i + 1]
                    self.splitInput.pop(i + 1)
                else:
                    i += 1
            self.time = float(".".join([str(num) for num in self.splitInput]))
        except:
            pass
        
class Time:
    def __init__(self):
        self.month = None
        self.year = 25
        self.day = None
        self.date = None
        
    def add(self, inputedDay):
        self.dayInput = inputedDay
        self.monthList = self.file_to_dict("final/months.txt")
        self.numbersList = self.file_to_dict("final/numbers.txt")
        
    def file_to_dict(self,filepath):
        with open(filepath, "r") as file:
            return {line.strip(): i + 1 for i, line in enumerate(filepath)}
    
    def spell_check(self, givenList):
        spell = SpellChecker()
        givenList = givenList.split()
        for i, word in enumerate(givenList):
            givenList[i] = spell.correction(word)
        return givenList
              
    def num_day(self):
        self.intDate = [i for i in self.dayInput if i.isdigit()]
        try:
            if len(self.intDate) == 6:
                self.date = int("".join(self.intDate))
            if len(self.intDate) == 4:
                self.date = int("".join(self.intDate) + "25")
            if len(self.intDate) == 1:
                self.day = self.intDate[0]
        except:
            pass
    
    def word_day(self):
        if self.day != None or self.date != None:
            return
        self.dayInput = self.spell_check(self.dayInput)
       
        for i,j in enumerate(self.dayInput):
            if j == "twenty" or j == "thirty":
                self.dayInput[i] = self.dayInput[i] + self.dayInput[i + 1]
                self.dayInput.pop(i + 1)
        
        for i,j in enumerate(self.dayInput):
            self.dayInput[i] = self.monthList.get(j, self.dayInput[i])
            
            if self.month == None and j in self.monthList:
                self.month = self.monthList[j]
                
            if type(j) == str and j.isdigit():
                self.dayInput[i] = int(j)
            
        if self.month in self.dayInput:    
            normalDateFormat = self.dayInput.index(self.month) == 1
        print(self.dayInput)
        if len(self.dayInput) >= 3:
            self.year = self.dayInput[2]
        self.monthDay = self.dayInput[-1 * (normalDateFormat - 1)]
        self.date = self.monthDay * 10000 + self.month * 100 + self.year

def main():
    teacher = Teacher()
    while teacher.name == None:
        teacherInput = input("What teacher would you like to find: ")
        teacher.add(teacherInput)
    teacher.get_current_time()
    teacher.current_position()
    
    print(f"Teacher's Location is {teacher.location}")
    print(f"Teacher's Class is {teacher.className}")
    print(f"Teacher's Class code is {teacher.classCode}")
    
    while True:
        newInfoInput = input("Would you like to pick a different teacher or time: ")
        newInfoInput = sentiment_finder(newInfoInput)
        if newInfoInput == None:
            print("Input again please")
            continue
        break
        
    if newInfoInput == False:
        exit_program()
    
    while teacher.name == None:
        teacherInput = input("What teacher would you like to find: ")
        teacher.add(teacherInput)
        
    period = Period()
    while period.period == None and period.time == None:
        inputedTime = input("What time of day:")
        period.add(inputedTime)
        period.num_time()
        period.word_time()
        print(period.period)
        print(period.time)
        
    time = Time()
    while time.day == None and time.date == None:
        inputedDay = input("What day would you like: ")
        time.add(inputedDay)
        time.num_day()
        time.word_day()
        print(time.date)
        print(time.day)
    
def sentiment_finder(word):
    word = word.replace(" ","")
    
    spell = SpellChecker(language = None)
    spell.word_frequency.load_text_file("final/yes.txt")
    if len(word) <= 3:
        spell.distance = 1
    else:
        spell.distance = 2
    
    if word in spell or spell.candidates(word) != None:
        sentiment = True
    else:
        spell = SpellChecker(language = None)
        spell.word_frequency.load_text_file("final/no.txt")    
        
        if word in spell or spell.candidates(word) != None:
            sentiment = False
        else:
            return None
    
    return sentiment

def exit_program():
    print("Thank you for using this teacher stalking machine\nI hope you found what you needed")
    exit()

if __name__ == "__main__":
    main()