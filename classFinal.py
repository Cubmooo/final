from datetime import datetime

import pandas as pd
from spellchecker import SpellChecker
from word2number import w2n


# The teacher class handles finding the teachers name and locating them
class Teacher:
    def __init__(self):
        self.location = None
        self.className = None
        self.classCode = None
        self.day = None
        self.time = None
        self.name = None
    
    # Find and store the name in the users input  
    def add(self, name):
        # Create list of teachers names and make input case insensitive
        name = name.replace(" ","").lower()
        teacherList=[]
        teachers = open("final/teachers.txt", "r")
        for i in teachers:
            teacherList.append(i.split(" ",1)[0])

        # Define spell checker
        spell = SpellChecker(language = None, distance=2)
        spell.word_frequency.load_words(teacherList)

        # Correct input and check that the user has inputted a name
        fixedName = spell.correction(name)
        name = fixedName if (name != fixedName) or (name in spell) else None
        if name == None:
            self.name = name
            return
        
        # turns list of teachers into a dict then finds filepath
        with open("final/teachers.txt") as gh:
            nameIndex = dict([line.strip().split(" ",1) for line in gh])
        name = nameIndex[name]
        self.name = name
    
    def get_current_time(self):
        # finds and formats the current time
        currentDateAndTime = datetime.now()
        self.day = currentDateAndTime.strftime("%d/%m/%Y")
        self.dayTime = currentDateAndTime.strftime("%H.%M")
        
        # calls the functions to find school period and days
        self.get_period()
        self.get_day()
        
    def add_day_time(self, dayTime):
        # defines the inputted time as a attribute of Teacher
        self.dayTime = dayTime
        
    def add_time(self, time):
        # defines the inputted period as a attribute of Teacher
        self.time = "Period " + str(time)
        
    def add_day(self, date):
        # defines the inputted date as a attribute of Teacher
        self.day = date
    
    # Finds the period in which any time sits
    def get_period(self):
        # Defines list of periods and there times
        bellTimes={
        "Before School" : [00.00, 8.40],
        "Morning Tutor":[8.40, 8.50],
        "Period 1" : [8.50, 9.40],
        "Period 2" : [9.40, 10.30],
        "Period 3" : [10.50, 11.40],
        "Period 4" : [11.40, 12.30],
        "ETT" : [12.30, 13.00],
        "Lunch" : [13.00, 13.50],
        "Period 5" : [13.50, 14.40],
        "Period 6" : [14.40, 15.30],
        "After School" : [15.30, 24.00],                 
        }
        
        # compares time to the period time to find correct period
        for period,times in bellTimes.items():
            if times[0] <= float(self.dayTime) < times[1]:
                self.time = period
    
    # Finds the school day for the given date           
    def get_day(self):
        # Defines calender
        schoolCalender = pd.read_csv("final/school_calender.csv")
        
        # iterates through the calender to find the correct school day
        for _,row in schoolCalender.iterrows():
            if row["start_date"] == self.day:
                self.day = row["name"][5:]
    
    # finds current position based on school day and period       
    def current_position(self):
        timetable = pd.read_csv(self.name)
        
        # checks that it is within school hours
        if ((self.day != "No School") and
                (self.time not in ["Before School", "After School"])):
            try:
                # finds the position of the information on the table
                loc = timetable.iloc[:, 0] == self.time
                periodIloc = timetable.index[loc][0]  
            except:
                return
            
            # find the correct information based on its location
            if self.day in timetable.columns:
                dayIloc = timetable.columns.get_loc(self.day)
                self.info = timetable.iloc[periodIloc:periodIloc + 3, dayIloc]

                # Store the location information
                self.className = self.info.tolist()[0]
                self.classCode = self.info.tolist()[1]
                self.location = self.info.tolist()[2]


