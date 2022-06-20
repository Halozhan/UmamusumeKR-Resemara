import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# install("wmi")
# install("pyautogui")
# install("psutil")
# install("pywin32")
# install("pywinauto")
# install("opencv-python")
# install("pillow")
# install("pyinstaller")
# 관리자 권한 필요함

import pyautogui
import subprocess
import psutil
import time
import pygetwindow as gw

main_location = "./"
confirm_location = main_location+"confirm.png"

def main():

    for i in range(4):
        # ImageMaxPName = "iMax.exe"
        subprocess.Popen(main_location+str(i+1)+"\\iMax.exe")
    # while True:
    # for i in range(14): # 개수 설정
        # time.sleep(2)
        # try:
        #     # start(i+1, main_location+str(i+1)+"\\iMax_"+str(i+1)+".exe")
        #     # start(i+1, main_location+str(i+1)+"\\iMax_.exe")
        #     # pyautogui.click(pyautogui.locateCenterOnScreen(confirm_location).x, pyautogui.locateCenterOnScreen(confirm_location).y + 50)
        #     # confirm = pyautogui.locateCenterOnScreen(confirm_location, confidence=0.98)
        #     # print(confirm.index())
        #     # originalPoint = pyautogui.position()
        #     # pyautogui.moveTo(confirm.x, confirm.y + 50)
        #     # pyautogui.moveTo(originalPoint)
        #     # print(confirm.x, confirm.y)
        # except:
        #     pass
    

def isImageMaxAlive(processName):
    for q in psutil.process_iter():
        if q.name() == processName:
            return True        
    return False


def isBlueStacksAlive(processName):
    title = gw.getAllTitles()
    if processName in title:
        return True
    return False


def start(n, location):
    ImageMaxPName = "iMax_"+str(n)+".exe"
    BlueStacksName = "BlueStacks "+str(n)
    if isBlueStacksAlive(BlueStacksName) and not isImageMaxAlive(ImageMaxPName):
        print(ImageMaxPName, "이 재시작됩니다.")
        subprocess.Popen(location)
        time.sleep(2)
        return True
    return False


main()