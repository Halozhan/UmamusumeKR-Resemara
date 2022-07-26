import time
import random
from ppadb.client import Client as AdbClient
import subprocess

def AdbConnect(InstancePort) -> AdbClient.device:
    try:
        client = AdbClient(host="127.0.0.1", port=5037)
        client.remote_connect(host="localhost", port=InstancePort)
        device = client.device("localhost:"+str(InstancePort))
        return device
    except:
        print("Fail to connect to adb, retry")
        
        subprocess.Popen("platform-tools/adb.exe start-server")
        time.sleep(1)
        
        client = AdbClient(host="127.0.0.1", port=5037)
        client.remote_connect(host="localhost", port=InstancePort)
        device = client.device("localhost:"+str(InstancePort))
        return device

def RandomPosition(x, y, deltaX, deltaY):
    try:
        x = int(x)
        y = int(y)
        x = random.randint(x - deltaX, x + deltaX)
        y = random.randint(y - deltaY, y + deltaY)
    
        return x, y
    except: pass

def BlueStacksOffset(x, y): # 블루스택 이미지 서칭에서 가져온 위치로 터치하기 위해 블루스택 좌표로 변환
    try:
        x -= 1
        y -= 33
    
        return x, y
    except: pass

def Offset(x, y, offsetX, offsetY):
    x += offsetX
    y += offsetY
    return x, y

def shell(device: AdbClient.device, InstancePort, shell: str):
    try:
        device.shell(shell)
    except:
        AdbConnect(InstancePort)
        try:
            device.shell(shell)
        except: pass

def AdbTap(device: AdbClient.device, InstancePort, x, y): # 0초 동안 누름
    try:
        device.shell("input touchscreen tap " + str(x) + " " + str(y))
    except:
        AdbConnect(InstancePort)
        try:
            device.shell("input touchscreen tap " + str(x) + " " + str(y))
        except: pass

def AdbSwipe(device: AdbClient.device, InstancePort, x, y, toX, toY, delay): # 딜레이를 줘서 누름
    try:
        device.shell("input swipe " + str(x) + " " + str(y) + " " + str(toX) + " " + str(toY) + " " + str(delay))
    except:
        AdbConnect(InstancePort)
        try:
            device.shell("input swipe " + str(x) + " " + str(y) + " " + str(toX) + " " + str(toY) + " " + str(delay))
        except: pass

def Key_event(device: AdbClient.device, InstancePort, key_code:str):
    try:
        device.shell("input " + str(key_code))
    except:
        AdbConnect(InstancePort)
        try:
            device.shell("input " + str(key_code))
        except: pass
    
def BlueStacksTap(device: AdbClient.device, InstancePort, position, offsetX = 0, offsetY = 0, deltaX = 0, deltaY = 0):
    try:
        x, y, width, height = position
        x += width/2
        y += height/2
        x, y = BlueStacksOffset(x, y)
        x, y = Offset(x, y, offsetX, offsetY)
        x, y = RandomPosition(x, y, deltaX, deltaY)
        AdbTap(device, InstancePort, x, y)
        return True
    except:
        try:
            AdbConnect(InstancePort)
            x, y, width, height = position
            x += width/2
            y += height/2
            x, y = BlueStacksOffset(x, y)
            x, y = Offset(x, y, offsetX, offsetY)
            x, y = RandomPosition(x, y, deltaX, deltaY)
            AdbTap(device, InstancePort, x, y)
        except: pass
        return False

def BlueStacksSwipe(device: AdbClient.device, InstancePort, position, offsetX = 0, offsetY = 0, deltaX = 0, deltaY = 0):
    try:
        x, y, width, height = position
        x += width/2
        y += height/2
        x, y = BlueStacksOffset(x, y)
        x, y = Offset(x, y, offsetX, offsetY)
        x, y = RandomPosition(x, y, deltaX, deltaY)
        AdbSwipe(device, InstancePort, x, y, x, y, random.randint(25, 75))
        return True
    except:
        AdbConnect(InstancePort)
        x, y, width, height = position
        x += width/2
        y += height/2
        x, y = BlueStacksOffset(x, y)
        x, y = Offset(x, y, offsetX, offsetY)
        x, y = RandomPosition(x, y, deltaX, deltaY)
        AdbSwipe(device, InstancePort, x, y, x, y, random.randint(25, 75))
        return False

if __name__ == "__main__":

    InstancePort = 6415
    device = AdbConnect(InstancePort)
    # device.shell("am force-stop org.mozilla.firefox")
    while 1:
        BlueStacksSwipe(device, InstancePort, (100, 100, 200, 200), offsetX = 0, offsetY = 0, deltaX = 5, deltaY = 5)
        
        time.sleep(0.1)

        
        
# reference: https://lemon7z.tistory.com/96#%EC%-D%B-%EB%AF%B-%EC%A-%--%--%EC%--%-C%EC%B-%--%EC%--%--%--%EA%B-%B-%ED%--%A-%ED%--%--%EA%B-%B-%---%EC%-D%B-%ED%--%B-%--%ED%--%--%EC%-A%---