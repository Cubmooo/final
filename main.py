"""This program finds the location of a teacher at saint kentigern college.

it automaticaly finds the current time and asks user for the teachers name
it then allows the user to input a new time and diffrent teacher

This is a program for Level 2 computer science
"""

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
    """Runs the whole program from the start to the ask second time function.
    
    this function:
        creates teacher object
        prompts user for teacher
        displays approiate location
        calls the ask_second_time function
        
    Arguments:
        config: config file

    """
    # creates teacher object then ask user for a teachers name
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
    
    # carry on to asking for a new teacher
    # program would have terminated earlier if requested
    ask_second_time(teacher, period, time)
    
def ask_second_time(teacher,period,time):
    """Displays a teacher location based on the user inputed name and time.
    Args:
        teacher (object): stores info about name and location
        period (object): stores info about inputed period
        time (object): stores info about the inputted day
    """
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
    """Asks user if they want to see the list of teachers this program stores.

    Args:
        teacher (object): stores the list of teachers
    """
    while True: # asks again until suitable answer found
        # asks user if the would like to see the list of teachers
        print_slow("Would you like to see a list of teachers: ", False)
        list_input = input()
        logger.info(f"list input: {list_input}")
        # evaluate wether the answer was yes or no
        list_input = sentiment_finder(config, list_input)
        logger.info(f"revised input {list_input}")

        if list_input is None: # if unknown repeat answer
            print_slow('Your input was unrecognised ' +
                       'please input either "yes" or "no"')
            continue
        if list_input: # prints teacher list if answer was yes
            teacher.print_teacher_list()
        break

def ask_teacher(teacher):
    """Asks user for the name of the teacher they wish to find.

    Args:
        teacher (object): finds and stores correct name
    """
    
    teacher_ask_num = 0
    while True: # asks until appropriate teacher name given
        # asks for teachers name
        print_slow("What teacher would you like to find: ", False)
        teacher_input = input()
        logger.info(f"teacher input: {teacher_input}")
        # Checks input is valid then makes it an atribute of teacher
        teacher.add(teacher_input)
        # Asks again if name not found
        if teacher.name is not None:
            logger.info(f"teacher known {teacher.name}")
            break
        # if too many invalid names given prints the teacher list again
        if teacher_ask_num >= 1:
            print_slow("Teacher not recognised " + 
                       "please input a name from this list")
            teacher.print_teacher_list()
        else:
            # informs user that they must reinput
            print_slow("Teacher Unknown Please Input again")
        teacher_ask_num += 1
        logger.info(f"teacher unknown input: {teacher_input}")
       
def display_teacher(teacher):
    """Displays to the user the infomation about the teachers location.

    Args:
        teacher (object): holds the teachers position to be displayed
    """
    logger.info(f"teacher location: {teacher.location}")
    if teacher.location is None: # location will be none if out of school hours
        logger.info(f"place unknown {teacher.location, teacher.class_code}")
        print_slow("location unknown its currently outside of school hours")
        return
    if isinstance(teacher.location, str): # will be string if location known
        logger.info(f"location known {teacher.location, teacher.class_code}")
        print_slow(f"Teacher's Location is {teacher.location}")
        print_slow(f"Teacher's Class is {teacher.class_name}")
        print_slow(f"Teacher's Class code is {teacher.class_code}")
    else: # location will be Nan if during school but teacher has no class
        logger.info(f"no class {teacher.location, teacher.class_code}")
        print_slow("Teacher does not currently have a class")
        print_slow("The teachers location is unknown")
                
def ask_continue(config):
    """Asks user if the wish to input another teacher or time.

    Args:
        config (dictonary): holds all the file paths used for yes and no files
    """
    while True: # repeats until valid answer given
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

def ask_period(period, teacher):
    """Asks the user what period they want the teachers location from.

    Args:
        period (object): procces iformation about the period
        teacher (object): stores the final period
    """
    
    while True: # repeat until a satasfactory answer is found
        logger.info("starting ask period loop")
        print_slow("What time of day e.g. period 5, 1:45: ", False)
        inputed_time = input()
        logger.info(f"inputed time: {inputed_time}")
        # add time as an atribute of the period object
        period.add(inputed_time)
        # procces the inputed time into a period or time of day
        period.num_time()
        period.word_time()
        # add the found time as an atribute of the teacher object
        if (period.period is None) and (period.time) is not None:
            teacher.add_day_time(period.add_pm(period.time))
            teacher.get_period()
        elif (period.period is not None):
            teacher.add_time(period.period)
        logger.info(f"period: {period.period} time: {period.time}")
        # if a time is found break else ask for time again
        if period.period is not None or period.time is not None:
            break
        print_slow('Your time was not recognised please input again')
            
def ask_day(time, teacher):
    """Asks the user for the day they want to know the teachers location.

    Args:
        time (object): process the user input into a time
        teacher (object): stores the final day
    """
    # repeat until a suitable date or day is found
    while True:
        logger.info("starting ask time loop")
        # ask for day then find intended day
        print_slow("What day would you like e.g. day 5, dd/mm/yy: ", False)
        inputed_day = input()
        logger.info(f"inputed day: {inputed_day}")
        # adds the inputed time as an atribute of the time object
        time.add(inputed_day)
        # tunrs the input into a date or school day
        time.word_day()
        time.num_day()
        logger.info(f"day: {time.day} date: {time.date}")
        # turns a date into a school
        compute_day(time, teacher)
        # if time is found move on else ask again
        if time.day is not None or time.date is not None:
            break
        print_slow("Your day was not recognised")
        
        
def compute_day(time, teacher):
    """turns date into a school day then stores school day.

    Args:
        time (object): holds the original date and school day
        teacher (object): stores the final school day
    """
    if (time.day is None) and (time.date is not None): # if time is a date
        try:
            # make sure time is not truncated i.e. mm/dd/yyyy
            time.date = datetime.strptime(str(time.date), "%d%m%y")
            time.date = datetime.strftime(time.date, "%d/%m/%Y")
        except ValueError as e:
            # if error is raised then date does not exsist
            logger.info(f"date failed {e}")
            # prompts user to input date again
            print_slow("Your date could not be understood " + 
                    "check your spelling or input you date as DD/MM/YY")
            time.day = None
            time.date = None
        except Exception as e:
            # if any other error occurs raise it
            logger.critical(f"unkown error {e}")
            raise
        teacher.add_day(time.date) # stores date as atribute of teacher
        teacher.get_day() # finds corrosponding school day
    elif (time.day is not None): # is school day known
        # store school day as attribute of teacher
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
        time.sleep(config.text_delay)
    print() if end_line else None

if __name__ == "__main__":
    config = ClassConfig()
    main(config)