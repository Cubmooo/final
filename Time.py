from spellchecker import SpellChecker
from config import ClassConfig

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
        try:
            print(self.int_date)
            # return the date if the inputted date is the right length
            if len(self.int_date) == 6:
                print("test")
                self.date = int("".join(self.int_date))
            if len(self.int_date) == 4 and int(self.int_date) != 2025:
                self.date = int("".join(self.int_date) + "25")
            # return the period if the input is one digit long
            if len(self.int_date) == 1:
                self.day = self.int_date[0]
        except:
            pass
    
    # Finds the date if it is inputed in words
    def word_day(self):
        # ensure this function isnt run unnecessarily 
        if self.day is not None or self.date is not None:
            return
        # spell check input
        self.day_input = self.spell_check(self.day_input)
       
        # make all two words numbers one e.g. twenty one -> twentyone
        for i,j in enumerate(self.day_input):
            if j == "twenty" or j == "thirty":
                self.day_input[i] = self.day_input[i] + self.day_input[i + 1]
                self.day_input.pop(i + 1)
        
        # replace all months and numbers with ints
        for i,j in enumerate(self.day_input):
            self.day_input[i] = self.month_list.get(j, self.day_input[i])
            self.day_input[i] = self.numbers_list.get(j, self.day_input[i])
            
            # store the month to know date format
            if (self.month is None) and (j in self.month_list):
                self.month = self.month_list[j]
            
            # replace all typed digits with ints    
            if isinstance(j, str) and j.isdigit():
                self.day_input[i] = int(j)
        
        # coverts all items of list into ints
        self.day_input = [
            int(num) for num in self.day_input if isinstance(num, int)
            or (isinstance(num, str) and  num.isdigit())
        ]
        
        normal_date_format = None
        # Finds the location of the month in the date
        if self.month in self.day_input:    
            normal_date_format = self.day_input.index(self.month) == 1
        # truncates the year if it is stated
        if len(self.day_input) >= 3:
            self.year = int(str(self.day_input[2])[-2:])
        # return date ensuring correct formating is used
        if normal_date_format is not None:
            self.month_day = self.day_input[-1 * (normal_date_format - 1)]
            self.date = self.month_day * 10000 + self.month * 100 + self.year