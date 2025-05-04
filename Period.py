from spellchecker import SpellChecker
from word2number import w2n
from logging_config import setup_logger
logger = setup_logger(__name__)

class Period:
    """Holds and proccese the information about the time of day.
    
    This class:
        Finds the correct time from multiple diffrent formats including:
            school period e.g. Period 1
            digital time e.g. 1:45
            spelled out e.g. five thirty, quarter to six
            includes am/pm
        
    Attributes:
        has_pm: a boolean of if pm is present in the input
        has_am: a boolean of if am is present in the input
        has_period: a boolean of if "period" is present in the input
        time: float of the time of day format Hour.Minute
        period: int of the period of the day
        to_or_past_index: int of the location of to or past in input
        has_to: a boolean of if to is present in the input
        split_input: a list of the user input split into words
        spaceless_input: a str of user input with no spaces
        list_input: the users input stored as a list of characters
    """
    
    def __init__(self):
        self.has_pm = False
        self.has_am = False
        self.has_period = False
        self.time = None
        self.period = None
        self.to_or_past_index = None
        self.has_to = False
    
    def add(self, inputedTime):
        """Stores the users inputted time as an various attributes

        Args:
            inputedTime (str): The time inputted by the user
        """
        # stores input as spell corrected and caps in-sensitive 
        self.split_input = self.num_word_spell_check(inputedTime.split())
        self.split_input = [word.lower() if isinstance(word, str) else word
                           for word in self.split_input]
        # stores input without spaces
        self.spaceless_input = inputedTime.replace(" ","")
        # stores input as a list of characters
        self.list_input = list(self.spaceless_input)
        logger.debug(f"split input: {self.split_input}")
        logger.debug(f"spacless input: {self.spaceless_input}")
        logger.debug(f"list input: {self.list_input}")
                
    def num_word_spell_check(self, str):
        """Spell corrects an input and turns written words into ints

        Args:
            str (str): given string to check

        Returns:
            str (str): the corrected str 
        """
        spell = SpellChecker()
        for i,word in enumerate(str):
            # Corrects the spelling of the input
            if word not in spell:
                str[i] = spell.correction(word)
            # Replaces all written out numbers with intergers
            if word == "quarter":
                str[i] = 15
            if word == "half":
                str[i] = 30
            try:
                str[i] = w2n.word_to_num(word)
            except ValueError:
                pass
        return str
        
    def num_time_set_up(self):
        """Gains info around an input such as  where pm and period are."""
        # Checks if time is inputed as a period or am or pm are present
        if "period" in self.split_input:
            self.has_period = True
        if "pm" in self.split_input:
            self.has_pm = True
        if "am" in self.split_input:
            self.has_am = True
        logger.debug(f"pm: {self.has_pm}, am: {self.has_am}")
        logger.debug(f"has period: {self.has_period}")
                
        # Returns the time as a period if the time is given as a period
        if self.has_period:
            try:
                index = self.split_input.index("period")
                self.period = int(self.split_input[index + 1])
                logger.debug(f" period: {self.period}")
                return
            except:
                return
            
        self.num_time() # finds the time of written as a digit
        
    def num_time(self):
        """Finds the given time if time is written in digits"""
        # remove all words from the inputted time and make all digits ints
        self.int_list = [int(num) for num in self.list_input if num.isdigit()]
        self.period_int = "".join(map(str, self.int_list))
        self.period_int = int(self.period_int) if self.period_int else None
        logger.debug(f"period as int {self.period_int}")
        
        # return if no time present
        if self.period_int is None:
            logger.debug("no num time")
            return
        # return the time either in hours or hours and minutes
        if len(str(self.period_int)) in [3, 4]:
            self.time = (self.period_int/100)
        elif len(str(self.period_int)) in [1, 2]:
            self.time = self.period_int
        logger.debug(f"num time found {self.time}")

    def to_or_past_time(self):
        """Finds the time if written using to or past"""
        # find the location of the words to and past if present
        if "to" in self.split_input:
            self.to_or_past_index = self.split_input.index("to")
            self.hasTo = True
        if "past" in self.split_input:
            self.to_or_past_index = self.split_input.index("past")
            logger.debug(f"has to {self.has_to} pos: {self.to_or_past_index}")
        
        # Finds the hours and minutes in the time
        try:
            minutes = self.split_input[self.to_or_past_index - 1]
            hours = self.split_input[self.to_or_past_index + 1]
            offset = (-2 * self.has_to + 1) * minutes - 40 * self.has_to
            self.time = hours + offset / 100 # finds final time
            logger.debug(f"minutes {minutes}, hours {hours}, offset {offset}")
            return # returns with self.time being defined if time found
        except (IndexError, TypeError) as e:
            logger.debug(f"not long enough time {e}")
            pass
        self.word_time()

    def word_time(self):
        """Finds the time if time written in words"""
        # remove all words from input
        self.split_input = [int(i) for i in self.split_input
                           if str(i).isdigit()]
        logger.debug(f"integer list {self.split_input}")
        i = 0
        """iterate through list combining all numbers larger then 10
        with there next number e.g. 40, 5 become 45"""
        try:
            while i < len(self.split_input) - 1:
                if self.split_input[i] >= 10:
                    self.split_input[i] += self.split_input[i + 1]
                    self.split_input.pop(i + 1)
                else:
                    i += 1
            # store final time as self.time then end function
            logger.debug(f"concentrated integer list {self.split_input}")
            self.time = float(".".join([str(i) for i in self.split_input]))
        except ValueError:
            logger.warning("word time empty")
            pass
        except Exception:
            logger.critical("unknown error")
            raise

    def add_pm(self, time):
        """Converts time between am and pm.
        
        if either am or pm are stated the code will follow that,
        however if nothing is stated the code will assume the most logical one
        Args:
            time (float): The given time

        Returns:
            _type_: The given time changed however best fit
        """
        # if pm present add 12 hours to the time
        if self.has_pm and (time < 12):
            time += 12
        # automaticaly assumes school hours unless otherwise stated
        elif (self.has_am != True) and (time < 6):
            time += 12
        return time