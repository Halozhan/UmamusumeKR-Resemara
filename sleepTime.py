from PyQt5.QtCore import QThread, pyqtSignal
import time
import psutil
from datetime import datetime
import math


class sleepTime(QThread):    
    sendSleepTime = pyqtSignal(float, float)
    
    def __init__(self, parent = None):
        super().__init__()
        
        if parent is not None:
            self.parent = parent
        self.isAlive = True
        self.sleepTime = 0.5

        self.sendSleepTime.connect(self.parent.SleepTimeFunction)
    
    def run(self):
        while self.isAlive:
            
            # CPU 풀로드 완화
            self.cpu_load = psutil.cpu_percent()
            if self.cpu_load <= 1: # 오류 무시
                pass
            else:
                self.sleepTime = round(((self.cpu_load*0.01)**(1.8*math.exp(1)))*8, 3) # 클수록 빨라짐
                self.sendSleepTime.emit(self.cpu_load, self.sleepTime)

            time.sleep(0.05)