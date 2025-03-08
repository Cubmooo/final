import pandas as pd
import datetime
def main():
    timetable = pd.read_csv('final/mrs_wilde.csv')
    day , period = ask_info()
    get_datetime()
    display_location(day,period,timetable)
    
def display_location(day,period,timetable):
    teacherDetails = timetable.iloc[(period-1)*3:(period-1)*3+3]["day "+day].values
    print(f"Teacher's Location is {teacherDetails[2]}")
    print(f"Teacher's Class is {teacherDetails[0]}")
    print(f"Teacher's Class code is {teacherDetails[1]}")
    
def get_datetime():
    bellTimes={
        "Morning Tutor":[8.40,8.50],
        "Period 1" : [8.50,9.40],
        "Period 2" : [9.40,10.30],
        "Period 3" : [10.50,11.40],
        "Period 4" : [11.40,12.30],        
    }
    
    currentDateAndTime = datetime.datetime.now()
    currentDate = currentDateAndTime.strftime("%d/%m/%Y")
    currentTime = currentDateAndTime.strftime("%H.%M")

    for period,time in bellTimes.items():
        print(time)
    
    

def ask_info():
    day=input("Day> ")
    period=input("Period: ")
    return day,int(period)

if __name__ == "__main__":
    main()