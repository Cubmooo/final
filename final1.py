import pandas as pd
import datetime
def main():
    timetable = pd.read_csv('final/mrs_wilde.csv')
    #day , period = ask_info()
    period , day = get_datetime()
    
    print(day,period)
    display_location(day,period,timetable)
    
def display_location(day,period,timetable):
    period = "Period 3"
    day = "Day 3"
    if day != "Not at School" and (period != "Before School" or period != "After School"):
        periodIndexPosition = timetable.index[timetable.iloc[:,0] == period][0]
        dayIndexPosition = timetable.columns.get_loc(day)
        teacherDetails = timetable.iloc[periodIndexPosition:periodIndexPosition+3,dayIndexPosition]
        print(teacherDetails)
        '''
        print(f"Teacher's Location is {teacherDetails[2]}")
        print(f"Teacher's Class is {teacherDetails[0]}")
        print(f"Teacher's Class code is {teacherDetails[1]}")
        '''
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
            
    currentDay = "_____Not at School"
    
    schoolCalender = pd.read_csv('final/school_calender.csv')
    for item,row in schoolCalender.iterrows():
        if row["start_date"] == currentDate:
            currentDay = row["name"]
        
    currentDay = currentDay[5:]
    
    return currentPeriod,currentDay
    
def ask_info():
    day=input("Day> ")
    period=input("Period: ")
    return day,int(period)

if __name__ == "__main__":
    main()