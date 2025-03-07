import pandas as pd
def main():
    timetable = pd.read_csv('final/mrs_wilde.csv')
    day , period = ask_info()
    display_location(day,period,timetable)
    
def display_location(day,period,timetable):
    print(timetable.iloc[(period-1)*3:(period-1)*3+3]["day "+day])

        

def ask_info():
    day=input("Day> ")
    period=input("Period: ")
    return day,int(period)

if __name__ == "__main__":
    main()