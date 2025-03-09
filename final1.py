import pandas as pd
import datetime
from spellchecker import SpellChecker

def main():
    timetable = pd.read_csv('final/mrs_wilde.csv')
    #day , period = ask_info()
    period, day = get_datetime()
    while True:
        display_location(day,period,timetable)
        period, day = ask_info() 
    
def display_location(day,period,timetable):
    
    if day != "No School" and period != ("Before School" or "After School"):
        
        periodIloc = timetable.index[timetable.iloc[:,0] == period][0]
        dayIloc = timetable.columns.get_loc(day)
        teacherDetails = timetable.iloc[periodIloc:periodIloc+3,dayIloc].tolist()
        
        print(f"Teacher's Location is {teacherDetails[2]}")
        print(f"Teacher's Class is {teacherDetails[0]}")
        print(f"Teacher's Class code is {teacherDetails[1]}")
        
    else:
        print("Teacher location is unknown\nOutside of school hours")
    
def get_datetime():
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
        "After School" : [15.30,23.59],                 
    }
    
    currentDateAndTime = datetime.datetime.now()
    currentDate = currentDateAndTime.strftime("%d/%m/%Y")
    currentTime = currentDateAndTime.strftime("%H.%M")
    
    for period,time in bellTimes.items():
        if time[0] <= float(currentTime) < time[1]:
            currentPeriod = period
            
    currentDay = "_____No School"
    
    schoolCalender = pd.read_csv('final/school_calender.csv')
    for item,row in schoolCalender.iterrows():
        if row["start_date"] == currentDate:
            currentDay = row["name"]
        
    currentDay = currentDay[5:]
    
    return currentPeriod,currentDay
    
def ask_info():
    gh = input("Would you like to pick a diffrent time: ")
    spell = SpellChecker(language=None)
    spell.word_frequency.load_text_file("final/yes.txt")
    if gh not in spell:
        gh = spell.correction(gh)
    print(gh)
    
def spellcheck(word,spell):
    if word not in spell:
        word = spell.correction(word)
        return word
        

if __name__ == "__main__":
    main()