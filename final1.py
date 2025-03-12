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
        "After School" : [15.30,24.00],                 
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
        gh = input("Would you like to pick a different teacher or time: ")
        simpleUserAnswer = sentiment_finder(gh)
        if simpleUserAnswer == None:
            print("Input again please")
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
    spacedInputTime = inputedTime
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
    if period == 0:
        period = figure_out_word_time(spacedInputTime)
        
    print(period,"test")
    return period, day

def figure_out_time(inputedTime):
    try:
        int(inputedTime)
        if len(inputedTime)>4:
            pass
        elif len(inputedTime)<3:
            if int(inputedTime)<25:
                return inputedTime
        else:
            print("test")
            print(inputedTime[:-2]+"."+inputedTime[-2:])
            return float(inputedTime[:-2]+"."+inputedTime[-2:])
        return None
           
    except:
        if ":" in inputedTime:
            colonIndex = inputedTime.index(":")
            if len(inputedTime)-2>colonIndex>1:
                hour = inputedTime[colonIndex-2:colonIndex]
                minute = inputedTime[colonIndex+1:colonIndex+3]
                if "pm" in inputedTime:
                    hour += 12
                if hour < 24 and minute < 60:
                    return float(hour+"."+minute)
                else:
                    return None
            else:
                return None
    return 0

def figure_out_word_time(inputedTime):
    inputedTime = inputedTime.split(" ")
    spell = SpellChecker()
    for i in inputedTime:
        if i not in spell:
            inputedTime[inputedTime.index(i)] = spell.correction(i)
        try:
            inputedTime[inputedTime.index(i)] = w2n.word_to_num(i)
        except:
            pass
    
    pm = False
    if "pm" in inputedTime:
        pm = True
    
    if "to" in inputedTime or "past" in inputedTime:
        for i in inputedTime:
            if i == "quarter":
                inputedTime[inputedTime.index(i)] = 15
            if i == "half":
                inputedTime[inputedTime.index(i)] = 30
        try:
            pivot = inputedTime.index("to")
        except:
            pivot = inputedTime.index("past")
        hours = inputedTime[pivot+1]
        minutes = inputedTime[pivot-1]
        if "to" in inputedTime:
            time = hours - minutes * 0.01 - 0.4
        else:
            time = hours + minutes * 0.01
        if pm == True:
            time += 12
        return time    
            
    i = 0
    for _ in inputedTime:
        if type(inputedTime[i]) == str:
            print(inputedTime[i])
            inputedTime.pop(i)
        i += 1
    
    i = 0
    for _ in inputedTime:
        if inputedTime[i] >= 10:
            inputedTime[i] = inputedTime[i] + inputedTime[i+1]
            inputedTime.pop(i+1)
        i += 1
    numTime = float(".".join(str(i) for i in inputedTime))
    if pm == True:
        numTime += 12
    return numTime
    
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
    print("Thank you for using this teacher stalking machine\nI hope you found what you needed")
    exit()
        

if __name__ == "__main__":
    ask_time()