import time
import random
from ppadb.client import Client as AdbClient
from ppadb.device import Device
import subprocess
import os


class AdbInput():
    MAX_RETRY_COUNT = 5

    def __init__(self, port) -> None:
        self.port = port
        self.connect()

    def startAdbServer(self):
        subprocess.Popen(
            os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
            + "/platform-tools/adb.exe start-server"
        )

    def connect(self) -> bool:
        retryCount = 0
        while retryCount <= self.MAX_RETRY_COUNT:
            try:
                client = AdbClient(host="127.0.0.1", port=5037)
                client.remote_connect(host="localhost", port=self.port)
                device = client.device("localhost:" + str(self.port))
                self.device: Device = device
                return True

            except Exception:
                retryCount += 1
                print("Fail to connect to adb, retry")
                self.startAdbServer()
                time.sleep(1)

        return False

    def randomPosition(self, x, y, deltaX, deltaY):
        x = int(x)
        y = int(y)
        x = random.randint(x - deltaX, x + deltaX)
        y = random.randint(y - deltaY, y + deltaY)

        return x, y

    def offset(self, x, y, offsetX, offsetY):
        x += offsetX
        y += offsetY
        return x, y

    def shell(self, command: str) -> bool:
        retryCount = 0
        while retryCount <= self.MAX_RETRY_COUNT:
            try:
                self.device.shell(command)
                return True

            except Exception:
                retryCount += 1
                self.connect()

        return False

    def tap(self, x, y) -> bool:  # 0초 동안 누름
        retryCount = 0
        while retryCount <= self.MAX_RETRY_COUNT:
            try:
                self.device.shell("input touchscreen tap " + str(x) + " " + str(y))
                return True

            except Exception:
                retryCount += 1
                self.connect()

        return False

    def swipe(self, x, y, toX, toY, delay) -> bool:
        retryCount = 0
        while retryCount <= self.MAX_RETRY_COUNT:
            try:
                self.device.shell(
                    "input swipe "
                    + str(x)
                    + " "
                    + str(y)
                    + " "
                    + str(toX)
                    + " "
                    + str(toY)
                    + " "
                    + str(delay)
                )
                return True

            except Exception:
                retryCount += 1
                self.connect()

        return False

    def keyEvent(self, key_code: str) -> bool:
        retryCount = 0
        while retryCount <= self.MAX_RETRY_COUNT:
            try:
                self.device.shell("input " + str(key_code))
                return True

            except Exception:
                retryCount += 1
                self.connect()
        return False


if __name__ == "__main__":
    """TEST CODE"""
    instancePort = 7894
    device = AdbInput(instancePort)
    # device.shell("am force-stop org.mozilla.firefox")
    while True:
        device.swipe(100, 100, 200, 200, 1000)
        time.sleep(0.1)

# reference: https://lemon7z.tistory.com/96#%EC%-D%B-%EB%AF%B-%EC%A-%--%--%EC%--%-C%EC%B-%--%EC%--%--%--%EA%B-%B-%ED%--%A-%ED%--%--%EA%B-%B-%---%EC%-D%B-%ED%--%B-%--%ED%--%--%EC%-A%---
