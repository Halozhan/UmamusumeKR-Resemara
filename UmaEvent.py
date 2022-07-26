import WindowsAPIInput
import adbInput
from ImageSearch import ImageSearch
from ImageSearch import screenshotToOpenCVImg
from OpenCV_imread import imreadUnicode
import time
import glob, os
from 이륙_조건 import 이륙_조건

# Images
path = './Images'
Images = dict()
for a in glob.glob(os.path.join(path, '*')):
    key = a.replace('.', '/').replace('\\', '/')
    key = key.split('/')
    Images[key[-2]] = imreadUnicode(a)

# 서포트 카드
path = './Supporter_cards'
Supporter_cards = dict()
for a in glob.glob(os.path.join(path, '*')):
    key = a.replace('.', '/').replace('\\', '/')
    key = key.split('/')
    Supporter_cards[key[-2]] = imreadUnicode(a)


def SKIP(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["SKIP"], confidence=0.85)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.3)
        # print(position)
        return count
    return None

def 우마무스메_실행(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["우마무스메_실행"], confidence=0.99, grayscale=False)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0])
        time.sleep(2)
        # print(position)
        return count
    return None

def 게스트_로그인(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["게스트_로그인"], 232, 926, 77, 14, confidence=0.6)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 게스트로_로그인_하시겠습니까(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["게스트로_로그인_하시겠습니까"], 162, 534, 218, 17, confidence = 0.9)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX = 120, offsetY = 117, deltaX=5, deltaY=5)
        time.sleep(2)
        # print(position)
        return count
    return None

def 전체_동의(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["전체_동의"], 23, 117, 22, 22, confidence=0.95, grayscale=False)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX = 0, offsetY = 0, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 시작하기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["시작하기"], 237, 396, 67, 23, grayscale=False)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def TAP_TO_START(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["TAP_TO_START"], 150, 860, 241, 34, confidence=0.6)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(2)
        # print(position)
        return count
    return None

def 계정_연동_설정_요청(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["계정_연동_설정_요청"], 176, 327, 186, 29)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX = -121, offsetY = 316, deltaX=5, deltaY=5)
        time.sleep(2) # 빨리 터치하면 튜토리얼 하기 부분에서도 같은 부분 클릭해버림
        # print(position)
        return count
    return None

