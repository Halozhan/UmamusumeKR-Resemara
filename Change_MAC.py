import pyautogui
import time

def PAG_MAC_Change():
        try:
            main_location = "./"
            Random_MAC_Address_Path = main_location+"Random_MAC_Address.png"
            Change_Now_Path = main_location+"Change_Now.png"

            Random_MAC_Address = pyautogui.locateCenterOnScreen(Random_MAC_Address_Path, confidence=0.9)
            originalPoint = pyautogui.position() # 처음 위치한 커서 좌표

            pyautogui.click(Random_MAC_Address.x, Random_MAC_Address.y)
            time.sleep(0.5)
            
            pyautogui.click(Random_MAC_Address.x, Random_MAC_Address.y)
            time.sleep(0.5)
            
            pyautogui.click(Random_MAC_Address.x - 202, Random_MAC_Address.y + 111)
            time.sleep(0.5)
            
            pyautogui.moveTo(originalPoint) # 원래 위치로 커서 되돌림
        except:
            pass
        
PAG_MAC_Change()