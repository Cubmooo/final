import json

class ClassConfig:
    def __init__(self, config_path = "config.json"):
        try:
            with open(config_path) as f:
                self.data = json.load(f)
            
            self.numbers_file = self.data.get("numbers_file")
            self.months_file = self.data.get("months_file")
            self.yes_file = self.data.get("yes_file")
            self.no_file = self.data.get("no_file")
            self.periods_file = self.data.get("periods_file")
            self.calendar_file = self.data.get("calender_file")
            self.teacher_file = self.data.get("teacher_file")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file: {config_path}")