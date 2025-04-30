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
        self.list_input = self.day_input.replace("/"," ").split()
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
    
    def num_day(self):
        self.contract_words()
    
    def contract_words(self):
        i = 0
        while i < len(self.list_input):
            logger.debug(f"i, input {i, self.list_input}")
            try:
                if (self.list_input[i][-6:] == "twenty"
                    or self.list_input[i][-6:] == "thirty"):
                    try:
                        self.list_input[i] = self.list_input[i] + self.list_input[i + 1]
                        self.list_input.pop(i + 1)
                    except:
                        i += 1
                else:
                    i += 1
            except:
                i =+ 1
        logger.debug(f"contracted: {self.list_input}")
        
    """
    def convert_words_to_nums(self):
        
        for i,j in self.enumerate(self.list_input):
            self.list_input[i] = self.month_list.get(j, self.list_input[i])
            if i = number
                self.month_day = i
            if i = month
                self.month = i
            if i = year
                self.year = i
                
        if loc(month) = 0
            day = self.list_input[1]
        else
            day = [0] and month = [1]
        
        
        year = month pos + 1 or day pos + 1
        """