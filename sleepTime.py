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
            if cpu_load <= 1: # 오류 무시
                pass
            # 속도 감소
            elif cpu_load >= 99:
                if self.sleepTime < 5: # 최고 지연
                    self.sleepTime += 2
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 97:
                if self.sleepTime < 5:
                    self.sleepTime += 1.5
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 93:
                if self.sleepTime < 5:
                    self.sleepTime += 1
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 90:
                if self.sleepTime < 5:
                    self.sleepTime += 0.8
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 87:
                if self.sleepTime < 5:
                    self.sleepTime += 0.6
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 83:
                if self.sleepTime < 5:
                    self.sleepTime += 0.4
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load >= 80:
                if self.sleepTime < 5:
                    self.sleepTime += 0.35
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 77:
                if self.sleepTime < 5:
                    self.sleepTime += 0.3
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 73:
                if self.sleepTime < 5:
                    self.sleepTime += 0.25
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 70:
                if self.sleepTime < 5:
                    self.sleepTime += 0.2
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 67:
                if self.sleepTime < 5:
                    self.sleepTime += 0.15
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 63:
                if self.sleepTime < 5:
                    self.sleepTime += 0.1
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            elif cpu_load >= 60:
                if self.sleepTime < 5:
                    self.sleepTime += 0.05
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 감소: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)


            # 속도 증가
            elif cpu_load <= 2:
                if self.sleepTime > 1.05:
                    self.sleepTime -= 1
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 3:
                if self.sleepTime > 1:
                    self.sleepTime -= 0.95
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 7:
                if self.sleepTime > 0.95:
                    self.sleepTime -= 0.9
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 10:
                if self.sleepTime > 0.9:
                    self.sleepTime -= 0.85
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 13:
                if self.sleepTime > 0.85:
                    self.sleepTime -= 0.8
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 17:
                if self.sleepTime > 0.8:
                    self.sleepTime -= 0.75
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 20:
                if self.sleepTime > 0.75:
                    self.sleepTime -= 0.7
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 23:
                if self.sleepTime > 0.7:
                    self.sleepTime -= 0.65
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 27:
                if self.sleepTime > 0.65:
                    self.sleepTime -= 0.6
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 30:
                if self.sleepTime > 0.6:
                    self.sleepTime -= 0.55
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 33:
                if self.sleepTime > 0.55:
                    self.sleepTime -= 0.5
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 37:
                if self.sleepTime > 0.5:
                    self.sleepTime -= 0.45
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 40:
                if self.sleepTime > 0.45:
                    self.sleepTime -= 0.4
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 43:
                if self.sleepTime > 0.45:
                    self.sleepTime -= 0.4
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 47:
                if self.sleepTime > 0.4:
                    self.sleepTime -= 0.35
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 50:
                if self.sleepTime > 0.35:
                    self.sleepTime -= 0.3
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 53:
                if self.sleepTime > 0.3:
                    self.sleepTime -= 0.25
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 57:
                if self.sleepTime > 0.25:
                    self.sleepTime -= 0.2
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 60:
                if self.sleepTime > 0.2:
                    self.sleepTime -= 0.15
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)

            elif cpu_load <= 63:
                if self.sleepTime > 0.15:
                    self.sleepTime -= 0.1
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
            
            elif cpu_load <= 67:
                if self.sleepTime > 0.1: # 최저 지연
                    self.sleepTime -= 0.05
                    self.sleepTime = round(self.sleepTime, 2)
                    print(now.strftime("%H:%M:%S") + " cpu 사용량: " + str(cpu_load) + "%")
                    print(now.strftime("%H:%M:%S") + " 속도 증가: " + str(self.sleepTime) + "s")
                    self.sendSleepTime.emit(self.sleepTime)
                    
            time.sleep(2)