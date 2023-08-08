import cv2
import numpy as np
from screenshot import screenshot


def screenshotToOpenCVImg(hwnd):  # PIL image to OpenCV
    try:
        img = np.array(screenshot(hwnd, isExport=False))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # RGB순의 이미지를 OpenCV에 맞게 BGR순으로 변경
        return img
    except:
        pass
    # reference: https://www.zinnunkebi.com/python-opencv-pil-convert/


def ImageSearch(img, template, roiLeft=0, roiTop=0, roiWidth=-1, roiHeight=-1,
                confidence=0.9, grayscale=True, isExport=False):
    try:
        # roiLeft = 0
        # roiTop = 0
        # roiWidth = -1
        # roiHeight = -1

        if roiWidth == -1 and roiHeight == -1:
            img = img[roiTop:-1, roiLeft:-1]  # Region of Interest, 관심 영역
        elif roiWidth == -1:
            img = img[roiTop:roiTop+roiHeight:, roiLeft:-1]
        elif roiHeight == -1:
            img = img[roiTop:-1, roiLeft:roiLeft+roiWidth]
        else:
            img = img[roiTop:roiTop+roiHeight, roiLeft:roiLeft+roiWidth]

        if grayscale:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # BGR순의 이미지를 흑백으로 변경
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)  # BGR순의 이미지를 흑백으로 변경
            h, w = template.shape  # 가져올 이미지의 해상도 (세로, 가로)
        elif grayscale == False:
            h, w = template.shape[:-1]  # 가져올 이미지의 해상도 (세로, 가로, 채널)

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        threshold = confidence  # 정확도
        loc = np.where(res >= threshold)  # 정확도 threshold % 이상 이미지 좌표 반환
        count = 0  # 찾은 갯수
        position = []  # 찾은 위치
        mask = np.zeros(img.shape[:2], np.uint8)

        # for pt in zip(*loc[::-1]):  # Switch collumns and rows
        for pt in zip(*loc[::-1]): # 순서를 거꾸로 하고 튜플로 묶고 리스트로 만듦.
            if mask[pt[1] + int(round(h/2)), pt[0] + int(round(w/2))] != 255:  # 마스킹 처리하여 중복제거
                mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255

                count += 1
                position.append((roiLeft + pt[0], roiTop + pt[1], w, h))  # 목표의 박스 (ROI로 잘린 영역 보정)
                if isExport:
                    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print("pt의 좌표" + str(pt))
                # print("중앙 좌표:" + str(pt[0] + w/2) + ", " + str(pt[1] + h/2))

        if isExport:
            cv2.imwrite('result.png', img)

        return count, position  # 갯수와 좌표 반환

    except:
        return False, False  # 예외 처리


if __name__ == "__main__":
    import win32gui
    from OpenCV_imread import imreadUnicode
    import adbInput

    hwndMain = win32gui.FindWindow(None, "Bluestacks Dev")  # hwnd ID 찾기
    img = screenshotToOpenCVImg(hwndMain)  # 윈도우의 스크린샷
    우마 = imreadUnicode("./Images/우마.png")  # 찾을 이미지
    count, position = ImageSearch(img, 우마, roiLeft=206, roiTop=604, roiWidth=52, roiHeight=58,
                                      confidence=0.8, grayscale=False, isExport=False)  # 스크린샷, 찾을 이미지, ROI, 정확도, 명암 변화, 추출
    print("갯수는 " + str(count) + "개")  # 찾은 갯수
    print(position)  # 박스 위치 출력

    instancePort = 6205  # adb instance 포트
    device = adbInput.AdbConnect(instancePort)  # 연결
    while 1:
        adbInput.BlueStacksSwipe(device, position[0], 5, 5)


# reference: https://stackoverflow.com/questions/7853628/how-do-i-find-an-image-contained-within-an-image
# reference: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=samsjang&logNo=220587092117

# preventing duplicate: https://stackoverflow.com/questions/21829469/removing-or-preventing-duplicate-template-matches-in-opencv-with-python
