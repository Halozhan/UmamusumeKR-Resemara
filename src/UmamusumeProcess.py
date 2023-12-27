import WindowsAPIInput
import adbInput
from ImageSearch import ImageSearch
from ImageSearch import screenshotToOpenCVImg
from OpenCV_imread import imreadUnicode
import time
from datetime import datetime
import glob
import os
import pickle
from multiprocessing import Queue
import threading
# from UmaEvent import UmaEvent
from 이륙_조건 import 이륙_조건


class UmaProcess:
    def __init__(self):
        pass

    def Receive_Worker(self):
        while self.ReceiverEvent.is_set() == False or self.toChild.empty() == False:
            if not self.Receive():
                time.sleep(0.01)

        while not self.toChild.empty():
            try:
                recv = self.toChild.get(timeout=0.001)
                print(recv)
            except:
                pass
        self.toChild.close()
        # print("자식 수신 종료")

    def Receive(self) -> bool:  # 통신용
        if self.toChild.empty() == False:
            self.Lock.acquire()

            recv = self.toChild.get()

            if recv[0] == "sleepTime":
                self.sleepTime = recv[1]
            elif recv[0] == "terminate": # 종료 신호
                self.isAlive = False

            elif recv[0] == "InstanceName":
                self.InstanceName = recv[1]
            elif recv[0] == "InstancePort":
                self.InstancePort = recv[1]
            elif recv[0] == "isDoneTutorial":
                self.isDoneTutorial = recv[1]
            elif recv[0] == "isMission":
                self.isMission = recv[1]
            elif recv[0] == "isSSRGacha":
                self.isSSRGacha = recv[1]

            elif recv[0] == "sendTotalResetCount":
                self.totalResetCount = recv[1]
                self.waiting = False

            self.Lock.release()
            return True

        return False

    def log_main(self, id, text) -> None:
        self.toParent.put(["sendLog_main", str(id), str(text)])

    def log(self, text) -> None:
        self.toParent.put(["sendLog", str(text)])

    def run_a(self, toParent: Queue, toChild: Queue):
        self.Lock = threading.Lock()
        # 선언
        self.toParent = toParent
        self.toChild = toChild
        self.InstanceName = ""
        self.InstancePort = 0
        self.isDoneTutorial = False  # 체크 박스로 튜토리얼 스킵 여부 결정
        self.isMission = False  # 체크 박스로 수령할 지 결정
        self.isSSRGacha = False
        self.totalResetCount = 0
        self.waiting = False

        self.isAlive = False
        self.sleepTime = 0.5

        # --------------------------------

        # 수신
        self.ReceiverEvent = threading.Event()
        self.Receiver = threading.Thread(target=self.Receive_Worker, daemon=True)
        self.Receiver.start()
        while self.Receiver.is_alive() == False:
            time.sleep(0.001)

        self.isAlive = True

        # 정보가 불러와졌을 때까지 기다림
        while self.InstanceName == "":
            time.sleep(0.001)
        while self.InstancePort == 0:
            time.sleep(0.001)

        while self.isAlive:
            isSuccessed = self.main()

            # print("-"*50)
            self.log_main(self.InstanceName, "-" * 50)
            self.log("-" * 50)

            now = datetime.now()
            self.log_main(self.InstanceName, now.strftime("%Y-%m-%d_%H:%M:%S"))
            self.log(now.strftime("%Y-%m-%d_%H:%M:%S"))

            if isSuccessed == "Failed":  # 리세 실패, 저장된 데이터 삭제
                try:
                    path = "./Saved_Data/" + str(self.InstancePort) + ".uma"
                    os.remove(path)
                except:
                    pass
                self.resetCount += 1

            if isSuccessed == "Stop":
                self.log_main(str(self.InstanceName), " thread was terminated.")
                self.log("This thread was terminated.")

            self.log_main(self.InstanceName, "리세 횟수: " + str(int(self.resetCount)))
            self.log("리세 횟수: " + str(int(self.resetCount)))
            self.toParent.put(["sendResetCount", self.resetCount])
            self.toParent.put(["requestTotalResetCount"])
            self.waiting = True
            while self.waiting:
                self.Receive()
                time.sleep(0.05)
            self.log_main("리세 총 횟수: ", str(int(self.totalResetCount)))

            if isSuccessed == True:
                self.isAlive = False
                print("리세 성공 " * 5)
                self.log_main(self.InstanceName, "리세 성공 " * 5)
                self.log("리세 성공 " * 5)

                self.toParent.put(["terminate"])

            if isSuccessed == "숫자4080_에러_코드":
                self.toParent.put(["숫자4080_에러_코드"])
                time.sleep(30)

            self.log_main(self.InstanceName, "-" * 50)
            self.log("-" * 50)

        self.log_main(self.InstanceName, "리세 종료")
        self.log("리세 종료")

        self.saveUma()  # Uma 파일 저장

        self.ReceiverEvent.set()  # Receiver 스레드 종료 준비
        self.Receiver.join()  # 수신 종료 대기
        self.ReceiverEvent.clear()

        while not self.toParent.empty():
            time.sleep(0.01)
        self.toParent.close()
        # 종료됨

    def saveUma(self) -> bool:
        """
        Uma 파일 저장
        """
        try:
            path = "./Saved_Data/" + str(self.InstancePort) + ".uma"
            with open(file=path, mode="wb") as file:
                pickle.dump(self.resetCount, file)  # -- pickle --
                pickle.dump(self.is시작하기, file)  # -- pickle --
                pickle.dump(self.isPAUSED, file)  # -- pickle --
                pickle.dump(self.is선물_이동, file)  # -- pickle --
                pickle.dump(self.is미션_이동, file)  # -- pickle --
                pickle.dump(self.is뽑기_이동, file)  # -- pickle --
                pickle.dump(self.is서포트_뽑기, file)  # -- pickle --
                pickle.dump(self.isSSR확정_뽑기, file)  # -- pickle --
                pickle.dump(self.is뽑기_결과, file)  # -- pickle --
                pickle.dump(self.is초기화하기, file)  # -- pickle --

                # 서포트 카드 총 갯수
                pickle.dump(self.Supporter_cards_total, file)  # -- pickle --
            return True
        except:
            path = "./Saved_Data/" + str(self.InstancePort) + ".uma"
            print(path + "를 저장하는데 실패했습니다.")
            # self.log(path+"를 저장하는데 실패했습니다.")
            return False

    def loadUma(self) -> bool:
        """
        Uma 파일 불러오기
        """
        try:
            path = "./Saved_Data/" + str(self.InstancePort) + ".uma"
            with open(file=path, mode="rb") as file:
                self.resetCount = pickle.load(file)  # -- pickle --
                self.is시작하기 = pickle.load(file)  # -- pickle --
                self.isPAUSED = pickle.load(file)  # -- pickle --
                self.is선물_이동 = pickle.load(file)  # -- pickle --
                self.is미션_이동 = pickle.load(file)  # -- pickle --
                self.is뽑기_이동 = pickle.load(file)  # -- pickle --
                self.is서포트_뽑기 = pickle.load(file)  # -- pickle --
                self.isSSR확정_뽑기 = pickle.load(file)  # -- pickle --
                self.is뽑기_결과 = pickle.load(file)  # -- pickle --
                self.is초기화하기 = pickle.load(file)  # -- pickle --

                # 서포트 카드 총 갯수
                self.Supporter_cards_total: dict = pickle.load(file)  # -- pickle --
                for key, value in self.Supporter_cards_total.items():
                    self.log(key + ": " + str(value))
                self.log("기존 데이터를 불러옵니다.")
            return True
        except:
            if "self.resetCount" not in locals():
                self.resetCount = 0  # -- pickle --
            self.is시작하기 = False  # -- pickle --
            self.isPAUSED = False  # -- pickle --
            self.is선물_이동 = True  # -- pickle --
            self.is미션_이동 = True  # -- pickle --
            self.is뽑기_이동 = True  # -- pickle --
            self.is서포트_뽑기 = False  # -- pickle --
            self.isSSR확정_뽑기 = False  # -- pickle --
            self.is뽑기_결과 = True  # -- pickle --
            self.is초기화하기 = False  # -- pickle --

            # 서포트 카드 총 갯수
            path = "./images/서포트_카드"
            self.Supporter_cards_total = dict()  # -- pickle --
            for a in glob.glob(os.path.join(path, "*")):
                key = a.replace(".", "/").replace("\\", "/")
                key = key.split("/")
                self.Supporter_cards_total[key[-2]] = 0
            return False

    def main(self):
        hwndMain = WindowsAPIInput.GetHwnd(self.InstanceName)  # hwnd ID 찾기
        if hwndMain == 0:
            self.toParent.put(["terminate"])
            return "Stop"

        WindowsAPIInput.SetWindowSize(hwndMain, 574, 994)
        self.device = adbInput.AdbConnect(self.InstancePort)

        self.loadUma()  # Uma 파일 불러오기

        self.toParent.put(["sendResetCount", self.resetCount])  # 리세 횟수 발신

        # images
        path = "./images"
        Images = dict()
        for a in glob.glob(os.path.join(path, "*")):
            if os.path.isfile(a):
                key = a.replace(".", "/").replace("\\", "/")
                key = key.split("/")
                Images[key[-2]] = imreadUnicode(a)

        # 서포트 카드
        path = "./images/서포트_카드"
        Supporter_cards = dict()
        for a in glob.glob(os.path.join(path, "*")):
            if os.path.isfile(a):
                key = a.replace(".", "/").replace("\\", "/")
                key = key.split("/")
                Supporter_cards[key[-2]] = imreadUnicode(a)

        updateTime = time.time()  # 타임 아웃용 터치

        while self.isAlive:
            # 잠수 클릭 20초 터치락 해제
            if self.isDoneTutorial and time.time() >= updateTime + 20:
                self.log("20초 정지 터치락 해제!!!")
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=(509, 66, 0, 0),
                    deltaX=0,
                    deltaY=0,
                )
                time.sleep(2)

            # 잠수 클릭 60초 이상 앱정지
            if self.isDoneTutorial and time.time() >= updateTime + 60:
                self.log("60초 정지 앱 강제종료!!!")
                adbInput.shell(
                    self.device,
                    self.InstancePort,
                    "am force-stop com.kakaogames.umamusume",
                )
                time.sleep(2)

            time.sleep(self.sleepTime)

            if self.isAlive == False:  # 중간에 멈춰야 할 경우
                break

            img = screenshotToOpenCVImg(hwndMain)  # 윈도우의 스크린샷

            count = 0
            count, position = ImageSearch(img, Images["SKIP"], confidence=0.85)
            if count:
                self.log("SKIP " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(0.3)
                continue

            count = 0
            count, position = ImageSearch(
                img, Images["우마무스메_실행"], confidence=0.99
            )
            if count:
                self.log("우마무스메_실행 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0]
                )
                # print(position)
                time.sleep(2)

            if self.is시작하기 == False:
                count = 0
                count, position = ImageSearch(
                    img, Images["게스트_로그인"], 232, 926, 77, 14, confidence=0.6
                )
                if count:
                    self.log("게스트_로그인 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["게스트로_로그인_하시겠습니까"], 162, 534, 218, 17, confidence=0.9
                )
                if count:
                    self.log("게스트로_로그인_하시겠습니까 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=120,
                        offsetY=117,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(2)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["전체_동의"], 23, 117, 22, 22, confidence=0.95, grayscale=False
                )
                if count:
                    self.log("전체_동의 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=0,
                        offsetY=0,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["시작하기"], 237, 396, 67, 23, grayscale=False
                )
                if count:
                    self.log("시작하기 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["노란색_start"], 246, 410, 43, 24
                )
                if count:
                    self.log("노란색_start " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["TAP_TO_START"], 150, 860, 241, 34, confidence=0.6
            )
            if count:
                self.log("TAP_TO_START " + str(count) + "개")
                updateTime = time.time()
                self.is시작하기 = True
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(2)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["계정_연동_설정_요청"], 176, 327, 186, 29
            )
            if count:
                self.log("계정_연동_설정_요청 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=-121,
                    offsetY=316,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(2)  # 빨리 터치하면 튜토리얼 하기 부분에서도 같은 부분 클릭해버림
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["튜토리얼을_스킵하시겠습니까"])
            if count:
                self.log("튜토리얼을_스킵하시겠습니까 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=120,
                    offsetY=140,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["게임_데이터_다운로드"], 170, 329, 200, 27
            )
            if count:
                self.log("게임_데이터_다운로드 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=132,
                    offsetY=316,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["트레이너_정보를_입력해주세요"])
            if count:
                self.log("트레이너_정보를_입력해주세요 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=61,
                    deltaX=5,
                )
                time.sleep(0.5)
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=555,
                    deltaX=5,
                )
                time.sleep(0.2)
                WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "a")
                time.sleep(0.3)
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["등록한다"], 206, 620, 106, 52)
            if count:
                self.log("등록한다 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["이_내용으로_등록합니다_등록하시겠습니까"], 72, 569, 333, 49
            )
            if count:
                self.log("이_내용으로_등록합니다_등록하시겠습니까 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=136,
                    offsetY=54,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["이_내용으로_등록합니다_진행하시겠습니까"], 91, 588, 314, 32
            )
            if count:
                self.log("이_내용으로_등록합니다_진행하시겠습니까 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=136,
                    offsetY=54,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            if self.isAlive == False:  # 중간에 멈춰야 할 경우
                break

            # 튜토리얼 진행. 자주 다루는 파트가 아니니, 멈출 경우 수동 조작 필요
            count = 0
            count, position = ImageSearch(img, Images["출전"])
            if count:
                self.log("출전 " + str(count) + "개")
                self.toParent.put(["isDoneTutorial", False])
                self.isDoneTutorial = False
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(1)

            if self.isDoneTutorial == False:
                updateTime = time.time()

                if self.isPAUSED == False:
                    count = 0
                    count, position = ImageSearch(img, Images["울려라_팡파레"])
                    if count:
                        self.log("울려라_팡파레 " + str(count) + "개")
                        self.isPAUSED = True
                        ConvertedPosition = []
                        ConvertedPosition.append(
                            position[0][0] / 1.750503018108652
                        )  # 1740 / 994 가로화면 가로배율
                        ConvertedPosition.append(position[0][1] / 1.750503018108652)
                        ConvertedPosition.append(
                            position[0][2] / 1.729965156794425
                        )  # 993 / 574 가로화면 세로배율
                        ConvertedPosition.append(position[0][3] / 1.729965156794425)
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=ConvertedPosition,
                            deltaX=5,
                            deltaY=5,
                        )
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)

                    count = 0
                    count, position = ImageSearch(img, Images["닿아라_골까지"])
                    if count:
                        self.log("닿아라_골까지 " + str(count) + "개")
                        self.isPAUSED = True
                        ConvertedPosition = []
                        ConvertedPosition.append(position[0][0] / 1.750503018108652)
                        ConvertedPosition.append(position[0][1] / 1.750503018108652)
                        ConvertedPosition.append(position[0][2] / 1.729965156794425)
                        ConvertedPosition.append(position[0][3] / 1.729965156794425)
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=ConvertedPosition,
                            deltaX=5,
                            deltaY=5,
                        )
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["라이브_메뉴"])
                if count:
                    self.log("라이브_메뉴 " + str(count) + "개")
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=ConvertedPosition,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["라이브_스킵"])
                if count:
                    self.log("라이브_스킵 " + str(count) + "개")
                    self.isPAUSED = False
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=ConvertedPosition,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["타즈나_씨와_레이스를_관전한"], 124, 808, 268, 52
                )
                if count:
                    self.log("타즈나_씨와_레이스를_관전한 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(3)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["일본_우마무스메_트레이닝_센터_학원"], 78, 844, 345, 53
                )
                if count:
                    self.log("일본_우마무스메_트레이닝_센터_학원 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["레이스의_세계를_꿈꾸는_아이들이"], 73, 810, 369, 70
                )
                if count:
                    self.log("레이스의_세계를_꿈꾸는_아이들이 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["환영"], 180, 811, 156, 68)
                if count:
                    self.log("환영 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["느낌표물음표"], 35, 449, 52, 54)
                if count:
                    self.log("느낌표물음표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["아키카와_이사장님"], 181, 811, 181, 49)
                if count:
                    self.log("아키카와_이사장님 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["장래_유망한_트레이너의_등장에"], 145, 808, 284, 50
                )
                if count:
                    self.log("장래_유망한_트레이너의_등장에 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["나는_이_학원의_이사장"], 98, 821, 209, 49
                )
                if count:
                    self.log("나는_이_학원의_이사장 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["자네에_대해_가르쳐_주게나"], 155, 833, 250, 48
                )
                if count:
                    self.log("자네에_대해_가르쳐_주게나 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                # 트레이너 정보 입력 -----------

                count = 0
                count, position = ImageSearch(
                    img, Images["자네는_트레센_학원의_일원일세"], 150, 833, 282, 49
                )
                if count:
                    self.log("자네는_트레센_학원의_일원일세 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["담당_우마무스메와_함께"], 172, 798, 224, 49
                )
                if count:
                    self.log("담당_우마무스메와_함께 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["학원에_다니는_우마무스메의"], 86, 798, 259, 50
                )
                if count:
                    self.log("학원에_다니는_우마무스메의 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["자네는_트레이너로서_담당_우마무스메를"], 79, 810, 358, 51
                )
                if count:
                    self.log("자네는_트레이너로서_담당_우마무스메를 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["가슴에_단_트레이너_배지에"], 159, 811, 248, 48
                )
                if count:
                    self.log("가슴에_단_트레이너_배지에 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["실전_연수를_하러_가시죠"], 207, 813, 224, 46
                )
                if count:
                    self.log("실전_연수를_하러_가시죠 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["프리티_더비_뽑기_5번_뽑기_무료"], 191, 710, 135, 125
                )
                if count:
                    self.log("프리티_더비_뽑기_5번_뽑기_무료 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["튜토리얼_용_프리티_더비_뽑기"], 130, 432, 258, 69
                )
                if count:
                    self.log("튜토리얼_용_프리티_더비_뽑기 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=180,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["서포트_카드_화살표"], confidence=0.6)
                if count:
                    self.log("서포트_카드_화살표 " + str(count) + "개")  # 느림
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["서포트_카드_뽑기_10번_뽑기_무료"])
                if count:
                    self.log("서포트_카드_뽑기_10번_뽑기_무료 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["튜토리얼_용_서포트_카드_뽑기"], 124, 431, 266, 71
                )
                if count:
                    self.log("튜토리얼_용_서포트_카드_뽑기 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=180,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성_화살표"], 350, 712, 117, 172)
                if count:
                    self.log("육성_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=50,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["육성_시나리오를_공략하자"], 59, 664, 399, 77
                )
                if count:
                    self.log("육성_시나리오를_공략하자 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=223,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["다음_화살표"])
                if count:
                    self.log("다음_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자"], 53, 614, 414, 125
                )
                if count:
                    self.log("트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=248,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["처음_육성은_우선_우마무스메들을_더욱_잘_알_수_있는"], 24, 772, 399, 100)
                if count:
                    self.log("처음_육성은_우선_우마무스메들을_더욱_잘_알_수_있는 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], offsetX=50, offsetY=120, deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["마음에_드는_우마무스메를_육성하자"], 21, 670, 473, 71
                )
                if count:
                    self.log("마음에_드는_우마무스메를_육성하자 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=217,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["다이와_스칼렛_클릭"], 0, 496, 138, 138)
                if count:
                    self.log("다이와_스칼렛_클릭 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["다음_화살표_육성_우마무스메_선택"], 212, 747, 91, 116
                )
                if count:
                    self.log("다음_화살표_육성_우마무스메_선택 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["플러스_계승_우마무스메_선택_화살표"], 34, 576, 96, 101
                )
                if count:
                    self.log("플러스_계승_우마무스메_선택_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["계승_보드카_선택_화살표"], 209, 496, 93, 161
                )
                if count:
                    self.log("계승_보드카_선택_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["보드카_결정_화살표"])
                if count:
                    self.log("보드카_결정_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["자동_선택_화살표"])
                if count:
                    self.log("자동_선택_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["자동_선택_확인_OK_화살표"], 334, 559, 84, 117
                )  # 느림
                if count:
                    self.log("자동_선택_확인_OK_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["마음을_이어서_꿈을_이루자"], 73, 661, 371, 79
                )
                if count:
                    self.log("마음을_이어서_꿈을_이루자 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=218,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["계승_최종_다음_화살표"])
                if count:
                    self.log("계승_최종_다음_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=35,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["서포트_카드를_편성해서_육성_효율_UP"], 67, 615, 383, 120
                )
                if count:
                    self.log("서포트_카드를_편성해서_육성_효율_UP " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=247,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["서포트_카드의_타입에_주목"], 38, 662, 439, 69
                )
                if count:
                    self.log("서포트_카드의_타입에_주목 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=225,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["우정_트레이닝이_육성의_열쇠를_쥐고_있다"])
                if count:
                    self.log("우정_트레이닝이_육성의_열쇠를_쥐고_있다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=212,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["서포트_자동_편성_화살표"])
                if count:
                    self.log("서포트_자동_편성_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성_시작_화살표"])
                if count:
                    self.log("육성_시작_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["TP를_소비해_육성_시작_화살표"], 305, 816, 142, 119
                )
                if count:
                    self.log("TP를_소비해_육성_시작_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["초록색_역삼각형"], 440, 850, -1, -1, confidence=0.8
                )  # 역 삼각형
                if count:
                    self.log("초록색_역삼각형 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)

                count = 0
                count, position = ImageSearch(img, Images["TAP"], confidence=0.7)
                if count:
                    self.log("TAP " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["우마무스메에겐_저마다_다른_목표가_있습니다"])
                if count:
                    self.log("우마무스메에겐_저마다_다른_목표가_있습니다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["이쪽은_육성을_진행할_때_필요한_커맨드입니다"])
                if count:
                    self.log("이쪽은_육성을_진행할_때_필요한_커맨드입니다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["커맨드를_하나_실행하면_턴을_소비합니다"])
                if count:
                    self.log("커맨드를_하나_실행하면_턴을_소비합니다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["우선_트레이닝을_선택해_보세요"])
                if count:
                    self.log("우선_트레이닝을_선택해_보세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=60,
                        offsetY=178,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["이게_실행할_수_있는_트레이닝들입니다"])
                if count:
                    self.log("이게_실행할_수_있는_트레이닝들입니다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["한_번_스피드를_골라_보세요"])
                if count:
                    self.log("한_번_스피드를_골라_보세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=-143,
                        offsetY=228,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["파란색_역삼각형"], 440, 850, -1, -1, confidence=0.9
                )  # 역 삼각형
                if count:
                    self.log("파란색_역삼각형 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)

                count = 0
                count, position = ImageSearch(img, Images["약속"], 38, 614, 80, 57)
                if count:
                    self.log("약속 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["서둘러_가봐"], 38, 617, 132, 53)
                if count:
                    self.log("서둘러_가봐 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["그때_번뜩였다"], 22, 740, 289, 102)
                if count:
                    self.log("그때_번뜩였다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["다이와_스칼렛의_성장으로_이어졌다"], 23, 741, 328, 55
                )
                if count:
                    self.log("다이와_스칼렛의_성장으로_이어졌다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["다음으로_육성_우마무스메의_체력에_관해_설명할게요"])
                if count:
                    self.log("다음으로_육성_우마무스메의_체력에_관해_설명할게요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["우선_아까처럼_트레이닝을_선택해_보세요"])
                if count:
                    self.log("우선_아까처럼_트레이닝을_선택해_보세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=90,
                        offsetY=173,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["여기_실패율에_주목해_주세요"])
                if count:
                    self.log("여기_실패율에_주목해_주세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["남은_체력이_적을수록_실패율이_높아지게_돼요"])
                if count:
                    self.log("남은_체력이_적을수록_실패율이_높아지게_돼요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["트레이닝에_실패하면_능력과_컨디션이"])
                if count:
                    self.log("트레이닝에_실패하면_능력과_컨디션이 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["돌아간다_화살표"], confidence=0.99, grayscale=False
                )
                if count:
                    self.log("돌아간다_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["체력이_적을_때는_우마무스메를"])
                if count:
                    self.log("체력이_적을_때는_우마무스메를 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=-125,
                        offsetY=180,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["먼저_여기_스킬을_선택해보세요"])
                if count:
                    self.log("먼저_여기_스킬을_선택해보세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=-70,
                        offsetY=170,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["다음으로_배울_스킬을_선택하세요"])
                if count:
                    self.log("다음으로_배울_스킬을_선택하세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["이번에는_이_스킬을_습득해_보세요"])
                if count:
                    self.log("이번에는_이_스킬을_습득해_보세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=273,
                        offsetY=183,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["스킬_결정_화살표"])
                if count:
                    self.log("스킬_결정_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["스킬_획득_화살표"])
                if count:
                    self.log("스킬_획득_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["스킬_획득_돌아간다_화살표"], 1, 857, 100, 115
                )
                if count:
                    self.log("스킬_획득_돌아간다_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["이제_준비가_다_끝났어요_레이스에_출전해_봐요"], 104, 644, 172, 48
                )
                if count:
                    self.log("이제_준비가_다_끝났어요_레이스에_출전해_봐요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=207,
                        offsetY=168,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["출전할_수_있는_레이스가_있으면"], 11, 558, 514, 117
                )
                if count:
                    self.log("출전할_수_있는_레이스가_있으면 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0]
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["출전_화살표"])
                if count:
                    self.log("출전_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["숫자1등이_되기_위해서도_말야"], 37, 615, 252, 58
                )
                if count:
                    self.log("숫자1등이_되기_위해서도_말야 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["패덕에서는_레이스에_출전하는_우마무스메의"])
                if count:
                    self.log("패덕에서는_레이스에_출전하는_우마무스메의 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["우선_예상_표시에_관해서_설명할게요"])
                if count:
                    self.log("우선_예상_표시에_관해서_설명할게요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["숫자3개의_표시는_전문가들의_예상을_나타내며"])
                if count:
                    self.log("3개의_표시는_전문가들의_예상을_나타내며 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["능력과_컨디션이_좋을수록_많은_기대를_받게_돼서"])
                if count:
                    self.log("능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["물론_반드시_우승하게_되는_건_아니지만"])
                if count:
                    self.log("물론_반드시_우승하게_되는_건_아니지만 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["또_패덕에서는_우마무스메의_작전을"])
                if count:
                    self.log("또_패덕에서는_우마무스메의_작전을 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=210,
                        offsetY=157,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["선행A_화살표"])
                if count:
                    self.log("선행A_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["작전_결정"])
                if count:
                    self.log("작전_결정 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["이것으로_준비는_다_됐어요"])
                if count:
                    self.log("이것으로_준비는_다_됐어요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=145,
                        offsetY=161,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["첫_우승_축하_드려요"])
                if count:
                    self.log("첫_우승_축하_드려요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=847,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["좋아"], 37, 613, 80, 59)
                if count:
                    self.log("좋아 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["목표_달성"], 114, 222, 293, 100)
                if count:
                    self.log("목표_달성 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=578,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성_목표_달성"], 31, 227, 469, 96)
                if count:
                    self.log("육성_목표_달성 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=578,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성_수고하셨습니다"])
                if count:
                    self.log("육성_수고하셨습니다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["스킬_포인트가_남았다면"])
                if count:
                    self.log("스킬_포인트가_남았다면 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성은_이것으로_종료입니다"])
                if count:
                    self.log("육성은_이것으로_종료입니다 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["또_연수_기간은_짧았지만"])
                if count:
                    self.log("또_연수_기간은_짧았지만 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성_완료_화살표"])
                if count:
                    self.log("육성_완료_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=40,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성_완료_확인_완료한다_화살표"])
                if count:
                    self.log("육성_완료_확인_완료한다_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후"])
                if count:
                    self.log("육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["최고_랭크를_목표로_힘내세요"])
                if count:
                    self.log("최고_랭크를_목표로_힘내세요 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["랭크_육성"])
                if count:
                    self.log("랭크_육성 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=837,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["육성을_끝낸_우마무스메는_인자를"])
                if count:
                    self.log("육성을_끝낸_우마무스메는_인자를 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["계승_우마무스메로_선택하면_새로운_우마무스메에게"])
                if count:
                    self.log("계승_우마무스메로_선택하면_새로운_우마무스메에게 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["인자획득"])
                if count:
                    self.log("인자획득 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=829,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["우마무스메_상세_닫기_화살표"])
                if count:
                    self.log("우마무스메_상세_닫기_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["평가점"], 293, 327, 75, 50)
                if count:
                    self.log("평가점 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=-75,
                        offsetY=552,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["보상획득"], 113, 21, 287, 103)
                if count:
                    self.log("보상획득 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=834,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img,
                    Images["강화_편성_화살표"],
                    19, 928, 73, 50,
                    confidence=0.99,
                )
                if count:
                    self.log("강화_편성_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img,
                    Images["레이스_화살표"],
                    350, 939, 83, 42,
                    confidence=0.99,
                )
                if count:
                    self.log("레이스_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["팀_경기장_화살표"], 82, 542, 130, 83)
                if count:
                    self.log("팀_경기장_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=50,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["오리지널_팀을_결성_상위_CLASS를_노려라"], 81, 622, 358, 118
                )
                if count:
                    self.log("오리지널_팀을_결성_상위_CLASS를_노려라 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=244,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["하이스코어를_기록해서_CLASS_승급을_노리자"], 78, 614, 362, 125
                )
                if count:
                    self.log("하이스코어를_기록해서_CLASS_승급을_노리자 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=250,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["기간_중에_개최되는_5개의_레이스에"], 8, 617, 504, 121
                )
                if count:
                    self.log("기간_중에_개최되는_5개의_레이스에 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=236,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["서포트_카드의_Lv을_UP해서"], 61, 630, 396, 111
                )
                if count:
                    self.log("서포트_카드의_Lv을_UP해서 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=244,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["팀_편성"], 264, 699, 126, 72)
                if count:
                    self.log("팀_편성 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["전당_입성_우마무스메로_자신만의_팀을_결성"], 59, 616, 395, 122
                )
                if count:
                    self.log("전당_입성_우마무스메로_자신만의_팀을_결성 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=247,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["팀_랭크를_올려서_최강의_팀이_되자"], 128, 616, 262, 122
                )
                if count:
                    self.log("팀_랭크를_올려서_최강의_팀이_되자 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=238,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠"], 84, 619, 352, 123
                )
                if count:
                    self.log("팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=246,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["팀_편성_다이와_스칼렛_화살표_클릭"], 225, 419, 89, 77
                )
                if count:
                    self.log("팀_편성_다이와_스칼렛_화살표_클릭 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["출전_우마무스메_선택_다이와_스칼렛_화살표"], 25, 666, 79, 66
                )
                if count:
                    self.log("출전_우마무스메_선택_다이와_스칼렛_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["팀_편성_확정_화살표"], 190, 736, 136, 124
                )
                if count:
                    self.log("팀_편성_확정_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["편성을_확정합니다_진행하시겠습니까"], 177, 524, 165, 75
                )
                if count:
                    self.log("편성을_확정합니다_진행하시겠습니까 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=121,
                        offsetY=77,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img, Images["팀_최고_평가점_갱신_닫기"], 223, 840, 98, 95
                )
                if count:
                    self.log("팀_최고_평가점_갱신_닫기 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=25,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img,
                    Images["홈_화살표"],
                    188,
                    845,
                    144,
                    134,
                    confidence=0.99
                )
                if count:
                    self.log("홈_화살표 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            count = 0
            count, position = ImageSearch(img, Images["공지사항_X"], 495, 52, 23, 22)
            if count:
                self.log("공지사항_X " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                self.isDoneTutorial = True
                self.toParent.put(["isDoneTutorial", True])
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["메인_스토리가_해방되었습니다"])
            if count:
                self.log("메인_스토리가_해방되었습니다 " + str(count) + "개")
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=90,
                    deltaX=5,
                    deltaY=5,
                )
                self.isDoneTutorial = True
                self.toParent.put(["isDoneTutorial", True])
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["여러_스토리를_해방할_수_있게_되었습니다"])
            if count:
                self.log("여러_스토리를_해방할_수_있게_되었습니다 " + str(count) + "개")
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=50,
                    deltaX=5,
                    deltaY=5,
                )
                self.isDoneTutorial = True
                self.toParent.put(["isDoneTutorial", True])
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            # 선물 수령
            if self.isDoneTutorial and self.is선물_이동 == True:
                count = 0
                count, position = ImageSearch(img, Images["선물_이동"], 456, 672, 47, 53)
                if count:
                    self.log("선물_이동 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img,
                    Images["선물_일괄_수령"],
                    319,
                    879,
                    115,
                    54,
                    confidence=0.99,
                    grayscale=False,
                )
                if count:
                    self.log("선물_일괄_수령 " + str(count) + "개")
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["상기의_선물을_수령했습니다"])
                if count:
                    self.log("상기의_선물을_수령했습니다 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=50,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["의상을_획득했습니다"])
                if count:
                    self.log("의상을_획득했습니다 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=50,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["곡을_획득했습니다"])
                if count:
                    self.log("곡을_획득했습니다 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=50,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["받을_수_있는_선물이_없습니다"], 143, 460, 231, 51
            )
            if count:
                self.log("받을_수_있는_선물이_없습니다 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=-125,
                    offsetY=420,
                    deltaX=5,
                    deltaY=5,
                )
                self.is선물_이동 = False
                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            # 미션 수령
            if (
                self.isDoneTutorial
                and self.isMission
                and self.is미션_이동
                and self.is선물_이동 == False
            ):
                count = 0
                count, position = ImageSearch(img, Images["미션_이동"], 454, 602, 49, 45)
                if count:
                    self.log("미션_이동 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["미션_메인"], 159, 359, 70, 47)
                if count:
                    self.log("미션_메인 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img,
                    Images["미션_일괄_수령"],
                    197,
                    803,
                    117,
                    58,
                    confidence=0.99
                )
                if count:
                    self.log("미션_일괄_수령 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(
                    img,
                    Images["미션_일괄_수령_확인됨"],
                    197,
                    803,
                    117,
                    58,
                    confidence=1,
                    grayscale=False,
                )
                if count:
                    self.log("미션_일괄_수령_확인됨 " + str(count) + "개")
                    updateTime = time.time()
                    self.is미션_이동 = False
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["상기의_보상을_수령했습니다"])
            if count:
                self.log("상기의_보상을_수령했습니다 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=90,
                    deltaX=5,
                    deltaY=5,
                )
                self.is미션_이동 = False
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            if self.is미션_이동 == False:
                count = 0
                count, position = ImageSearch(img, Images["돌아간다"])  # 바로 뽑기로 이동
                if count:
                    self.log("돌아간다 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=423,
                        offsetY=117,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

            if self.isAlive == False:  # 중간에 멈춰야 할 경우
                break

            # 뽑기
            if self.isDoneTutorial and self.is뽑기_이동:
                count = 0
                count, position = ImageSearch(img, Images["뽑기_이동"], 464, 666, 52, 62)
                if count:
                    self.log("뽑기_이동 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=245,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(1.5)
                    img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(
                img, Images["프리티_더비_뽑기"], confidence=0.95
            )
            if count:
                self.log("프리티_더비_뽑기 " + str(count) + "개")
                updateTime = time.time()

                if self.isSSR확정_뽑기 == False:
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=400,
                        offsetY=470,
                        deltaX=5,
                        deltaY=5,
                    )
                    self.is서포트_뽑기 = True
                else:
                    if 이륙_조건(self.Supporter_cards_total):  # 이륙 조건
                        return True  # 루프 탈출
                    adbInput.Key_event(
                        self.device, self.InstancePort, key_code="keyevent 4"
                    )  # "KEYCODE_BACK"
                    self.is뽑기_이동 = False
                    self.is초기화하기 = True

                # print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            if self.is서포트_뽑기:
                count = 0
                count, position = ImageSearch(
                    img, Images["서포트_카드_뽑기"], confidence=0.95
                )  # 돌이 없는거 클릭 해봐야 암
                if count:
                    self.log("서포트_카드_뽑기 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=340,
                        offsetY=650,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

            if self.isDoneTutorial and self.is뽑기_이동:
                if self.isAlive == False:  # 중간에 멈춰야 할 경우
                    break

                count = 0
                count, position = ImageSearch(img, Images["무료_쥬얼부터_먼저_사용됩니다"])
                if count:
                    self.log("무료_쥬얼부터_먼저_사용됩니다 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=112,
                        offsetY=55,
                        deltaX=5,
                        deltaY=5,
                    )
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetX=131,
                        offsetY=149,
                        deltaX=5,
                        deltaY=5,
                    )
                    self.is뽑기_결과 = True
                    # print(position)
                    time.sleep(1.5)

                    img = screenshotToOpenCVImg(hwndMain)

                if self.is뽑기_결과:  # ===== 뽑기 결과
                    count = 0
                    count, position = ImageSearch(img, Images["뽑기_결과"])
                    if count:
                        self.is뽑기_결과 = False

                        # 서포터 카드 지금 갯수
                        Supporter_cards_now = dict()
                        for i in self.Supporter_cards_total.keys():
                            Supporter_cards_now[i] = 0

                        for _ in range(2):
                            updateTime = time.time()
                            time.sleep(0.1)
                            img = screenshotToOpenCVImg(hwndMain)

                            for key, value in Supporter_cards.items():
                                card_count = 0
                                card_count, position = ImageSearch(
                                    img, value, 46, 122, 451, 715
                                )
                                if card_count:
                                    if Supporter_cards_now[key] < card_count:
                                        Supporter_cards_now[key] = card_count
                                    # print(key + " " + str(Supporter_cards_now[key]) + "개")
                                    self.log(key + " " + str(Supporter_cards_now[key]) + "개")

                        # 지금 뽑힌 결과 총 서포터 카드 갯수에 더하기
                        for key, value in self.Supporter_cards_total.items():
                            self.Supporter_cards_total[key] += Supporter_cards_now[key]

                        # print(position)
                        updateTime = time.time()
                        self.log("뽑기_결과 " + str(count) + "개")

                        # 총 서포터 카드 갯수
                        total_count = 0
                        for key, value in self.Supporter_cards_total.items():
                            if value:
                                total_count += value

                        if total_count:
                            self.log_main(self.InstanceName, "-" * 50)
                            self.log("-" * 50)
                            for key, value in self.Supporter_cards_total.items():
                                if value:
                                    self.log_main(
                                        self.InstanceName, key + ": " + str(value)
                                    )
                                    self.log(key + ": " + str(value))
                            self.log_main(self.InstanceName, "-" * 50)
                            self.log("-" * 50)
                # =========================== 뽑기 결과

                if self.isAlive == False:  # 중간에 멈춰야 할 경우
                    break

                count = 0
                count, position = ImageSearch(img, Images["한_번_더_뽑기"], 267, 675, 247, 318)
                if count:
                    self.log("한_번_더_뽑기 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

            if self.isDoneTutorial:
                count = 0
                count, position = ImageSearch(img, Images["쥬얼이_부족합니다"])
                if count:
                    self.log("쥬얼이_부족합니다 " + str(count) + "개")
                    updateTime = time.time()

                    if 이륙_조건(self.Supporter_cards_total):  # 이륙 조건
                        return True

                    if self.isSSRGacha:
                        self.is서포트_뽑기 = False
                        self.isSSR확정_뽑기 = True
                    else:
                        self.is뽑기_이동 = False
                        self.is초기화하기 = True

                    adbInput.Key_event(
                        self.device, self.InstancePort, key_code="keyevent 4"
                    )  # "KEYCODE_BACK"
                    time.sleep(0.5)
                    adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, Images["상점_화면을_표시할_수_없습니다"])
                if count:
                    self.log("상점_화면을_표시할_수_없습니다 " + str(count) + "개")
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(
                        self.device,
                        self.InstancePort,
                        position=position[0],
                        offsetY=147,
                        deltaX=5,
                        deltaY=5,
                    )
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                if self.isDoneTutorial and self.isSSRGacha and self.isSSR확정_뽑기:
                    # ========= SSR 뽑기
                    count = 0
                    count, position = ImageSearch(
                        img, Images["서포트_카드_뽑기"], confidence=0.95
                    )  # 돌이 없는거 클릭 해봐야 암
                    if count:
                        self.log("서포트_카드_뽑기 " + str(count) + "개")
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=position[0],
                            offsetX=272,
                            deltaX=5,
                            deltaY=5,
                        )
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                    # ===================

                    count = 0
                    count, position = ImageSearch(
                        img, Images["숫자3성_확정"], 144, 558, 235, 108, confidence=0.6
                    )
                    if count:
                        self.log("숫자3성_확정 " + str(count) + "개")
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=position[0],
                            offsetX=247,
                            deltaX=5,
                            deltaY=5,
                        )
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)

                    count = 0
                    count, position = ImageSearch(
                        img, Images["SSR_확정_스타트_대시"], 144, 558, 235, 108, confidence=0.6
                    )
                    if count:
                        self.log("SSR_확정_스타트_대시 " + str(count) + "개")
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=position[0],
                            offsetX=248,
                            deltaX=5,
                            deltaY=5,
                        )
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)

                    count = 0
                    count, position = ImageSearch(
                        img, Images["SSR_확정_메이크_데뷔_뽑기"], 144, 558, 235, 108, confidence=0.6
                    )
                    if count:
                        self.log("SSR_확정_메이크_데뷔_뽑기 " + str(count) + "개")
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=position[0],
                            offsetY=195,
                            deltaX=5,
                            deltaY=5,
                        )
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)

                    count = 0
                    count, position = ImageSearch(
                        img,
                        Images["SSR_확정_메이크_데뷔_티켓을_1장_사용해"],
                        98,
                        449,
                        342,
                        35,
                        confidence=0.6,
                    )
                    if count:
                        self.log("SSR_확정_메이크_데뷔_티켓을_1장_사용해 " + str(count) + "개")
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(
                            self.device,
                            self.InstancePort,
                            position=position[0],
                            offsetX=117,
                            offsetY=190,
                            deltaX=5,
                            deltaY=5,
                        )
                        self.is뽑기_결과 = True
                        # print(position)
                        time.sleep(3)
                        img = screenshotToOpenCVImg(hwndMain)

                    count = 0
                    count, position = ImageSearch(img, Images["뽑기_결과_OK"])
                    if count:
                        self.log("뽑기_결과_OK " + str(count) + "개")
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(
                            self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                        )
                        # print(position)
                        time.sleep(3)
                        img = screenshotToOpenCVImg(hwndMain)

                if self.is초기화하기:
                    adbInput.shell(
                        self.device,
                        self.InstancePort,
                        "am force-stop com.kakaogames.umamusume",
                    )
                    time.sleep(1)
                    adbInput.shell(
                        self.device,
                        self.InstancePort,
                        "/system/xbin/bstk/su -c rm -rf /data/data/com.kakaogames.umamusume/shared_prefs",
                    )
                    self.log("삭제_완료")
                    return "Failed"

            # 특수 이벤트
            count = 0
            count, position = ImageSearch(img, Images["모두_지우기"], 428, 40, 96, 48)
            if count:
                self.log("모두_지우기 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(self.device, 0, position=position[0])
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["추가_데이터를_다운로드합니다"])
            if count:
                self.log("추가_데이터를_다운로드합니다 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetX=125,
                    offsetY=155,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["재시도"])
            if count:
                self.log("재시도 " + str(count) + "개")
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                continue

            count = 0
            count, position = ImageSearch(img, Images["타이틀_화면으로"])
            if count:
                self.log("타이틀_화면으로 " + str(count) + "개")
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                continue

            count = 0
            count, position = ImageSearch(img, Images["확인"])
            if count:
                self.log("확인 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["앱_닫기"], 78, 425, 391, 205)
            if count:
                self.log("앱_닫기 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5
                )
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["날짜가_변경됐습니다"])
            if count:
                self.log("날짜가_변경됐습니다 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=142,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)
                time.sleep(3)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, Images["숫자4080_에러_코드"], confidence=0.97)
            if count:
                self.log("숫자4080_에러_코드 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=156,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)

            count = 0
            count, position = ImageSearch(img, Images["오류코드_2002"], confidence=0.97)
            if count:
                self.log("오류코드_2002 " + str(count) + "개")
                updateTime = time.time()
                adbInput.BlueStacksSwipe(
                    self.device,
                    self.InstancePort,
                    position=position[0],
                    offsetY=156,
                    deltaX=5,
                    deltaY=5,
                )
                # print(position)

            count = 0
            count, position = ImageSearch(img, Images["오류코드_451"])
            if count:
                self.log("오류코드_451 " + str(count) + "개")
                updateTime = time.time()
                adbInput.shell(
                    self.device, self.InstancePort, "am force-stop com.kakaogames.umamusume"
                )
                # print(position)

            count = 0
            count, position = ImageSearch(img, Images["오류코드_451_재시작"])
            if count:
                self.log("오류코드_451_재시작 " + str(count) + "개")
                updateTime = time.time()
                adbInput.shell(
                    self.device, self.InstancePort, "am force-stop com.kakaogames.umamusume"
                )
                # print(position)

            del img

        return "Stop"
