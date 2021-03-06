import datetime as dt
from datetime import timedelta
from pytz import timezone
import time
import copy

import io 
import os

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

class timer:
    def __init__(self):
        now = dt.datetime.now()
        self.tz = now.astimezone()
        self.__resetThen()

    def getNow(self):
        return (self.getHour() * 100 + self.getMin())

    def getHour(self):
        now = dt.datetime.now()
        hour = (now.hour) % 12
        if is_raspberrypi():
            hour = (now.hour - 4) % 12
        if hour == 0:
            hour = 12
        return hour

    def getMin(self):
        return dt.datetime.now().minute

    def getThen(self):
        return self.then

    def __resetThen(self):
        self.then = copy.deepcopy(dt.datetime.now())

    def beenSecond(self):
        if self.getThen().second is dt.datetime.now().second:
            return False
        else:
            self.__resetThen()
            return True
    
    def beenMinute(self):
        if self.getThen().minute is dt.datetime.now().minute:
            return False
        else:
            self.__resetThen()
            return True
    
    def beenHour(self):
        if self.getThen().hour is dt.datetime.now().hour:
            return False
        else:
            self.__resetThen()
            return True

    def beenXmils(self, x):
        waitTill = self.then + timedelta(milliseconds = x)
        if waitTill > dt.datetime.now():
            return False
        else:
            self.__resetThen()
            return True      

if __name__ == '__main__':
    t = timer()
    while True:
        if t.beenMinute():
            print(t.getNow())