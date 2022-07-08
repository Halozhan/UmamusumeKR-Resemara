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

main_location = "./"
Random_MAC_Address_Path = main_location+"Random_MAC_Address.png"
Change_Now_Path = main_location+"Change_Now.png"

def PAG_MAC_Change():
        try:
            Random_MAC_Address = pyautogui.locateCenterOnScreen(Random_MAC_Address_Path, confidence=0.95)
            originalPoint = pyautogui.position()
            pyautogui.click(Random_MAC_Address.x, Random_MAC_Address.y)
            time.sleep(0.1)
            pyautogui.click(Random_MAC_Address.x, Random_MAC_Address.y)
            time.sleep(0.1)
            
            Change_Now = pyautogui.locateCenterOnScreen(Change_Now_Path, confidence=0.95)
            originalPoint = pyautogui.position()
            pyautogui.click(Change_Now.x, Change_Now.y)
            
            pyautogui.moveTo(originalPoint)
        except:
            pass
        
        
PAG_MAC_Change()