import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("untitled.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 버튼 기능
        self.start.clicked.connect(self.startFunction)
        self.stop.clicked.connect(self.stopFunction)
        
        tab1 = QWidget()
        tab2 = QWidget()
        
        tabs = QTabWidget()
        tabs.addTab(tab1, '탭1')
        tabs.addTab(tab2, '탭2')
        
        self.vbox.addWidget(tabs)
        
    
    def startFunction(self):
        self.logs.append("-"*50)
        self.logs.append("시작!!")
        self.logs.append("-"*50)
        
    def stopFunction(self):
        self.logs.append("-"*50)
        self.logs.append("멈춤!!")
        self.logs.append("-"*50)
    
        
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    
    #WindowClass 조작
    myWindow.logs.append("ㅎㅇㅎㅇ")
    myWindow.logs.append("ㅎㅇㅎㅇ")
    myWindow.logs.append("ㅎㅇㅎㅇ")

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()