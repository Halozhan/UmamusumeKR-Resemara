import sys
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
# from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSlot, QObject, pyqtSignal
from Umamusume import *
from ASUS_Router_Mac_Change import *
from Change_MAC import *
from sleepTime import sleepTime

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        
        
        # self.ASUSCheckBox = QCheckBox("ASUS 공유기 버전")
        # self.PAGCheckBox = QCheckBox("Technitium MAC Address Changer 버전")

        # self.vbox = QVBoxLayout()

        # self.vbox.addWidget(self.ASUSCheckBox)
        # self.vbox.addWidget(self.PAGCheckBox)
        # self.verticalTabWidgetPage1.setLayout(self.vbox)
        # self.setLayout(self.vbox)

        self.Tab = []
        count = 8 # 8개의 탭 생성
        for i in range(count):
            self.Tab.append(newTab(self)) # self를 상속받은 newTab
            self.verticalTabWidget.addTab(self.Tab[i].newTab(), "탭 %d" % (self.verticalTabWidget.count()))
        
        
        self.sleepTime = sleepTime(self)
        self.sleepTime.start()
        
        
        self.verticalTabWidget.setMovable(True)
        # print(len(Tab)) 탭 갯수
        
        self.verticalTabWidget.addTab(QTextEdit("미구현"), "+")
        
        self.ASUSCheckBox.clicked.connect(self.ASUSCheckBoxFunction)
        self.PAGCheckBox.clicked.connect(self.PAGCheckBoxFunction)
        
        
    @pyqtSlot(float)
    def SleepTimeFunction(self, Time):
        for i in self.Tab:
            i.umamusume.sleepTime = Time
    
    @pyqtSlot()
    def ASUSCheckBoxFunction(self):
        if self.ASUSCheckBox.isChecked():
            print("ASUSCheckBox가 활성화됨")
        else:
            print("ASUSCheckBox가 비활성화됨")
        
    
    @pyqtSlot()
    def PAGCheckBoxFunction(self):
        if self.PAGCheckBox.isChecked():
            print("PAGCheckBox가 활성화됨")
        else:
            print("PAGCheckBox가 비활성화됨")
            
    
    @pyqtSlot()
    def AllStopFunction(self):
        for i in self.Tab:
            i.umamusume.isDoingMAC_Change = True
        print("-"*50)
        print("초기화"*10)
        print("-"*50)
        if self.PAGCheckBox.isChecked():
            PAG_MAC_Change()
        if self.ASUSCheckBox.isChecked():
            Change_Mac_Address()
        for i in self.Tab:
            i.umamusume.isDoingMAC_Change = False
        
