from PyQt5.QtCore import QThread, pyqtSignal
import time
import psutil
from datetime import datetime


class sleepTime(QThread):    
    sendSleepTime = pyqtSignal(float)
    
    def __init__(self, parent = None):
        
        super().__init__()
        
        if parent is not None:
            self.parent = parent
        self.isAlive = True
        self.sleepTime = 0.5

        self.sendSleepTime.connect(self.parent.SleepTimeFunction)
        
    # def terminate(self) -> None:
    #     return super().terminate()
    
    def run(self):
        while self.isAlive:
            # CPU 풀로드 완화
            now = datetime.now()
            cpu_load = psutil.cpu_percent()
            if cpu_load <= 1:
                pass
            elif cpu_load >= 99:
                if self.sleepTime < 5: # 최고 지연
                    self.sleepTime += 2
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 97.5:
                if self.sleepTime < 5:
                    self.sleepTime += 1.5
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 95:
                if self.sleepTime < 0.5:
                    self.sleepTime += 0.8
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 92.5:
                if self.sleepTime < 5:
                    self.sleepTime += 0.6
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 90:
                if self.sleepTime < 5:
                    self.sleepTime += 0.4
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 87.5:
                if self.sleepTime < 5:
                    self.sleepTime += 0.3
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load >= 85:
                if self.sleepTime < 5:
                    self.sleepTime += 0.2
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 82.5:
                if self.sleepTime < 5:
                    self.sleepTime += 0.1
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 80:
                if self.sleepTime < 5:
                    self.sleepTime += 0.05
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            else:
                if self.sleepTime > 0.2: # 최저 지연
                    self.sleepTime -= 0.1
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            time.sleep(1)