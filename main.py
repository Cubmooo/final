from datetime import datetime
from spellchecker import SpellChecker
import time

from config import ClassConfig
import Teacher
import Period
import Time
from logging_config import setup_logger
logger = setup_logger(__name__)


def main(config):
    # creates teacher object then ask for teacher location
    teacher = Teacher.Teacher()
    ask_teacher_list(teacher)
    ask_teacher(teacher)
    # Get and display current position of teacher
    teacher.get_current_time()
    teacher.current_position()
    logger.info(f"teacher current position {teacher.location}")
    logger.info(f"teacher class {teacher.class_code}")
    display_teacher(teacher)
    
    # ask if they wish to input another teacher
    ask_continue(config)
    # create objects
    teacher.name = None
    period = Period.Period()
    time = Time.Time()
    logger.info("asking second time")
    ask_second_time(teacher, period, time)
    
def ask_second_time(teacher,period,time):
    #ask users for what teacher they want
    ask_teacher(teacher)
    
    # ask user for desired time of day
    ask_period(period, teacher)
    
    # asks user for desired day
    ask_day(time, teacher)
    
    # Gets and displays teacher position based on new information
    teacher.current_position()
    display_teacher(teacher)

# ask user if they want to see list of teachers
def ask_teacher_list(teacher):
    while True:
        print_slow("Would you like to see a list of teachers: ", False)
        list_input = input()
        logger.info(f"list input: {list_input}")
        # evaluate wether the answer was yes or no
        list_input = sentiment_finder(config, list_input)
        logger.info(f"revised input {list_input}")
        # if unknown repeat answer
        if list_input is None:
            print_slow('Your input was unrecognised ' +
                       'please input either "yes" or "no"')
            continue
        if list_input:
            teacher.print_teacher_list()
        break

# Asks user to input new teachers name
def ask_teacher(teacher):
    teacher_ask_num = 0    
    while True:
        print_slow("What teacher would you like to find: ", False)
        teacher_input = input()
        logger.info(f"teacher input: {teacher_input}")
        # Checks input is valid then makes it an atribute of teacher
        teacher.add(teacher_input)
        # Asks again if name not found
        if teacher.name is not None:
            logger.info(f"teacher known {teacher.name}")
            break
        if teacher_ask_num >= 1:
            print_slow("Teacher not recognised " + 
                       "please input a name from this list")
            teacher.print_teacher_list()
        print_slow("Teacher Unknown Please Input again")
        teacher_ask_num += 1
        logger.info(f"teacher unknown input: {teacher_input}")

# Prints out information about the teacher        
def display_teacher(teacher):
    logger.info(f"teacher location: {teacher.location}")
    if teacher.location is None:
        logger.info(f"place unknown {teacher.location, teacher.class_code}")
        print_slow("location unknown its currently outside of school hours")
        return
    if isinstance(teacher.location, str):
        logger.info(f"location known {teacher.location, teacher.class_code}")
        print_slow(f"Teacher's Location is {teacher.location}")
        print_slow(f"Teacher's Class is {teacher.class_name}")
        print_slow(f"Teacher's Class code is {teacher.class_code}")
    else:
        logger.info(f"no class {teacher.location, teacher.class_code}")
        print_slow("Teacher does not currently have a class")
        print_slow("The teachers location is unknown")
           
# Ask if the user would like to terminate the program      
def ask_continue(config):
    while True:
        print_slow("Would you like to pick " +
                    "a different teacher or time (yes/no): ", False)
        new_info_input = input()
        logger.info(f"user carry on input {new_info_input}")
        # evaluate wether the answer was yes or no
        new_info_input = sentiment_finder(config, new_info_input)
        logger.info(f"revised input {new_info_input}")
        # if unknown repeat answer
        if new_info_input is None:
            print_slow('Answer not recognised please input "yes" or "no"')
            continue
        break
    
    # Exit program if answer was no    
    if new_info_input == False:
        exit_program()

# ask the user for the period the want
def ask_period(period, teacher):
    # repeat until a satasfactory answer is found
    while True:
        logger.info("starting ask period loop")
        print_slow("What time of day e.g. period 5, 1:45: ", False)
        inputed_time = input()
        logger.info(f"inputed time: {inputed_time}")
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
        logger.info(f"period: {period.period} time: {period.time}")
        if period.period is not None or period.time is not None:
            break
        print_slow('Your time was not recognised please input again')
            
# ask the user for what time they would like to chose
def ask_day(time, teacher):
    # repeat until a suitable date or day is found
    while True:
        logger.info("starting ask time loop")
        # ask for day then find intended day
        print_slow("What day would you like e.g. day 5, dd/mm/yy: ", False)
        inputed_day = input()
        logger.info(f"inputed day: {inputed_day}")
        time.add(inputed_day)
        time.word_day()
        time.num_day()
        logger.info(f"day: {time.day} date: {time.date}")
        compute_day(time, teacher)
        if time.day is not None or time.date is not None:
            break
        print_slow("Your day was not recognised")
        
        
def compute_day(time, teacher):
        # add time as a period as an attribute of Teacher
        if (time.day is None) and (time.date is not None):
            try:
                time.date = datetime.strptime(str(time.date), "%d%m%y")
                time.date = datetime.strftime(time.date, "%d/%m/%Y")
            except ValueError as e:
                logger.info(f"date failed {e}")
                print_slow("Your date could not be understood " + 
                      "check your spelling or input you date as DD/MM/YY")
                time.day = None
                time.date = None
            except Exception as e:
                logger.critical(f"unkown error {e}")
                raise
            teacher.add_day(time.date)
            teacher.get_day()
        elif (time.day is not None):
            time.day = "day " + str(time.day)
            teacher.add_day(time.day)
        logger.info(f"day: {time.day} date: {time.date}")

#  Finds if a given input is affirmative or not
def sentiment_finder(config, word):
    # loads positive spell checker and makes input space insensitive
    word = word.replace(" ","")
    logger.debug(f"no space word {word}")
    # finds if word is negative of positive
    is_positive = sentiment(word, config.yes_file)
    logger.debug(f"is word positive {is_positive}")
    is_negative = sentiment(word, config.no_file)
    logger.debug(f"is word negative {is_negative}")
    # returns if the program should carry on
    if is_positive:
        return True
    elif is_negative:
        return False
    return None
        
def sentiment(word, file):
    # loads spell checker and might reduce word Levenshtein distance
    spell = SpellChecker(language = None)
    spell.word_frequency.load_text_file(file)
    if len(word) <= 3:
        spell.distance = 1
    
    # compare word to word list and return if the word is in the list   
    candidates = spell.correction(word)
    logger.debug(f"word candidates {candidates}")
    if candidates and ((word in spell) or (word not in candidates)):
        return True
    else:
        return False

# thanks the user and exits the program
def exit_program():
    print_slow("Thank you for using this program\n" +
          "I hope you found what you needed")
    logger.info("user exited program")
    exit()
    
def print_slow(str, end_line = True):
    for i in str:
        print(i, end = "")
        time.sleep(0.03)
    print() if end_line else None

if __name__ == "__main__":
    config = ClassConfig()
    main(config)