class Period:
    def __init__(self):
        self.hasPm = False
        self.hasAm = False
        self.hasPeriod = False
        self.time = None
        self.period = None
        self.toOrPastIndex = None
        self.hasTo = False
    
    # Store the users time input as various attributes
    def add(self, inputedTime):
        # stores input as spell corrected and caps in-sensitive 
        self.splitInput = self.num_word_spell_check(inputedTime.split())
        self.splitInput = [word.lower() if isinstance(word, str) else word
                           for word in self.splitInput]
        self.spacelessInput = inputedTime.replace(" ","")
        self.listInput = list(self.spacelessInput)
                
    def num_word_spell_check(self, str):
        # iterates through the inputs
        spell = SpellChecker()
        for i,word in enumerate(str):
            # Corrects the spelling of the input
            if word not in spell:
                str[i] = spell.correction(word)
            # Replaces all written out numbers with intergers
            if word == "quarter":
                str[i] = 15
            if word == "half":
                str[i] = 30
            try:
                str[i] = w2n.word_to_num(word)
            except:
                pass
        return str
    
    # find the time if written in a hour minute format    
    def num_time(self):
        # Checks if time is inputed as a period or am or pm are present
        if "period" in self.splitInput:
            self.hasPeriod = True
        if "pm" in self.splitInput:
            self.hasPm = True
        if "am" in self.splitInput:
            self.hasAm = True
        
        # Returns the time as a period if the time is given as a period
        if self.hasPeriod:
            try:
                index = self.splitInput.index("period")
                self.period = int(self.splitInput[index + 1])
                return
            except:
                pass
        
        # remove all words from the inputted time
        self.intList = [int(num) for num in self.listInput if num.isdigit()]
        self.periodInt = "".join(map(str, self.intList))
        self.periodInt = int(self.periodInt) if self.periodInt else None
        
        # return if no time present
        if self.periodInt == None:
            return
        # return the time either in hours or hours and minutes
        if len(str(self.periodInt)) in [3, 4]:
            self.time = (self.periodInt/100)
        elif len(str(self.periodInt)) in [1, 2]:
            self.time = self.periodInt

    def word_time(self):
        # find the location of the words to and past if present
        if "to" in self.splitInput:
            self.toOrPastIndex = self.splitInput.index("to")
            self.hasTo = True
        if "past" in self.splitInput:
            self.toOrPastIndex = self.splitInput.index("past")
        
        # Finds the time based on the location found earlier
        try:
            minutes = self.splitInput[self.toOrPastIndex - 1]
            hours = self.splitInput[self.toOrPastIndex + 1]
            offset = (-2 * self.hasTo + 1) * minutes - 40 * self.hasTo
            self.time = hours + offset / 100
            return
        except:
            pass
        
        # remove all words from input
        self.splitInput = [int(i) for i in self.splitInput
                           if str(i).isdigit()]
        i = 0
        """iterate through list combining all numbers larger then 10
        with there next number e.g. 40, 5 become 45"""
        try:
            while i < len(self.splitInput) - 1:
                if self.splitInput[i] >= 10:
                    self.splitInput[i] += self.splitInput[i + 1]
                    self.splitInput.pop(i + 1)
                else:
                    i += 1
            # return final time
            self.time = float(".".join([str(num) for num in self.splitInput]))
        except:
            pass

    # converts 12 hour time to 24 hour time
    def add_pm(self, time):
        if (self.hasPm == True) and (time < 12):
            time += 12
        # automaticaly assumes school hours unless otherwise stated
        elif (self.hasAm != True) and (time < 6):
            time += 12
        return time


class Time:
    def __init__(self):
        self.month = None
        self.year = 25
        self.day = None
        self.date = None
        self.monthList = self.file_to_dict("final/months.txt")
        self.numbersList = self.file_to_dict("final/numbers.txt")
    
    # store inputed day as a attribute or Time    
    def add(self, inputedDay):
        self.dayInput = inputedDay
    
    # takes a file of nums or months and creates dict with same ints    
    def file_to_dict(self, filepath):
        with open(filepath, "r") as file:
            return {line.strip(): i + 1 for i, line in enumerate(file)}
    
    # iterate through word in list spell checking it
    def spell_check(self, givenList):
        spell = SpellChecker()
        givenList = givenList.split()
        for i, word in enumerate(givenList):
            givenList[i] = spell.correction(word)
        return givenList
    
    # finds the date or period if given in digits          
    def num_day(self):
        # remove all words from list
        self.intDate = [i for i in self.dayInput if i.isdigit()]
        try:
            # return the date if the inputted date is of the right length
            if len(self.intDate) == 6:
                self.date = int("".join(self.intDate))
            if len(self.intDate) == 4:
                self.date = int("".join(self.intDate) + "25")
            # return the period if the input is one digit long
            if len(self.intDate) == 1:
                self.day = self.intDate[0]
        except:
            pass
    
    # Finds the date if it is inputed in words
    def word_day(self):
        # ensure this function isnt run unnecessarily 
        if self.day != None or self.date != None:
            return
        # spell check input
        self.dayInput = self.spell_check(self.dayInput)
       
        # make all two words numbers one e.g. twenty one -> twentyone
        for i,j in enumerate(self.dayInput):
            if j == "twenty" or j == "thirty":
                self.dayInput[i] = self.dayInput[i] + self.dayInput[i + 1]
                self.dayInput.pop(i + 1)
        
        # replace all months and numbers with ints
        for i,j in enumerate(self.dayInput):
            self.dayInput[i] = self.monthList.get(j, self.dayInput[i])
            self.dayInput[i] = self.numbersList.get(j, self.dayInput[i])
            
            # store the month to know date format
            if (self.month == None) and (j in self.monthList):
                self.month = self.monthList[j]
            
            # replace all typed digits with ints    
            if isinstance(j, str) and j.isdigit():
                self.dayInput[i] = int(j)
        
        # coverts all items of list into ints
        self.dayInput = [
            int(num) for num in self.dayInput if isinstance(num, int)
            or (isinstance(num, str) and  num.isdigit())
        ]
        
        # Finds the location of the month in the date
        if self.month in self.dayInput:    
            normalDateFormat = self.dayInput.index(self.month) == 1

        # truncates the year if it is stated
        if len(self.dayInput) >= 3:
            self.year = self.dayInput[2]
        # return date ensuring correct formating is used
        if normalDateFormat != None:
            self.monthDay = self.dayInput[-1 * (normalDateFormat - 1)]
            self.date = self.monthDay * 10000 + self.month * 100 + self.year


