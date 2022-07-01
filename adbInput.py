# pip install pure-python-adb
import time
import random
from ppadb.client import Client as AdbClient


def AdbConnect(instancePort):
    client = AdbClient(host="127.0.0.1", port=5037)
    client.remote_connect(host="localhost", port=instancePort)
    device = client.device("localhost:"+str(instancePort))
    return device


def RandomPosition(x, y, deltaX, deltaY):
    try:
        x = int(x)
        y = int(y)
        x = random.randint(x - deltaX, x + deltaX)
        y = random.randint(y - deltaY, y + deltaY)
    
        return x, y
    except:
        pass


def BlueStacksOffset(x, y): # 블루스택 이미지 서칭에서 가져온 위치로 터치하기 위해 블루스택 좌표로 변환
    try:
        x -= 1
        y -= 33
    
        return x, y
    except:
        pass


def Offset(x, y, offsetX, offsetY):
    x += offsetX
    y += offsetY
    return x, y


def AdbTap(device, x, y): # 0초 동안 누름
    device.shell("input touchscreen tap " + str(x) + " " + str(y))


def AdbSwipe(device, x, y, toX, toY, delay): # 딜레이를 줘서 누름
    device.shell("input swipe " + str(x) + " " + str(y) + " " + str(toX) + " " + str(toY) + " " + str(delay))


def BlueStacksClick(device, position, offsetX = 0, offsetY = 0, deltaX = 0, deltaY = 0):
    try:
        x, y, width, height = position
        x += width/2
        y += height/2
        x, y = BlueStacksOffset(x, y)
        x, y = Offset(x, y, offsetX, offsetY)
        x, y = RandomPosition(x, y, deltaX, deltaY)
        AdbSwipe(device, x, y, x, y, random.randint(50, 150))
        return True
    except:
        return False

if __name__ == "__main__":

    instancePort = 6205
    device = AdbConnect(instancePort)
    while 1:
        BlueStacksClick(device, (100, 100, 200, 200), offsetX = 0, offsetY = 0, deltaX = 5, deltaY = 5)
        
        # time.sleep(0.15)
        
        
# reference: https://lemon7z.tistory.com/96#%EC%-D%B-%EB%AF%B-%EC%A-%--%--%EC%--%-C%EC%B-%--%EC%--%--%--%EA%B-%B-%ED%--%A-%ED%--%--%EA%B-%B-%---%EC%-D%B-%ED%--%B-%--%ED%--%--%EC%-A%---