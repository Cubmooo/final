from datetime import datetime

import pandas as pd
from spellchecker import SpellChecker

from config import ClassConfig

# The teacher class handles finding the teachers name and locating them
class Teacher:
    def __init__(self):
        self.location = None
        self.class_name = None
        self.class_code = None
        self.day = None
        self.time = None
        self.name = None
        self.config = ClassConfig()
    
    # Find and store the name in the users input  
    def add(self, name):
        # Create list of teachers names and make input case insensitive
        name = name.replace(" ","").lower()
        teacher_list=[]
        teachers = open(self.config.teacher_file, "r")
        for i in teachers:
            teacher_list.append(i.split(" ",1)[0])

        # Define spell checker
        spell = SpellChecker(language = None, distance=2)
        spell.word_frequency.load_words(teacher_list)

        # Correct input and check that the user has inputted a name
        fixed_name = spell.correction(name)
        name = fixed_name if (name != fixed_name) or (name in spell) else None
        if name is None:
            self.name = name
            return
        
        # turns list of teachers into a dict then finds filepath
        with open(self.config.teacher_file) as gh:
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
        school_calender = pd.read_csv(self.config.calendar_file)
        
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