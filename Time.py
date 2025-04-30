from spellchecker import SpellChecker
from config import ClassConfig
from word2number import w2n
from logging_config import setup_logger
logger = setup_logger(__name__)

class Time:
    def __init__(self):
        self.month = None
        self.month_day = None
        self.year = None
        self.day = None
        self.date = None
        self.year_list = None
        self.has_day = False
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
    
    def word_day(self):
        self.contract_words()
        self.month_to_num()
        self.day_to_num()
        self.short_year_to_num()
    
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
    
    def month_to_num(self):
        for i,j in enumerate(self.list_input):
            self.list_input[i] = self.month_list.get(j, self.list_input[i])
            if self.list_input[i] != j:
                self.month = self.list_input[i]
            logger.debug(f"input {self.list_input}")
            logger.debug(f"month:{self.month}")
    
    def day_to_num(self):
        for i,j in enumerate(self.list_input):
            self.list_input[i] = self.numbers_list.get(j, self.list_input[i])
            if self.list_input[i] != j:
                self.month_day = self.list_input[i]
            logger.debug(f"input {self.list_input}")
            logger.debug(f"day:{self.month_day}")
            
    def short_year_to_num(self):
        for i,j in enumerate(self.list_input):
            if isinstance(j, str):
                self.list_input[i] = j.replace("teen", "teen ")
                self.list_input[i] = j.replace("ty", "ty ")
                if self.list_input[i] != j:
                    self.year_list = self.list_input[i].split()
                    logger.debug(f"split list: {self.year_list}")
                    break
        if self.year_list == None:
            logger.debug(f"list not split")
            return
        
        for i,j in enumerate(self.year_list):
            self.year_list[i] = w2n.word_to_num(j)
        logger.debug(f"num split list: {self.year_list}")
        
        if len(self.year_list) == 3:
            self.year = self.year_list[0] * 100 + sum(self.year_list[1:3])
        logger.debug(f"year: {self.year}")
        
    def num_day(self):
        self.digit_to_num()
        self.compare_date()
        
    def digit_to_num(self):
        if "day" in self.list_input:
            self.has_day = True
        self.list_input = [int(i) for i in self.list_input if isinstance(i, str) and i.isdigit()]
        if self.has_day and len(self.list_input) == 1:
            self.day = self.list_input[0]
        logger.debug(f"num list: {self.list_input}")
        
    def compare_date(self):
        if None not in (self.month_day, self.month, self.year):
            self.final_date()
            return
        if len(self.list_input) > 0:
            if self.month is None and self.month_day is not None:
                self.month = self.list_input[0]
                self.list_input.pop(0)
            elif self.month_day is None and self.month is not None:
                self.month_day = self.list_input[0]
                self.list_input.pop(0)
        if None not in (self.month_day, self.month):
            self.year = self.list_input[0] if self.list_input else 25
            self.final_date()
        if all(x is None for x in (self.month_day, self.month)):
            if len(self.list_input) in [2, 3]:
                self.month_day = self.list_input[0]
                self.month = self.list_input[1]
                if len(self.list_input) == 3 and self.year is None:
                    self.year = self.list_input[2]
                else:
                    self.year = 25
                self.final_date()
                    
                
    def final_date(self):
        logger.debug(f"info long{self.month_day}:{self.month}:{self.year}")
        logger.debug(f"info{self.month_day:02d}:{self.month:02d}:{self.year % 100}")
        self.date = f"{self.month_day:02d}{self.month:02d}{self.year % 100}"
        logger.info(f"date: {self.date}")