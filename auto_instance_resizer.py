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
confirm2_location = main_location+"confirm2.png"

def main():
    while True:
        time.sleep(2)
        try:
            confirm = pyautogui.locateCenterOnScreen(confirm_location, confidence=0.98)
            originalPoint = pyautogui.position()
            pyautogui.click(confirm.x + 10, confirm.y + 70)
            # pyautogui.moveTo(originalPoint)
            # print(confirm.x, confirm.y)
        except:
            pass
        time.sleep(0.5)
        try:
            confirm2 = pyautogui.locateCenterOnScreen(confirm2_location, confidence=0.98)
            originalPoint = pyautogui.position()
            pyautogui.click(confirm2.x + 45, confirm2.y + 80)
            # pyautogui.moveTo(originalPoint)
            # print(confirm2.x, confirm2.y)
        except:
            pass
        
        
main()