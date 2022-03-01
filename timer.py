from zoneinfo import ZoneInfo, available_timezones
from datetime import datetime, timedelta
import time
import copy


class timer:
    def __init__(self):
        self.then = copy.deepcopy(time.localtime())

    def getThen(self):
        return self.then

    def beenSecond(self):
        if self.then.tm_sec is time.localtime().tm_sec:
            return False
        else:
            self.then = copy.deepcopy(time.localtime())
            return True
    
    def beenMinute(self):
        if self.then.tm_min is time.localtime().tm_min:
            return False
        else:
            self.then = copy.deepcopy(time.localtime())
            return True
    
    def beenHour(self):
        if self.then.tm_hour is time.localtime().tm_hour:
            return False
        else:
            self.then = copy.deepcopy(time.localtime())
            return True

if __name__ == '__main__':
    dt = different_time()

    while True:
        if dt.beenMinute():
            print(dt.getThen().tm_min)