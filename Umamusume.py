from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
import multiprocessing as mp
import threading
import time
from UmamusumeProcess import UmaProcess

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyqtWidget import *


class Umamusume(QObject):
    sendLog = pyqtSignal(str)
    sendLog_Main = pyqtSignal(str, str)
    Error_4080 = pyqtSignal()
    
    def __init__(self, parent: "newTab"=None):
        super().__init__()
        if parent is not None:
            self.parent: "newTab" = parent

        self.ResetCount = -1

        # 커스텀 시그널 정의
        self.sendLog.connect(self.parent.recvLog)
        self.sendLog_Main.connect(self.parent.parent.recvLog_Main)
        self.Error_4080.connect(self.parent.parent.MAC_Address_Change)

    def Receive_Worker(self):
        while self.ReceiverEvent.is_set() == False or self.toParent.empty() == False:
            if not self.Receive():
                time.sleep(0.01)
        while not self.toParent.empty():
            try:
                recv = self.toParent.get(timeout=0.001)
                print(recv)
            except:
                pass
        self.toParent.close()
        # print("부모 수신 종료")

    def Receive(self): # 통신용
        if self.toParent.empty() == False:
            self.Lock.acquire()
            recv = self.toParent.get()
            # print(recv)
            if recv[0] == "sendLog":
                self.sendLog.emit(str(recv[1]))
            elif recv[0] == "sendLog_main":
                self.sendLog_Main.emit(str(recv[1]), str(recv[2]))
            elif recv[0] == "isDoneTutorial":
                self.parent.isDoneTutorialCheckBox.setChecked(recv[1])

            elif recv[0] == "InstanceComboBox.setEnabled":
                self.parent.InstanceComboBox.setEnabled(recv[1])
            elif recv[0] == "InstanceRefreshButton.setEnabled":
                self.parent.InstanceRefreshButton.setEnabled(recv[1])

            
            elif recv[0] == "InstanceComboBox.setEnabled":
                self.parent.InstanceComboBox.setEnabled(recv[1])
            elif recv[0] == "InstanceRefreshButton.setEnabled":
                self.parent.InstanceRefreshButton.setEnabled(recv[1])
            elif recv[0] == "startButton.setEnabled":
                self.parent.startButton.setEnabled(recv[1])
            elif recv[0] == "stopButton.setEnabled":
                self.parent.stopButton.setEnabled(recv[1])
            elif recv[0] == "resetButton.setEnabled":
                self.parent.resetButton.setEnabled(recv[1])
            elif recv[0] == "isDoneTutorialCheckBox.setEnabled":
                self.parent.isDoneTutorialCheckBox.setEnabled(recv[1])

            elif recv[0] == "sendResetCount":
                self.ResetCount = recv[1]
            elif recv[0] == "requestTotalResetCount":
                TotalResetCount = 0
                for i in self.parent.parent.Tab:
                    if i.stopButton.isEnabled():
                        if not (i.umamusume.ResetCount == -1):
                            TotalResetCount += i.umamusume.ResetCount
                self.toChild.put(["sendTotalResetCount", TotalResetCount])

            elif recv[0] == "숫자4080_에러_코드":
                self.Error_4080.emit()

            elif recv[0] == "terminate":
                th = threading.Thread(target=self.terminate)
                th.start()
            self.Lock.release()
            return True

        return False


    def start(self):
        # 초기화
        self.Lock = threading.Lock()
        self.toParent = mp.Queue() # 다른 프로세스와의 연결고리 생성
        self.toChild = mp.Queue()

        self.toChild.put(["InstanceName", self.parent.InstanceName])
        self.toChild.put(["InstancePort", self.parent.InstancePort])
        self.toChild.put(["isDoneTutorial", self.parent.isDoneTutorialCheckBox.isChecked()])
        self.toChild.put(["isSSRGacha", self.parent.isSSRGachaCheckBox.isChecked()])
        
        self.uma = UmaProcess()
        self.process = mp.Process(name=str(self.parent.InstancePort), target=self.uma.run_a, args=(self.toParent, self.toChild, ), daemon=True)
        self.process.start()

        self.ReceiverEvent = threading.Event()
        self.Receiver = threading.Thread(target=self.Receive_Worker, daemon=True)
        self.Receiver.start()
        
    def terminate(self):
        self.toChild.put(["terminate"])
        # print("terminate 신호 보냄")
        while self.process.is_alive():
            time.sleep(0.01)
        # print("자식 프로세스 생존?", self.process.is_alive())
        self.ReceiverEvent.set()
        self.Receiver.join() # 종료 대기
        # while self.Receiver.is_alive():
        #     time.sleep(0.01)
        self.ReceiverEvent.clear()
        while not self.toChild.empty():
            try:
                recv = self.toChild.get(timeout=0.001)
                print(recv)
            except:
                pass
        self.toChild.close() # 자식 수신 큐도 삭제해야함
        self.process.close()
        # print("process 삭제")



        # 버튼 활성화
        # self.toParent.put(["InstanceComboBox.setEnabled", True])
        self.parent.InstanceComboBox.setEnabled(True)
        # self.toParent.put(["InstanceRefreshButton.setEnabled", True])
        self.parent.InstanceRefreshButton.setEnabled(True)
        
        # self.toParent.put(["startButton.setEnabled", True])
        self.parent.startButton.setEnabled(True)
        # self.toParent.put(["stopButton.setEnabled", False])
        self.parent.stopButton.setEnabled(False)
        # self.toParent.put(["resetButton.setEnabled", True])
        self.parent.resetButton.setEnabled(True)
        # self.toParent.put(["isDoneTutorialCheckBox.setEnabled", True])
        self.parent.isDoneTutorialCheckBox.setEnabled(True)



        # self.toParent.close()
        # self.toChild.close()
        # self.process.join() # 종료 대기
