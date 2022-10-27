from time import time, localtime, strftime


def getWDay():
    return localtime(time()).tm_wday


class Time:
    def __init__(self):
        self.pre = getWDay()

    def isDayChange(self):
        wday = getWDay()
        ans = wday != self.pre
        self.pre = wday
        return ans

    def getTime(self):
        return strftime('%H:%M:%S', localtime(time()))

    def getDate(self):
        return strftime('%Y%m%d', localtime(time()))
