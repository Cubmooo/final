from spellchecker import SpellChecker
from config import ClassConfig
from word2number import w2n
from logging_config import setup_logger
logger = setup_logger(__name__)

class Time:
    def __init__(self):
        self.month = None
        self.year = 25
        self.day = None
        self.date = None
        self.config = ClassConfig()
        self.month_list = self.file_to_dict(self.config.months_file)
        self.numbers_list = self.file_to_dict(self.config.numbers_file)
    
    # store inputed day as a attribute or Time    
    def add(self, inputed_day):
        self.day_input = inputed_day
        logger.debug(f"self.day_input {self.day_input}")
    
    # takes a file of nums or months and creates dict with same ints
    def file_to_dict(self, filepath):
        with open(filepath, "r") as file:
            return {line.strip(): i + 1 for i, line in enumerate(file)}
    
    # iterate through word in list spell checking it
    def spell_check(self, given_list):
        spell = SpellChecker()
        given_list = given_list.split()
        for i, word in enumerate(given_list):
            given_list[i] = spell.correction(word)
        return given_list
    
    # finds the date or period if given in digits          
    def num_day(self):
        # remove all words from list
        self.int_date = [i for i in self.day_input if i.isdigit()]
        logger.debug(f"date of ints {self.int_date}")
        try:
            # return the date if the inputted date is the right length
            if len(self.int_date) == 6:
                logger.debug("int date length 6")
                self.date = int("".join(self.int_date))
            elif len(self.int_date) == 4 and int(self.int_date) != 2025:
                logger.debug("int date length 4")
                self.date = int("".join(self.int_date) + "25")
            # return the school day if the input is one digit long
            elif len(self.int_date) == 1:
                logger.debug("int date length 1")
                self.day = self.int_date[0]
            
        # catch errors such as int_date having no numbers
        except (ValueError, TypeError, IndexError) as e:
            logger.debug(f"date not found: {e}")
            pass
        except Exception as e:
            logger.critical(f"unknown error {e}")
            raise
    
    # Finds the date if it is inputed in words
    def word_day(self):
        # ensure this function isnt run unnecessarily 
        if self.day is not None or self.date is not None:
            return
        # spell check input
        self.day_input = self.spell_check(self.day_input)
        self.combine_number_words()
        self.convert_words_to_ints()
        self.convert_digits_to_ints()
        self.define_date()
    
    def combine_number_words(self):   
        # make all two words numbers one e.g. twenty one -> twentyone
        i = 0
        while i < len(self.day_input):
            logger.debug(f"last bit of word {self.day_input[i][-6:]}")
            if (self.day_input[i][-6:] == "twenty"
                or self.day_input[i][-6:] == "thirty"):
                self.day_input[i] = self.day_input[i] + self.day_input[i + 1]
                self.day_input.pop(i + 1)
            else:
                i += 1
        logger.debug(f"combined words {self.day_input}")
        
    def convert_words_to_ints(self):
        # replace all months and numbers with ints
        for i,j in enumerate(self.day_input):
            self.day_input[i] = self.month_list.get(j, self.day_input[i])
            self.day_input[i] = self.numbers_list.get(j, self.day_input[i])
            logger.debug(f"start of j = {j[:6]}")
            if j[:6] == "twenty":
                logger.debug(f"year {j[:6]}, {j[6:]}")
                for letter in j[:6]:
                    if letter == y:
                        j
                logger.debug(f"year as num {self.day_input[i]}")
            
            
            # store the month to know date format
            if (self.month is None) and (j in self.month_list):
                self.month = self.month_list[j]
            
            # replace all typed digits with ints    
            if isinstance(j, str) and j.isdigit():
                self.day_input[i] = int(j)
            logger.debug(f"months as ints {self.day_input}")
            logger.debug(f"month: {self.month}")
    def convert_digits_to_ints(self):
        # coverts all items of list into ints
        self.day_input = [
            int(num) for num in self.day_input if isinstance(num, int)
            or (isinstance(num, str) and  num.isdigit())
        ]
    
    def define_date(self):
        normal_date_format = None
        # Finds the location of the month in the date
        if self.month in self.day_input:    
            normal_date_format = self.day_input.index(self.month) == 1
        logger.debug(f"normal_date_format = {normal_date_format}")
        # truncates the year if it is stated
        if len(self.day_input) >= 3:
            self.year = int(str(self.day_input[2])[-2:])
        # return date ensuring correct formating is used
        if normal_date_format is not None:
            self.month_day = self.day_input[-1 * (normal_date_format - 1)]
            logger.debug(f"day: {self.month_day}")
            logger.debug(f"month: {self.month}")
            logger.debug(f"year: {self.year}")
            self.date = self.month_day * 10000 + self.month * 100 + self.year