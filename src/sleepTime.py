from PyQt5.QtCore import QThread, pyqtSignal
import time
import psutil
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyqtWidget import WindowClass


class sleepTime(QThread):
    sendSleepTime = pyqtSignal(float, float)

    def __init__(self, parent: "WindowClass"):
        super().__init__()
        self.parent = parent

        self.isAlive = True
        self.sleepTime = 0.5
        self.timeRate1 = 1.8
        self.timeRate2 = 8

        self.sendSleepTime.connect(self.parent.SleepTimeFunction)

    def run(self):
        while self.isAlive:
            # CPU 풀로드 완화
            self.cpu_load = psutil.cpu_percent()
            if self.cpu_load <= 1:  # 오류 무시
                pass
            else:
                self.sleepTime = round(
                    ((self.cpu_load * 0.01) ** (self.timeRate1 * math.exp(1)))
                    * self.timeRate2,
                    3,
                )  # 클수록 빨라짐
                self.sendSleepTime.emit(self.cpu_load, self.sleepTime)

            time.sleep(0.1)
