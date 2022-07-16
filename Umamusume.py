from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
import multiprocessing as mp
from threading import Thread
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
            self.parent = parent

        # 커스텀 시그널 정의
        self.sendLog.connect(self.parent.recvLog)
        self.sendLog_Main.connect(self.parent.parent.recvLog_Main)
        self.Error_4080.connect(self.parent.parent.MAC_Address_Change)


    def Receive(self): # 통신용
        while True:
            if self.toParent.empty() == False:
                recv = self.toParent.get()
                print(recv)
                if recv[0] == "sendLog":
                    self.sendLog.emit(str(recv[1]))
                    # print(recv[1])
                if recv[0] == "sendLog_main":
                    self.sendLog_Main.emit(str(recv[1]), str(recv[2]))
                    # print(recv[1])
                if recv[0] == "isDoneTutorial":
                    self.parent.isDoneTutorialCheckBox.setChecked(recv[1])
                    # print(recv[1])

                if recv[0] == "InstanceComboBox.setEnabled":
                    self.parent.isDoneTutorialCheckBox.setEnabled(recv[1])
                    # print(recv[1])
                if recv[0] == "InstanceRefreshButton.setEnabled":
                    self.parent.InstanceRefreshButton.setEnabled(recv[1])
                    # print(recv[1])

                if recv[0] == "startButton.setEnabled":
                    self.parent.startButton.setEnabled(recv[1])
                    # print(recv[1])
                if recv[0] == "stopButton.setEnabled":
                    self.parent.stopButton.setEnabled(recv[1])
                    # print(recv[1])
                if recv[0] == "resetButton.setEnabled":
                    self.parent.resetButton.setEnabled(recv[1])
                    # print(recv[1])
                if recv[0] == "isDoneTutorialCheckBox.setEnabled":
                    self.parent.isDoneTutorialCheckBox.setEnabled(recv[1])
                    # print(recv[1])


                if recv[0] == "requestResetCount":
                    total_resetCount = 0
                    for i in self.parent.parent.Tab:
                        total_resetCount += i.umamusume.resetCount
                    self.toChild.put(["recvResetCount", total_resetCount])
                    # print(recv[1])

                if recv[0] == "4080":
                    self.Error_4080.emit()
                    # print(recv[1])
                time.sleep(0.001)



    # def recvLog(self, text):
    #     self.sendLog.emit(text)

    # def recvLog_main(self, id, text):
    #     self.sendLog_Main.emit(str(id), str(text))

    def start(self):
        # 초기화
        self.toParent = mp.Queue() # 다른 프로세스와의 연결고리 생성
        self.toChild = mp.Queue()

        self.toChild.put(["InstanceName", self.parent.InstanceName])
        self.toChild.put(["InstancePort", self.parent.InstancePort])
        self.toChild.put(["isDoneTutorial", self.parent.isDoneTutorialCheckBox.isChecked()])
        self.toChild.put(["isSSRGacha", self.parent.isSSRGachaCheckBox.isChecked()])
        # self.p = mp.Process(name=str(self.parent.InstancePort), target=self.run_a, args=(self.pipeChild, ), daemon=True)
        self.uma = UmaProcess()
        self.process = mp.Process(name=str(self.parent.InstancePort), target=self.uma.run_a, args=(self.toParent, self.toChild, ), daemon=True)
        # self.pipeParent.send("ㅎㅇ1")
        # self.pipeParent.send("ㅎㅇ2")
        # self.pipeParent.send("ㅎㅇ3")
        self.process.start()

        self.Receiver = Thread(target=self.Receive, daemon=True)
        self.Receiver.start()
        
    def terminate(self):
        self.toChild.put(["terminate"])
        # pass # not yet