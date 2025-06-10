
import datetime
class Time():
    def __init__(self):
        self.now = datetime.datetime.now()

    def getStrYMD(self):
        return self.now.strftime('%Y-%m-%d')

    def getStrYMD2(self):
        return self.now.strftime('%Y%m%d_%H%M')

    def getStrYMDT(self):
        return self.now.strftime('%Y-%m-%d %H:%M:%S')

    def getNow(self):
        return  datetime.datetime.now()

    def getdeltaToSecond(self,datetime):
        return(datetime - self.now).seconds



    def getTimeSub(self,startTime,endTime):
        return(endTime - startTime).seconds


