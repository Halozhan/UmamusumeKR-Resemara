import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from Umamusume import *

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 버튼 기능
        # self.start.clicked.connect(self.startFunction)
        # self.stop.clicked.connect(self.stopFunction)
        # self.reset.clicked.connect(self.resetFunction)
        
        # tab1 = QWidget()
        # tab2 = QWidget()
        # tab3 = QWidget()
        
        # tabs = QTabWidget()
        # tabs.addTab(tab1, '탭1')
        # tabs.addTab(tab2, '탭2')
        
        # self.verticalTabWidget.addTab(tab1, "탭추가1")
        # self.verticalTabWidget.addTab(tab2, "탭추가2")
        # self.verticalTabWidget.addTab(tab3, "탭추가3")
        # self.verticalTabWidget.addTab(QTextEdit(), "tab %d" % (self.verticalTabWidget.count() + 1))
        # print(self.verticalTabWidget.currentIndex()) # 현재 인덱스
        # self.verticalTabWidget.addTab(QTextEdit(), "tab %d" % (self.verticalTabWidget.count() + 1))
        # self.verticalTabWidget.addTab(QTextEdit(), "tab %d" % (self.verticalTabWidget.count() + 1))
        # self.verticalTabWidget.setTabText(4, "아무거나 바껴바라")
        
        # self.verticalTabWidget.addTab(self.makeTab1(), "tab %d" % (self.verticalTabWidget.count() + 1))
        
        # self.a = self.newTab()
        # self.b = self.newTab()
        # self.c = self.newTab()
        self.Tab = []
        for i in range(8):
            self.Tab.append(self.newTab())
            self.verticalTabWidget.addTab(self.Tab[i].newTab(), "탭 %d" % (self.verticalTabWidget.count()))
        print(len(self.Tab))
        
        
        
        self.verticalTabWidget.addTab(QTextEdit("미구현"), "+")
        
        # self.verticalTabWidget.tabBarClicked(2)
        # self.verticalTabWidget.currentChanged.connect(self.isChanged)
        # self.verticalTabWidget.changeEvent(self, isChanged)
        # def isChanged(self):
            # print(tab)
        # print(self.verticalTabWidget.currentIndex()) # 현재 인덱스
        # self.verticalTabWidget.addTab(self.newTab(), "tab %d" % (self.verticalTabWidget.count() + 1))
        self.verticalTabWidget.setMovable(True)
        self.Tab[0].logs.append("ㅎㅇ1")
        self.Tab[1].logs.append("ㅎㅇ2")
        self.Tab[2].logs.append("ㅎㅇ3")
        self.Tab[3].logs.append("ㅎㅇ4")
        # self.verticalTabWidget.indexOf(3)
        # print(self.verticalTabWidget.tabText(4))
        # index = self.verticalTabWidget.indexOf(4)
        # self.index = QVBoxLayout()

                
        # self.verticalTabWidget.layout = QVBoxLayout(self)
        # self.pushButton5 = QPushButton("Pyqt5 button")
        # print(QTextEdit())

        
        
    class newTab(QMainWindow):
        def __init__(self):
            super().__init__()
            self.start = QPushButton("시작", self)
            self.stop = QPushButton("정지", self)
            self.start.setChecked(False)
            self.reset = QPushButton("초기화", self)
            self.isDoneTutorial = QCheckBox("튜토리얼 스킵 여부", self)
            self.isDoneTutorial.setChecked(True)
            self.logs = QTextBrowser()
            self.Instance = QComboBox()
            
            lines = []

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
            except:
                self.Instance.addItem("불러올 수 없습니다. Instance.txt 파일을 다시 확인해주세요")
                pass
            
            
            self.start.clicked.connect(self.startFunction)
            self.stop.clicked.connect(self.stopFunction)
            self.reset.clicked.connect(self.resetFunction)
            self.isDoneTutorial.clicked.connect(self.isDoneTutorialFunction)
            
            self.Instance.currentIndexChanged.connect(self.InstanceFunction)
            
            # self.newTab()
            
        def newTab(self):
            self.hbox = QHBoxLayout()
            self.hbox.addWidget(self.start)
            self.hbox.addWidget(self.stop)
            self.hbox.addWidget(self.reset)
            self.hbox.addWidget(self.isDoneTutorial)
            
            self.vbox = QVBoxLayout()
            
            self.vbox.addWidget(self.Instance)
            self.vbox.addLayout(self.hbox)
            self.vbox.addWidget(self.logs)
            
            # vbox.addWidget()
            
            self.tab = QWidget()
            self.tab.setLayout(self.vbox)
            
            return self.tab
        
        # events
        
        def startFunction(self):
            self.start.setEnabled(False)
            self.stop.setEnabled(True)
            self.reset.setEnabled(False)
            self.isDoneTutorial.setEnabled(False)
            self.logs.append("-"*50)
            self.logs.append("시작!!")
            Tutorial = self.isDoneTutorial.isChecked()
            self.umamusume = Umamusume(self.WindowName, self.InstancePort, Tutorial, 0)
            self.umamusume.start()
            self.logs.append("-"*50)
        
        def stopFunction(self):
            self.start.setEnabled(True)
            self.stop.setEnabled(False)
            self.reset.setEnabled(True)
            self.isDoneTutorial.setEnabled(True)
            self.logs.append("-"*50)
            self.umamusume.stop()
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
        
        def InstanceFunction(self):
            self.logs.append("-"*50)
            self.SelectedInstance = self.Instance.currentText()
            self.SelectedInstance = self.SelectedInstance.split(",")
            self.SelectedInstance[0] = self.SelectedInstance[0].replace('"', '')
            self.SelectedInstance[1] = self.SelectedInstance[1].strip()
            self.WindowName, self.InstancePort = self.SelectedInstance
            self.InstancePort = int(self.InstancePort)
            # print(SelectedInstance)
            self.logs.append(str(self.WindowName) + " 윈도우, " + str(self.InstancePort) + "번 포트가 선택되었습니다.")
            
            self.logs.append("-"*50)

    
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    
    #WindowClass 조작
    

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()