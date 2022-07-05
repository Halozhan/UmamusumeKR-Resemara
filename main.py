from Umamusume import *
from pyqtWidget import *


if __name__ =="__main__":
    
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    
    Tab = []
    count = 8
    for i in range(count):
        Tab.append(Umamusume()) # newTab을 상속받은 Umamusume
        myWindow.verticalTabWidget.addTab(Umamusume.newTab(Tab[i]), "탭 %d" % (myWindow.verticalTabWidget.count()))
    
    
    # myWindow.TabSetup(Tab=Tab, count=8)
    # messageSender(0, "ㅎㅇ")

    # if __name__ == "__main__" :
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    # messageSender("asdfasdfasdfddd", 0)
        

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()