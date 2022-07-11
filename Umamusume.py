# pip install pure-python-adb
import WindowsAPIInput
import adbInput
from ImageSearch import ImageSearch
from ImageSearch import screenshotToOpenCVImg
import time
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
from ImageVariables import * # 이미지
import glob, os
import pickle


class Umamusume(QThread):
    recvLog = pyqtSignal(str)
    recvLog_Main = pyqtSignal(str, str)
    Error_4080 = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        self.isAlive = False
        self.resetCount = 0
        
        try:
            self.sleepTime = self.parent.sleepTime
        except:
            self.sleepTime = 0.5

        self.isStopped = False
        self.isDoingMAC_Change = False
        
        # 커스텀 시그널 정의
        
        self.recvLog.connect(self.parent.sendLog)
        self.recvLog_Main.connect(self.parent.parent.sendLog_Main)
        self.Error_4080.connect(self.parent.Error_4080Function)
       
    def log(self, text):
        self.recvLog.emit(text)

    def log_main(self, id, text):
        self.recvLog_Main.emit(str(id), str(text))
    
    def Error_4080Function(self):
        self.Error_4080.emit()
        
    def run(self):
        self.isAlive = True
        self.isStopped = False
        
        self.InstanceName = self.parent.InstanceName
        self.InstancePort = self.parent.InstancePort
        
        
        while self.isAlive:
            isSuccessed = self.main()

            # print("-"*50)
            self.log_main(self.InstanceName, "-"*50)
            self.log("-"*50)

            now = datetime.now()
            # print(now.strftime("%Y-%m-%d %H:%M:%S"))
            self.log_main(self.InstanceName, now.strftime("%Y-%m-%d %H:%M:%S"))
            self.log(now.strftime("%Y-%m-%d %H:%M:%S"))

            # print("튜토리얼 스킵 여부:", self.parent.isDoneTutorialCheckBox.isChecked())
            self.log_main(self.InstanceName, "튜토리얼 스킵 여부: " + str(self.parent.isDoneTutorialCheckBox.isChecked()))
            self.log("튜토리얼 스킵 여부: " + str(self.parent.isDoneTutorialCheckBox.isChecked()))

            if isSuccessed == "Failed": # 데이터 삭제
                try:
                    path = "./Saved_Data/"+str(self.parent.InstancePort)+".uma"
                    os.remove(path)
                except:
                    pass
                self.resetCount += 1

            if isSuccessed == "Stop":
                # print("This thread was terminated.")
                self.log_main(self.InstanceName,  str(self.InstanceName) + " thread was terminated.")
                self.log("This thread was terminated.")

            # print("리세 횟수:", self.resetCount)
            total_resetCount = 0
            for i in self.parent.parent.Tab:
                total_resetCount += i.umamusume.resetCount
            self.log_main("리세 총 횟수: ", str(int(total_resetCount)))
            self.log_main(self.InstanceName, "리세 횟수: " + str(int(self.resetCount)))
            self.log("리세 횟수: " + str(int(self.resetCount)))

            if isSuccessed == True:
                self.parent.stopButton.setEnabled(False)
                self.isAlive = False
                # print("리세 성공 "*5)
                self.log_main(self.InstanceName, "리세 성공 "*5)
                self.log("리세 성공 "*5)

                self.parent.InstanceComboBox.setEnabled(True)
                self.parent.InstanceRefreshButton.setEnabled(True)
                break

            if isSuccessed == "4080_에러_코드":
                self.Error_4080Function()
                time.sleep(20)
            
            # print("-"*50)
            self.log_main(self.InstanceName, "-"*50)
            self.log("-"*50)
            
        # print("리세 종료")
        self.log_main(self.InstanceName, "리세 종료")
        self.log("리세 종료")
        self.isStopped = True

    def terminate(self):
        self.isAlive = False
        while self.isStopped == False:
            pass
        try:
            os.makedirs("./Saved_Data")
        except:
            pass
        try:
            path = "./Saved_Data/"+str(self.parent.InstancePort)+".uma"
            with open(file=path, mode='wb') as file:
                pickle.dump(self.resetCount, file) # -- pickle --
                pickle.dump(self.is시작하기, file) # -- pickle --
                pickle.dump(self.isPAUSED, file) # -- pickle --
                pickle.dump(self.is선물_이동, file) # -- pickle --
                pickle.dump(self.is뽑기_이동, file) # -- pickle --
                pickle.dump(self.is뽑기_결과, file) # -- pickle --
                pickle.dump(self.is쥬얼부족, file) # -- pickle --
                pickle.dump(self.is연동하기, file) # -- pickle --
                pickle.dump(self.is초기화하기, file) # -- pickle --
                
                # 서포트 카드 총 갯수
                pickle.dump(self.Supporter_cards_total, file) # -- pickle --
        except:
            path = "./Saved_Data/"+str(self.parent.InstancePort)+".uma"
            # print(path+"를 저장하는데 실패했습니다. (동시작업 가능성)")
            self.log(path+"를 저장하는데 실패했습니다. (동시작업 가능성)")

        self.parent.InstanceComboBox.setEnabled(True)
        self.parent.InstanceRefreshButton.setEnabled(True)
        
        self.parent.startButton.setEnabled(True)
        self.parent.stopButton.setEnabled(False)
        self.parent.resetButton.setEnabled(True)
        self.parent.isDoneTutorialCheckBox.setEnabled(True)
        
    def main(self):
        hwndMain = WindowsAPIInput.GetHwnd(self.InstanceName) # hwnd ID 찾기
        WindowsAPIInput.SetWindowSize(hwndMain, 574, 994)
        self.device = adbInput.AdbConnect(self.InstancePort)
        
        # 불러오기
        try:
            path = "./Saved_Data/"+str(self.parent.InstancePort)+".uma"
            with open(file=path,  mode='rb') as file:
                self.resetCount = pickle.load(file) # -- pickle --
                self.is시작하기 = pickle.load(file) # -- pickle --
                self.isPAUSED = pickle.load(file) # -- pickle --
                self.is선물_이동 = pickle.load(file) # -- pickle --
                self.is뽑기_이동 = pickle.load(file) # -- pickle --
                self.is뽑기_결과 = pickle.load(file) # -- pickle --
                self.is쥬얼부족 = pickle.load(file) # -- pickle --
                self.is연동하기 = pickle.load(file) # -- pickle --
                self.is초기화하기 = pickle.load(file) # -- pickle --
                
                # 서포트 카드 총 갯수
                self.Supporter_cards_total = pickle.load(file) # -- pickle --
                for key, value in self.Supporter_cards_total.items():
                    self.log(key + ": " + str(value))
                self.log("기존 데이터를 불러옵니다.")
        except:
            self.is시작하기 = False # -- pickle --
            self.isPAUSED = False # -- pickle --
            self.is선물_이동 = True # -- pickle --
            self.is뽑기_이동 = True # -- pickle --
            self.is뽑기_결과 = True # -- pickle --
            self.is쥬얼부족 = False # -- pickle --
            self.is연동하기 = False # -- pickle --
            self.is초기화하기 = False # -- pickle --
            
            # 서포트 카드 총 갯수
            path = './Supporter_cards'
            self.Supporter_cards_total = dict() # -- pickle --
            for a in glob.glob(os.path.join(path, '*')):
                key = a.replace('.', '/').replace('\\', '/')
                key = key.split('/')
                self.Supporter_cards_total[key[-2]] = 0


        updateTime = time.time() # 타임 아웃 터치

        while self.isAlive:
            # 잠수 클릭 20초 터치락 해제
            if self.parent.isDoneTutorialCheckBox.isChecked() and time.time() >= updateTime + 20:
                # print("20초 정지 터치락 해제!!! "*3)
                self.log("20초 정지 터치락 해제!!! "*3)
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=(0,0,0,0))
                time.sleep(2)
            
            # 잠수 클릭 40초 이상 앱정지
            if self.parent.isDoneTutorialCheckBox.isChecked() and time.time() >= updateTime + 40:
                # print("40초 정지 앱 강제종료!!! "*3)
                self.log("40초 정지 앱 강제종료!!! "*3)
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                time.sleep(2)
                
            time.sleep(self.sleepTime)
            
            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break

            
            img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
            
            
            if self.is초기화하기 == False:
                count = 0
                count, position = ImageSearch(img, SKIP, confidence=0.85)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("SKIP " + str(count) + "개")
                    self.log("SKIP " + str(count) + "개")
                    # print(position)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우마무스메_실행, confidence=0.99, grayscale=False)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0])
                    # print("우마무스메_실행 " + str(count) + "개")
                    self.log("우마무스메_실행 " + str(count) + "개")
                    # print(position)
                    time.sleep(2)
                
                if self.is시작하기 == False:
                    count = 0
                    count, position = ImageSearch(img, 게스트_로그인, 232, 926, 77, 14, confidence=0.7)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("게스트_로그인 " + str(count) + "개")
                        self.log("게스트_로그인 " + str(count) + "개")
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = 0
                    count, position = ImageSearch(img, 게스트로_로그인_하시겠습니까, 162, 534, 218, 17, confidence = 0.9)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX = 120, offsetY = 117, deltaX=5, deltaY=5)
                        # print("게스트로_로그인_하시겠습니까 " + str(count) + "개")
                        self.log("게스트로_로그인_하시겠습니까 " + str(count) + "개")
                        # print(position)
                        time.sleep(2)
                        img = screenshotToOpenCVImg(hwndMain)
                    
                    count = 0
                    count, position = ImageSearch(img, 전체_동의, 23, 117, 22, 22, confidence=0.95, grayscale=False)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX = 0, offsetY = 0, deltaX=5, deltaY=5)
                        # print("전체_동의 " + str(count) + "개")
                        self.log("전체_동의 " + str(count) + "개")
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 시작하기, 237, 396, 67, 23, grayscale=False)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("시작하기 " + str(count) + "개")
                        self.log("시작하기 " + str(count) + "개")
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                count = 0
                count, position = ImageSearch(img, TAP_TO_START, 150, 860, 241, 34, confidence=0.7)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    self.is시작하기 = True
                    # print("TAP_TO_START " + str(count) + "개")
                    self.log("TAP_TO_START " + str(count) + "개")
                    # print(position)
                    time.sleep(2)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 계정_연동_설정_요청, 176, 327, 186, 29)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX = -121, offsetY = 316, deltaX=5, deltaY=5)
                    # print("계정_연동_설정_요청 " + str(count) + "개")
                    self.log("계정_연동_설정_요청 " + str(count) + "개")
                    # print(position)
                    time.sleep(2) # 빨리 터치하면 튜토리얼 하기 부분에서도 같은 부분 클릭해버림
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 튜토리얼을_스킵하시겠습니까)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=120, offsetY=140, deltaX=5, deltaY=5)
                    # print("튜토리얼을_스킵하시겠습니까 " + str(count) + "개")
                    self.log("튜토리얼을_스킵하시겠습니까 " + str(count) + "개")
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 게임_데이터_다운로드, 170, 329, 200, 27)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX = 132, offsetY = 316, deltaX=5, deltaY=5)
                    # print("게임_데이터_다운로드 " + str(count) + "개")
                    self.log("게임_데이터_다운로드 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 트레이너_정보를_입력해주세요)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=61, deltaX=5)
                    time.sleep(0.5)
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=555, deltaX=5)
                    # print("트레이너_정보를_입력해주세요 " + str(count) + "개")
                    self.log("트레이너_정보를_입력해주세요 " + str(count) + "개")
                    time.sleep(0.2)
                    # print(position)
                    for _ in range(10):
                        WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                    time.sleep(0.2)
                    WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "UmaPyoi")
                    time.sleep(0.5)
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 등록한다, 206, 620, 106, 52)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("등록한다 " + str(count) + "개")
                    self.log("등록한다 " + str(count) + "개")
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, 이_내용으로_등록합니다_등록하시겠습니까, 72, 569, 333, 49)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=136, offsetY=54, deltaX=5, deltaY=5)
                    # print("이_내용으로_등록합니다_등록하시겠습니까 " + str(count) + "개")
                    self.log("이_내용으로_등록합니다_등록하시겠습니까 " + str(count) + "개")
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                if self.isAlive == False: # 중간에 멈춰야 할 경우
                    break
                    
                # 튜토리얼 진행, 귀찮아서 튜토리얼 멈추면 알아서 하셈
                count = 0
                count, position = ImageSearch(img, 출전)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("출전 " + str(count) + "개")
                    self.log("출전 " + str(count) + "개")
                    self.parent.isDoneTutorialCheckBox.setChecked(False)
                    print(position)
                    time.sleep(1)
                    continue
                
            if self.parent.isDoneTutorialCheckBox.isChecked() == False:
                updateTime = time.time()
                
                if self.isPAUSED == False:
                    count = 0
                    count, position = ImageSearch(img, 울려라_팡파레)
                    if count:
                        ConvertedPosition = []
                        ConvertedPosition.append(position[0][0] / 1.750503018108652) # 1740 / 994 가로화면 가로배율
                        ConvertedPosition.append(position[0][1] / 1.750503018108652)
                        ConvertedPosition.append(position[0][2] / 1.729965156794425) # 993 / 574 가로화면 세로배율
                        ConvertedPosition.append(position[0][3] / 1.729965156794425)
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
                        print("울려라_팡파레 " + str(count) + "개")
                        self.log("울려라_팡파레 " + str(count) + "개")
                        print(position)
                        self.isPAUSED = True
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 닿아라_골까지)
                    if count:
                        ConvertedPosition = []
                        ConvertedPosition.append(position[0][0] / 1.750503018108652)
                        ConvertedPosition.append(position[0][1] / 1.750503018108652)
                        ConvertedPosition.append(position[0][2] / 1.729965156794425)
                        ConvertedPosition.append(position[0][3] / 1.729965156794425)
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
                        print("닿아라_골까지 " + str(count) + "개")
                        self.log("닿아라_골까지 " + str(count) + "개")
                        print(position)
                        self.isPAUSED = True
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 라이브_메뉴)
                if count:
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
                    print("라이브_메뉴 " + str(count) + "개")
                    self.log("라이브_메뉴 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 라이브_스킵)
                if count:
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=ConvertedPosition, deltaX=5, deltaY=5)
                    print("라이브_스킵 " + str(count) + "개")
                    self.log("라이브_스킵 " + str(count) + "개")
                    print(position)
                    self.isPAUSED = False
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 타즈나_씨와_레이스를_관전한, 124, 808, 268, 52)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("타즈나_씨와_레이스를_관전한 " + str(count) + "개")
                    self.log("타즈나_씨와_레이스를_관전한 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 일본_우마무스메_트레이닝_센터_학원, 78, 844, 345, 53)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("일본_우마무스메_트레이닝_센터_학원 " + str(count) + "개")
                    self.log("일본_우마무스메_트레이닝_센터_학원 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 레이스의_세계를_꿈꾸는_아이들이, 73, 810, 369, 70)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("레이스의_세계를_꿈꾸는_아이들이 " + str(count) + "개")
                    self.log("레이스의_세계를_꿈꾸는_아이들이 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 환영, 180, 811, 156, 68)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("환영 " + str(count) + "개")
                    self.log("환영 " + str(count) + "개")
                    print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 느낌표물음표, 35, 449, 52, 54)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("느낌표물음표 " + str(count) + "개")
                    self.log("느낌표물음표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 아키카와_이사장님, 181, 811, 181, 49)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("아키카와_이사장님 " + str(count) + "개")
                    self.log("아키카와_이사장님 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 장래_유망한_트레이너의_등장에, 145, 808, 284, 50)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("장래_유망한_트레이너의_등장에 " + str(count) + "개")
                    self.log("장래_유망한_트레이너의_등장에 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 나는_이_학원의_이사장, 98, 821, 209, 49)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("나는_이_학원의_이사장 " + str(count) + "개")
                    self.log("나는_이_학원의_이사장 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 자네에_대해_가르쳐_주게나, 155, 833, 250, 48)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("자네에_대해_가르쳐_주게나 " + str(count) + "개")
                    self.log("자네에_대해_가르쳐_주게나 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                # 트레이너 정보 입력 -----------
                # 위에 빼둠
                # -----------------------------
            
                count = 0
                count, position = ImageSearch(img, 자네는_트레센_학원의_일원일세, 150, 833, 282, 49)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("자네는_트레센_학원의_일원일세 " + str(count) + "개")
                    self.log("자네는_트레센_학원의_일원일세 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 담당_우마무스메와_함께, 172, 798, 224, 49)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("담당_우마무스메와_함께 " + str(count) + "개")
                    self.log("담당_우마무스메와_함께 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 학원에_다니는_우마무스메의, 86, 798, 259, 50)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("학원에_다니는_우마무스메의 " + str(count) + "개")
                    self.log("학원에_다니는_우마무스메의 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 자네는_트레이너로서_담당_우마무스메를, 79, 810, 358, 51)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("자네는_트레이너로서_담당_우마무스메를 " + str(count) + "개")
                    self.log("자네는_트레이너로서_담당_우마무스메를 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 가슴에_단_트레이너_배지에, 159, 811, 248, 48)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("가슴에_단_트레이너_배지에 " + str(count) + "개")
                    self.log("가슴에_단_트레이너_배지에 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 실전_연수를_하러_가시죠, 207, 813, 224, 46)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("실전_연수를_하러_가시죠 " + str(count) + "개")
                    self.log("실전_연수를_하러_가시죠 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 프리티_더비_뽑기_5번_뽑기_무료, 191, 710, 135, 125)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("프리티_더비_뽑기_5번_뽑기_무료 " + str(count) + "개")
                    self.log("프리티_더비_뽑기_5번_뽑기_무료 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 튜토리얼_용_프리티_더비_뽑기, 130, 432, 258, 69)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=180, deltaX=5, deltaY=5)
                    print("튜토리얼_용_프리티_더비_뽑기 " + str(count) + "개")
                    self.log("튜토리얼_용_프리티_더비_뽑기 " + str(count) + "개")
                    print(position)
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드_화살표, 410, 508, 124, 135)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("서포트_카드_화살표 " + str(count) + "개") # 느림
                    self.log("서포트_카드_화살표 " + str(count) + "개") # 느림
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드_화살표2, 410, 508, 124, 135)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("서포트_카드_화살표2 " + str(count) + "개") # 느림
                    self.log("서포트_카드_화살표2 " + str(count) + "개") # 느림
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드_뽑기_10번_뽑기_무료)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("서포트_카드_뽑기_10번_뽑기_무료 " + str(count) + "개")
                    self.log("서포트_카드_뽑기_10번_뽑기_무료 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 튜토리얼_용_서포트_카드_뽑기, 124, 431, 266, 71)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=180, deltaX=5, deltaY=5)
                    print("튜토리얼_용_서포트_카드_뽑기 " + str(count) + "개")
                    self.log("튜토리얼_용_서포트_카드_뽑기 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 육성_화살표, 350, 712, 117, 172)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                    print("육성_화살표 " + str(count) + "개")
                    self.log("육성_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                
                # 이미지 바꿀 예정
                count = 0
                count, position = ImageSearch(img, 육성_시나리오를_공략하자, 59, 664, 399, 77)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=223, deltaX=5, deltaY=5)
                    print("육성_시나리오를_공략하자 " + str(count) + "개")
                    self.log("육성_시나리오를_공략하자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 다음_화살표, 195, 742, 120, 117)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("다음_화살표 " + str(count) + "개")
                    self.log("다음_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자, 53, 614, 414, 125)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=248, deltaX=5, deltaY=5)
                    print("트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 " + str(count) + "개")
                    self.log("트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 마음에_드는_우마무스메를_육성하자, 21, 670, 473, 71)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=217, deltaX=5, deltaY=5)
                    print("마음에_드는_우마무스메를_육성하자 " + str(count) + "개")
                    self.log("마음에_드는_우마무스메를_육성하자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 다이와_스칼렛_클릭, 0, 496, 138, 138)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("다이와_스칼렛_클릭 " + str(count) + "개")
                    self.log("다이와_스칼렛_클릭 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 다음_화살표_육성_우마무스메_선택, 212, 747, 91, 116)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("다음_화살표_육성_우마무스메_선택 " + str(count) + "개")
                    self.log("다음_화살표_육성_우마무스메_선택 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 플러스_계승_우마무스메_선택_화살표, 19, 520, 103, 152)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("플러스_계승_우마무스메_선택_화살표 " + str(count) + "개")
                    self.log("플러스_계승_우마무스메_선택_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 계승_보드카_선택_화살표, 209, 496, 93, 161)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("계승_보드카_선택_화살표 " + str(count) + "개")
                    self.log("계승_보드카_선택_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 보드카_결정_화살표, 213, 740, 90, 120)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("보드카_결정_화살표 " + str(count) + "개")
                    self.log("보드카_결정_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 자동_선택_화살표, 329, 668, 105, 105)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("자동_선택_화살표 " + str(count) + "개")
                    self.log("자동_선택_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 자동_선택_확인_OK_화살표, 334, 559, 84, 117) # 느림
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("자동_선택_확인_OK_화살표 " + str(count) + "개")
                    self.log("자동_선택_확인_OK_화살표 " + str(count) + "개")
                    print(position)
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 마음을_이어서_꿈을_이루자, 73, 661, 371, 79)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=218, deltaX=5, deltaY=5)
                    print("마음을_이어서_꿈을_이루자 " + str(count) + "개")
                    self.log("마음을_이어서_꿈을_이루자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 계승_최종_다음_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=35, deltaX=5, deltaY=5)
                    print("계승_최종_다음_화살표 " + str(count) + "개")
                    self.log("계승_최종_다음_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 서포트_카드를_편성해서_육성_효율_UP, 67, 615, 383, 120)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=247, deltaX=5, deltaY=5)
                    print("서포트_카드를_편성해서_육성_효율_UP " + str(count) + "개")
                    self.log("서포트_카드를_편성해서_육성_효율_UP " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 서포트_카드의_타입에_주목, 38, 662, 439, 69)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=225, deltaX=5, deltaY=5)
                    print("서포트_카드의_타입에_주목 " + str(count) + "개")
                    self.log("서포트_카드의_타입에_주목 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 우정_트레이닝이_육성의_열쇠를_쥐고_있다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=212, deltaX=5, deltaY=5)
                    print("우정_트레이닝이_육성의_열쇠를_쥐고_있다 " + str(count) + "개")
                    self.log("우정_트레이닝이_육성의_열쇠를_쥐고_있다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 서포트_자동_편성_화살표, 324, 629, 107, 102)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("서포트_자동_편성_화살표 " + str(count) + "개")
                    self.log("서포트_자동_편성_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성_시작_화살표, 184, 732, 160, 129)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("육성_시작_화살표 " + str(count) + "개")
                    self.log("육성_시작_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, TP를_소비해_육성_시작_화살표, 305, 816, 142, 119)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("TP를_소비해_육성_시작_화살표 " + str(count) + "개")
                    self.log("TP를_소비해_육성_시작_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 초록색_역삼각형, 440, 850, -1, -1, confidence=0.8) # 역 삼각형
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("초록색_역삼각형 " + str(count) + "개")
                    self.log("초록색_역삼각형 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                
                count = 0
                count, position = ImageSearch(img, TAP)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("TAP " + str(count) + "개")
                    self.log("TAP " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, TAP)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("TAP " + str(count) + "개")
                    self.log("TAP " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 우마무스메에겐_저마다_다른_목표가_있습니다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("우마무스메에겐_저마다_다른_목표가_있습니다 " + str(count) + "개")
                    self.log("우마무스메에겐_저마다_다른_목표가_있습니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 이쪽은_육성을_진행할_때_필요한_커맨드입니다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("이쪽은_육성을_진행할_때_필요한_커맨드입니다 " + str(count) + "개")
                    self.log("이쪽은_육성을_진행할_때_필요한_커맨드입니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 커맨드를_하나_실행하면_턴을_소비합니다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("커맨드를_하나_실행하면_턴을_소비합니다 " + str(count) + "개")
                    self.log("커맨드를_하나_실행하면_턴을_소비합니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 우선_트레이닝을_선택해_보세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=60, offsetY=178, deltaX=5, deltaY=5)
                    print("우선_트레이닝을_선택해_보세요 " + str(count) + "개")
                    self.log("우선_트레이닝을_선택해_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 이게_실행할_수_있는_트레이닝들입니다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("이게_실행할_수_있는_트레이닝들입니다 " + str(count) + "개")
                    self.log("이게_실행할_수_있는_트레이닝들입니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 한_번_스피드를_골라_보세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=-143, offsetY=228, deltaX=5, deltaY=5)
                    print("한_번_스피드를_골라_보세요 " + str(count) + "개")
                    self.log("한_번_스피드를_골라_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 파란색_역삼각형, 440, 850, -1, -1, confidence=0.9) # 역 삼각형
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("파란색_역삼각형 " + str(count) + "개")
                    self.log("파란색_역삼각형 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                
                count = 0
                count, position = ImageSearch(img, 약속, 38, 614, 80, 57)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("약속 " + str(count) + "개")
                    self.log("약속 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 서둘러_가봐, 38, 617, 132, 53)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("서둘러_가봐 " + str(count) + "개")
                    self.log("서둘러_가봐 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 그때_번뜩였다, 22, 740, 289, 102)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("그때_번뜩였다 " + str(count) + "개")
                    self.log("그때_번뜩였다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 다이와_스칼렛의_성장으로_이어졌다, 23, 741, 328, 55)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("다이와_스칼렛의_성장으로_이어졌다 " + str(count) + "개")
                    self.log("다이와_스칼렛의_성장으로_이어졌다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 다음으로_육성_우마무스메의_체력에_관해_설명할게요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("다음으로_육성_우마무스메의_체력에_관해_설명할게요 " + str(count) + "개")
                    self.log("다음으로_육성_우마무스메의_체력에_관해_설명할게요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 우선_아까처럼_트레이닝을_선택해_보세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=90, offsetY=173, deltaX=5, deltaY=5)
                    print("우선_아까처럼_트레이닝을_선택해_보세요 " + str(count) + "개")
                    self.log("우선_아까처럼_트레이닝을_선택해_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 여기_실패율에_주목해_주세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("여기_실패율에_주목해_주세요 " + str(count) + "개")
                    self.log("여기_실패율에_주목해_주세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 남은_체력이_적을수록_실패율이_높아지게_돼요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("남은_체력이_적을수록_실패율이_높아지게_돼요 " + str(count) + "개")
                    self.log("남은_체력이_적을수록_실패율이_높아지게_돼요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 트레이닝에_실패하면_능력과_컨디션이)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("트레이닝에_실패하면_능력과_컨디션이 " + str(count) + "개")
                    self.log("트레이닝에_실패하면_능력과_컨디션이 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 돌아간다_화살표, grayscale=False)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("돌아간다_화살표 " + str(count) + "개")
                    self.log("돌아간다_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 체력이_적을_때는_우마무스메를)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=-125, offsetY=180, deltaX=5, deltaY=5)
                    print("체력이_적을_때는_우마무스메를 " + str(count) + "개")
                    self.log("체력이_적을_때는_우마무스메를 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 먼저_여기_스킬을_선택해보세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=-70, offsetY=170, deltaX=5, deltaY=5)
                    print("먼저_여기_스킬을_선택해보세요 " + str(count) + "개")
                    self.log("먼저_여기_스킬을_선택해보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 다음으로_배울_스킬을_선택하세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("다음으로_배울_스킬을_선택하세요 " + str(count) + "개")
                    self.log("다음으로_배울_스킬을_선택하세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 이번에는_이_스킬을_습득해_보세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=273, offsetY=183, deltaX=5, deltaY=5)
                    print("이번에는_이_스킬을_습득해_보세요 " + str(count) + "개")
                    self.log("이번에는_이_스킬을_습득해_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 스킬_결정_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("스킬_결정_화살표 " + str(count) + "개")
                    self.log("스킬_결정_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 스킬_획득_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("스킬_획득_화살표 " + str(count) + "개")
                    self.log("스킬_획득_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 스킬_획득_돌아간다_화살표, 1, 857, 100, 115)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("스킬_획득_돌아간다_화살표 " + str(count) + "개")
                    self.log("스킬_획득_돌아간다_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 이졔_준비가_다_끝났어요_레이스에_출전해_봐요, 85, 621, 191, 69)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=207, offsetY=168, deltaX=5, deltaY=5)
                    print("이졔_준비가_다_끝났어요_레이스에_출전해_봐요 " + str(count) + "개")
                    self.log("이졔_준비가_다_끝났어요_레이스에_출전해_봐요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 출전_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("출전_화살표 " + str(count) + "개")
                    self.log("출전_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 숫자1등이_되기_위해서도_말야, 37, 615, 252, 58)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("1등이_되기_위해서도_말야 " + str(count) + "개")
                    self.log("1등이_되기_위해서도_말야 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 패덕에서는_레이스에_출전하는_우마무스메의)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("패덕에서는_레이스에_출전하는_우마무스메의 " + str(count) + "개")
                    self.log("패덕에서는_레이스에_출전하는_우마무스메의 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 우선_예상_표시에_관해서_설명할게요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("우선_예상_표시에_관해서_설명할게요 " + str(count) + "개")
                    self.log("우선_예상_표시에_관해서_설명할게요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 숫자3개의_표시는_전문가들의_예상을_나타내며)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("3개의_표시는_전문가들의_예상을_나타내며 " + str(count) + "개")
                    self.log("3개의_표시는_전문가들의_예상을_나타내며 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 능력과_컨디션이_좋을수록_많은_기대를_받게_돼서)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 " + str(count) + "개")
                    self.log("능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 물론_반드시_우승하게_되는_건_아니지만)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("물론_반드시_우승하게_되는_건_아니지만 " + str(count) + "개")
                    self.log("물론_반드시_우승하게_되는_건_아니지만 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 또_패덕에서는_우마무스메의_작전을)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=210, offsetY=157, deltaX=5, deltaY=5)
                    print("또_패덕에서는_우마무스메의_작전을 " + str(count) + "개")
                    self.log("또_패덕에서는_우마무스메의_작전을 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 선행A_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("선행A_화살표 " + str(count) + "개")
                    self.log("선행A_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 작전_결정)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("작전_결정 " + str(count) + "개")
                    self.log("작전_결정 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 이것으로_준비는_다_됐어요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=145, offsetY=161, deltaX=5, deltaY=5)
                    print("이것으로_준비는_다_됐어요 " + str(count) + "개")
                    self.log("이것으로_준비는_다_됐어요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 첫_우승_축하_드려요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=847, deltaX=5, deltaY=5)
                    print("첫_우승_축하_드려요 " + str(count) + "개")
                    self.log("첫_우승_축하_드려요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 좋아, 37, 613, 80, 59)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("좋아 " + str(count) + "개")
                    self.log("좋아 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 목표_달성, 114, 222, 293, 100)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=578, deltaX=5, deltaY=5)
                    print("목표_달성 " + str(count) + "개")
                    self.log("목표_달성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성_목표_달성, 31, 227, 469, 96)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=578, deltaX=5, deltaY=5)
                    print("육성_목표_달성 " + str(count) + "개")
                    self.log("육성_목표_달성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성_수고하셨습니다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("육성_수고하셨습니다 " + str(count) + "개")
                    self.log("육성_수고하셨습니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 스킬_포인트가_남았다면)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("스킬_포인트가_남았다면 " + str(count) + "개")
                    self.log("스킬_포인트가_남았다면 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성은_이것으로_종료입니다)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("육성은_이것으로_종료입니다 " + str(count) + "개")
                    self.log("육성은_이것으로_종료입니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 또_연수_기간은_짧았지만)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("또_연수_기간은_짧았지만 " + str(count) + "개")
                    self.log("또_연수_기간은_짧았지만 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성_완료_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=40, deltaX=5, deltaY=5)
                    print("육성_완료_화살표 " + str(count) + "개")
                    self.log("육성_완료_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성_완료_확인_완료한다_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("육성_완료_확인_완료한다_화살표 " + str(count) + "개")
                    self.log("육성_완료_확인_완료한다_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 " + str(count) + "개")
                    self.log("육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 최고_랭크를_목표로_힘내세요)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("최고_랭크를_목표로_힘내세요 " + str(count) + "개")
                    self.log("최고_랭크를_목표로_힘내세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 랭크_육성)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=837, deltaX=5, deltaY=5)
                    print("랭크_육성 " + str(count) + "개")
                    self.log("랭크_육성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 육성을_끝낸_우마무스메는_인자를)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("육성을_끝낸_우마무스메는_인자를 " + str(count) + "개")
                    self.log("육성을_끝낸_우마무스메는_인자를 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 계승_우마무스메로_선택하면_새로운_우마무스메에게)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("계승_우마무스메로_선택하면_새로운_우마무스메에게 " + str(count) + "개")
                    self.log("계승_우마무스메로_선택하면_새로운_우마무스메에게 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 인자획득)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=829, deltaX=5, deltaY=5)
                    print("인자획득 " + str(count) + "개")
                    self.log("인자획득 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 우마무스메_상세_닫기_화살표)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("우마무스메_상세_닫기_화살표 " + str(count) + "개")
                    self.log("우마무스메_상세_닫기_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 평가점, 293, 327, 75, 50)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=-75, offsetY=552, deltaX=5, deltaY=5)
                    print("평가점 " + str(count) + "개")
                    self.log("평가점 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 보상획득, 113, 21, 287, 103)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=834, deltaX=5, deltaY=5)
                    print("보상획득 " + str(count) + "개")
                    self.log("보상획득 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                count = 0
                count, position = ImageSearch(img, 강화_편성_화살표, 0, 910, 97, -1, grayscale=False) # -5, 910, 97, 67
                if count:
                    print(position[0])
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("강화_편성_화살표 " + str(count) + "개")
                    self.log("강화_편성_화살표 " + str(count) + "개")
                    print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 레이스_화살표, 329, 908, 103, -1, grayscale=False) # 329, 908, 103, 71
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("레이스_화살표 " + str(count) + "개")
                    self.log("레이스_화살표 " + str(count) + "개")
                    print(position)
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_경기장_화살표, 82, 542, 130, 83)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                    print("팀_경기장_화살표 " + str(count) + "개")
                    self.log("팀_경기장_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 오리지널_팀을_결성_상위_CLASS를_노려라, 81, 622, 358, 118)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=244, deltaX=5, deltaY=5)
                    print("오리지널_팀을_결성_상위_CLASS를_노려라 " + str(count) + "개")
                    self.log("오리지널_팀을_결성_상위_CLASS를_노려라 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 하이스코어를_기록해서_CLASS_승급을_노리자, 78, 614, 362, 125)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=250, deltaX=5, deltaY=5)
                    print("하이스코어를_기록해서_CLASS_승급을_노리자 " + str(count) + "개")
                    self.log("하이스코어를_기록해서_CLASS_승급을_노리자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 기간_중에_개최되는_5개의_레이스에, 8, 617, 504, 121)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=236, deltaX=5, deltaY=5)
                    print("기간_중에_개최되는_5개의_레이스에 " + str(count) + "개")
                    self.log("기간_중에_개최되는_5개의_레이스에 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드의_Lv을_UP해서, 61, 630, 396, 111)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=244, deltaX=5, deltaY=5)
                    print("서포트_카드의_Lv을_UP해서 " + str(count) + "개")
                    self.log("서포트_카드의_Lv을_UP해서 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_편성, 264, 699, 126, 72)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    print("팀_편성 " + str(count) + "개")
                    self.log("팀_편성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 전당_입성_우마무스메로_자신만의_팀을_결성, 59, 616, 395, 122)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=247, deltaX=5, deltaY=5)
                    print("전당_입성_우마무스메로_자신만의_팀을_결성 " + str(count) + "개")
                    self.log("전당_입성_우마무스메로_자신만의_팀을_결성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_랭크를_올려서_최강의_팀이_되자, 128, 616, 262, 122)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=238, deltaX=5, deltaY=5)
                    print("팀_랭크를_올려서_최강의_팀이_되자 " + str(count) + "개")
                    self.log("팀_랭크를_올려서_최강의_팀이_되자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠, 84, 619, 352, 123)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=246, deltaX=5, deltaY=5)
                    print("팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠 " + str(count) + "개")
                    self.log("팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_편성_다이와_스칼렛_화살표_클릭, 200, 341, 116, 160)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("팀_편성_다이와_스칼렛_화살표_클릭 " + str(count) + "개")
                    self.log("팀_편성_다이와_스칼렛_화살표_클릭 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 출전_우마무스메_선택_다이와_스칼렛_화살표, 0, 591, 121, 138)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("출전_우마무스메_선택_다이와_스칼렛_화살표 " + str(count) + "개")
                    self.log("출전_우마무스메_선택_다이와_스칼렛_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_편성_확정_화살표, 190, 736, 136, 124)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("팀_편성_확정_화살표 " + str(count) + "개")
                    self.log("팀_편성_확정_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 편성을_확정합니다_진행하시겠습니까, 177, 524, 165, 75)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=121, offsetY=77, deltaX=5, deltaY=5)
                    print("편성을_확정합니다_진행하시겠습니까 " + str(count) + "개")
                    self.log("편성을_확정합니다_진행하시겠습니까 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 팀_최고_평가점_갱신_닫기, 223, 840, 98, 95)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("팀_최고_평가점_갱신_닫기 " + str(count) + "개")
                    self.log("팀_최고_평가점_갱신_닫기 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 홈_화살표, 188, 845, 144, 134)
                if count:
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("홈_화살표 " + str(count) + "개")
                    self.log("홈_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
                
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            # ------------------------------ 리세 -----------------------------
            if self.is초기화하기 == False:
                count = 0
                count, position = ImageSearch(img, 공지사항_X, 495, 52, 23, 22)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("공지사항_X " + str(count) + "개")
                    self.log("공지사항_X " + str(count) + "개")
                    self.parent.isDoneTutorialCheckBox.setChecked(True)
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)
                
                    
                count = 0
                count, position = ImageSearch(img, 메인_스토리가_해방되었습니다)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=90, deltaX=5, deltaY=5)
                    # print("메인_스토리가_해방되었습니다 " + str(count) + "개")
                    self.log("메인_스토리가_해방되었습니다 " + str(count) + "개")
                    self.parent.isDoneTutorialCheckBox.setChecked(True)
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 여러_스토리를_해방할_수_있게_되었습니다)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                    # print("여러_스토리를_해방할_수_있게_되었습니다 " + str(count) + "개")
                    self.log("여러_스토리를_해방할_수_있게_되었습니다 " + str(count) + "개")
                    self.parent.isDoneTutorialCheckBox.setChecked(True)
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)
            
            
            # 가챠
            if self.parent.isDoneTutorialCheckBox.isChecked() and self.is선물_이동 == True:
                count = 0
                count, position = ImageSearch(img, 선물_이동, 456, 672, 47, 53)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("선물_이동 " + str(count) + "개")
                    self.log("선물_이동 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, 선물_일괄_수령, 319, 879, 115, 54, confidence=0.99, grayscale=False)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("선물_일괄_수령 " + str(count) + "개")
                    self.log("선물_일괄_수령 " + str(count) + "개")
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, 상기의_선물을_수령했습니다)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                    # print("상기의_선물을_수령했습니다 " + str(count) + "개")
                    self.log("상기의_선물을_수령했습니다 " + str(count) + "개")
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, 받을_수_있는_선물이_없습니다, 143, 460, 231, 51)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=-125, offsetY=420, deltaX=5, deltaY=5)
                    # print("받을_수_있는_선물이_없습니다 " + str(count) + "개")
                    self.log("받을_수_있는_선물이_없습니다 " + str(count) + "개")
                    # print(position)
                    self.is선물_이동 = False
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break

            if self.parent.isDoneTutorialCheckBox.isChecked() and self.is뽑기_이동:
                count = 0
                count, position = ImageSearch(img, 뽑기_이동, 464, 666, 52, 62)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=245, deltaX=5, deltaY=5)
                    # print("뽑기_이동 " + str(count) + "개")
                    self.log("뽑기_이동 " + str(count) + "개")
                    # print(position)
                    time.sleep(2)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, 프리티_더비_뽑기, 154, 551, 175, 93, confidence=0.6)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=254, deltaX=5, deltaY=5)
                    # print("프리티_더비_뽑기 " + str(count) + "개")
                    self.log("프리티_더비_뽑기 " + str(count) + "개")
                    # print(position)
                    time.sleep(1)
                    img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 서포트_카드_뽑기, 160, 552, 154, 94, confidence=0.6) # 돌이 없는거 클릭 해봐야 암
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=196, offsetY=186, deltaX=5, deltaY=5)
                # print("서포트_카드_뽑기 " + str(count) + "개")
                self.log("서포트_카드_뽑기 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            if self.parent.isDoneTutorialCheckBox.isChecked() and self.is뽑기_이동:
                if self.isAlive == False: # 중간에 멈춰야 할 경우
                    break
                
                count = 0
                count, position = ImageSearch(img, 무료_쥬얼부터_먼저_사용됩니다)
                if count:
                    updateTime = time.time()
                    self.is뽑기_결과 = True
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=112, offsetY=55, deltaX=5, deltaY=5)
                    # print("무료_쥬얼부터_먼저_사용됩니다 " + str(count) + "개")
                    self.log("무료_쥬얼부터_먼저_사용됩니다 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(1.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 뽑기_결과, 208, 48, 97, 47)
                if count and self.is뽑기_결과:
                    updateTime = time.time()
                    self.is뽑기_결과 = False
                    # print("뽑기_결과 " + str(count) + "개")
                    self.log("뽑기_결과 " + str(count) + "개")
                    # print(position)
                    
                    # 서포터 카드 지금 갯수
                    path = './Supporter_cards'
                    Supporter_cards_now = dict()
                    for a in glob.glob(os.path.join(path, '*')):
                        key = a.replace('.', '/').replace('\\', '/')
                        key = key.split('/')
                        Supporter_cards_now[key[-2]] = 0
                        
                    for i in range(2):
                        updateTime = time.time()
                        time.sleep(0.25)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                        for key, value in Supporter_cards.items():
                            count = 0
                            count, position = ImageSearch(img, value, grayscale=False)
                            if count:
                                if Supporter_cards_now[key] < count:
                                    Supporter_cards_now[key] = count
                                # print(key + " " + str(Supporter_cards_now[key]) + "개")
                                self.log(key + " " + str(Supporter_cards_now[key]) + "개")
                                # print(position)
                                
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

                count = 0
                count, position = ImageSearch(img, 한_번_더_뽑기)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("한_번_더_뽑기 " + str(count) + "개")
                    self.log("한_번_더_뽑기 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                
            
            if self.parent.isDoneTutorialCheckBox.isChecked() and self.is초기화하기 == False:
                count = 0
                count, position = ImageSearch(img, 쥬얼이_부족합니다)
                if count:
                    updateTime = time.time()
                    # 이륙 조건식 -----------------------------------------------
                    # 이륙 조건식 -----------------------------------------------
                    # 이륙 조건식 -----------------------------------------------
                    SCT = self.Supporter_cards_total
                                
                    if SCT["SSR_파인_모션"] and SCT["SSR_슈퍼_크릭"] and SCT["SSR_하야카와_타즈나"]:
                        return True
                    
                    if SCT["SSR_파인_모션"] and SCT["SSR_비코_페가수스"] and SCT["SSR_하야카와_타즈나"]:
                        return True
                    
                    if SCT["SSR_파인_모션"] and SCT["SSR_사쿠라_바쿠신_오"] and SCT["SSR_하야카와_타즈나"]:
                        return True
                        
                    if SCT["SSR_파인_모션"] >= 2 and (SCT["SSR_슈퍼_크릭"] or SCT["SSR_하야카와_타즈나"]):
                        return True
                        
                    if SCT["SSR_슈퍼_크릭"] >= 2  and (SCT["SSR_파인_모션"] or SCT["SSR_하야카와_타즈나"]):
                        return True
                    
                    if SCT["SSR_비코_페가수스"] >= 2 and (SCT["SSR_슈퍼_크릭"] or SCT["SSR_하야카와_타즈나"]):
                        return True
                    
                    if SCT["SSR_사쿠라_바쿠신_오"] >= 2 and (SCT["SSR_파인_모션"] or SCT["SSR_슈퍼_크릭"] or SCT["SSR_하야카와_타즈나"]):
                        return True
                    
                    if SCT["SSR_파인_모션"] >= 3:
                        return True
                        
                    if SCT["SSR_슈퍼_크릭"] >= 3:
                        return True
                    
                    if SCT["SSR_비코_페가수스"] >= 3:
                        return True
                    
                    if SCT["SSR_사쿠라_바쿠신_오"] >= 3:
                        return True
                    
                    if SCT["SSR_하야카와_타즈나"] >= 3:
                        return True
                    
                    if SCT["SR_스윕_토쇼"] >= 5 and SCT["SSR_파인_모션"] and SCT["SSR_하야카와_타즈나"] and (SCT["SSR_슈퍼_크릭"] or SCT["SSR_비코_페가수스"] or SCT["SSR_사쿠라_바쿠신_오"]):
                        return True
                    
                    self.is쥬얼부족 = True
                    self.is뽑기_이동 = False
                    self.is연동하기 = True
                    adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4") # "KEYCODE_BACK" 
                    time.sleep(0.5)
                    adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4")
                    # print("쥬얼이_부족합니다 " + str(count) + "개")
                    self.log("쥬얼이_부족합니다 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 상점_화면을_표시할_수_없습니다)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=147, deltaX=5, deltaY=5)
                    # print("상점_화면을_표시할_수_없습니다 " + str(count) + "개")
                    self.log("상점_화면을_표시할_수_없습니다 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                if self.is연동하기:
                    count = 0
                    count, position = ImageSearch(img, 메뉴, 452, 48, 57, 48)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=5, offsetY=5)
                        # print("메뉴 " + str(count) + "개")
                        self.log("메뉴 " + str(count) + "개")
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 메뉴_단축, 511, 73, 19, 31, confidence=0.98, grayscale=False)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=4)
                        # print("메뉴_단축 " + str(count) + "개")
                        self.log("메뉴_단축 " + str(count) + "개")
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 계정_정보, 354, 635, 111, 51)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("계정_정보 " + str(count) + "개")
                        self.log("계정_정보 " + str(count) + "개")
                        # print(position)
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)

                    if self.isAlive == False: # 중간에 멈춰야 할 경우
                        break
                    
                    count = 0
                    count, position = ImageSearch(img, 카카오_로그인, 211, 446, 115, 50)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("카카오_로그인 " + str(count) + "개")
                        self.log("카카오_로그인 " + str(count) + "개")
                        # print(position)
                        time.sleep(2)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 확인하고_계속하기, 186, 623, 144, 53)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("확인하고_계속하기 " + str(count) + "개")
                        self.log("확인하고_계속하기 " + str(count) + "개")
                        # print(position)
                        time.sleep(2)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 확인하고_계속하기2, 186, 625, 143, 50)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("확인하고_계속하기2 " + str(count) + "개")
                        self.log("확인하고_계속하기2 " + str(count) + "개")
                        # print(position)
                        time.sleep(2)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 확인하고_계속하기3)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("확인하고_계속하기3 " + str(count) + "개")
                        self.log("확인하고_계속하기3 " + str(count) + "개")
                        # print(position)
                        # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                        time.sleep(2)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 계속하기, 214, 620, 85, 47)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                        # print("계속하기 " + str(count) + "개")
                        self.log("계속하기 " + str(count) + "개")
                        # print(position)
                        # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                        time.sleep(2)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 정보_확인_중, 105, 167, 188, 49)
                    if count:
                        updateTime = time.time()
                        adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4")
                        # print("정보_확인_중 " + str(count) + "개")
                        self.log("정보_확인_중 " + str(count) + "개")
                        # print(position)
                        # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, Google_계정으로_로그인)
                    if count:
                        updateTime = time.time()
                        adbInput.Key_event(self.device, self.InstancePort, key_code="keyevent 4")
                        # print("Google_계정으로_로그인 " + str(count) + "개")
                        self.log("Google_계정으로_로그인 " + str(count) + "개")
                        # print(position)
                        # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 인증되지_않는_로그인_방법_입니다)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=143, deltaX=5, deltaY=5)
                        # print("인증되지_않는_로그인_방법_입니다 " + str(count) + "개")
                        self.log("인증되지_않는_로그인_방법_입니다 " + str(count) + "개")
                        # print(position)
                        # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                        time.sleep(0.5)
                        img = screenshotToOpenCVImg(hwndMain)
                        
                    count = 0
                    count, position = ImageSearch(img, 카카오_로그인_연동에_실패하였습니다)
                    if count:
                        updateTime = time.time()
                        adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=150, deltaX=5, deltaY=5)
                        # print("카카오_로그인_연동에_실패하였습니다 " + str(count) + "개")
                        self.log("카카오_로그인_연동에_실패하였습니다 " + str(count) + "개")
                        # print(position)
                        time.sleep(5)
                
            count = 0
            count, position = ImageSearch(img, 카카오_로그인_연동에_성공하였습니다, 68, 469, 384, 65)
            if count:
                updateTime = time.time()
                self.is초기화하기 = True
                # adbInput.Key_event(device=device, key_code="keyevent 1") # KEYCODE_MENU
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                # print("카카오_로그인_연동에_성공하였습니다 " + str(count) + "개")
                self.log("카카오_로그인_연동에_성공하였습니다 " + str(count) + "개")
                self.parent.isDoneTutorialCheckBox.setChecked(True)
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 로그아웃)
            if count:
                updateTime = time.time()
                self.is초기화하기 = True
                # adbInput.Key_event(device=device, key_code="keyevent 1") # KEYCODE_MENU
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                # print("로그아웃 " + str(count) + "개")
                self.log("로그아웃 " + str(count) + "개")
                # print(position)
                # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 모두_지우기, 428, 40, 96, 48)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0])
                # print("모두_지우기 " + str(count) + "개")
                self.log("모두_지우기 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            # count = 0
            # count, position = ImageSearch(img, 크롬_실행)
            # if count and is초기화하기:
            #     updateTime = time.time()
            #     adbInput.BlueStacksClick(device=device, position=position[0])
            #     # print("크롬_실행 " + str(count) + "개")
            #     self.log("크롬_실행 " + str(count) + "개")
            #     print(position)
            #     time.sleep(0.5)
            #     img = screenshotToOpenCVImg(hwndMain)
                
            # count = 0
            # count, position = ImageSearch(img, 크롬_실행2)
            # if count and is초기화하기:
            #     updateTime = time.time()
            #     adbInput.BlueStacksClick(device=device, position=position[0])
            #     # print("크롬_실행 " + str(count) + "개")
            #     self.log("크롬_실행 " + str(count) + "개")
            #     print(position)
            #     time.sleep(0.5)
            #     img = screenshotToOpenCVImg(hwndMain)
            
            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break

            if self.parent.isDoneTutorialCheckBox.isChecked() and self.is초기화하기:
                count = 0
                count, position = ImageSearch(img, 파이어폭스_실행)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0])
                    # print("파이어폭스_실행 " + str(count) + "개")
                    self.log("파이어폭스_실행 " + str(count) + "개")
                    # print(position)
                    time.sleep(1.5)
                    img = screenshotToOpenCVImg(hwndMain)

                count = 0
                count, position = ImageSearch(img, 파이어폭스_연결된_서비스_관리)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # print("파이어폭스_실행 " + str(count) + "개")
                    self.log("파이어폭스_연결된_서비스_관리 " + str(count) + "개")
                    # print(position)
                    time.sleep(1.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 파이어폭스_문제_닫기, confidence=0.99)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0])
                    # print("파이어폭스_문제_닫기 " + str(count) + "개")
                    self.log("파이어폭스_문제_닫기 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                count = 0
                count, position = ImageSearch(img, 연결된_서비스_관리)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("연결된_서비스_관리 " + str(count) + "개")
                    self.log("연결된_서비스_관리 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 우마무스메_서비스)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("우마무스메_서비스 " + str(count) + "개")
                    self.log("우마무스메_서비스 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.2)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 모든_정보_삭제)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("모든_정보_삭제 " + str(count) + "개")
                    self.log("모든_정보_삭제 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.2)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 이_서비스의_모든_정보를_삭제하시겠습니까)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 205, 90)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], offsetX=205, offsetY=90, deltaX=5, deltaY=5)
                    time.sleep(0.5)
                    for _ in range(15):
                        WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                    time.sleep(0.2)
                    WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "우마무스메 프리티 더비")
                    # print("이_서비스의_모든_정보를_삭제하시겠습니까 " + str(count) + "개")
                    self.log("이_서비스의_모든_정보를_삭제하시겠습니까 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.2)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷

                count = 0
                count, position = ImageSearch(img, 이_서비스의_모든_정보를_삭제하시겠습니까2)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 100, 90)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], offsetX=205, offsetY=90, deltaX=5, deltaY=5)
                    time.sleep(0.5)
                    for _ in range(15):
                        WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                    time.sleep(0.2)
                    WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "우마무스메 프리티 더비")
                    # print("이_서비스의_모든_정보를_삭제하시겠습니까 " + str(count) + "개")
                    self.log("이_서비스의_모든_정보를_삭제하시겠습니까 " + str(count) + "개")
                    # print(position)
                    # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 모든_정보_삭제_빨간_박스, confidence=0.95, grayscale=False)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("모든_정보_삭제_빨간_박스 " + str(count) + "개")
                    self.log("모든_정보_삭제_빨간_박스 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.2)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 비밀번호, 0, 242, 78, 51, confidence=0.99, grayscale=False)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("비밀번호 " + str(count) + "개")
                    self.log("비밀번호 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.2)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 회원님의_소중한_정보_보호를_위해, confidence=0.99, grayscale=False)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 95)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("회원님의_소중한_정보_보호를_위해 " + str(count) + "개")
                    self.log("회원님의_소중한_정보_보호를_위해 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 제안된_로그인, confidence=0.99, grayscale=False)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 0, 0)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    time.sleep(0.5)
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, -57)
                        x, y = adbInput.RandomPosition(x, y, 0, 0)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("제안된_로그인 " + str(count) + "개")
                    self.log("제안된_로그인 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 자동완성_Continue, 214, 923, 90, 47)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("자동완성_Continue " + str(count) + "개")
                    self.log("자동완성_Continue " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 자동완성_계속, 226, 907, 62, 49)
                if count:
                    updateTime = time.time()
                    adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                    # print("자동완성_계속 " + str(count) + "개")
                    self.log("자동완성_계속 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 비밀번호_확인, confidence=0.95, grayscale=False)
                if count:
                    updateTime = time.time()
                    try:
                        x, y, width, height = position[0]
                        x += width/2
                        y += height/2
                        x, y = adbInput.BlueStacksOffset(x, y)
                        x, y = adbInput.Offset(x, y, 0, 0)
                        x, y = adbInput.RandomPosition(x, y, 5, 5)
                        adbInput.AdbTap(self.device, self.InstancePort, x, y)
                    except:
                        pass
                    # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    # print("비밀번호_확인 " + str(count) + "개")
                    self.log("비밀번호_확인 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                    
                count = 0
                count, position = ImageSearch(img, 숫자2단계_인증)
                if count:
                    updateTime = time.time()
                    WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                    # print("2단계_인증 " + str(count) + "개")
                    self.log("2단계_인증 " + str(count) + "개")
                    # print(position)
                    time.sleep(0.5)
                    img = screenshotToOpenCVImg(hwndMain)
            
            # 예외
            count = 0
            count, position = ImageSearch(img, 삭제_완료, confidence=0.95)
            if count:
                updateTime = time.time()
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                # print("삭제_완료 " + str(count) + "개")
                self.log("삭제_완료 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                return "Failed"
                
            if self.parent.isDoneTutorialCheckBox.isChecked() and self.is초기화하기:    
                # 무한 로딩 크롬 전용
                if time.time() >= updateTime + 5:
                    count = 0
                    count, position = ImageSearch(img, 로딩)
                    if count:
                        updateTime = time.time()
                        try:
                            x, y = adbInput.RandomPosition(540 / 2, 960 / 3, 5, 5)
                            adbInput.AdbSwipe(self.device, self.InstancePort, x, y, x, y + 960 / 3, adbInput.random.randint(25, 75))
                        except:
                            pass
                        
                        # print("로딩 " + str(count) + "개")
                        self.log("로딩 " + str(count) + "개")
                        # print(position)
                        # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                        self.log("무한 로딩 새로고침")
                        print("무한 로딩 새로고침")
                        time.sleep(3)
                        img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 카카오메일_아이디_이메일_전화번호, confidence=0.99)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                time.sleep(0.3)
                WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "a")
                for _ in range(2):
                    WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                time.sleep(0.3)
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=45, deltaX=5, deltaY=5)
                # print("카카오메일_아이디_이메일_전화번호 " + str(count) + "개")
                self.log("카카오메일_아이디_이메일_전화번호 " + str(count) + "개")
                # print(position)
                # print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break
            
            count = 0
            count, position = ImageSearch(img, 로그인, confidence=0.99, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                # print("로그인 " + str(count) + "개")
                self.log("로그인 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                
            if self.isAlive == False: # 중간에 멈춰야 할 경우
                break

            # 특수 이벤트
            count = 0
            count, position = ImageSearch(img, 추가_데이터를_다운로드합니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetX=125, offsetY=155, deltaX=5, deltaY=5)
                # print("추가_데이터를_다운로드합니다 " + str(count) + "개")
                self.log("추가_데이터를_다운로드합니다 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 재시도)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                # print("재시도 " + str(count) + "개")
                self.log("재시도 " + str(count) + "개")
                # print(position)
                continue
            
            count = 0
            count, position = ImageSearch(img, 타이틀_화면으로)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                # print("타이틀_화면으로 " + str(count) + "개")
                self.log("타이틀_화면으로 " + str(count) + "개")
                # print(position)
                continue
            
            count = 0
            count, position = ImageSearch(img, 확인)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                # print("확인 " + str(count) + "개")
                self.log("확인 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 앱_닫기, 78, 425, 391, 205)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], deltaX=5, deltaY=5)
                # print("앱_닫기 " + str(count) + "개")
                self.log("앱_닫기 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 날짜가_변경됐습니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=142, deltaX=5, deltaY=5)
                # print("날짜가_변경됐습니다 " + str(count) + "개")
                self.log("날짜가_변경됐습니다 " + str(count) + "개")
                # print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 숫자4080_에러_코드)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(self.device, self.InstancePort, position=position[0], offsetY=156, deltaX=5, deltaY=5)
                print("4080_에러_코드 " + str(count) + "개")
                self.log("4080_에러_코드 " + str(count) + "개")
                # print(position)
                if self.isDoingMAC_Change == False:
                    return "4080_에러_코드"

        return "Stop"