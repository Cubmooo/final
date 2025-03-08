import pandas as pd
import datetime
def main():
    timetable = pd.read_csv('final/mrs_wilde.csv')
    day , period = ask_info()
    
    display_location(day,period,timetable)
    
def display_location(day,period,timetable):
    teacherDetails = timetable.iloc[(period-1)*3:(period-1)*3+3]["day "+day].values
    print(f"Teacher's Location is {teacherDetails[2]}")
    print(f"Teacher's Class is {teacherDetails[0]}")
    print(f"Teacher's Class code is {teacherDetails[1]}")
    
def get_datetime():
    currentDateAndTime = datetime.datetime.now()
    currentDate = currentDateAndTime.strftime("%d/%m/%Y")
    currentTime = currentDateAndTime.strftime("%H:%M:%S")
    print(currentDate,currentTime)
    
    

def ask_info():
    day=input("Day> ")
    period=input("Period: ")
    return day,int(period)

if __name__ == "__main__":
    main()