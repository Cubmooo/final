from spellchecker import SpellChecker
from word2number import w2n

class Period:
    def __init__(self):
        self.has_pm = False
        self.has_am = False
        self.has_period = False
        self.time = None
        self.period = None
        self.to_or_past_index = None
        self.has_to = False
    
    # Store the users time input as various attributes
    def add(self, inputedTime):
        # stores input as spell corrected and caps in-sensitive 
        self.split_input = self.num_word_spell_check(inputedTime.split())
        self.split_input = [word.lower() if isinstance(word, str) else word
                           for word in self.split_input]
        self.spaceless_input = inputedTime.replace(" ","")
        self.list_input = list(self.spaceless_input)
                
    def num_word_spell_check(self, str):
        # iterates through the inputs
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
            str[i] = w2n.word_to_num(word) if str[i].isdigit() else word
        return str
    
    # find the time if written in a hour minute format    
    def num_time(self):
        # Checks if time is inputed as a period or am or pm are present
        if "period" in self.split_input:
            self.has_period = True
        if "pm" in self.split_input:
            self.has_pm = True
        if "am" in self.split_input:
            self.has_am = True
        
        # Returns the time as a period if the time is given as a period
        if self.has_period:
            try:
                index = self.split_input.index("period")
                self.period = int(self.split_input[index + 1])
                return
            except:
                pass
        
        # remove all words from the inputted time
        self.int_list = [int(num) for num in self.list_input if num.isdigit()]
        self.period_int = "".join(map(str, self.int_list))
        self.period_int = int(self.period_int) if self.period_int else None
        
        # return if no time present
        if self.period_int is None:
            return
        # return the time either in hours or hours and minutes
        if len(str(self.period_int)) in [3, 4]:
            self.time = (self.period_int/100)
        elif len(str(self.period_int)) in [1, 2]:
            self.time = self.period_int

    def word_time(self):
        # find the location of the words to and past if present
        if "to" in self.split_input:
            self.to_or_past_index = self.split_input.index("to")
            self.hasTo = True
        if "past" in self.split_input:
            self.to_or_past_index = self.split_input.index("past")
        
        # Finds the time based on the location found earlier
        try:
            minutes = self.split_input[self.to_or_past_index - 1]
            hours = self.split_input[self.to_or_past_index + 1]
            offset = (-2 * self.has_to + 1) * minutes - 40 * self.has_to
            self.time = hours + offset / 100
            return
        except:
            pass
        
        # remove all words from input
        self.split_input = [int(i) for i in self.split_input
                           if str(i).isdigit()]
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
            # return final time
            self.time = float(".".join([str(i) for i in self.split_input]))
        except:
            pass

    # converts 12 hour time to 24 hour time
    def add_pm(self, time):
        if self.has_pm and (time < 12):
            time += 12
        # automaticaly assumes school hours unless otherwise stated
        elif (self.has_am != True) and (time < 6):
            time += 12
        return time