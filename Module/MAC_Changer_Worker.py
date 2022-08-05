from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
import ASUS_Router_Mac_Change
import mac_address_changer_windows

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyqtWidget import *

class Worker(QThread):
    sendLog_Main = pyqtSignal(str, str)
    def __init__(self, parent) -> None:
        super().__init__()
        if parent is not None:
            self.parent: "WindowClass" = parent
        self.isReboot = False
        self.sendLog_Main.connect(self.parent.recvLog_Main)

    def MAC_Change(self) -> None:
        if not self.isRunning():
            self.start()
            return True
        return False

    def run(self) -> None:
        try:
            for i in self.parent.Tab:
                i.umamusume.toChild(["isDoingMAC_Change", True])
        except:
            pass
        print("-"*50)
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.sendLog_Main.emit("MAC Worker:", str(now + " MAC 주소 변경 중"))
        print(now + " MAC 주소 변경 중")
        if self.parent.ManualButton.isChecked():
            print("수동 조작이 필요합니다. MAC 주소를 변경 후 시작을 눌러주세요.")
            self.parent.AllStopInstance()
        elif self.parent.ASUSRadioButton.isChecked():
            ASUS_Router_Mac_Change.ASUS_Change_MAC(self.isReboot)
        elif self.parent.PythonMACChangerRadioButton.isChecked():
            mac_address_changer_windows.main()
        try:
            for i in self.parent.Tab:
                i.umamusume.toChild(["isDoingMAC_Change", False])
        except:
            pass