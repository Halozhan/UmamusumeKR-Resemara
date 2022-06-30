import screenshot
import WindowsAPIInput
import adbInput
import pyautogui as pag
from PIL import Image
import time
import random
from PIL import ImageGrab
import cv2
import numpy

# 게스트_로그인 = Image.open(r"Images/테스트.png")
# 임시_스크린 = Image.open(r"Images/임시_스크린.png")

# if __name__ == "__main__":
#     hwndMain = WindowsAPIInput.GetHwnd("BlueStacks Dev")
    
#     while 1:
#         instanceImage = screenshot.screenshot(hwndMain, False)
#         # count = pag.locate(게스트_로그인, instanceImage, confidence=0.8, grayscale=True)
#         count = pag.locate(게스트_로그인, 임시_스크린, confidence=0.8, grayscale=True)
#         instancePort = 6205
#         device = adbInput.AdbConnect(instancePort)
            
#         # count
#         if count:
#             print(count)
#             # x, y = pag.center(count)
#             # print(x, y)
#             # x, y = adbInput.BlueStacksOffset(x, y)
#             # x, y = adbInput.RandomPosition(x, y, 5, 5)
#             # adbInput.AdbSwipe(device, x, y, x, y, random.randint(50, 150))
            
            
#         else:
#             print("없음")
#         # print("\n")
#         time.sleep(3)
#
# 테스트 = cv2.imread("./Images/테스트.png")
# 임시_스크린 = cv2.imread("./Images/임시_스크린.png")
# result = cv2.matchTemplate(임시_스크린, 테스트, cv2.TM_SQDIFF_NORMED)


img_rgb = cv2.imread('./Images/screen.png')
template = cv2.imread('./Images/test.png')
h, w = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.90
loc = numpy.where(res >= threshold)
count = 0
# for pt in zip(*loc[::-1]):  # Switch collumns and rows
for pt in zip(*loc[::-1]):  # Switch collumns and rows
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    print("pt의 좌표" + str(pt))
    count += 1


cv2.imwrite('result.png', img_rgb)


print("\n")
print("갯수는 " + str(count) + "개")
print("a")