def 튜토리얼을_스킵하시겠습니까(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["튜토리얼을_스킵하시겠습니까"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=120, offsetY=140, deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 게임_데이터_다운로드(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["게임_데이터_다운로드"], 170, 329, 200, 27)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX = 132, offsetY = 316, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 트레이너_정보를_입력해주세요(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int, hwnd: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["트레이너_정보를_입력해주세요"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=61, deltaX=5)
        time.sleep(0.5)
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=555, deltaX=5)
        time.sleep(0.2)
        for _ in range(10):
            WindowsAPIInput.WindowsAPIKeyboardInput(hwnd, WindowsAPIInput.win32con.VK_BACK)
        time.sleep(0.2)
        WindowsAPIInput.WindowsAPIKeyboardInputString(hwnd, "UmaPyoi")
        time.sleep(0.5)
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 등록한다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["등록한다"], 206, 620, 106, 52)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 이_내용으로_등록합니다_등록하시겠습니까(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["이_내용으로_등록합니다_등록하시겠습니까"], 72, 569, 333, 49)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=136, offsetY=54, deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

# 튜토리얼에 쓸 예정
def a(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    if count:
        # print(position)
        return count
    return None

def 공지사항_X(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["공지사항_X"], 495, 52, 23, 22)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 메인_스토리가_해방되었습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["메인_스토리가_해방되었습니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=90, deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 여러_스토리를_해방할_수_있게_되었습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["여러_스토리를_해방할_수_있게_되었습니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 선물_이동(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["선물_이동"], 456, 672, 47, 53)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 선물_일괄_수령(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["선물_일괄_수령"], 319, 879, 115, 54, confidence=0.99, grayscale=False)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 상기의_선물을_수령했습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["상기의_선물을_수령했습니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=105, deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 받을_수_있는_선물이_없습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["받을_수_있는_선물이_없습니다"], 143, 460, 231, 51)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=-125, offsetY=420, deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 미션_이동(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["미션_이동"], 454, 602, 49, 45)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(1)
        # print(position)
        return count
    return None

def 미션_메인(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["미션_메인"], 159, 359, 70, 47)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 미션_일괄_수령(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["미션_일괄_수령"], 197, 803, 117, 58, confidence=1, grayscale=False)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 미션_일괄_수령_확인됨(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["미션_일괄_수령_확인됨"], 197, 803, 117, 58, confidence=1, grayscale=False)
    if count:
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 상기의_보상을_수령했습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["상기의_보상을_수령했습니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=90, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 돌아간다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["돌아간다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 뽑기_이동(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["뽑기_이동"], 464, 666, 52, 62)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=245, deltaX=5, deltaY=5)
        time.sleep(1.5)
        # print(position)
        return count
    return None

# def 프리티_더비_뽑기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
#     count = 0
#     if count:
#         # print(position)
#         return count
#     return None

# def 서포트_카드_뽑기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
#     count = 0
#     if count:
#         # print(position)
#         return count
#     return None

def 무료_쥬얼부터_먼저_사용됩니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["무료_쥬얼부터_먼저_사용됩니다"], 126, 570, 280, 76)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=112, offsetY=55, deltaX=5, deltaY=5)
        time.sleep(1.5)
        # print(position)
        return count
    return None

def 뽑기_결과(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["뽑기_결과"], 208, 35, 97, 247)
    if count:
        # print(position)
        return count
    return None

def 한_번_더_뽑기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["한_번_더_뽑기"], 267, 675, 247, 318)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 상점_화면을_표시할_수_없습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["상점_화면을_표시할_수_없습니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=147, deltaX=5, deltaY=5)
        # print(position)
        time.sleep(0.5)
        return count
    return None

def 숫자3성_확정(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["숫자3성_확정"], 144, 558, 235, 108, confidence=0.6)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=247, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def SSR_확정_스타트_대시(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["SSR_확정_스타트_대시"], 144, 558, 235, 108, confidence=0.6)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=248, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def SSR_확정_메이크_데뷔_뽑기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["SSR_확정_메이크_데뷔_뽑기"], 144, 558, 235, 108, confidence=0.6)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=195, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def SSR_확정_메이크_데뷔_티켓을_1장_사용해(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["SSR_확정_메이크_데뷔_티켓을_1장_사용해"], 98, 449, 342, 35, confidence=0.6)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=117, offsetY=190, deltaX=5, deltaY=5)
        time.sleep(3)
        # print(position)
        return count
    return None

def 뽑기_결과_OK(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["뽑기_결과_OK"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(3)
        # print(position)
        return count
    return None


# 특수 이벤트
def 모두_지우기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect) -> int:
    count = 0
    count, position = ImageSearch(img, Images["모두_지우기"], 428, 40, 96, 48)
    if count:
        adbInput.BlueStacksSwipe(device, 0, position=position[0])
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 추가_데이터를_다운로드합니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["추가_데이터를_다운로드합니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetX=125, offsetY=155, deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 재시도(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["재시도"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        # print(position)
        return count
    return None

def 타이틀_화면으로(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["타이틀_화면으로"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        # print(position)
        return count
    return None

def 확인(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["확인"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 앱_닫기(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["앱_닫기"], 78, 425, 391, 205)
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], deltaX=5, deltaY=5)
        time.sleep(0.5)
        # print(position)
        return count
    return None

def 날짜가_변경됐습니다(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["날짜가_변경됐습니다"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=142, deltaX=5, deltaY=5)
        time.sleep(3)
        # print(position)
        return count
    return None

def 숫자4080_에러_코드(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    count, position = ImageSearch(img, Images["숫자4080_에러_코드"])
    if count:
        adbInput.BlueStacksSwipe(device, InstancePort, position=position[0], offsetY=156, deltaX=5, deltaY=5)
        # print(position)
        return count
    return None

def a(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    if count:
        # print(position)
        return count
    return None

def a(img: screenshotToOpenCVImg, device: adbInput.AdbConnect, InstancePort: int) -> int:
    count = 0
    if count:
        # print(position)
        return count
    return None