class newTab(QMainWindow):
    AllStop = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__()
        # 변수 초기화
        self.parent = parent
        
        self.InstanceName = ""
        self.InstancePort = 0
        self.sleepTime = 0.5
        
        # 객체 초기화
        self.InstanceComboBox = QComboBox()
        self.InstanceRefreshButton = QPushButton("새로고침", self)
        
        self.startButton = QPushButton("시작", self)
        self.stopButton = QPushButton("정지", self)
        self.resetButton = QPushButton("초기화", self)
        self.isDoneTutorialCheckBox = QCheckBox("튜토리얼 스킵 여부", self)
        self.isDoneTutorialCheckBox.setChecked(True)
        
        self.logs = QTextBrowser()

        self.umamusume = Umamusume(self)
        
        # 함수 초기화
        self.InstanceFunction()
        self.InstanceRefreshFunction()
        
        # 시그널 정의
        self.InstanceComboBox.currentIndexChanged.connect(self.InstanceFunction)
        self.InstanceRefreshButton.clicked.connect(self.InstanceRefreshFunction)
        
        self.startButton.clicked.connect(self.startFunction)
        self.stopButton.clicked.connect(self.stopFunction)
        self.resetButton.clicked.connect(self.resetFunction)
        self.isDoneTutorialCheckBox.clicked.connect(self.isDoneTutorialFunction)
        
        # 커스텀 시그널 정의
        self.AllStop.connect(self.parent.AllStopFunction)
                        
    @pyqtSlot(str)
    def sendLog(self, text):
        self.logs.append(text)
        
    @pyqtSlot()
    def Error_4080Function(self):
        self.AllStop.emit()
        
        
    def newTab(self):
        
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.InstanceComboBox, stretch=2)
        self.hbox1.addWidget(self.InstanceRefreshButton, stretch=1)
        
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.startButton)
        self.hbox2.addWidget(self.stopButton)
        self.hbox2.addWidget(self.resetButton)
        self.hbox2.addWidget(self.isDoneTutorialCheckBox)
        
        self.vbox = QVBoxLayout()
        
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addWidget(self.logs)
        
        # vbox.addWidget()
        
        self.tab = QWidget()
        self.tab.setLayout(self.vbox)
        
        return self.tab
    
    # events
    def InstanceFunction(self):
        if self.InstanceComboBox.count() == 0:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.resetButton.setEnabled(False)
            self.isDoneTutorialCheckBox.setEnabled(False)
            return
        
        self.logs.append("-"*50)
        if self.InstanceComboBox.currentText() == "선택 안함":
            self.logs.append("선택해주세요")
            
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.resetButton.setEnabled(False)
            self.isDoneTutorialCheckBox.setEnabled(False)
            
        else:
            self.SelectedInstance = self.InstanceComboBox.currentText()
            self.SelectedInstance = self.SelectedInstance.split(",")
            self.SelectedInstance[0] = self.SelectedInstance[0].replace('"', '')
            self.SelectedInstance[1] = self.SelectedInstance[1].strip()
            self.InstanceName, self.InstancePort = self.SelectedInstance
            
            self.InstancePort = int(self.InstancePort)
            self.logs.append(str(self.InstanceName) + " 윈도우, " + str(self.InstancePort) + "번 포트가 선택되었습니다.")
            
            self.umamusume = Umamusume(self)
            
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(True)
            self.resetButton.setEnabled(True)
            self.isDoneTutorialCheckBox.setEnabled(True)
            
        self.logs.append("-"*50)
            
        
    def InstanceRefreshFunction(self):
        self.InstanceComboBox.clear()
        
        lines = ["선택 안함"]
        try:
            f = open("Instances.txt", "r", encoding="UTF-8")
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip() # 줄 끝의 줄 바꿈 문자를 제거한다.
                lines.append(line)
            f.close()
            self.InstanceComboBox.addItems(lines)
            self.logs.append("불러오기 성공")
        except:
            self.logs.append("불러올 수 없습니다. Instance.txt 파일을 다시 확인해주세요")
            pass
    
    
    def startFunction(self):
        self.InstanceComboBox.setEnabled(False)
        self.InstanceRefreshButton.setEnabled(False)
        
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.resetButton.setEnabled(False)
        self.isDoneTutorialCheckBox.setEnabled(False)
        
        self.logs.append("-"*50)
        self.logs.append("시작!!")
        self.umamusume.start()
        self.logs.append("-"*50)
    
    
    def stopFunction(self):
        self.InstanceComboBox.setEnabled(True)
        self.InstanceRefreshButton.setEnabled(True)
        
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.resetButton.setEnabled(True)
        self.isDoneTutorialCheckBox.setEnabled(True)
        
        self.logs.append("-"*50)
        self.umamusume.stopping()
        self.logs.append("멈춤!!")
        self.logs.append("-"*50)
    
    
    def resetFunction(self):
        self.resetButton.setEnabled(False)
        self.logs.append("-"*50)
        self.logs.append("초기화!!")
        self.logs.append("-"*50)
    
    def isDoneTutorialFunction(self):
        self.logs.append("-"*50)
        if self.isDoneTutorialCheckBox.isChecked():
            self.logs.append("튜토리얼 스킵 활성화!!")
        else:
            self.logs.append("튜토리얼 진행 (다소 렉 유발)")
        self.logs.append("-"*50)
    
        
if __name__ =="__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()        

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()