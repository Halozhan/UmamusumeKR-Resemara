import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from Umamusume import *
from ASUS_Router_Mac_Change import *
from Change_MAC import *
from sleepTime import sleepTime
from datetime import datetime

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
# form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sleepTime = sleepTime(self)

        self.resize(600, 600) # 사이즈 변경
        self.setWindowTitle("우마뾰이")
        self.setWindowIcon(QIcon("channels4_profile.jpg"))

        self.verticalTabWidget = QTabWidget() # 탭 위젯
        self.verticalTabWidget.setMovable(True)
        QMainWindow.setCentralWidget(self, self.verticalTabWidget) # 중앙 위젯에 탭 위젯 추가

        self.메인페이지 = QWidget() # ---------------------------------
        self.verticalBox = QVBoxLayout()

        self.MenuHBox = QHBoxLayout() # --------------

        self.TaskViewVBox = QVBoxLayout()
        self.CPU_now = QLabel()
        self.Latency = QLabel()
        self.TaskViewVBox.addWidget(self.CPU_now)
        self.TaskViewVBox.addWidget(self.Latency)

        self.StopButton = QPushButton("모두 정지")
        
        self.MenuHBox.addLayout(self.TaskViewVBox)
        self.MenuHBox.addWidget(self.StopButton) # ----


        self.timeRateGroupBox = QGroupBox("부하를 정합니다. 1번은 높을수록, 2번은 낮출수록 반응이 빨라짐") # ---------
        self.timeRateVBox = QVBoxLayout()

        self.timeRateLabel_help = QLineEdit()
        self.timeRateLabel1 = QLabel()
        self.timeRateLabel2 = QLabel()
        
        self.timeRateSlider1 = QSlider(Qt.Horizontal, self)
        self.timeRateSlider1.setRange(0, 300)
        self.timeRateSlider1.setTickInterval(10)
        self.timeRateSlider1.setSliderPosition(180)
        self.timeRateSlider1.setTickPosition(QSlider.TicksBelow)
        
        self.timeRateSlider2 = QSlider(Qt.Horizontal, self)
        self.timeRateSlider2.setRange(0, 100)
        self.timeRateSlider2.setTickInterval(10)
        self.timeRateSlider2.setSliderPosition(80)
        self.timeRateSlider2.setTickPosition(QSlider.TicksBelow)

        self.timeRateFunction()
        
        self.timeRateVBox.addWidget(self.timeRateLabel_help)
        self.timeRateVBox.addWidget(self.timeRateLabel1)
        self.timeRateVBox.addWidget(self.timeRateSlider1)

        self.timeRateVBox.addWidget(self.timeRateLabel2)
        self.timeRateVBox.addWidget(self.timeRateSlider2)

        self.timeRateGroupBox.setLayout(self.timeRateVBox) # --------------------------------

        self.ASUSRadioButton = QRadioButton("ASUS 공유기 버전")
        self.ASUSRadioButton.setChecked(True)
        self.PAGRadioButton = QRadioButton("Technitium MAC Address Changer 버전")

        self.logs = QTextBrowser()

        self.verticalBox.addLayout(self.MenuHBox)

        self.verticalBox.addWidget(self.timeRateGroupBox)

        self.verticalBox.addWidget(self.ASUSRadioButton)
        self.verticalBox.addWidget(self.PAGRadioButton)
        
        self.verticalBox.addWidget(self.logs)
        
        self.메인페이지.setLayout(self.verticalBox)
        self.verticalTabWidget.addTab(self.메인페이지, "Main") # --------

        self.Tab = []
        count = 10 # 10개의 탭 생성
        for i in range(count):
            self.Tab.append(newTab(self)) # self를 상속받은 newTab
            self.verticalTabWidget.addTab(self.Tab[i].newTab(), "탭 %d" % (self.verticalTabWidget.count()))
        
        
        
        self.sleepTime.start()
                
        self.verticalTabWidget.addTab(QTextEdit("미구현"), "+")

        # Event
        self.timeRateSlider1.valueChanged.connect(self.timeRateFunction)
        self.timeRateSlider2.valueChanged.connect(self.timeRateFunction)

        self.StopButton.clicked.connect(self.AllStopInstance)

        self.ASUSRadioButton.clicked.connect(self.ASUSCheckBoxFunction)
        self.PAGRadioButton.clicked.connect(self.PAGCheckBoxFunction)
    
    def AllStopInstance(self):
        for i in self.Tab:
            if i.stopButton.isEnabled():
                i.stopFunction()

    def timeRateFunction(self):
        value1 = self.timeRateSlider1.value()
        value2 = self.timeRateSlider2.value()
        self.sleepTime.timeRate1 = value1*0.01
        self.sleepTime.timeRate2 = value2*0.1
        self.timeRateLabel1.setText("기울기: " + str(round(value1*0.01, 3)))
        self.timeRateLabel2.setText("최고 지연: " + str(round(value2*0.1, 3)) + "s")
        self.timeRateLabel_help.setText("x^{"+str(round(value1*0.01, 3))+"e}\cdot" + str(round(value2*0.1, 3)) +"를 https://www.desmos.com/calculator/ifg3mwmqun에 붙여넣기하면 그래프를 볼 수 있음")

    @pyqtSlot(str, str)
    def sendLog_Main(self, id, text):
        self.logs.append(id + " " + text)
        
    @pyqtSlot(float, float)
    def SleepTimeFunction(self, cpu_load, Time):
        self.CPU_now.setText("CPU 사용률: " + str(cpu_load) + "%")
        self.Latency.setText("지연률: " + str(Time) + "s")
        for i in self.Tab:
            i.umamusume.sleepTime = Time
    
    @pyqtSlot()
    def ASUSCheckBoxFunction(self):
        if self.ASUSRadioButton.isChecked():
            self.logs.append("ASUSRadioButton가 활성화됨")
        else:
            self.logs.append("ASUSRadioButton가 비활성화됨")
        
    
    @pyqtSlot()
    def PAGCheckBoxFunction(self):
        if self.PAGRadioButton.isChecked():
            self.logs.append("PAGRadioButton가 활성화됨")
        else:
            self.logs.append("PAGRadioButton가 비활성화됨")
            
    
    @pyqtSlot()
    def MAC_Address_Change(self):
        for i in self.Tab:
            i.umamusume.isDoingMAC_Change = True
        print("-"*50)
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(now + " MAC 주소 변경 중")
        print(now + " MAC 주소 변경 중")
        if self.PAGRadioButton.isChecked():
            PAG_MAC_Change()
        if self.ASUSRadioButton.isChecked():
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
        self.AllStop.connect(self.parent.MAC_Address_Change)
                        
    @pyqtSlot(str)
    def sendLog(self, text):
        self.logs.append(text)

        
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
            self.stopButton.setEnabled(False)
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
        self.logs.append("-"*50)
        self.umamusume.terminate()
        self.logs.append("멈춤!!")
        self.logs.append("-"*50)
        
    
    def resetFunction(self):
        self.resetButton.setEnabled(False)
        self.logs.append("-"*50)
        self.logs.append("초기화!!")
        self.logs.append("-"*50)
        try:
            path = "./Saved_Data/"+str(self.InstancePort)+".uma"
            os.remove(path)
        except:
            pass
        
    
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