import datetime
import csv


with open('SYSTEMS.csv') as f:
    reader = csv.reader(f)
    ALLOWED_SYSTEMS = [l[0] for l in reader]


class IntelEntry:
    KEYS = ["timer_name", "alliance", "system", "time", "date", "location"]

    def __init__(self, timer_name="", alliance="", system="", time="", date="", location=""):
        if timer_name != "":
            self.timer_name = timer_name
        else:
            raise ValueError("Provided timer not valid.")

        if alliance != "":
            self.alliance = alliance.strip()
        else:
            raise ValueError("Provided alliance not valid.")

        system = system.upper()
        if system in ALLOWED_SYSTEMS:
            self.system = system
        else:
            raise ValueError("Provided solar system not valid.")

        self.location = location

        if time != "":
            self.time = datetime.datetime.strptime(' '.join([date, time]), '%m/%d/%y %H:%M')
            if self.time < datetime.datetime.now():
                raise ValueError("Provided date/time not valid. Time must be in the future.")
        else:
            raise ValueError("Provided date/time not valid. Time must be in format '%m/%d/%y %H:%M'.")

    def to_dict(self):
        return { "timer_name": self.timer_name,
                 "alliance": self.alliance,
                 "system": self.system,
                 "location": self.location,
                 "time": self.time }
