import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
# from Umamusume import *

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.verticalTabWidget.setMovable(True)
        # print(len(Tab)) 탭 갯수
        
        self.verticalTabWidget.addTab(QTextEdit("미구현"), "+")
        
        
class newTab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Instance = QComboBox()
        self.InstanceRefresh = QPushButton("새로고침", self)
        
        self.start = QPushButton("시작", self)
        self.stop = QPushButton("정지", self)
        self.reset = QPushButton("초기화", self)
        self.isDoneTutorial = QCheckBox("튜토리얼 스킵 여부", self)
        self.isDoneTutorial.setChecked(True)
        
        self.logs = QTextBrowser()
        
        # 처음 설정
        # self.InstanceRefreshFunction()
        # self.InstanceFunction()
        
        # self.Instance.currentIndexChanged.connect(self.InstanceFunction)
        # self.InstanceRefresh.clicked.connect(self.InstanceRefreshFunction)
        
        # self.start.clicked.connect(self.startFunction)
        # self.stop.clicked.connect(self.stopFunction)
        # self.reset.clicked.connect(self.resetFunction)
        # self.isDoneTutorial.clicked.connect(self.isDoneTutorialFunction)
                
        
    def newTab(self):
        
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.Instance, stretch=2)
        self.hbox1.addWidget(self.InstanceRefresh, stretch=1)
        
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.start)
        self.hbox2.addWidget(self.stop)
        self.hbox2.addWidget(self.reset)
        self.hbox2.addWidget(self.isDoneTutorial)
        
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
        if self.Instance.count() == 0:
            self.start.setEnabled(False)
            self.stop.setEnabled(False)
            self.reset.setEnabled(False)
            self.isDoneTutorial.setEnabled(False)
            return
        
        self.logs.append("-"*50)
        if self.Instance.currentText() == "선택 안함":
            self.logs.append("선택해주세요")
            
            self.start.setEnabled(False)
            self.stop.setEnabled(False)
            self.reset.setEnabled(False)
            self.isDoneTutorial.setEnabled(False)
            
        else:
            try:
                self.SelectedInstance = self.Instance.currentText()
                self.SelectedInstance = self.SelectedInstance.split(",")
                self.SelectedInstance[0] = self.SelectedInstance[0].replace('"', '')
                self.SelectedInstance[1] = self.SelectedInstance[1].strip()
                self.InstanceName, self.InstancePort = self.SelectedInstance
                
                self.InstancePort = int(self.InstancePort)
                self.InstancePort = int(self.InstancePort)
                self.logs.append(str(self.InstanceName) + " 윈도우, " + str(self.InstancePort) + "번 포트가 선택되었습니다.")
                
                self.start.setEnabled(True)
                self.stop.setEnabled(True)
                self.reset.setEnabled(True)
                self.isDoneTutorial.setEnabled(True)
            
            except:
                self.logs.append("선택 실패")
        self.logs.append("-"*50)
            
        
    def InstanceRefreshFunction(self):
        self.Instance.clear()
        
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
            self.Instance.addItems(lines)
            self.logs.append("불러오기 성공")
        except:
            self.logs.append("불러올 수 없습니다. Instance.txt 파일을 다시 확인해주세요")
            pass
        
    def startFunction(self):
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        self.reset.setEnabled(False)
        self.isDoneTutorial.setEnabled(False)
        self.logs.append("-"*50)
        self.logs.append("시작!!")
        # self.start()
        self.logs.append("-"*50)
    
    def stopFunction(self):
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        self.reset.setEnabled(True)
        self.isDoneTutorial.setEnabled(True)
        self.logs.append("-"*50)
        # self.stop()
        self.logs.append("멈춤!!")
        self.logs.append("-"*50)
    
    def resetFunction(self):
        self.reset.setEnabled(False)
        self.logs.append("-"*50)
        self.logs.append("초기화!!")
        self.logs.append("-"*50)
    
    def isDoneTutorialFunction(self):
        self.logs.append("-"*50)
        if self.isDoneTutorial.isChecked():
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