from PyQt5.QtCore import QThread, pyqtSignal
import time
import psutil
from datetime import datetime
import math


class sleepTime(QThread):    
    sendSleepTime = pyqtSignal(float)
    
    def __init__(self, parent = None):
        
        super().__init__()
        
        if parent is not None:
            self.parent = parent
        self.isAlive = True
        self.sleepTime = 0.5
        self.now = time.time()

        self.sendSleepTime.connect(self.parent.SleepTimeFunction)
    
    def run(self):
        while self.isAlive:
            
            # CPU 풀로드 완화
            now = datetime.now()
            cpu_load = psutil.cpu_percent()
            if cpu_load <= 1: # 오류 무시
                pass
            else:
                self.sleepTime = round(((cpu_load*0.01)**(1.5*math.exp(1)))*8, 3) # 클수록 빨라짐
                self.sendSleepTime.emit(self.sleepTime)
                    
            if time.time() >= self.now + 2:
                self.now = time.time()
                print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                print(now.strftime("%H:%M:%S") + " 속도: " + str(int(self.sleepTime * 1000)) + "ms")

            time.sleep(0.05)