import cv2
import numpy as np
import win32gui
from screenshot import screenshot
from OpenCV_imread import imreadUnicode
import adbInput


def hwndImageSearch(hwnd, template, threshold=0.8, Grayscale=False, isExport=False):
    img_rgb = np.array(screenshot(hwnd, isExport=False))
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR) # RGB순의 이미지를 OpenCV에 맞게 BGR순으로 변경
    img_rgb = cv2.imread('./Images/screen.png') # 테스트용
    if Grayscale:
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) # BGR순의 이미지를 흑백으로 변경
    

    # template = cv2.imread('./Images/test.png') Main에서 사용함


    if Grayscale:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # template = imreadUnicode("./Images/우마.png")
    # h, w, _ = template.shape # 가져올 이미지의 해상도 (세로, 가로, 채널)
    if Grayscale:
        h, w = template.shape # 가져올 이미지의 해상도 (세로, 가로)
    else:
        h, w = template.shape[:-1] # 가져올 이미지의 해상도 (세로, 가로, 채널)
    # print(template.shape[:-1])

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    # threshold = 0.8 # 인자에서 사용됨
    loc = np.where(res >= threshold)
    count = 0
    mask = np.zeros(img_rgb.shape[:2], np.uint8)
    # for pt in zip(*loc[::-1]):  # Switch collumns and rows
    for pt in zip(*loc[::-1]):  # Switch collumns and rows 순서를 거꾸로 하고 튜플로 묶고 리스트로 만듦.
        if mask[pt[1] + int(round(h/2)), pt[0] + int(round(w/2))] != 255: # 마스킹 처리하여 중복제거
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            count += 1
            print("pt의 좌표" + str(pt))
            print("중앙 좌표:" + str(pt[0] + w/2) + ", " + str(pt[1] + h/2))
        # instancePort = 6205
        # device = adbInput.AdbConnect(instancePort)
        # while 1:
        #     x, y = adbInput.RandomPosition(pt[0] + w/2, pt[1] + h/2, 1, 1)
        #     x, y = adbInput.BlueStacksOffset(x, y)
        #     # AdbTap(device, x, y)
        #     adbInput.AdbSwipe(device, x, y, x, y, adbInput.random.randint(50, 150))
            
            


    cv2.imwrite('result.png', img_rgb)


    print("\n")
    print("갯수는 " + str(count) + "개")
    print("a")


if __name__ == "__main__":
    hwndMain = win32gui.FindWindow(None, "Bluestacks Dev")
    # hwndImageSearch(hwndMain, imreadUnicode('./Images/test.png'), 0.8, True) 테스트용
    hwndImageSearch(hwndMain, imreadUnicode('./Images/test.png'), 0.8, True)


# reference: https://stackoverflow.com/questions/7853628/how-do-i-find-an-image-contained-within-an-image
# reference: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=samsjang&logNo=220587092117

# preventing duplicate: https://stackoverflow.com/questions/21829469/removing-or-preventing-duplicate-template-matches-in-opencv-with-python