import WindowsAPIInput
import adbInput
from ImageSearch import ImageSearch
from ImageSearch import screenshotToOpenCVImg
import time
from datetime import datetime
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import QThread, pyqtSignal, QObject
import glob, os
import pickle
from 이륙_조건 import 이륙_조건
from multiprocessing import Queue
import threading
from UmaEvent import *


class UmaProcess():
    def __init__(self):
        pass
    
    def Receive_Worker(self):
        while self.ReceiverEvent.is_set() == False or self.toChild.empty() == False:
            # self.lock.acquire()
            if not self.Receive():
                time.sleep(0.01)
            # self.lock.release()
        while not self.toChild.empty():
            try:
                recv = self.toChild.get(timeout=0.001)
                print(recv)
            except:
                pass
        self.toChild.close()
        # print("자식 수신 종료")

    def Receive(self) -> bool: # 통신용
        if self.toChild.empty() == False:
            self.Lock.acquire()
            recv = self.toChild.get()
            # print(recv)
            if recv[0] == "sleepTime":
                self.sleepTime = recv[1]
                # print(recv[1])
            elif recv[0] == "terminate":
                # print("종료 신호")
                # th = threading.Thread(target=self.terminate)
                # th.start()
                self.isAlive = False
                # print(recv[1])

            elif recv[0] == "InstanceName":
                self.InstanceName = recv[1]
                # print(recv[1])
            elif recv[0] == "InstancePort":
                self.InstancePort = recv[1]
                # print(recv[1])
            elif recv[0] == "isDoneTutorial":
                self.isDoneTutorial = recv[1]
                # print(recv[1])
            elif recv[0] == "isMission":
                self.isMission = recv[1]
                # print(recv[1])
            elif recv[0] == "isSSRGacha":
                self.isSSRGacha = recv[1]
                # print(recv[1])

            elif recv[0] == "sendTotalResetCount":
                self.totalResetCount = recv[1]
                self.waiting = False
                # print(recv[1])

            elif recv[0] == "isDoingMAC_Change":
                self.isDoingMAC_Change = recv[1]
                # print(recv[1])
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
        self.isDoneTutorial = False # 체크 박스로 튜토리얼 스킵 여부 결정
        self.isMission = False # 체크 박스로 수령할 지 결정
        self.isSSRGacha = False
        self.totalResetCount = 0
        self.waiting = False
        
        self.isAlive = False
        self.sleepTime = 0.5

        self.isDoingMAC_Change = False

        # 기본 값 - pickle 불러오기 전 ---
        self.resetCount = 0
        
        # 서포트 카드 총 갯수
        path = './Supporter_cards'
        self.Supporter_cards_total = dict()
        for a in glob.glob(os.path.join(path, '*')):
            key = a.replace('.', '/').replace('\\', '/')
            key = key.split('/')
            self.Supporter_cards_total[key[-2]] = 0
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
        
        # 시작 후 버튼 잠금
        self.toParent.put(["InstanceComboBox.setEnabled", False])
        self.toParent.put(["InstanceRefreshButton.setEnabled", False])
        
        # self.toParent.put(["startButton.setEnabled", False])
        self.toParent.put(["stopButton.setEnabled", True])
        self.toParent.put(["resetButton.setEnabled", False])
        self.toParent.put(["isDoneTutorialCheckBox.setEnabled", False])
        self.toParent.put(["isMissionCheckBox.setEnabled", False])
        self.toParent.put(["isSSRGachaCheckBox.setEnabled", False])

        while self.isAlive:
            isSuccessed = self.main()

            # print("-"*50)
            self.log_main(self.InstanceName, "-"*50)
            self.log("-"*50)

            now = datetime.now()
            # print(now.strftime("%Y-%m-%d %H:%M:%S"))
            self.log_main(self.InstanceName, now.strftime("%Y-%m-%d %H:%M:%S"))
            self.log(now.strftime("%Y-%m-%d %H:%M:%S"))

            if isSuccessed == "Failed": # 리세 실패, 저장된 데이터 삭제
                try:
                    path = "./Saved_Data/"+str(self.InstancePort)+".uma"
                    os.remove(path)
                except:
                    pass
                self.resetCount += 1

            if isSuccessed == "Stop":
                # print("This thread was terminated.")
                self.log_main(str(self.InstanceName), " thread was terminated.")
                self.log("This thread was terminated.")

            # print("리세 횟수:", self.resetCount)
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
                print("리세 성공 "*5)
                self.log_main(self.InstanceName, "리세 성공 "*5)
                self.log("리세 성공 "*5)

                self.toParent.put(["terminate"])

            if isSuccessed == "숫자4080_에러_코드":
                self.toParent.put(["숫자4080_에러_코드"])
                time.sleep(30)
            
            # print("-"*50)
            self.log_main(self.InstanceName, "-"*50)
            self.log("-"*50)
            
        # print("리세 종료")
        self.log_main(self.InstanceName, "리세 종료")
        self.log("리세 종료")

        self.ReceiverEvent.set() # Receiver 스레드 종료 준비
        self.Receiver.join() # 수신 종료 대기
        self.ReceiverEvent.clear()

        # 데이터 저장
        try:
            os.makedirs("./Saved_Data")
        except:
            pass
        try:
            path = "./Saved_Data/"+str(self.InstancePort)+".uma"
            with open(file=path, mode='wb') as file:
                pickle.dump(self.resetCount, file) # -- pickle --
                pickle.dump(self.is시작하기, file) # -- pickle --
                pickle.dump(self.isPAUSED, file) # -- pickle --
                pickle.dump(self.is선물_이동, file) # -- pickle --
                pickle.dump(self.is미션_이동, file) # -- pickle --
                pickle.dump(self.is뽑기_이동, file) # -- pickle --
                pickle.dump(self.is서포트_뽑기, file) # -- pickle --
                pickle.dump(self.isSSR확정_뽑기, file) # -- pickle --
                pickle.dump(self.is뽑기_결과, file) # -- pickle --
                pickle.dump(self.is연동하기, file) # -- pickle --
                pickle.dump(self.is초기화하기, file) # -- pickle --
                
                # 서포트 카드 총 갯수
                pickle.dump(self.Supporter_cards_total, file) # -- pickle --
        except:
            path = "./Saved_Data/"+str(self.InstancePort)+".uma"
            print(path+"를 저장하는데 실패했습니다.")
            # self.log(path+"를 저장하는데 실패했습니다.")

        
        while not self.toParent.empty():
            time.sleep(0.01)
        self.toParent.close()
        # 종료됨

    def main(self):
        hwndMain = WindowsAPIInput.GetHwnd(self.InstanceName) # hwnd ID 찾기
        if hwndMain == 0:
            self.toParent.put(["terminate"])
            return "Stop"
        
        WindowsAPIInput.SetWindowSize(hwndMain, 574, 994)
        self.device = adbInput.AdbConnect(self.InstancePort)
        
        self.event: UmaEvent = UmaEvent(hwnd=hwndMain, device=self.device, InstancePort=self.InstancePort, parent=self)
        
        # 불러오기
        try:
            path = "./Saved_Data/"+str(self.InstancePort)+".uma"
            with open(file=path,  mode='rb') as file:
                self.resetCount = pickle.load(file) # -- pickle --
                self.is시작하기 = pickle.load(file) # -- pickle --
                self.isPAUSED = pickle.load(file) # -- pickle --
                self.is선물_이동 = pickle.load(file) # -- pickle --
                self.is미션_이동 = pickle.load(file) # -- pickle --
                self.is뽑기_이동 = pickle.load(file) # -- pickle --
                self.is서포트_뽑기 = pickle.load(file) # -- pickle --
                self.isSSR확정_뽑기 = pickle.load(file) # -- pickle --
                self.is뽑기_결과 = pickle.load(file) # -- pickle --
                self.is연동하기 = pickle.load(file) # -- pickle --
                self.is초기화하기 = pickle.load(file) # -- pickle --
                
                # 서포트 카드 총 갯수
                self.Supporter_cards_total = pickle.load(file) # -- pickle --
                for key, value in self.Supporter_cards_total.items():
                    self.log(key + ": " + str(value))
                self.log("기존 데이터를 불러옵니다.")
        except:
            # self.resetCount = 0 # -- pickle -- 다른건 초기화해도 리세 횟수는 초기화 하는 거 아님
            self.is시작하기 = False # -- pickle --
            self.isPAUSED = False # -- pickle --
            self.is선물_이동 = True # -- pickle --
            self.is미션_이동 = True # -- pickle --
            self.is뽑기_이동 = True # -- pickle --
            self.is서포트_뽑기 = False # -- pickle --
            self.isSSR확정_뽑기 = False # -- pickle --
            self.is뽑기_결과 = True # -- pickle --
            self.is연동하기 = False # -- pickle --
            self.is초기화하기 = False # -- pickle --
            
            # 서포트 카드 총 갯수
            path = './Supporter_cards'
            self.Supporter_cards_total = dict() # -- pickle --
            for a in glob.glob(os.path.join(path, '*')):
                key = a.replace('.', '/').replace('\\', '/')
                key = key.split('/')
                self.Supporter_cards_total[key[-2]] = 0

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

        self.toParent.put(["sendResetCount", self.resetCount]) # 리세 횟수 발신
        # 타임 = time.time()
        
        updateTime = time.time() # 타임 아웃 터치

        while self.isAlive:
            # 잠수 클릭 20초 터치락 해제
            if self.isDoneTutorial and time.time() >= updateTime + 20:
                # print("20초 정지 터치락 해제!!! "*3)
                self.log("20초 정지 터치락 해제!!! ")
                adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=(509, 66, 0, 0), deltaX=0, deltaY=0)
                time.sleep(2)
            
            # 잠수 클릭 60초 이상 앱정지
            if self.isDoneTutorial and time.time() >= updateTime + 60:
                # print("60초 정지 앱 강제종료!!! "*3)
                self.log("60초 정지 앱 강제종료!!! ")
                # WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                adbInput.shell(self.device, self.InstancePort, "am force-stop com.kakaogames.umamusume")
                adbInput.shell(self.device, self.InstancePort, "am force-stop org.mozilla.firefox")
                time.sleep(2)
                
            time.sleep(self.sleepTime)
            
            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break

            img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
            
            if self.is초기화하기 == False:
                count = self.event.SKIP(img)
                if count:
                    updateTime = time.time()
                    # print("SKIP " + str(count) + "개")
                    self.log("SKIP " + str(count) + "개")
                    continue
                
                count = self.event.우마무스메_실행(img)
                if count:
                    updateTime = time.time()
                    # print("우마무스메_실행 " + str(count) + "개")
                    self.log("우마무스메_실행 " + str(count) + "개")
                
                if self.is시작하기 == False:
                    count = self.event.게스트_로그인(img)
                    if count:
                        updateTime = time.time()
                        # print("게스트_로그인 " + str(count) + "개")
                        self.log("게스트_로그인 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.게스트로_로그인_하시겠습니까(img)
                    if count:
                        updateTime = time.time()
                        # print("게스트로_로그인_하시겠습니까 " + str(count) + "개")
                        self.log("게스트로_로그인_하시겠습니까 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.전체_동의(img)
                    if count:
                        updateTime = time.time()
                        # print("전체_동의 " + str(count) + "개")
                        self.log("전체_동의 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = self.event.시작하기(img)
                    if count:
                        updateTime = time.time()
                        # print("시작하기 " + str(count) + "개")
                        self.log("시작하기 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.TAP_TO_START(img)
                if count:
                    updateTime = time.time()
                    self.is시작하기 = True
                    # print("TAP_TO_START " + str(count) + "개")
                    self.log("TAP_TO_START " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.계정_연동_설정_요청(img)
                if count:
                    updateTime = time.time()
                    # print("계정_연동_설정_요청 " + str(count) + "개")
                    self.log("계정_연동_설정_요청 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.튜토리얼을_스킵하시겠습니까(img)
                if count:
                    updateTime = time.time()
                    # print("튜토리얼을_스킵하시겠습니까 " + str(count) + "개")
                    self.log("튜토리얼을_스킵하시겠습니까 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.게임_데이터_다운로드(img)
                if count:
                    updateTime = time.time()
                    # print("게임_데이터_다운로드 " + str(count) + "개")
                    self.log("게임_데이터_다운로드 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.트레이너_정보를_입력해주세요(img)
                if count:
                    updateTime = time.time()
                    # print("트레이너_정보를_입력해주세요 " + str(count) + "개")
                    self.log("트레이너_정보를_입력해주세요 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.등록한다(img)
                if count:
                    updateTime = time.time()
                    # print("등록한다 " + str(count) + "개")
                    self.log("등록한다 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                count = self.event.이_내용으로_등록합니다_등록하시겠습니까(img)
                if count:
                    updateTime = time.time()
                    # print("이_내용으로_등록합니다_등록하시겠습니까 " + str(count) + "개")
                    self.log("이_내용으로_등록합니다_등록하시겠습니까 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                if self.isAlive == False: # 중간에 멈춰야 할 경우
                    break
                    
                # 튜토리얼 진행, 귀찮아서 튜토리얼 멈추면 알아서 하셈
                count = self.event.출전(img)
                if count:
                    # print("출전 " + str(count) + "개")
                    self.log("출전 " + str(count) + "개")
                    self.toParent.put(["isDoneTutorial", False])
                    self.isDoneTutorial = False
                    time.sleep(1)
                
            if self.isDoneTutorial == False:
                updateTime = time.time()
                
                if self.isPAUSED == False:
                    count = self.event.울려라_팡파레(img)
                    if count:
                        # print("울려라_팡파레 " + str(count) + "개")
                        self.log("울려라_팡파레 " + str(count) + "개")
                        self.isPAUSED = True
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = self.event.닿아라_골까지(img)
                    if count:
                        # print("닿아라_골까지 " + str(count) + "개")
                        self.log("닿아라_골까지 " + str(count) + "개")
                        
                        self.isPAUSED = True
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.라이브_메뉴(img)
                if count:
                    # print("라이브_메뉴 " + str(count) + "개")
                    self.log("라이브_메뉴 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.라이브_스킵(img)
                if count:
                    # print("라이브_스킵 " + str(count) + "개")
                    self.log("라이브_스킵 " + str(count) + "개")
                    
                    self.isPAUSED = False
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.타즈나_씨와_레이스를_관전한(img)
                if count:
                    print("타즈나_씨와_레이스를_관전한 " + str(count) + "개")
                    self.log("타즈나_씨와_레이스를_관전한 " + str(count) + "개")
                    time.sleep(3)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.일본_우마무스메_트레이닝_센터_학원(img)
                if count:
                    print("일본_우마무스메_트레이닝_센터_학원 " + str(count) + "개")
                    self.log("일본_우마무스메_트레이닝_센터_학원 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.레이스의_세계를_꿈꾸는_아이들이(img)
                if count:
                    print("레이스의_세계를_꿈꾸는_아이들이 " + str(count) + "개")
                    self.log("레이스의_세계를_꿈꾸는_아이들이 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.환영(img)
                if count:
                    print("환영 " + str(count) + "개")
                    self.log("환영 " + str(count) + "개")
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.느낌표물음표(img)
                if count:
                    print("느낌표물음표 " + str(count) + "개")
                    self.log("느낌표물음표 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.아키카와_이사장님(img)
                if count:
                    print("아키카와_이사장님 " + str(count) + "개")
                    self.log("아키카와_이사장님 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.장래_유망한_트레이너의_등장에(img)
                if count:
                    print("장래_유망한_트레이너의_등장에 " + str(count) + "개")
                    self.log("장래_유망한_트레이너의_등장에 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.나는_이_학원의_이사장(img)
                if count:
                    print("나는_이_학원의_이사장 " + str(count) + "개")
                    self.log("나는_이_학원의_이사장 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.자네에_대해_가르쳐_주게나(img)
                if count:
                    print("자네에_대해_가르쳐_주게나 " + str(count) + "개")
                    self.log("자네에_대해_가르쳐_주게나 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                # 트레이너 정보 입력 -----------
            
                count = self.event.자네는_트레센_학원의_일원일세(img)
                if count:
                    print("자네는_트레센_학원의_일원일세 " + str(count) + "개")
                    self.log("자네는_트레센_학원의_일원일세 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.담당_우마무스메와_함께(img)
                if count:
                    print("담당_우마무스메와_함께 " + str(count) + "개")
                    self.log("담당_우마무스메와_함께 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.학원에_다니는_우마무스메의(img)
                if count:
                    print("학원에_다니는_우마무스메의 " + str(count) + "개")
                    self.log("학원에_다니는_우마무스메의 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.자네는_트레이너로서_담당_우마무스메를(img)
                if count:
                    print("자네는_트레이너로서_담당_우마무스메를 " + str(count) + "개")
                    self.log("자네는_트레이너로서_담당_우마무스메를 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.가슴에_단_트레이너_배지에(img)
                if count:
                    print("가슴에_단_트레이너_배지에 " + str(count) + "개")
                    self.log("가슴에_단_트레이너_배지에 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.실전_연수를_하러_가시죠(img)
                if count:
                    print("실전_연수를_하러_가시죠 " + str(count) + "개")
                    self.log("실전_연수를_하러_가시죠 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.프리티_더비_뽑기_5번_뽑기_무료(img)
                if count:
                    print("프리티_더비_뽑기_5번_뽑기_무료 " + str(count) + "개")
                    self.log("프리티_더비_뽑기_5번_뽑기_무료 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.튜토리얼_용_프리티_더비_뽑기(img)
                if count:
                    print("튜토리얼_용_프리티_더비_뽑기 " + str(count) + "개")
                    self.log("튜토리얼_용_프리티_더비_뽑기 " + str(count) + "개")
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.서포트_카드_화살표(img)
                if count:
                    print("서포트_카드_화살표 " + str(count) + "개") # 느림
                    self.log("서포트_카드_화살표 " + str(count) + "개") # 느림
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.서포트_카드_뽑기_10번_뽑기_무료(img)
                if count:
                    print("서포트_카드_뽑기_10번_뽑기_무료 " + str(count) + "개")
                    self.log("서포트_카드_뽑기_10번_뽑기_무료 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.튜토리얼_용_서포트_카드_뽑기(img)
                if count:
                    print("튜토리얼_용_서포트_카드_뽑기 " + str(count) + "개")
                    self.log("튜토리얼_용_서포트_카드_뽑기 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.육성_화살표(img)
                if count:
                    print("육성_화살표 " + str(count) + "개")
                    self.log("육성_화살표 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                # 이미지 바꿀 예정
                count = self.event.육성_시나리오를_공략하자(img)
                if count:
                    print("육성_시나리오를_공략하자 " + str(count) + "개")
                    self.log("육성_시나리오를_공략하자 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.다음_화살표(img)
                if count:
                    print("다음_화살표 " + str(count) + "개")
                    self.log("다음_화살표 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자(img)
                if count:
                    print("트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 " + str(count) + "개")
                    self.log("트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.마음에_드는_우마무스메를_육성하자(img)
                if count:
                    print("마음에_드는_우마무스메를_육성하자 " + str(count) + "개")
                    self.log("마음에_드는_우마무스메를_육성하자 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.다이와_스칼렛_클릭(img)
                if count:
                    print("다이와_스칼렛_클릭 " + str(count) + "개")
                    self.log("다이와_스칼렛_클릭 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.다음_화살표_육성_우마무스메_선택(img)
                if count:
                    print("다음_화살표_육성_우마무스메_선택 " + str(count) + "개")
                    self.log("다음_화살표_육성_우마무스메_선택 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.플러스_계승_우마무스메_선택_화살표(img)
                
                if count:
                    
                    print("플러스_계승_우마무스메_선택_화살표 " + str(count) + "개")
                    self.log("플러스_계승_우마무스메_선택_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.계승_보드카_선택_화살표(img)
                
                if count:
                    
                    print("계승_보드카_선택_화살표 " + str(count) + "개")
                    self.log("계승_보드카_선택_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.보드카_결정_화살표(img)
                
                if count:
                    
                    print("보드카_결정_화살표 " + str(count) + "개")
                    self.log("보드카_결정_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.자동_선택_화살표(img)
                
                if count:
                    
                    print("자동_선택_화살표 " + str(count) + "개")
                    self.log("자동_선택_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.자동_선택_확인_OK_화살표(img)
                
                if count:
                    
                    print("자동_선택_확인_OK_화살표 " + str(count) + "개")
                    self.log("자동_선택_확인_OK_화살표 " + str(count) + "개")
                    
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.마음을_이어서_꿈을_이루자(img)
                
                if count:
                    
                    print("마음을_이어서_꿈을_이루자 " + str(count) + "개")
                    self.log("마음을_이어서_꿈을_이루자 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.계승_최종_다음_화살표(img)
                
                if count:
                    
                    print("계승_최종_다음_화살표 " + str(count) + "개")
                    self.log("계승_최종_다음_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.서포트_카드를_편성해서_육성_효율_UP(img)
                
                if count:
                    
                    print("서포트_카드를_편성해서_육성_효율_UP " + str(count) + "개")
                    self.log("서포트_카드를_편성해서_육성_효율_UP " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.서포트_카드의_타입에_주목(img)
                
                if count:
                    
                    print("서포트_카드의_타입에_주목 " + str(count) + "개")
                    self.log("서포트_카드의_타입에_주목 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.우정_트레이닝이_육성의_열쇠를_쥐고_있다(img)
                
                if count:
                    
                    print("우정_트레이닝이_육성의_열쇠를_쥐고_있다 " + str(count) + "개")
                    self.log("우정_트레이닝이_육성의_열쇠를_쥐고_있다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.서포트_자동_편성_화살표(img)
                
                if count:
                    
                    print("서포트_자동_편성_화살표 " + str(count) + "개")
                    self.log("서포트_자동_편성_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성_시작_화살표(img)
                
                if count:
                    
                    print("육성_시작_화살표 " + str(count) + "개")
                    self.log("육성_시작_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.TP를_소비해_육성_시작_화살표(img)
                
                if count:
                    
                    print("TP를_소비해_육성_시작_화살표 " + str(count) + "개")
                    self.log("TP를_소비해_육성_시작_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.초록색_역삼각형(img)
                
                if count:
                    
                    print("초록색_역삼각형 " + str(count) + "개")
                    self.log("초록색_역삼각형 " + str(count) + "개")
                    
                    time.sleep(0.5)
                
                count = self.event.TAP(img)
                
                if count:
                    
                    print("TAP " + str(count) + "개")
                    self.log("TAP " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.우마무스메에겐_저마다_다른_목표가_있습니다(img)
                
                if count:
                    
                    print("우마무스메에겐_저마다_다른_목표가_있습니다 " + str(count) + "개")
                    self.log("우마무스메에겐_저마다_다른_목표가_있습니다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.이쪽은_육성을_진행할_때_필요한_커맨드입니다(img)
                
                if count:
                    
                    print("이쪽은_육성을_진행할_때_필요한_커맨드입니다 " + str(count) + "개")
                    self.log("이쪽은_육성을_진행할_때_필요한_커맨드입니다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.커맨드를_하나_실행하면_턴을_소비합니다(img)
                
                if count:
                    
                    print("커맨드를_하나_실행하면_턴을_소비합니다 " + str(count) + "개")
                    self.log("커맨드를_하나_실행하면_턴을_소비합니다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.우선_트레이닝을_선택해_보세요(img)
                
                if count:
                    
                    print("우선_트레이닝을_선택해_보세요 " + str(count) + "개")
                    self.log("우선_트레이닝을_선택해_보세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.이게_실행할_수_있는_트레이닝들입니다(img)
                
                if count:
                    
                    print("이게_실행할_수_있는_트레이닝들입니다 " + str(count) + "개")
                    self.log("이게_실행할_수_있는_트레이닝들입니다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.한_번_스피드를_골라_보세요(img)
                
                if count:
                    
                    print("한_번_스피드를_골라_보세요 " + str(count) + "개")
                    self.log("한_번_스피드를_골라_보세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.파란색_역삼각형(img)
                
                if count:
                    
                    print("파란색_역삼각형 " + str(count) + "개")
                    self.log("파란색_역삼각형 " + str(count) + "개")
                    
                    time.sleep(0.5)
                
                count = self.event.약속(img)
                
                if count:
                    
                    print("약속 " + str(count) + "개")
                    self.log("약속 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.서둘러_가봐(img)
                
                if count:
                    
                    print("서둘러_가봐 " + str(count) + "개")
                    self.log("서둘러_가봐 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.그때_번뜩였다(img)
                
                if count:
                    
                    print("그때_번뜩였다 " + str(count) + "개")
                    self.log("그때_번뜩였다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.다이와_스칼렛의_성장으로_이어졌다(img)
                
                if count:
                    
                    print("다이와_스칼렛의_성장으로_이어졌다 " + str(count) + "개")
                    self.log("다이와_스칼렛의_성장으로_이어졌다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.다음으로_육성_우마무스메의_체력에_관해_설명할게요(img)
                
                if count:
                    
                    print("다음으로_육성_우마무스메의_체력에_관해_설명할게요 " + str(count) + "개")
                    self.log("다음으로_육성_우마무스메의_체력에_관해_설명할게요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.우선_아까처럼_트레이닝을_선택해_보세요(img)
                
                if count:
                    
                    print("우선_아까처럼_트레이닝을_선택해_보세요 " + str(count) + "개")
                    self.log("우선_아까처럼_트레이닝을_선택해_보세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.여기_실패율에_주목해_주세요(img)
                
                if count:
                    
                    print("여기_실패율에_주목해_주세요 " + str(count) + "개")
                    self.log("여기_실패율에_주목해_주세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.남은_체력이_적을수록_실패율이_높아지게_돼요(img)
                
                if count:
                    
                    print("남은_체력이_적을수록_실패율이_높아지게_돼요 " + str(count) + "개")
                    self.log("남은_체력이_적을수록_실패율이_높아지게_돼요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.트레이닝에_실패하면_능력과_컨디션이(img)
                
                if count:
                    
                    print("트레이닝에_실패하면_능력과_컨디션이 " + str(count) + "개")
                    self.log("트레이닝에_실패하면_능력과_컨디션이 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.돌아간다_화살표(img)
                
                if count:
                    
                    print("돌아간다_화살표 " + str(count) + "개")
                    self.log("돌아간다_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.체력이_적을_때는_우마무스메를(img)
                
                if count:
                    
                    print("체력이_적을_때는_우마무스메를 " + str(count) + "개")
                    self.log("체력이_적을_때는_우마무스메를 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.먼저_여기_스킬을_선택해보세요(img)
                
                if count:
                    
                    print("먼저_여기_스킬을_선택해보세요 " + str(count) + "개")
                    self.log("먼저_여기_스킬을_선택해보세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.다음으로_배울_스킬을_선택하세요(img)
                
                if count:
                    
                    print("다음으로_배울_스킬을_선택하세요 " + str(count) + "개")
                    self.log("다음으로_배울_스킬을_선택하세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.이번에는_이_스킬을_습득해_보세요(img)
                
                if count:
                    
                    print("이번에는_이_스킬을_습득해_보세요 " + str(count) + "개")
                    self.log("이번에는_이_스킬을_습득해_보세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.스킬_결정_화살표(img)
                
                if count:
                    
                    print("스킬_결정_화살표 " + str(count) + "개")
                    self.log("스킬_결정_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.스킬_획득_화살표(img)
                
                if count:
                    
                    print("스킬_획득_화살표 " + str(count) + "개")
                    self.log("스킬_획득_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.스킬_획득_돌아간다_화살표(img)
                
                if count:
                    
                    print("스킬_획득_돌아간다_화살표 " + str(count) + "개")
                    self.log("스킬_획득_돌아간다_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.이졔_준비가_다_끝났어요_레이스에_출전해_봐요(img)
                
                if count:
                    
                    print("이졔_준비가_다_끝났어요_레이스에_출전해_봐요 " + str(count) + "개")
                    self.log("이졔_준비가_다_끝났어요_레이스에_출전해_봐요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.출전_화살표(img)
                
                if count:
                    
                    print("출전_화살표 " + str(count) + "개")
                    self.log("출전_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.숫자1등이_되기_위해서도_말야(img)
                
                if count:
                    
                    print("숫자1등이_되기_위해서도_말야 " + str(count) + "개")
                    self.log("숫자1등이_되기_위해서도_말야 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.패덕에서는_레이스에_출전하는_우마무스메의(img)
                
                if count:
                    
                    print("패덕에서는_레이스에_출전하는_우마무스메의 " + str(count) + "개")
                    self.log("패덕에서는_레이스에_출전하는_우마무스메의 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.우선_예상_표시에_관해서_설명할게요(img)
                
                if count:
                    
                    print("우선_예상_표시에_관해서_설명할게요 " + str(count) + "개")
                    self.log("우선_예상_표시에_관해서_설명할게요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.숫자3개의_표시는_전문가들의_예상을_나타내며(img)
                
                if count:
                    
                    print("3개의_표시는_전문가들의_예상을_나타내며 " + str(count) + "개")
                    self.log("3개의_표시는_전문가들의_예상을_나타내며 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.능력과_컨디션이_좋을수록_많은_기대를_받게_돼서(img)
                
                if count:
                    
                    print("능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 " + str(count) + "개")
                    self.log("능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.물론_반드시_우승하게_되는_건_아니지만(img)
                
                if count:
                    
                    print("물론_반드시_우승하게_되는_건_아니지만 " + str(count) + "개")
                    self.log("물론_반드시_우승하게_되는_건_아니지만 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.또_패덕에서는_우마무스메의_작전을(img)
                
                if count:
                    
                    print("또_패덕에서는_우마무스메의_작전을 " + str(count) + "개")
                    self.log("또_패덕에서는_우마무스메의_작전을 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.선행A_화살표(img)
                
                if count:
                    
                    print("선행A_화살표 " + str(count) + "개")
                    self.log("선행A_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.작전_결정(img)
                
                if count:
                    
                    print("작전_결정 " + str(count) + "개")
                    self.log("작전_결정 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.이것으로_준비는_다_됐어요(img)
                
                if count:
                    
                    print("이것으로_준비는_다_됐어요 " + str(count) + "개")
                    self.log("이것으로_준비는_다_됐어요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.첫_우승_축하_드려요(img)
                
                if count:
                    
                    print("첫_우승_축하_드려요 " + str(count) + "개")
                    self.log("첫_우승_축하_드려요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.좋아(img)
                
                if count:
                    
                    print("좋아 " + str(count) + "개")
                    self.log("좋아 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.목표_달성(img)
                
                if count:
                    
                    print("목표_달성 " + str(count) + "개")
                    self.log("목표_달성 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성_목표_달성(img)
                
                if count:
                    
                    print("육성_목표_달성 " + str(count) + "개")
                    self.log("육성_목표_달성 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성_수고하셨습니다(img)
                
                if count:
                    
                    print("육성_수고하셨습니다 " + str(count) + "개")
                    self.log("육성_수고하셨습니다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.스킬_포인트가_남았다면(img)
                
                if count:
                    
                    print("스킬_포인트가_남았다면 " + str(count) + "개")
                    self.log("스킬_포인트가_남았다면 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성은_이것으로_종료입니다(img)
                
                if count:
                    
                    print("육성은_이것으로_종료입니다 " + str(count) + "개")
                    self.log("육성은_이것으로_종료입니다 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.또_연수_기간은_짧았지만(img)
                
                if count:
                    
                    print("또_연수_기간은_짧았지만 " + str(count) + "개")
                    self.log("또_연수_기간은_짧았지만 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성_완료_화살표(img)
                
                if count:
                    
                    print("육성_완료_화살표 " + str(count) + "개")
                    self.log("육성_완료_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성_완료_확인_완료한다_화살표(img)
                
                if count:
                    
                    print("육성_완료_확인_완료한다_화살표 " + str(count) + "개")
                    self.log("육성_완료_확인_완료한다_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후(img)
                
                if count:
                    
                    print("육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 " + str(count) + "개")
                    self.log("육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.최고_랭크를_목표로_힘내세요(img)
                
                if count:
                    
                    print("최고_랭크를_목표로_힘내세요 " + str(count) + "개")
                    self.log("최고_랭크를_목표로_힘내세요 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.랭크_육성(img)
                
                if count:
                    
                    print("랭크_육성 " + str(count) + "개")
                    self.log("랭크_육성 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.육성을_끝낸_우마무스메는_인자를(img)
                
                if count:
                    
                    print("육성을_끝낸_우마무스메는_인자를 " + str(count) + "개")
                    self.log("육성을_끝낸_우마무스메는_인자를 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.계승_우마무스메로_선택하면_새로운_우마무스메에게(img)
                
                if count:
                    
                    print("계승_우마무스메로_선택하면_새로운_우마무스메에게 " + str(count) + "개")
                    self.log("계승_우마무스메로_선택하면_새로운_우마무스메에게 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.인자획득(img)
                
                if count:
                    
                    print("인자획득 " + str(count) + "개")
                    self.log("인자획득 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.우마무스메_상세_닫기_화살표(img)
                
                if count:
                    
                    print("우마무스메_상세_닫기_화살표 " + str(count) + "개")
                    self.log("우마무스메_상세_닫기_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.평가점(img)
                
                if count:
                    
                    print("평가점 " + str(count) + "개")
                    self.log("평가점 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.보상획득(img)
                
                if count:
                    
                    print("보상획득 " + str(count) + "개")
                    self.log("보상획득 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = self.event.강화_편성_화살표(img)
                
                if count:
                    print(position[0])
                    
                    print("강화_편성_화살표 " + str(count) + "개")
                    self.log("강화_편성_화살표 " + str(count) + "개")
                    
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.레이스_화살표(img)
                
                if count:
                    
                    print("레이스_화살표 " + str(count) + "개")
                    self.log("레이스_화살표 " + str(count) + "개")
                    
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_경기장_화살표(img)
                
                if count:
                    
                    print("팀_경기장_화살표 " + str(count) + "개")
                    self.log("팀_경기장_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.오리지널_팀을_결성_상위_CLASS를_노려라(img)
                
                if count:
                    
                    print("오리지널_팀을_결성_상위_CLASS를_노려라 " + str(count) + "개")
                    self.log("오리지널_팀을_결성_상위_CLASS를_노려라 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.하이스코어를_기록해서_CLASS_승급을_노리자(img)
                
                if count:
                    
                    print("하이스코어를_기록해서_CLASS_승급을_노리자 " + str(count) + "개")
                    self.log("하이스코어를_기록해서_CLASS_승급을_노리자 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.기간_중에_개최되는_5개의_레이스에(img)
                
                if count:
                    
                    print("기간_중에_개최되는_5개의_레이스에 " + str(count) + "개")
                    self.log("기간_중에_개최되는_5개의_레이스에 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.서포트_카드의_Lv을_UP해서(img)
                
                if count:
                    
                    print("서포트_카드의_Lv을_UP해서 " + str(count) + "개")
                    self.log("서포트_카드의_Lv을_UP해서 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_편성(img)
                
                if count:
                    
                    print("팀_편성 " + str(count) + "개")
                    self.log("팀_편성 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.전당_입성_우마무스메로_자신만의_팀을_결성(img)
                
                if count:
                    
                    print("전당_입성_우마무스메로_자신만의_팀을_결성 " + str(count) + "개")
                    self.log("전당_입성_우마무스메로_자신만의_팀을_결성 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_랭크를_올려서_최강의_팀이_되자(img)
                
                if count:
                    
                    print("팀_랭크를_올려서_최강의_팀이_되자 " + str(count) + "개")
                    self.log("팀_랭크를_올려서_최강의_팀이_되자 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠(img)
                
                if count:
                    
                    print("팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠 " + str(count) + "개")
                    self.log("팀_평가를_높이는_것이_팀_경기장을_공략하는_열쇠 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_편성_다이와_스칼렛_화살표_클릭(img)
                
                if count:
                    
                    print("팀_편성_다이와_스칼렛_화살표_클릭 " + str(count) + "개")
                    self.log("팀_편성_다이와_스칼렛_화살표_클릭 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.출전_우마무스메_선택_다이와_스칼렛_화살표(img)
                
                if count:
                    
                    print("출전_우마무스메_선택_다이와_스칼렛_화살표 " + str(count) + "개")
                    self.log("출전_우마무스메_선택_다이와_스칼렛_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_편성_확정_화살표(img)
                
                if count:
                    
                    print("팀_편성_확정_화살표 " + str(count) + "개")
                    self.log("팀_편성_확정_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.편성을_확정합니다_진행하시겠습니까(img)
                
                if count:
                    
                    print("편성을_확정합니다_진행하시겠습니까 " + str(count) + "개")
                    self.log("편성을_확정합니다_진행하시겠습니까 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.팀_최고_평가점_갱신_닫기(img)
                
                if count:
                    
                    print("팀_최고_평가점_갱신_닫기 " + str(count) + "개")
                    self.log("팀_최고_평가점_갱신_닫기 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.홈_화살표(img)
                
                if count:
                    
                    print("홈_화살표 " + str(count) + "개")
                    self.log("홈_화살표 " + str(count) + "개")
                    
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
            
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            if self.is초기화하기 == False:

                count = self.event.공지사항_X(img)
                if count:
                    updateTime = time.time()
                    # print("공지사항_X " + str(count) + "개")
                    self.log("공지사항_X " + str(count) + "개")
                    self.isDoneTutorial = True
                    self.toParent.put(["isDoneTutorial", True])
                    # self.parent.isDoneTutorialCheckBox.setChecked(True)
                    img = screenshotToOpenCVImg(hwndMain)
                
                    
                count = self.event.메인_스토리가_해방되었습니다(img)
                if count:
                    updateTime = time.time()
                    # print("메인_스토리가_해방되었습니다 " + str(count) + "개")
                    self.log("메인_스토리가_해방되었습니다 " + str(count) + "개")
                    self.isDoneTutorial = True
                    self.toParent.put(["isDoneTutorial", True])
                    # self.parent.isDoneTutorialCheckBox.setChecked(True)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.여러_스토리를_해방할_수_있게_되었습니다(img)
                if count:
                    updateTime = time.time()
                    # print("여러_스토리를_해방할_수_있게_되었습니다 " + str(count) + "개")
                    self.log("여러_스토리를_해방할_수_있게_되었습니다 " + str(count) + "개")
                    self.isDoneTutorial = True
                    self.toParent.put(["isDoneTutorial", True])
                    # self.parent.isDoneTutorialCheckBox.setChecked(True)
                    img = screenshotToOpenCVImg(hwndMain)
            
            # 선물 수령
            if self.isDoneTutorial and self.is선물_이동 == True:
                
                count = self.event.선물_이동(img)
                if count:
                    updateTime = time.time()
                    # print("선물_이동 " + str(count) + "개")
                    self.log("선물_이동 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                count = self.event.선물_일괄_수령(img)
                if count:
                    # updateTime = time.time() 먹통 예상
                    # print("선물_일괄_수령 " + str(count) + "개")
                    self.log("선물_일괄_수령 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                count = self.event.상기의_선물을_수령했습니다(img)
                if count:
                    updateTime = time.time()
                    # print("상기의_선물을_수령했습니다 " + str(count) + "개")
                    self.log("상기의_선물을_수령했습니다 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

            if self.is초기화하기 == False:
                count = self.event.받을_수_있는_선물이_없습니다(img)
                if count:
                    updateTime = time.time()
                    # print("받을_수_있는_선물이_없습니다 " + str(count) + "개")
                    self.log("받을_수_있는_선물이_없습니다 " + str(count) + "개")
                    self.is선물_이동 = False
                    img = screenshotToOpenCVImg(hwndMain)

            # 미션 수령
            if self.isDoneTutorial and self.isMission and self.is미션_이동:
                count = self.event.미션_이동(img)
                if count:
                    updateTime = time.time()
                    # print("미션_이동 " + str(count) + "개")
                    self.log("미션_이동 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                count = self.event.미션_메인(img)
                if count:
                    updateTime = time.time()
                    # print("미션_메인 " + str(count) + "개")
                    self.log("미션_메인 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                count = self.event.미션_일괄_수령(img)
                if count:
                    updateTime = time.time()
                    # print("미션_일괄_수령 " + str(count) + "개")
                    self.log("미션_일괄_수령 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

                count = self.event.미션_일괄_수령_확인됨(img)
                if count:
                    updateTime = time.time()
                    # print("미션_일괄_수령_확인됨 " + str(count) + "개")
                    self.log("미션_일괄_수령_확인됨 " + str(count) + "개")
                    self.is미션_이동 = False
                    img = screenshotToOpenCVImg(hwndMain)

            count = self.event.상기의_보상을_수령했습니다(img)
            if count:
                updateTime = time.time()
                # print("상기의_보상을_수령했습니다 " + str(count) + "개")
                self.log("상기의_보상을_수령했습니다 " + str(count) + "개")
                self.is미션_이동 = False
                img = screenshotToOpenCVImg(hwndMain)

            if self.is미션_이동 == False:
                count = self.event.돌아간다(img)
                if count:
                    updateTime = time.time()
                    # print("돌아간다 " + str(count) + "개")
                    self.log("돌아간다 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break

            # 뽑기
            if self.isDoneTutorial and self.is뽑기_이동:
                count = self.event.뽑기_이동(img)
                if count:
                    updateTime = time.time()
                    # print("뽑기_이동 " + str(count) + "개")
                    self.log("뽑기_이동 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)

            if self.is초기화하기 == False:
                count = 0
                count, position = ImageSearch(img, Images["프리티_더비_뽑기"], 154, 551, 175, 93, confidence=0.6)
                if count:
                    updateTime = time.time()
                    # print("프리티_더비_뽑기 " + str(count) + "개")
                    self.log("프리티_더비_뽑기 " + str(count) + "개")
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    if self.isSSR확정_뽑기 == False:
                        adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=262, deltaX=5, deltaY=5)
                        self.is서포트_뽑기 = True
                    else:
                        if 이륙_조건(self.Supporter_cards_total): # 이륙 조건
                            return True
                        adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4") # "KEYCODE_BACK"
                        self.is뽑기_이동 = False
                        self.is연동하기 = True
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

            if self.is서포트_뽑기:
                count = 0
                count, position = ImageSearch(img, Images["서포트_카드_뽑기"], 160, 552, 154, 94, confidence=0.6) # 돌이 없는거 클릭 해봐야 암
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=199, offsetY=191, deltaX=5, deltaY=5)
                    # print("서포트_카드_뽑기 " + str(count) + "개")
                    self.log("서포트_카드_뽑기 " + str(count) + "개")
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

            if self.isDoneTutorial and self.is뽑기_이동:
                if self.isAlive == False: # 중간에 멈춰야 할 경우
                    break
                
                count = self.event.무료_쥬얼부터_먼저_사용됩니다(img)
                if count:
                    updateTime = time.time()
                    self.is뽑기_결과 = True
                    # print("무료_쥬얼부터_먼저_사용됩니다 " + str(count) + "개")
                    self.log("무료_쥬얼부터_먼저_사용됩니다 " + str(count) + "개")
                    
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.뽑기_결과(img)
                if count and self.is뽑기_결과:
                    updateTime = time.time()
                    self.is뽑기_결과 = False
                    # print("뽑기_결과 " + str(count) + "개")
                    self.log("뽑기_결과 " + str(count) + "개")
                    
                    # 서포터 카드 지금 갯수
                    path = './Supporter_cards'
                    Supporter_cards_now = dict()
                    for a in glob.glob(os.path.join(path, '*')):
                        key = a.replace('.', '/').replace('\\', '/')
                        key = key.split('/')
                        Supporter_cards_now[key[-2]] = 0
                        
                    for _ in range(2):
                        updateTime = time.time()
                        time.sleep(0.1)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                        for key, value in Supporter_cards.items():
                            count = 0
                            count, position = ImageSearch(img, value, 46, 122, 451, 715, grayscale=False)
                            if count:
                                if Supporter_cards_now[key] < count:
                                    Supporter_cards_now[key] = count
                                # print(key + " " + str(Supporter_cards_now[key]) + "개")
                                self.log(key + " " + str(Supporter_cards_now[key]) + "개")
                                
                                
                    # 지금 뽑힌 결과 총 서포터 카드 갯수에 더하기
                    for key, value in self.Supporter_cards_total.items():
                        self.Supporter_cards_total[key] += Supporter_cards_now[key]
                    
                    # 총 서포터 카드 갯수
                    total_count = 0
                    for key, value in self.Supporter_cards_total.items():
                        if value:
                            total_count += value
                    
                    if total_count:
                        # print("-"*50)
                        self.log_main(self.InstanceName, "-"*50)
                        self.log("-"*50)
                    
                        for key, value in self.Supporter_cards_total.items():
                            if value:
                                # print(key + ": " + str(value))
                                self.log_main(self.InstanceName, key + ": " + str(value))
                                self.log(key + ": " + str(value))
                    
                        # print("-"*50)
                        self.log_main(self.InstanceName, "-"*50)
                        self.log("-"*50)
                    
                if self.isAlive == False: # 중간에 멈춰야 할 경우
                    break

                count = self.event.한_번_더_뽑기(img)
                if count:
                    updateTime = time.time()
                    # print("한_번_더_뽑기 " + str(count) + "개")
                    self.log("한_번_더_뽑기 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                
            
            if self.isDoneTutorial and self.is초기화하기 == False:
                count = 0
                count, position = ImageSearch(img, Images["쥬얼이_부족합니다"], 165, 586, 207, 41)
                if count:
                    updateTime = time.time()

                    if 이륙_조건(self.Supporter_cards_total): # 이륙 조건
                        return True

                    if self.isSSRGacha:
                        self.is서포트_뽑기 = False
                        self.isSSR확정_뽑기 = True
                    else:
                        self.is뽑기_이동 = False
                        self.is연동하기 = True
                    
                    adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4") # "KEYCODE_BACK" 
                    time.sleep(0.5)
                    adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4")
                    # print("쥬얼이_부족합니다 " + str(count) + "개")
                    self.log("쥬얼이_부족합니다 " + str(count) + "개")
                    
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = self.event.상점_화면을_표시할_수_없습니다(img)
                if count:
                    updateTime = time.time()
                    # print("상점_화면을_표시할_수_없습니다 " + str(count) + "개")
                    self.log("상점_화면을_표시할_수_없습니다 " + str(count) + "개")
                    img = screenshotToOpenCVImg(hwndMain)
                
                if self.isDoneTutorial and self.isSSRGacha and self.isSSR확정_뽑기:
                    count = 0
                    count, position = ImageSearch(img, Images["서포트_카드_뽑기"], 160, 552, 154, 94, confidence=0.6) # 돌이 없는거 클릭 해봐야 암
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksSwipe(self.device, self.InstancePort, position=position[0], offsetX=272, deltaX=5, deltaY=5)
                        # print("서포트_카드_뽑기 " + str(count) + "개")
                        self.log("서포트_카드_뽑기 " + str(count) + "개")
                        
                        time.sleep(0.8)
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.숫자3성_확정(img)
                    if count:
                        updateTime = time.time()
                        # print("숫자3성_확정 " + str(count) + "개")
                        self.log("숫자3성_확정 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.SSR_확정_스타트_대시(img)
                    if count:
                        updateTime = time.time()
                        # print("SSR_확정_스타트_대시 " + str(count) + "개")
                        self.log("SSR_확정_스타트_대시 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.SSR_확정_메이크_데뷔_뽑기(img)
                    if count:
                        updateTime = time.time()
                        # print("SSR_확정_메이크_데뷔_뽑기 " + str(count) + "개")
                        self.log("SSR_확정_메이크_데뷔_뽑기 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.SSR_확정_메이크_데뷔_티켓을_1장_사용해(img)
                    if count:
                        updateTime = time.time()
                        self.is뽑기_결과 = True
                        # print("SSR_확정_메이크_데뷔_티켓을_1장_사용해 " + str(count) + "개")
                        self.log("SSR_확정_메이크_데뷔_티켓을_1장_사용해 " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = self.event.뽑기_결과_OK(img)
                    if count:
                        updateTime = time.time()
                        # print("뽑기_결과_OK " + str(count) + "개")
                        self.log("뽑기_결과_OK " + str(count) + "개")
                        img = screenshotToOpenCVImg(hwndMain)

                    
                if self.is연동하기:
                    # adbInput.shell(self.device, self.InstancePort, "")
                    adbInput.shell(self.device, self.InstancePort, "am force-stop com.kakaogames.umamusume")
                    time.sleep(1)
                    adbInput.shell(self.device, self.InstancePort, "/system/xbin/bstk/su -c rm -rf /data/data/com.kakaogames.umamusume/shared_prefs")
                    self.log("삭제_완료")
                    return "Failed"

            # 특수 이벤트
            count = self.event.모두_지우기(img)
            if count:
                updateTime = time.time()
                # print("모두_지우기 " + str(count) + "개")
                self.log("모두_지우기 " + str(count) + "개")
                img = screenshotToOpenCVImg(hwndMain)


            count = self.event.추가_데이터를_다운로드합니다(img)
            if count:
                updateTime = time.time()
                # print("추가_데이터를_다운로드합니다 " + str(count) + "개")
                self.log("추가_데이터를_다운로드합니다 " + str(count) + "개")
                img = screenshotToOpenCVImg(hwndMain)
                
            count = self.event.재시도(img)
            if count:
                updateTime = time.time()
                # print("재시도 " + str(count) + "개")
                self.log("재시도 " + str(count) + "개")
                continue
            
            count = self.event.타이틀_화면으로(img)
            if count:
                updateTime = time.time()
                # print("타이틀_화면으로 " + str(count) + "개")
                self.log("타이틀_화면으로 " + str(count) + "개")
                continue
            
            count = self.event.확인(img)
            if count:
                updateTime = time.time()
                # print("확인 " + str(count) + "개")
                self.log("확인 " + str(count) + "개")
                img = screenshotToOpenCVImg(hwndMain)
            
            count = self.event.앱_닫기(img)
            if count:
                updateTime = time.time()
                # print("앱_닫기 " + str(count) + "개")
                self.log("앱_닫기 " + str(count) + "개")
                img = screenshotToOpenCVImg(hwndMain)
            
            count = self.event.날짜가_변경됐습니다(img)
            if count:
                updateTime = time.time()
                # print("날짜가_변경됐습니다 " + str(count) + "개")
                self.log("날짜가_변경됐습니다 " + str(count) + "개")
                img = screenshotToOpenCVImg(hwndMain)
            
            count = self.event.숫자4080_에러_코드(img)
            if count:
                updateTime = time.time()
                print("숫자4080_에러_코드 " + str(count) + "개")
                self.log("숫자4080_에러_코드 " + str(count) + "개")
                if self.isDoingMAC_Change == False:
                    return "숫자4080_에러_코드"

        return "Stop"