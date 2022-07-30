import WindowsAPIInput
import adbInput
from ImageSearch import ImageSearch
from ImageSearch import screenshotToOpenCVImg
from OpenCV_imread import imreadUnicode
import time
import glob, os
from 이륙_조건 import 이륙_조건

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from UmamusumeProcess import *

class UmaEvent:
    def __init__(self, hwnd: int, device: adbInput.AdbConnect, InstancePort: int, parent = None) -> bool:
        """
        윈도우 hwnd, adb device, adb Port
        """
        self.parent: UmaProcess = parent
        self.hwnd: int = hwnd
        self.device: adbInput.AdbConnect = device
        self.InstancePort: int = InstancePort
    
        # Images
        path = './Images'
        self.Images = dict()
        for a in glob.glob(os.path.join(path, '*')):
            key = a.replace('.', '/').replace('\\', '/')
            key = key.split('/')
            self.Images[key[-2]] = imreadUnicode(a)

        # 서포트 카드
        path = './Supporter_cards'
        self.Supporter_cards = dict()
        for a in glob.glob(os.path.join(path, '*')):
            key = a.replace('.', '/').replace('\\', '/')
            key = key.split('/')
            self.Supporter_cards[key[-2]] = imreadUnicode(a)

    def 탈출(self):
        if self.parent.isAlive == False:
            return "Exit"

    def SKIP(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["SKIP"], confidence=0.85)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.3)
            # print(position)
            return count
        return None

    def 우마무스메_실행(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우마무스메_실행"], confidence=0.99, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0])
            time.sleep(2)
            # print(position)
            return count
        return None

    def 게스트_로그인(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["게스트_로그인"], 232, 926, 77, 14, confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 게스트로_로그인_하시겠습니까(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["게스트로_로그인_하시겠습니까"], 162, 534, 218, 17, confidence = 0.9)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX = 120, offsetY = 117, deltaX=5, deltaY=5)
            time.sleep(2)
            # print(position)
            return count
        return None

    def 전체_동의(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["전체_동의"], 23, 117, 22, 22, confidence=0.95, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX = 0, offsetY = 0, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 시작하기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["시작하기"], 237, 396, 67, 23, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def TAP_TO_START(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["TAP_TO_START"], 150, 860, 241, 34, confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(2)
            # print(position)
            return count
        return None

    def 계정_연동_설정_요청(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["계정_연동_설정_요청"], 176, 327, 186, 29)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX = -121, offsetY = 316, deltaX=5, deltaY=5)
            time.sleep(2) # 빨리 터치하면 튜토리얼 하기 부분에서도 같은 부분 클릭해버림
            # print(position)
            return count
        return None

    def 튜토리얼을_스킵하시겠습니까(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["튜토리얼을_스킵하시겠습니까"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=120, offsetY=140, deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 게임_데이터_다운로드(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["게임_데이터_다운로드"], 170, 329, 200, 27)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX = 132, offsetY = 316, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 트레이너_정보를_입력해주세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["트레이너_정보를_입력해주세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=61, deltaX=5)
            time.sleep(0.5)
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=555, deltaX=5)
            time.sleep(0.2)
            for _ in range(10):
                WindowsAPIInput.WindowsAPIKeyboardInput(self.hwnd, WindowsAPIInput.win32con.VK_BACK)
            time.sleep(0.2)
            WindowsAPIInput.WindowsAPIKeyboardInputString(self.hwnd, "UmaPyoi")
            time.sleep(0.5)
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 등록한다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["등록한다"], 206, 620, 106, 52)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 이_내용으로_등록합니다_등록하시겠습니까(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["이_내용으로_등록합니다_등록하시겠습니까"], 72, 569, 333, 49)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=136, offsetY=54, deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None


    # 튜토리얼
    def 출전(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["출전"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 울려라_팡파레(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["울려라_팡파레"])
        if count:
            ConvertedPosition = []
            ConvertedPosition.append(position[0][0] / 1.750503018108652) # 1740 / 994 가로화면 가로배율
            ConvertedPosition.append(position[0][1] / 1.750503018108652)
            ConvertedPosition.append(position[0][2] / 1.729965156794425) # 993 / 574 가로화면 세로배율
            ConvertedPosition.append(position[0][3] / 1.729965156794425)
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 닿아라_골까지(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["닿아라_골까지"])
        if count:
            ConvertedPosition = []
            ConvertedPosition.append(position[0][0] / 1.750503018108652)
            ConvertedPosition.append(position[0][1] / 1.750503018108652)
            ConvertedPosition.append(position[0][2] / 1.729965156794425)
            ConvertedPosition.append(position[0][3] / 1.729965156794425)
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 라이브_메뉴(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["라이브_메뉴"])
        if count:
            ConvertedPosition = []
            ConvertedPosition.append(position[0][0] / 1.750503018108652)
            ConvertedPosition.append(position[0][1] / 1.750503018108652)
            ConvertedPosition.append(position[0][2] / 1.729965156794425)
            ConvertedPosition.append(position[0][3] / 1.729965156794425)
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 라이브_스킵(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["라이브_스킵"])
        if count:
            ConvertedPosition = []
            ConvertedPosition.append(position[0][0] / 1.750503018108652)
            ConvertedPosition.append(position[0][1] / 1.750503018108652)
            ConvertedPosition.append(position[0][2] / 1.729965156794425)
            ConvertedPosition.append(position[0][3] / 1.729965156794425)
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 타즈나_씨와_레이스를_관전한(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["타즈나_씨와_레이스를_관전한"], 124, 808, 268, 52)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 일본_우마무스메_트레이닝_센터_학원(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["일본_우마무스메_트레이닝_센터_학원"], 78, 844, 345, 53)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 레이스의_세계를_꿈꾸는_아이들이(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["레이스의_세계를_꿈꾸는_아이들이"], 73, 810, 369, 70)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 환영(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["환영"], 180, 811, 156, 68)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 느낌표물음표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["느낌표물음표"], 35, 449, 52, 54)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 아키카와_이사장님(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["아키카와_이사장님"], 181, 811, 181, 49)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 장래_유망한_트레이너의_등장에(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["장래_유망한_트레이너의_등장에"], 145, 808, 284, 50)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 나는_이_학원의_이사장(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["나는_이_학원의_이사장"], 98, 821, 209, 49)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 자네에_대해_가르쳐_주게나(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["자네에_대해_가르쳐_주게나"], 155, 833, 250, 48)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 자네는_트레센_학원의_일원일세(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["자네는_트레센_학원의_일원일세"], 150, 833, 282, 49)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 담당_우마무스메와_함께(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["담당_우마무스메와_함께"], 172, 798, 224, 49)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 학원에_다니는_우마무스메의(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["학원에_다니는_우마무스메의"], 86, 798, 259, 50)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 자네는_트레이너로서_담당_우마무스메를(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["자네는_트레이너로서_담당_우마무스메를"], 79, 810, 358, 51)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 가슴에_단_트레이너_배지에(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["가슴에_단_트레이너_배지에"], 159, 811, 248, 48)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 실전_연수를_하러_가시죠(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["실전_연수를_하러_가시죠"], 207, 813, 224, 46)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 프리티_더비_뽑기_5번_뽑기_무료(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["프리티_더비_뽑기_5번_뽑기_무료"], 191, 710, 135, 125)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 튜토리얼_용_프리티_더비_뽑기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["튜토리얼_용_프리티_더비_뽑기"], 130, 432, 258, 69)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=180, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서포트_카드_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_카드_화살표"], confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서포트_카드_뽑기_10번_뽑기_무료(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_카드_뽑기_10번_뽑기_무료"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 튜토리얼_용_서포트_카드_뽑기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["튜토리얼_용_서포트_카드_뽑기"], 124, 431, 266, 71)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=180, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_화살표"], 350, 712, 117, 172)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_시나리오를_공략하자(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_시나리오를_공략하자"], 59, 664, 399, 77)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=223, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 다음_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["다음_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자"], 53, 614, 414, 125)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=248, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 마음에_드는_우마무스메를_육성하자(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["마음에_드는_우마무스메를_육성하자"], 21, 670, 473, 71)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=217, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 다이와_스칼렛_클릭(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["다이와_스칼렛_클릭"], 0, 496, 138, 138)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 다음_화살표_육성_우마무스메_선택(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["다음_화살표_육성_우마무스메_선택"], 212, 747, 91, 116)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 플러스_계승_우마무스메_선택_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["플러스_계승_우마무스메_선택_화살표"], 19, 520, 103, 152)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 계승_보드카_선택_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["계승_보드카_선택_화살표"], 209, 496, 93, 161)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 보드카_결정_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["보드카_결정_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 자동_선택_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["자동_선택_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 자동_선택_확인_OK_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["자동_선택_확인_OK_화살표"], 334, 559, 84, 117) # 느림
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 마음을_이어서_꿈을_이루자(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["마음을_이어서_꿈을_이루자"], 73, 661, 371, 79)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=218, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 계승_최종_다음_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["계승_최종_다음_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=35, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서포트_카드를_편성해서_육성_효율_UP(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_카드를_편성해서_육성_효율_UP"], 67, 615, 383, 120)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=247, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서포트_카드의_타입에_주목(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_카드의_타입에_주목"], 38, 662, 439, 69)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=225, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 우정_트레이닝이_육성의_열쇠를_쥐고_있다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우정_트레이닝이_육성의_열쇠를_쥐고_있다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=212, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서포트_자동_편성_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_자동_편성_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_시작_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_시작_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def TP를_소비해_육성_시작_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["TP를_소비해_육성_시작_화살표"], 305, 816, 142, 119)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 초록색_역삼각형(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["초록색_역삼각형"], 440, 850, -1, -1, confidence=0.8) # 역 삼각형
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def TAP(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["TAP"], confidence=0.7)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 우마무스메에겐_저마다_다른_목표가_있습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우마무스메에겐_저마다_다른_목표가_있습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 이쪽은_육성을_진행할_때_필요한_커맨드입니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["이쪽은_육성을_진행할_때_필요한_커맨드입니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 커맨드를_하나_실행하면_턴을_소비합니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["커맨드를_하나_실행하면_턴을_소비합니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 우선_트레이닝을_선택해_보세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우선_트레이닝을_선택해_보세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=60, offsetY=178, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 이게_실행할_수_있는_트레이닝들입니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["이게_실행할_수_있는_트레이닝들입니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 한_번_스피드를_골라_보세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["한_번_스피드를_골라_보세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=-143, offsetY=228, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 파란색_역삼각형(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["파란색_역삼각형"], 440, 850, -1, -1, confidence=0.9) # 역 삼각형
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 약속(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["약속"], 38, 614, 80, 57)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서둘러_가봐(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서둘러_가봐"], 38, 617, 132, 53)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 그때_번뜩였다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["그때_번뜩였다"], 22, 740, 289, 102)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 다이와_스칼렛의_성장으로_이어졌다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["다이와_스칼렛의_성장으로_이어졌다"], 23, 741, 328, 55)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 다음으로_육성_우마무스메의_체력에_관해_설명할게요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["다음으로_육성_우마무스메의_체력에_관해_설명할게요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 우선_아까처럼_트레이닝을_선택해_보세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우선_아까처럼_트레이닝을_선택해_보세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=90, offsetY=173, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 여기_실패율에_주목해_주세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["여기_실패율에_주목해_주세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 남은_체력이_적을수록_실패율이_높아지게_돼요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["남은_체력이_적을수록_실패율이_높아지게_돼요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 트레이닝에_실패하면_능력과_컨디션이(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["트레이닝에_실패하면_능력과_컨디션이"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 돌아간다_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["돌아간다_화살표"], confidence=1.0, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 체력이_적을_때는_우마무스메를(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["체력이_적을_때는_우마무스메를"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=-125, offsetY=180, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 먼저_여기_스킬을_선택해보세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["먼저_여기_스킬을_선택해보세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=-70, offsetY=170, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 다음으로_배울_스킬을_선택하세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["다음으로_배울_스킬을_선택하세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 이번에는_이_스킬을_습득해_보세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["이번에는_이_스킬을_습득해_보세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=273, offsetY=183, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 스킬_결정_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["스킬_결정_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 스킬_획득_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["스킬_획득_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 스킬_획득_돌아간다_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["스킬_획득_돌아간다_화살표"], 1, 857, 100, 115)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 이졔_준비가_다_끝났어요_레이스에_출전해_봐요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["이졔_준비가_다_끝났어요_레이스에_출전해_봐요"], 85, 621, 191, 69)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=207, offsetY=168, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 출전_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["출전_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 숫자1등이_되기_위해서도_말야(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["숫자1등이_되기_위해서도_말야"], 37, 615, 252, 58)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 패덕에서는_레이스에_출전하는_우마무스메의(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["패덕에서는_레이스에_출전하는_우마무스메의"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 우선_예상_표시에_관해서_설명할게요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우선_예상_표시에_관해서_설명할게요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 숫자3개의_표시는_전문가들의_예상을_나타내며(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["숫자3개의_표시는_전문가들의_예상을_나타내며"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 능력과_컨디션이_좋을수록_많은_기대를_받게_돼서(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["능력과_컨디션이_좋을수록_많은_기대를_받게_돼서"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 물론_반드시_우승하게_되는_건_아니지만(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["물론_반드시_우승하게_되는_건_아니지만"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 또_패덕에서는_우마무스메의_작전을(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["또_패덕에서는_우마무스메의_작전을"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=210, offsetY=157, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 선행A_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["선행A_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 작전_결정(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["작전_결정"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 이것으로_준비는_다_됐어요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["이것으로_준비는_다_됐어요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=145, offsetY=161, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 첫_우승_축하_드려요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["첫_우승_축하_드려요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=847, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 좋아(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["좋아"], 37, 613, 80, 59)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 목표_달성(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["목표_달성"], 114, 222, 293, 100)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=578, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_목표_달성(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_목표_달성"], 31, 227, 469, 96)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=578, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_수고하셨습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_수고하셨습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 스킬_포인트가_남았다면(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["스킬_포인트가_남았다면"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성은_이것으로_종료입니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성은_이것으로_종료입니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 또_연수_기간은_짧았지만(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["또_연수_기간은_짧았지만"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_완료_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_완료_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=40, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성_완료_확인_완료한다_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성_완료_확인_완료한다_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 최고_랭크를_목표로_힘내세요(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["최고_랭크를_목표로_힘내세요"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 랭크_육성(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["랭크_육성"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=837, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 육성을_끝낸_우마무스메는_인자를(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["육성을_끝낸_우마무스메는_인자를"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 계승_우마무스메로_선택하면_새로운_우마무스메에게(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["계승_우마무스메로_선택하면_새로운_우마무스메에게"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 인자획득(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["인자획득"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=829, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 우마무스메_상세_닫기_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["우마무스메_상세_닫기_화살표"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 평가점(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["평가점"], 293, 327, 75, 50)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=-75, offsetY=552, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 보상획득(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["보상획득"], 113, 21, 287, 103)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=834, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 강화_편성_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["강화_편성_화살표"], 0, 910, 97, -1, confidence=1.0, grayscale=False) # -5, 910, 97, 67
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 레이스_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["레이스_화살표"], 329, 908, 103, -1, confidence=1.0, grayscale=False) # 329, 908, 103, 71
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_경기장_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_경기장_화살표"], 82, 542, 130, 83)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 오리지널_팀을_결성_상위_CLASS를_노려라(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["오리지널_팀을_결성_상위_CLASS를_노려라"], 81, 622, 358, 118)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=244, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 하이스코어를_기록해서_CLASS_승급을_노리자(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["하이스코어를_기록해서_CLASS_승급을_노리자"], 78, 614, 362, 125)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=250, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 기간_중에_개최되는_5개의_레이스에(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["기간_중에_개최되는_5개의_레이스에"], 8, 617, 504, 121)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=236, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 서포트_카드의_Lv을_UP해서(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_카드의_Lv을_UP해서"], 61, 630, 396, 111)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=244, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_편성(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_편성"], 264, 699, 126, 72)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 전당_입성_우마무스메로_자신만의_팀을_결성(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["전당_입성_우마무스메로_자신만의_팀을_결성"], 59, 616, 395, 122)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=247, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_랭크를_올려서_최강의_팀이_되자(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_랭크를_올려서_최강의_팀이_되자"], 128, 616, 262, 122)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=238, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠"], 84, 619, 352, 123)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=246, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_편성_다이와_스칼렛_화살표_클릭(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_편성_다이와_스칼렛_화살표_클릭"], 200, 341, 116, 160)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 출전_우마무스메_선택_다이와_스칼렛_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["출전_우마무스메_선택_다이와_스칼렛_화살표"], 0, 591, 121, 138)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_편성_확정_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_편성_확정_화살표"], 190, 736, 136, 124)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 편성을_확정합니다_진행하시겠습니까(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["편성을_확정합니다_진행하시겠습니까"], 177, 524, 165, 75)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=121, offsetY=77, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 팀_최고_평가점_갱신_닫기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["팀_최고_평가점_갱신_닫기"], 223, 840, 98, 95)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 홈_화살표(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["홈_화살표"], 188, 845, 144, 134, confidence=1.0, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    # def a(self, img: screenshotToOpenCVImg) -> int:
    #     count = 0
    #     if count:
    #         # print(position)
    #         return count
    #     return None
    # ---------------------------

    def 공지사항_X(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["공지사항_X"], 495, 52, 23, 22)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 메인_스토리가_해방되었습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["메인_스토리가_해방되었습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=90, deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 여러_스토리를_해방할_수_있게_되었습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["여러_스토리를_해방할_수_있게_되었습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 선물_이동(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["선물_이동"], 456, 672, 47, 53)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 선물_일괄_수령(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["선물_일괄_수령"], 319, 879, 115, 54, confidence=0.99, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 상기의_선물을_수령했습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["상기의_선물을_수령했습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
            # adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=105, deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 받을_수_있는_선물이_없습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["받을_수_있는_선물이_없습니다"], 143, 460, 231, 51)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=-125, offsetY=420, deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 미션_이동(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["미션_이동"], 454, 602, 49, 45)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(1)
            # print(position)
            return count
        return None

    def 미션_메인(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["미션_메인"], 159, 359, 70, 47)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 미션_일괄_수령(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["미션_일괄_수령"], 197, 803, 117, 58, confidence=1, grayscale=False)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 미션_일괄_수령_확인됨(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["미션_일괄_수령_확인됨"], 197, 803, 117, 58, confidence=1, grayscale=False)
        if count:
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 상기의_보상을_수령했습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["상기의_보상을_수령했습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=90, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 돌아간다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["돌아간다"]) # 바로 뽑기로 이동
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=423, offsetY=117, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 뽑기_이동(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["뽑기_이동"], 464, 666, 52, 62)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=245, deltaX=5, deltaY=5)
            time.sleep(1.5)
            # print(position)
            return count
        return None

    def 프리티_더비_뽑기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["프리티_더비_뽑기"], 154, 551, 175, 93, confidence=0.6)
        if count:
            if self.parent.isSSR확정_뽑기 == False:
                adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=262, deltaX=5, deltaY=5)
                self.parent.is서포트_뽑기 = True
            else:
                if 이륙_조건(self.parent.Supporter_cards_total): # 이륙 조건
                    return "Exit"
                adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4") # "KEYCODE_BACK"
                self.parent.is뽑기_이동 = False
                self.parent.is초기화하기 = True
            # print(position)
            return count
        return None

    def 서포트_카드_뽑기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["서포트_카드_뽑기"], 160, 552, 154, 94, confidence=0.6) # 돌이 없는거 클릭 해봐야 암
        if count:
            if self.parent.is서포트_뽑기:
                adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=199, offsetY=191, deltaX=5, deltaY=5)
            if self.parent.isSSRGacha and self.parent.isSSR확정_뽑기:
                adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=272, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 무료_쥬얼부터_먼저_사용됩니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["무료_쥬얼부터_먼저_사용됩니다"], 126, 570, 280, 76)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=112, offsetY=55, deltaX=5, deltaY=5)
            time.sleep(1.5)
            # print(position)
            return count
        return None

    def 뽑기_결과(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["뽑기_결과"])
        if count:
            self.parent.is뽑기_결과 = False

            # 서포터 카드 지금 갯수
            Supporter_cards_now = dict()
            for i in self.parent.Supporter_cards_total.keys():
                Supporter_cards_now[i] = 0
                
            for _ in range(2):
                updateTime = time.time()
                time.sleep(0.1)
                img = screenshotToOpenCVImg(self.hwnd)
                
                for key, value in self.Supporter_cards.items():
                    card_count = 0
                    card_count, position = ImageSearch(img, value, 46, 122, 451, 715, grayscale=False)
                    if card_count:
                        if Supporter_cards_now[key] < card_count:
                            Supporter_cards_now[key] = card_count
                        # print(key + " " + str(Supporter_cards_now[key]) + "개")
                        self.parent.log(key + " " + str(Supporter_cards_now[key]) + "개")
                    
            # 지금 뽑힌 결과 총 서포터 카드 갯수에 더하기
            for key, value in self.parent.Supporter_cards_total.items():
                self.parent.Supporter_cards_total[key] += Supporter_cards_now[key]

            # print(position)
            return count
        return None

    def 한_번_더_뽑기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["한_번_더_뽑기"], 267, 675, 247, 318)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 쥬얼이_부족합니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["쥬얼이_부족합니다"], 165, 586, 207, 41)
        if count:
            if 이륙_조건(self.parent.Supporter_cards_total): # 이륙 조건
                return "Exit"

            if self.parent.isSSRGacha:
                self.parent.is서포트_뽑기 = False
                self.parent.isSSR확정_뽑기 = True
            else:
                self.parent.is뽑기_이동 = False
                self.parent.is초기화하기 = True
            
            adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4") # "KEYCODE_BACK" 
            time.sleep(0.5)
            adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4")
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 상점_화면을_표시할_수_없습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["상점_화면을_표시할_수_없습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=147, deltaX=5, deltaY=5)
            # print(position)
            time.sleep(0.5)
            return count
        return None

    def 숫자3성_확정(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["숫자3성_확정"], 144, 558, 235, 108, confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=247, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def SSR_확정_스타트_대시(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["SSR_확정_스타트_대시"], 144, 558, 235, 108, confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=248, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def SSR_확정_메이크_데뷔_뽑기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["SSR_확정_메이크_데뷔_뽑기"], 144, 558, 235, 108, confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=195, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def SSR_확정_메이크_데뷔_티켓을_1장_사용해(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["SSR_확정_메이크_데뷔_티켓을_1장_사용해"], 98, 449, 342, 35, confidence=0.6)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=117, offsetY=190, deltaX=5, deltaY=5)
            time.sleep(3)
            # print(position)
            return count
        return None

    def 뽑기_결과_OK(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["뽑기_결과_OK"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(3)
            # print(position)
            return count
        return None


    # 특수 이벤트
    def 모두_지우기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["모두_지우기"], 428, 40, 96, 48)
        if count:
            adbInput.BlueStacksSwipe(self.device, 0, position=position[0])
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 추가_데이터를_다운로드합니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["추가_데이터를_다운로드합니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=125, offsetY=155, deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 재시도(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["재시도"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 타이틀_화면으로(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["타이틀_화면으로"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            # print(position)
            return count
        return None

    def 확인(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["확인"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 앱_닫기(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["앱_닫기"], 78, 425, 391, 205)
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
            time.sleep(0.5)
            # print(position)
            return count
        return None

    def 날짜가_변경됐습니다(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["날짜가_변경됐습니다"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=142, deltaX=5, deltaY=5)
            time.sleep(3)
            # print(position)
            return count
        return None

    def 숫자4080_에러_코드(self, img: screenshotToOpenCVImg) -> int:
        count = 0
        count, position = ImageSearch(img, self.Images["숫자4080_에러_코드"])
        if count:
            adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetY=156, deltaX=5, deltaY=5)
            # print(position)
            return count
        return None