def main():
    # creates teacher object then ask for teacher location
    teacher = Teacher()
    ask_teacher(teacher)
    # Get and displaycurrent position of teacher
    teacher.get_current_time()
    teacher.current_position()
    display_teacher(teacher)
    
    # ask if they wish to input another teacher
    ask_continue()
    
    # Remove old teacher and ask for new one
    teacher.name = None
    ask_teacher(teacher)
    
    # create period object and user for what period they want.    
    period = Period()
    ask_period(period, teacher)
    print(teacher.time)
    
    # Creates time object and asks user for their desired time    
    time = Time()
    ask_day(time, teacher)
    
    # Gets and displays teacher position based on new information
    teacher.current_position()
    display_teacher(teacher)

# Asks user to input new teachers name
def ask_teacher(teacher):
    while True:
        teacherInput = input("What teacher would you like to find: ")
        # Checks input is valid then makes it an atribute of teacher
        teacher.add(teacherInput)
        # Asks again if name not found
        if teacher.name != None:
            break
        print("Teacher Unknown Please Input again")

# Prints out information about the teacher        
def display_teacher(teacher):
    if teacher.location == None:
        print("location unkown its currently outsie of school hours")
        return
    if isinstance(teacher.location, str):
        print(f"Teacher's Location is {teacher.location}")
        print(f"Teacher's Class is {teacher.className}")
        print(f"Teacher's Class code is {teacher.classCode}")
    else:
        print("Teacher does not currently have a class")
        print("The teachers location is unknown")
           
# Ask if the user would like to terminate the program      
def ask_continue():
    while True:
        newInfoInput = input("Would you like to pick" +
                             "a different teacher or time: ")
        # evalute wether the answer was yes or no
        newInfoInput = sentiment_finder(newInfoInput)
        # if unknown repeat answer
        if newInfoInput == None:
            print("Input again please")
            continue
        break
    
    # Exit program if answer was no    
    if newInfoInput == False:
        exit_program()

# ask the user for the period the want
def ask_period(period, teacher):
    # repeat until a satasfactory answer is found
    while period.period == None and period.time == None:
        inputedTime = input("What time of day:")
        # add time as an atribute of the period object
        period.add(inputedTime)
        period.num_time()
        print(period.time)
        period.word_time()
        print(period.time)
        # add the found time as an atribute of the teacher object
        if (period.period == None) and (period.time) != None:
            teacher.add_day_time(period.add_pm(period.time))
            teacher.get_period()
        elif (period.period != None):
            teacher.add_time(period.period)
            
# ask the user for what time they would like to chose
def ask_day(time, teacher):
    # repeat until a suitable date or day is found
    while time.day == None and time.date == None:
        # ask for day then find intended day
        inputedDay = input("What day would you like: ")
        time.add(inputedDay)
        time.num_day()
        time.word_day()
        # add time as a period as an attribute of Teacher
        if (time.day == None) and (time.date != None):
            time.date = datetime.strptime(str(time.date), "%m%d%y")
            time.date = datetime.strftime(time.date, "%m/%d/%Y")
            teacher.add_day(time.date)
            teacher.get_day()
        elif (time.day != None):
            time.day = "Day " + str(time.day)
            teacher.add_day(time.day)

#  Finds if a given input is affirmative or not
def sentiment_finder(word):
    # loads positive spell checker and makes input space insensitive
    word = word.replace(" ","")
    spell = SpellChecker(language = None)
    spell.word_frequency.load_text_file("final/yes.txt")
    if len(word) <= 3:
        spell.distance = 1
    
    # Checks if the word is in the yes list
    candidates = spell.candidates(word)
    if candidates and ((word in spell) or (word not in candidates)):
        return True
    else:
        # Loads negative spell checker
        spell = SpellChecker(language = None)
        spell.word_frequency.load_text_file("final/no.txt")
        if len(word) <= 3:
            spell.distance = 1    
        candidates = spell.candidates(word)
        
        # checks if word is any no list and returns None if not
        if candidates and ((word in spell) or (word not in candidates)):
            return False
        else:
            return None

# thanks the user and exits the program
def exit_program():
    print("Thank you for using this teacher stalking machine\n" +
          "I hope you found what you needed")
    exit()

if __name__ == "__main__":
    main()