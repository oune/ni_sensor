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

    def getNow(self):
        return strftime('%H:%M:%S', localtime(time()))
