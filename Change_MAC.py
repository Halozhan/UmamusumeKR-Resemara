import sys
import pyautogui
import subprocess
import time

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

main_location = "./"
Random_MAC_Address_Path = main_location+"Random_MAC_Address.png"
Change_Now_Path = main_location+"Change_Now.png"

def PAG_MAC_Change():
        try:
            Random_MAC_Address = pyautogui.locateCenterOnScreen(Random_MAC_Address_Path, confidence=0.9)
            originalPoint = pyautogui.position()
            pyautogui.click(Random_MAC_Address.x, Random_MAC_Address.y)
            time.sleep(0.2)
            pyautogui.click(Random_MAC_Address.x, Random_MAC_Address.y)
            time.sleep(0.2)
            
            originalPoint = pyautogui.position()
            pyautogui.click(Random_MAC_Address.x - 202, Random_MAC_Address.y + 111)
            
            pyautogui.moveTo(originalPoint)
        except:
            pass
        
        
PAG_MAC_Change()