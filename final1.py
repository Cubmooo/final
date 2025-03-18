import pandas as pd
import datetime
from spellchecker import SpellChecker
from word2number import w2n

def main():
    teacher = ask_teacher()
    timetable = pd.read_csv(teacher)
    #day , period = ask_info()
    period, day = get_datetime()
    print(period,day)
    display_location(day,period,timetable)
    while True:
       ask_info() 
    
def display_location(day,period,timetable):
    
    if day != "No School" and period not in ["Before School", "After School"]:
        try:
            periodIloc = timetable.index[timetable.iloc[:,0] == period][0]
        except:
            print("teacher location unknown")
            return
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
    while True:
        inputedTime = input("What time of day:")
        spacedInputTime = inputedTime
        inputedTime = inputedTime.replace(" ","")      
        period = period_time(spacedInputTime)
        if period == None:
            period = military_time(inputedTime)
            if period == None:
                period = word_to_past_time(spacedInputTime)
                if period == None:
                    period = word_time(spacedInputTime)
        print(period)
        
def period_time(inputedTime):
    spell = SpellChecker()
    inputedTime = inputedTime.split(" ")
    for i,word in enumerate(inputedTime):
        if word not in spell:
            inputedTime[i] = spell.correction(word)
    try:
        index = inputedTime.index("period")
        number = inputedTime[index + 1]
        try:
            number = int(number)
        except:
            number = w2n.word_to_num(number)
        
        if 1 <= number <=6:
            return ("Period" + str(number))
        else:
            return 1
    except:
        return None

def military_time(inputedTime):
    pm = False
    if "pm" in inputedTime:
        pm = True
    inputedTime = list(inputedTime)
    i = 0
    while i < len(inputedTime):
        char = inputedTime[i]
        try:
            inputedTime[i] = int(char)
            i += 1
        except:
            inputedTime.pop(i)
    inputedTime = int("".join(str(char) for char in inputedTime))
    
    if len(str(inputedTime)) > 4:
        return None
    if len(str(inputedTime)) >= 3:
        inputedTime = inputedTime/100
    if 0 <=inputedTime <= 24:
        return inputedTime + 12*pm
        

def word_time(inputedTime):
    print("4")
    
    inputedTime = inputedTime.split(" ")
    spell = SpellChecker()
    spell.word_frequency.remove("fourth")
    spell.word_frequency.add("forty")
    for i in inputedTime:
        if i not in spell:
            inputedTime[inputedTime.index(i)] = spell.correction(i)
        try:
            inputedTime[inputedTime.index(i)] = w2n.word_to_num(i)
        except:
            pass 
    print(inputedTime)
    pm = False
    if "pm" in inputedTime:
        pm = True
        
    for i,_ in enumerate(inputedTime):
        if type(inputedTime[i]) == str:
            print(inputedTime[i])
            inputedTime.pop(i)
            
    print(inputedTime)
    for i,_ in enumerate(inputedTime):
        if inputedTime[i] >= 10:
            inputedTime[i] = inputedTime[i] + inputedTime[i+1]
            inputedTime.pop(i+1)

    numTime = float(".".join(str(i) for i in inputedTime))
    if pm == True:
        numTime += 12
    return numTime
        
def word_to_past_time(inputedTime):  
    print("5") 
    inputedTime = inputedTime.split(" ")
    spell = SpellChecker()
    
    
    for i in inputedTime:
        if i not in spell:
            inputedTime[inputedTime.index(i)] = spell.correction(i)
        try:
            inputedTime[inputedTime.index(i)] = w2n.word_to_num(i)
        except:
            pass
    
    if ("to" and "past") not in inputedTime:
        return None
    
            
    for i in inputedTime:
        if i == "quarter":
            inputedTime[inputedTime.index(i)] = 15
        if i == "half":
            inputedTime[inputedTime.index(i)] = 30   
    
    print("uyfu t fgi")
    
    pm = False
    if "pm" in inputedTime:
        pm = True    
    try:    
        index = inputedTime.index("to")
    except:
        index = inputedTime.index("past")
    hours = inputedTime[index]
    minutes = inputedTime[index - 1]
    
    print(minutes,hours)
    if inputedTime[index] == "past":
        return hours + minutes*0.01
    else:
        return hours - 0.4 -minutes*0.01

    
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
    
    
    
    """ timeFunctions = [period_time(inputedTime),military_time(inputedTime),digits_time(inputedTime),word_time(spacedInputTime),word_to_past_time(spacedInputTime)]
        
        for i in timeFunctions:
            period = i
            print(period)
            if period != None:"""