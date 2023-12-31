from AdbInput import AdbInput
import WindowsAPIInput
import random
import ImageSearch


class BlueStacksController:
    instancePort = 0

    def __init__(self, instanceName: str, instancePort: int):
        self.getHwnd(instanceName)
        if self.hwnd == 0:
            raise Exception("No BlueStacks Instance Found")
        self.instancePort = instancePort
        self.connectAdb(instancePort)

    def getHwnd(self, instanceName: str):
        """# hwnd ID 찾기"""
        self.hwnd = WindowsAPIInput.GetHwnd(instanceName)

    def setWindowSize(self, width: int, height: int) -> bool:
        return WindowsAPIInput.SetWindowSize(self.hwnd, width, height)

    def WindowsAPIKeyboardInput(self, key):
        WindowsAPIInput.WindowsAPIKeyboardInput(self.hwnd, key)

    def WindowsAPIKeyboardInputString(self, contents):
        WindowsAPIInput.WindowsAPIKeyboardInputString(self.hwnd, contents)

    def WindowsAPIMouseClick(self, x, y):
        WindowsAPIInput.WindowsAPIMouseClick(self.hwnd, x, y)

    def getScreenShot(self):
        """윈도우의 스크린샷"""
        return ImageSearch.screenshot_to_opencv_img(self.hwnd)

    def connectAdb(self, instancePort: int):
        self.device = AdbInput(instancePort)

    def shell(self, command: str):
        self.device.shell(command)

    def getBlueStacksOffset(self, x, y):
        """블루스택 이미지 서칭에서 가져온 위치로 터치하기 위해 블루스택 좌표로 변환"""
        x -= 1
        y -= 33
        return x, y

    def tap(self, position, offsetX=0, offsetY=0, deltaX=0, deltaY=0):
        x, y, width, height = position
        x += width / 2
        y += height / 2
        x, y = self.getBlueStacksOffset(x, y)
        x, y = self.device.offset(x, y, offsetX, offsetY)
        x, y = self.device.randomPosition(x, y, deltaX, deltaY)
        self.device.tap(x, y)

    def swipe(self, position, offsetX=0, offsetY=0, deltaX=0, deltaY=0):
        """
        tap보다 swipe를 사용하는 이유: 블루스택에서는 tap이 잘 안먹힘,
        터치가 눌렸다 바로 떼어지는 경우 인식이 안되는 경우가 있음
        """
        x, y, width, height = position
        x += width / 2
        y += height / 2
        x, y = self.getBlueStacksOffset(x, y)
        x, y = self.device.offset(x, y, offsetX, offsetY)
        x, y = self.device.randomPosition(x, y, deltaX, deltaY)
        self.device.swipe(x, y, x, y, random.randint(25, 75))

    def keyEvent(self, key_code: str) -> bool:
        return self.device.keyEvent(key_code)


if __name__ == "__main__":
    """TEST CODE"""
    device = BlueStacksController("BlueStacks 1", 12167)
    device.setWindowSize(574, 994)
    img = device.getScreenShot()

    # device.tap((200, 200, 0, 0))
    # device.swipe((100, 100, 200, 200))

    # device.shell("input keyevent 4")
