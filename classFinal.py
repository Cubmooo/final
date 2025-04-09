from datetime import datetime
from spellchecker import SpellChecker

import Teacher
import Period
import Time


def main():
    # creates teacher object then ask for teacher location
    teacher = Teacher.Teacher()
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
    period = Period.Period()
    ask_period(period, teacher)
    
    # Creates time object and asks user for their desired time    
    time = Time.Time()
    ask_day(time, teacher)
    print(time.date)
    print(time.day)
    
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
        if teacher.name is not None:
            break
        print("Teacher Unknown Please Input again")

# Prints out information about the teacher        
def display_teacher(teacher):
    if teacher.location is None:
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
        if new_info_input is None:
            print("Input again please")
            continue
        break
    
    # Exit program if answer was no    
    if new_info_input == False:
        exit_program()

# ask the user for the period the want
def ask_period(period, teacher):
    # repeat until a satasfactory answer is found
    while period.period is None and period.time is None:
        inputed_time = input("What time of day:")
        # add time as an atribute of the period object
        period.add(inputed_time)
        period.num_time()
        period.word_time()
        # add the found time as an atribute of the teacher object
        if (period.period is None) and (period.time) is not None:
            teacher.add_day_time(period.add_pm(period.time))
            teacher.get_period()
        elif (period.period is not None):
            teacher.add_time(period.period)
            
# ask the user for what time they would like to chose
def ask_day(time, teacher):
    # repeat until a suitable date or day is found
    while time.day is None and time.date is None:
        # ask for day then find intended day
        inputed_day = input("What day would you like: ")
        time.add(inputed_day)
        print(time.date)
        print(time.day)
        print(time.day_input)
        time.num_day()
        print(time.date)
        print(time.day)
        print(time.day_input)
        time.word_day()
        print(time.date)
        print(time.day)
        print(time.day_input)
        # add time as a period as an attribute of Teacher
        if (time.day is None) and (time.date is not None):
            time.date = datetime.strptime(str(time.date), "%m%d%y")
            time.date = datetime.strftime(time.date, "%m/%d/%Y")
            teacher.add_day(time.date)
            teacher.get_day()
        elif (time.day is not None):
            time.day = "Day " + str(time.day)
            teacher.add_day(time.day)

#  Finds if a given input is affirmative or not
def sentiment_finder(word):
    # loads positive spell checker and makes input space insensitive
    word = word.replace(" ","")
    spell = SpellChecker(language = None)
    spell.word_frequency.load_text_file("yes.txt")
    if len(word) <= 3:
        spell.distance = 1
    
    # Checks if the word is in the yes list
    candidates = spell.candidates(word)
    if candidates and ((word in spell) or (word not in candidates)):
        return True
    else:
        # Loads negative spell checker
        spell = SpellChecker(language = None)
        spell.word_frequency.load_text_file("no.txt")
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