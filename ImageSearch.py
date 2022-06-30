import cv2
import numpy as np
from screenshot import screenshot
import win32gui
from OpenCV_imread import imreadUnicode
import adbInput

def hwndImageSearch(hwnd, template, threshold=0.8, Grayscale=False, isExport=False):
    try:
        img = np.array(screenshot(hwnd, isExport=False))
        if Grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # BGR순의 이미지를 흑백으로 변경
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) # BGR순의 이미지를 흑백으로 변경
            h, w = template.shape # 가져올 이미지의 해상도 (세로, 가로)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # RGB순의 이미지를 OpenCV에 맞게 BGR순으로 변경
            h, w = template.shape[:-1] # 가져올 이미지의 해상도 (세로, 가로, 채널)
                
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        # threshold = 0.8 # 인자에서 사용됨
        loc = np.where(res >= threshold) # 정확도 threshold % 이상 이미지 좌표 반환
        count = 0 # 찾은 갯수
        position = [] # 찾은 위치
        mask = np.zeros(img.shape[:2], np.uint8)
        
        # for pt in zip(*loc[::-1]):  # Switch collumns and rows
        for pt in zip(*loc[::-1]): # 순서를 거꾸로 하고 튜플로 묶고 리스트로 만듦.
            if mask[pt[1] + int(round(h/2)), pt[0] + int(round(w/2))] != 255: # 마스킹 처리하여 중복제거
                mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
                
                count += 1
                position.append((str(pt[0] + w/2), str(pt[1] + h/2))) # 목표의 중앙 좌표
                if isExport:
                    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print("pt의 좌표" + str(pt))
                # print("중앙 좌표:" + str(pt[0] + w/2) + ", " + str(pt[1] + h/2))

        if isExport:
            cv2.imwrite('result.png', img)

        return count, position # 갯수와 좌표 반환
    
    except:
        return False, False # 예외 처리


if __name__ == "__main__":
    hwndMain = win32gui.FindWindow(None, "Bluestacks Dev")
    # hwndImageSearch(hwndMain, imreadUnicode('./Images/test.png'), 0.8, True) 테스트용
    # count, position = hwndImageSearch(hwndMain, imreadUnicode("./Images/test.png"), 0.8, True, True)
    count, position = hwndImageSearch(hwndMain, imreadUnicode("./Images/우마.png"), 0.8, True, True)
    print("갯수는 " + str(count) + "개")
    print(position)
    # print(position[0][1])
    
    instancePort = 6205
    device = adbInput.AdbConnect(instancePort)
    while 1:
        x, y = adbInput.BlueStacksOffset(int(float(position[0][0])), int(float(position[0][1])))
        x, y = adbInput.RandomPosition(x, y, 5, 5)
        # AdbTap(device, x, y)
        adbInput.AdbSwipe(device, x, y, x, y, adbInput.random.randint(50, 150))
    

# reference: https://stackoverflow.com/questions/7853628/how-do-i-find-an-image-contained-within-an-image
# reference: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=samsjang&logNo=220587092117

# preventing duplicate: https://stackoverflow.com/questions/21829469/removing-or-preventing-duplicate-template-matches-in-opencv-with-python
