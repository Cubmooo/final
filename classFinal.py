from datetime import datetime

import pandas as pd
from spellchecker import SpellChecker
from word2number import w2n


# The teacher class handles finding the teachers name and locating them
class Teacher:
    def __init__(self):
        self.location = None
        self.class_name = None
        self.class_code = None
        self.day = None
        self.time = None
        self.name = None
    
    # Find and store the name in the users input  
    def add(self, name):
        # Create list of teachers names and make input case insensitive
        name = name.replace(" ","").lower()
        teacher_list=[]
        teachers = open("final/teachers.txt", "r")
        for i in teachers:
            teacher_list.append(i.split(" ",1)[0])

        # Define spell checker
        spell = SpellChecker(language = None, distance=2)
        spell.word_frequency.load_words(teacher_list)

        # Correct input and check that the user has inputted a name
        fixed_name = spell.correction(name)
        name = fixed_name if (name != fixed_name) or (name in spell) else None
        if name == None:
            self.name = name
            return
        
        # turns list of teachers into a dict then finds filepath
        with open("final/teachers.txt") as gh:
            name_index = dict([line.strip().split(" ",1) for line in gh])
        name = name_index[name]
        self.name = name
    
    def get_current_time(self):
        # finds and formats the current time
        current_date_and_time = datetime.now()
        self.day = current_date_and_time.strftime("%d/%m/%Y")
        self.day_time = current_date_and_time.strftime("%H.%M")
        
        # calls the functions to find school period and days
        self.get_period()
        self.get_day()
        
    def add_day_time(self, dayTime):
        # defines the inputted time as a attribute of Teacher
        self.day_time = dayTime
        
    def add_time(self, time):
        # defines the inputted period as a attribute of Teacher
        self.time = "Period " + str(time)
        
    def add_day(self, date):
        # defines the inputted date as a attribute of Teacher
        self.day = date
    
    # Finds the period in which any time sits
    def get_period(self):
        # Defines list of periods and there times
        bell_times={
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
        for period,times in bell_times.items():
            if times[0] <= float(self.day_time) < times[1]:
                self.time = period
    
    # Finds the school day for the given date           
    def get_day(self):
        # Defines calender
        school_calender = pd.read_csv("final/school_calender.csv")
        
        # iterates through the calender to find the correct school day
        for _,row in school_calender.iterrows():
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
                period_iloc = timetable.index[loc][0]  
            except:
                return
            
            # find the correct information based on its location
            if self.day in timetable.columns:
                day_iloc = timetable.columns.get_loc(self.day)
                self.info = timetable.iloc[period_iloc:period_iloc + 3, day_iloc]

                # Store the location information
                self.class_name = self.info.tolist()[0]
                self.class_code = self.info.tolist()[1]
                self.location = self.info.tolist()[2]


class Period:
    def __init__(self):
        self.has_pm = False
        self.has_am = False
        self.has_period = False
        self.time = None
        self.period = None
        self.to_or_past_index = None
        self.has_to = False
    
    # Store the users time input as various attributes
    def add(self, inputedTime):
        # stores input as spell corrected and caps in-sensitive 
        self.split_input = self.num_word_spell_check(inputedTime.split())
        self.split_input = [word.lower() if isinstance(word, str) else word
                           for word in self.split_input]
        self.spaceless_input = inputedTime.replace(" ","")
        self.list_input = list(self.spaceless_input)
                
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
        if "period" in self.split_input:
            self.has_period = True
        if "pm" in self.split_input:
            self.has_pm = True
        if "am" in self.split_input:
            self.has_am = True
        
        # Returns the time as a period if the time is given as a period
        if self.has_period:
            try:
                index = self.split_input.index("period")
                self.period = int(self.split_input[index + 1])
                return
            except:
                pass
        
        # remove all words from the inputted time
        self.int_list = [int(num) for num in self.list_input if num.isdigit()]
        self.period_int = "".join(map(str, self.int_list))
        self.period_int = int(self.period_int) if self.period_int else None
        
        # return if no time present
        if self.period_int == None:
            return
        # return the time either in hours or hours and minutes
        if len(str(self.period_int)) in [3, 4]:
            self.time = (self.period_int/100)
        elif len(str(self.period_int)) in [1, 2]:
            self.time = self.period_int

    def word_time(self):
        # find the location of the words to and past if present
        if "to" in self.split_input:
            self.to_or_past_index = self.split_input.index("to")
            self.hasTo = True
        if "past" in self.split_input:
            self.to_or_past_index = self.split_input.index("past")
        
        # Finds the time based on the location found earlier
        try:
            minutes = self.split_input[self.to_or_past_index - 1]
            hours = self.split_input[self.to_or_past_index + 1]
            offset = (-2 * self.has_to + 1) * minutes - 40 * self.has_to
            self.time = hours + offset / 100
            return
        except:
            pass
        
        # remove all words from input
        self.split_input = [int(i) for i in self.split_input
                           if str(i).isdigit()]
        i = 0
        """iterate through list combining all numbers larger then 10
        with there next number e.g. 40, 5 become 45"""
        try:
            while i < len(self.split_input) - 1:
                if self.split_input[i] >= 10:
                    self.split_input[i] += self.split_input[i + 1]
                    self.split_input.pop(i + 1)
                else:
                    i += 1
            # return final time
            self.time = float(".".join([str(num) for num in self.split_input]))
        except:
            pass

    # converts 12 hour time to 24 hour time
    def add_pm(self, time):
        if (self.has_pm == True) and (time < 12):
            time += 12
        # automaticaly assumes school hours unless otherwise stated
        elif (self.has_am != True) and (time < 6):
            time += 12
        return time


class Time:
    def __init__(self):
        self.month = None
        self.year = 25
        self.day = None
        self.date = None
        self.month_list = self.file_to_dict("final/months.txt")
        self.numbers_list = self.file_to_dict("final/numbers.txt")
    
    # store inputed day as a attribute or Time    
    def add(self, inputed_day):
        self.day_input = inputed_day
    
    # takes a file of nums or months and creates dict with same ints    
    def file_to_dict(self, filepath):
        with open(filepath, "r") as file:
            return {line.strip(): i + 1 for i, line in enumerate(file)}
    
    # iterate through word in list spell checking it
    def spell_check(self, given_list):
        spell = SpellChecker()
        given_list = given_list.split()
        for i, word in enumerate(given_list):
            given_list[i] = spell.correction(word)
        return given_list
    
    # finds the date or period if given in digits          
    def num_day(self):
        # remove all words from list
        self.int_date = [i for i in self.day_input if i.isdigit()]
        try:
            # return the date if the inputted date is of the right length
            if len(self.int_date) == 6:
                self.date = int("".join(self.int_date))
            if len(self.int_date) == 4 and int(self.int_date) != 2025:
                self.date = int("".join(self.int_date) + "25")
            # return the period if the input is one digit long
            if len(self.int_date) == 1:
                self.day = self.int_date[0]
        except:
            pass
    
    # Finds the date if it is inputed in words
    def word_day(self):
        # ensure this function isnt run unnecessarily 
        if self.day != None or self.date != None:
            return
        # spell check input
        self.day_input = self.spell_check(self.day_input)
       
        # make all two words numbers one e.g. twenty one -> twentyone
        for i,j in enumerate(self.day_input):
            if j == "twenty" or j == "thirty":
                self.day_input[i] = self.day_input[i] + self.day_input[i + 1]
                self.day_input.pop(i + 1)
        
        # replace all months and numbers with ints
        for i,j in enumerate(self.day_input):
            self.day_input[i] = self.month_list.get(j, self.day_input[i])
            self.day_input[i] = self.numbers_list.get(j, self.day_input[i])
            
            # store the month to know date format
            if (self.month is None) and (j in self.month_list):
                self.month = self.month_list[j]
            
            # replace all typed digits with ints    
            if isinstance(j, str) and j.isdigit():
                self.day_input[i] = int(j)
        
        # coverts all items of list into ints
        self.day_input = [
            int(num) for num in self.day_input if isinstance(num, int)
            or (isinstance(num, str) and  num.isdigit())
        ]
        
        # Finds the location of the month in the date
        if self.month in self.day_input:    
            normal_date_format = self.day_input.index(self.month) == 1
        # truncates the year if it is stated
        if len(self.day_input) >= 3:
            self.year = int(str(self.day_input[2])[-2:])
        # return date ensuring correct formating is used
        if normal_date_format != None:
            self.month_day = self.day_input[-1 * (normal_date_format - 1)]
            self.date = self.month_day * 10000 + self.month * 100 + self.year


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
        print(f"Teacher's Class is {teacher.class_name}")
        print(f"Teacher's Class code is {teacher.class_code}")
    else:
        print("Teacher does not currently have a class")
        print("The teachers location is unknown")
           
# Ask if the user would like to terminate the program      
def ask_continue():
    while True:
        new_info_input = input("Would you like to pick" +
                             "a different teacher or time: ")
        # evalute wether the answer was yes or no
        new_info_input = sentiment_finder(new_info_input)
        # if unknown repeat answer
        if new_info_input == None:
            print("Input again please")
            continue
        break
    
    # Exit program if answer was no    
    if new_info_input == False:
        exit_program()

# ask the user for the period the want
def ask_period(period, teacher):
    # repeat until a satasfactory answer is found
    while period.period == None and period.time == None:
        inputed_time = input("What time of day:")
        # add time as an atribute of the period object
        period.add(inputed_time)
        period.num_time()
        period.word_time()
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
        inputed_day = input("What day would you like: ")
        time.add(inputed_day)
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