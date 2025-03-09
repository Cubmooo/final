import pandas as pd
import datetime
from spellchecker import SpellChecker
from word2number import w2n

def main():
    teacher = ask_teacher()
    timetable = pd.read_csv(teacher)
    #day , period = ask_info()
    period, day = get_datetime()
    display_location(day,period,timetable)
    while True:
       ask_info() 
    
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
    while True:
        gh = input("Would you like to pick a diffrent teacher or time: ")
        simpleUserAnswer = sentiment_finder(gh)
        if simpleUserAnswer == None:
            print("Input agian please")
            continue
        break
    
    if simpleUserAnswer == False:
        exit_program()
        
    teacher = ask_teacher()
    print(teacher)
    period, day = ask_time()
    display_location(day,period,pd.read_csv(teacher))
    
def ask_time():
    inputedTime = input("What time of day:")
    inputedTime = inputedTime.replace(" ","")
    
    periodsList=[]
    periods = open("final/periods.txt", "r")
    for i in periods:
        periodsList.append(i.split(" ",1)[0])
        
    spell = SpellChecker(language = None)
    spell.word_frequency.load_words(periodsList)
    
    if inputedTime in periodsList:
        period = inputedTime
    else:
        period = spell.correction(inputedTime)

    try:
        int(inputedTime)
        period = None
    except:
        pass
    
    if period == None:
        period = figure_out_time(inputedTime)
        
    print(period,"test")
    return period, day

def figure_out_time(inputedTime):
    print("made it")
    try:
        inputedTime = int(inputedTime)
        if len(inputedTime)>4:
            return None
        elif len(inputedTime)<3 and inputedTime<25:
            return inputedTime
        else:
            print(int(str(inputedTime[-2:])+"."+str(inputedTime[:-2])))
            return int(str(inputedTime[-2:])+"."+str(inputedTime[:-2]))
        
        
    except:
        if ":" in inputedTime:
            print("::::::")
            
    inputedTime = w2n.word_to_num(inputedTime)
    if "to" or "past" in inputedTime:
        print("to,past")
    
def ask_teacher():
    while True:
        teacher = input("What teacher would you like to find: ")
        teacher = teacher.replace(" ","")
        
        teacherList=[]
        teachers = open("final/teachers.txt", "r")
        for i in teachers:
            teacherList.append(i.split(" ",1)[0])
            
        spell = SpellChecker(language = None)
        spell.word_frequency.load_words(teacherList)
        
        teacher = spell.correction(teacher)
        if teacher == None:
            continue
        
        with open("final/teachers.txt") as gh:
            teacherIndex = dict([line.strip().split(" ",1) for line in gh])
        teacher = teacherIndex[teacher]
        
        return teacher   
    
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
    
def spellcheck(word,spell):
    if word not in spell:
        word = spell.correction(word)
        return word

def exit_program():
    print("Thank you for using this teacher stalking machine\nI hope you found whay you needed")
    exit()
        

if __name__ == "__main__":
    ask_time()