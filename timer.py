from zoneinfo import ZoneInfo, available_timezones
import datetime as dt
from datetime import timedelta
from pytz import timezone
import time
import copy


class timer:
    def __init__(self):
        now = dt.datetime.now()
        self.tz = now.astimezone()
        self.resetThen()

    def getThen(self):
        return self.then

    def resetThen(self):
        self.then = copy.deepcopy(dt.datetime.now())

    def beenSecond(self):
        if self.getThen().second is dt.datetime.now().second:
            return False
        else:
            self.resetThen()
            return True
    
    def beenMinute(self):
        if self.getThen().minute is dt.datetime.now().minute:
            return False
        else:
            self.resetThen()
            return True
    
    def beenHour(self):
        if self.getThen().hour is dt.datetime.now().hour:
            return False
        else:
            self.resetThen()
            return True

    def beenXmils(self, x):
        waitTill = self.then + timedelta(milliseconds = x)
        if waitTill > dt.datetime.now():
            return False
        else:
            self.resetThen()
            return True
        

if __name__ == '__main__':
    t = timer()

    while True:
        if t.beenXmils(1750):
            print(t.getThen())