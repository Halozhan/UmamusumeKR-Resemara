if __name__ =="__main__":
    from Umamusume import *




from pyqtWidget import *

Tab = []

#QApplication : 프로그램을 실행시켜주는 클래스
app = QApplication(sys.argv)
for i in range(8):
    Tab.append(Umamusume())






def messageSender(index, Contents):
    global Tab
    Tab[index].logs.append(Contents)



if __name__ =="__main__":

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    
    
    myWindow.TabSetup(Tab=Tab, count=8)
    # messageSender(0, "ㅎㅇ")

    # if __name__ == "__main__" :
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    # messageSender("asdfasdfasdfddd", 0)
        

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()