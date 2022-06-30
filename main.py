import screenshot
import WindowsAPIInput
import adbInput
from OpenCV_imread import imreadUnicode
from ImageSearch import hwndImageSearch
from PIL import Image
import time
import random
import cv2
import numpy as np

게스트_로그인 = imreadUnicode(r"./Images/게스트_로그인.png")

if __name__ == "__main__":
    hwndMain = WindowsAPIInput.GetHwnd("BlueStacks Dev")
    instancePort = 6205
    device = adbInput.AdbConnect(instancePort)
    
    while 1:
        count = 0; position = 0; x = 0; y = 0
        count, position = hwndImageSearch(hwndMain, 게스트_로그인, confidence=0.8, grayscale=False, isExport=False)
        if count:
            print(count)
            print(position)
            x, y = position[0]
            x, y = adbInput.BlueStacksOffset(x, y)
            x, y = adbInput.RandomPosition(x, y, 5, 5)
            adbInput.AdbSwipe(device, x, y, x, y, random.randint(50, 150))
            
        else:
            print("없음")
        # print("\n")
        # time.sleep(1)
        time.sleep(0.2)

테스트 = cv2.imread("./Images/테스트.png")
임시_스크린 = cv2.imread("./Images/임시_스크린.png")
result = cv2.matchTemplate(임시_스크린, 테스트, cv2.TM_SQDIFF_NORMED)