import os
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QSlider,
    QTextBrowser,
    QPushButton,
    QLabel,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QTextEdit,
)
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtGui import QIcon
from Umamusume import Umamusume
from sleepTime import sleepTime


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sleepTime = sleepTime(self)
        self.sleepTime.start()

        self.resize(600, 600)  # 사이즈 변경
        self.setWindowTitle("우마뾰이 - Github: Halozhan")
        self.setWindowIcon(QIcon("./icon/channels4_profile.jpg"))

        self.verticalTabWidget = QTabWidget()  # 탭 위젯
        self.verticalTabWidget.setMovable(True)
        QMainWindow.setCentralWidget(self, self.verticalTabWidget)  # 중앙 위젯에 탭 위젯 추가

        self.메인페이지 = QWidget()  # ---------------------------------
        self.verticalBox = QVBoxLayout()

        self.MenuHBox = QHBoxLayout()  # --------------

        self.TaskViewVBox = QVBoxLayout()
        self.CPU_now = QLabel("CPU_now")
        self.Latency = QLabel("Latency")
        self.TaskViewVBox.addWidget(self.CPU_now)
        self.TaskViewVBox.addWidget(self.Latency)

        self.AllStopButton = QPushButton("모두 정지")
        self.clearLogsButton = QPushButton("로그 삭제", self)

        self.MenuHBox.addLayout(self.TaskViewVBox)
        self.MenuHBox.addWidget(self.AllStopButton)  # ----
        self.MenuHBox.addWidget(self.clearLogsButton)

        self.timeRateGroupBox = QGroupBox(
            "부하를 정합니다. 1번은 높을수록, 2번은 낮출수록 반응이 빨라짐"
        )  # ---------
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

        self.timeRateGroupBox.setLayout(
            self.timeRateVBox
        )  # --------------------------------

        self.logs = QTextBrowser()

        self.verticalBox.addLayout(self.MenuHBox)

        self.verticalBox.addWidget(self.timeRateGroupBox)

        self.verticalBox.addWidget(self.logs)

        self.메인페이지.setLayout(self.verticalBox)
        self.verticalTabWidget.addTab(self.메인페이지, "Main")  # --------

        self.Tab: list[newTab] = []
        for i in range(10):  # 10개의 탭 생성
            self.Tab.append(newTab(self))  # self를 상속받은 newTab
            self.verticalTabWidget.addTab(
                self.Tab[i].tab, "탭 %d" % (self.verticalTabWidget.count())
            )

        self.verticalTabWidget.addTab(QTextEdit("미구현"), "+")

        # Event
        self.timeRateSlider1.valueChanged.connect(self.timeRateFunction)
        self.timeRateSlider2.valueChanged.connect(self.timeRateFunction)

        self.AllStopButton.clicked.connect(self.AllStopInstance)
        self.clearLogsButton.clicked.connect(self.logs.clear)

    def AllStopInstance(self):
        for i in self.Tab:
            if i.stopButton.isEnabled():  # 정지 버튼이 켜져있는 인스턴스만
                i.stopButtonFunction()  # 종료

    def timeRateFunction(self):
        value1 = self.timeRateSlider1.value()
        value2 = self.timeRateSlider2.value()
        self.sleepTime.timeRate1 = value1 * 0.01
        self.sleepTime.timeRate2 = value2 * 0.1
        self.timeRateLabel1.setText("기울기: " + str(round(value1 * 0.01, 3)))
        self.timeRateLabel2.setText("최고 지연: " + str(round(value2 * 0.1, 3)) + "s")
        self.timeRateLabel_help.setText(
            "x^{"
            + str(round(value1 * 0.01, 3))
            + "e}\\cdot"
            + str(round(value2 * 0.1, 3))
            + "를 https://www.desmos.com/calculator/ifg3mwmqun에 붙여넣기하면 그래프를 볼 수 있음"
        )

    @pyqtSlot(str, str)
    def recvLog_Main(self, id, text):
        self.logs.append(id + " " + text)

    @pyqtSlot(float, float)
    def SleepTimeFunction(self, cpu_load, Time):
        self.CPU_now.setText("CPU 사용률: " + str(cpu_load) + "%")
        self.Latency.setText("지연률: " + str(Time) + "s")
        for i in self.Tab:
            if i.stopButton.isEnabled():
                i.umamusume.toChild.put(["sleepTime", float(Time)])

    def closeEvent(self, a0: QCloseEvent) -> None:
        reply = QMessageBox.question(
            self,
            "너 지금 딸들과의 추억을 버리려는거야?",
            "정말 종료하시겠습니까?\n(인스턴스를 정지합니다.)",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.AllStopInstance()
            a0.accept()
        else:
            a0.ignore()


class newTab(QMainWindow):
    def __init__(self, parent: "QMainWindow"):
        super().__init__()
        # 변수 초기화
        self.parent: "QMainWindow" = parent

        self.InstanceName = ""
        self.InstancePort = 0
        self.sleepTime = 0.5

        # 객체 초기화
        self.vbox = QVBoxLayout()  # --------------------------------

        self.hbox1 = QHBoxLayout()
        self.InstanceComboBox = QComboBox()
        self.InstanceRefreshButton = QPushButton("새로고침", self)
        self.hbox1.addWidget(self.InstanceComboBox, stretch=2)
        self.hbox1.addWidget(self.InstanceRefreshButton, stretch=1)

        self.hbox2 = QHBoxLayout()
        self.startButton = QPushButton("시작", self)
        self.hbox2.addWidget(self.startButton)
        self.stopButton = QPushButton("정지", self)
        self.hbox2.addWidget(self.stopButton)
        self.resetButton = QPushButton("초기화", self)
        self.hbox2.addWidget(self.resetButton)
        self.isDoneTutorialCheckBox = QCheckBox("튜토리얼 스킵 여부", self)
        self.isDoneTutorialCheckBox.setChecked(True)
        self.hbox2.addWidget(self.isDoneTutorialCheckBox)
        self.isMissionCheckBox = QCheckBox("미션 수령", self)
        self.isMissionCheckBox.setChecked(False)
        self.hbox2.addWidget(self.isMissionCheckBox)
        self.isSSRGachaCheckBox = QCheckBox("SSR 확정권 사용", self)
        self.isSSRGachaCheckBox.setChecked(False)
        self.hbox2.addWidget(self.isSSRGachaCheckBox)
        self.clearLogsButton = QPushButton("로그 삭제", self)
        self.hbox2.addWidget(self.clearLogsButton)

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.logs = QTextBrowser()
        self.vbox.addWidget(self.logs)

        self.tab = QWidget()
        self.tab.setLayout(self.vbox)  # ------------------------------

        # 우마무스메
        self.umamusume = Umamusume(self)

        # 함수 초기화 (일회성 실행)
        self.InstanceFunction()
        self.InstanceRefreshFunction()

        # 시그널 정의
        self.InstanceComboBox.currentIndexChanged.connect(self.InstanceFunction)
        self.InstanceRefreshButton.clicked.connect(self.InstanceRefreshFunction)

        self.startButton.clicked.connect(self.startButtonFunction)
        self.stopButton.clicked.connect(self.stopButtonFunction)
        self.resetButton.clicked.connect(self.resetButtonFunction)
        self.isDoneTutorialCheckBox.clicked.connect(self.isDoneTutorialCheckBoxFunction)
        self.isSSRGachaCheckBox.clicked.connect(self.isSSRGachaCheckBoxFunction)
        self.isMissionCheckBox.clicked.connect(self.isMissionCheckBoxFunction)
        self.clearLogsButton.clicked.connect(self.logs.clear)

        # 커스텀 시그널 정의
        # 없음

    @pyqtSlot(str)
    def recvLog(self, text):
        self.logs.append(text)

    # events
    def InstanceFunction(self):
        if self.InstanceComboBox.count() == 0:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.resetButton.setEnabled(False)
            self.isDoneTutorialCheckBox.setEnabled(False)
            self.isMissionCheckBox.setEnabled(False)
            self.isSSRGachaCheckBox.setEnabled(False)
            return

        self.logs.append("-" * 50)
        if self.InstanceComboBox.currentText() == "선택 안함":
            self.logs.append("선택해주세요")

            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(False)
            self.resetButton.setEnabled(False)
            self.isDoneTutorialCheckBox.setEnabled(False)
            self.isMissionCheckBox.setEnabled(False)
            self.isSSRGachaCheckBox.setEnabled(False)

        else:
            self.SelectedInstance = self.InstanceComboBox.currentText()
            self.SelectedInstance = self.SelectedInstance.split(",")
            self.SelectedInstance[0] = self.SelectedInstance[0].replace('"', "")
            self.SelectedInstance[1] = self.SelectedInstance[1].strip()
            self.InstanceName, self.InstancePort = self.SelectedInstance

            self.InstancePort = int(self.InstancePort)
            self.logs.append(
                str(self.InstanceName)
                + " 윈도우, "
                + str(self.InstancePort)
                + "번 포트가 선택되었습니다."
            )

            self.umamusume = Umamusume(self)

            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(False)
            self.resetButton.setEnabled(True)
            self.isDoneTutorialCheckBox.setEnabled(True)
            self.isMissionCheckBox.setEnabled(True)
            self.isSSRGachaCheckBox.setEnabled(True)

        self.logs.append("-" * 50)

    def InstanceRefreshFunction(self):
        self.InstanceComboBox.clear()

        lines = ["선택 안함"]
        try:
            file = "./Instances.txt"
            f = open(file, "r", encoding="UTF-8")
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
                lines.append(line)
            f.close()
            self.InstanceComboBox.addItems(lines)
            self.logs.append("불러오기 성공")
        except Exception:
            self.logs.append("불러올 수 없습니다. Instance.txt 파일을 다시 확인해주세요")
            pass

    def startButtonFunction(self):
        self.startButton.setEnabled(False)

        self.logs.append("-" * 50)
        self.logs.append("시작!!")
        self.umamusume.start()
        self.lockButtonFunction()
        self.logs.append("-" * 50)

    def lockButtonFunction(self):
        # 시작 후 버튼 잠금
        self.InstanceComboBox.setEnabled(False)
        self.InstanceRefreshButton.setEnabled(False)

        self.stopButton.setEnabled(True)
        self.resetButton.setEnabled(False)
        self.isDoneTutorialCheckBox.setEnabled(False)
        self.isMissionCheckBox.setEnabled(False)
        self.isSSRGachaCheckBox.setEnabled(False)

    def stopButtonFunction(self):
        self.stopButton.setEnabled(False)
        self.logs.append("-" * 50)
        self.logs.append("정지 중!!")
        self.umamusume.terminate()
        self.logs.append("-" * 50)

    def restoreButtonFunction(self):
        # 종료 후 버튼 복구
        self.InstanceComboBox.setEnabled(True)
        self.InstanceRefreshButton.setEnabled(True)

        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.resetButton.setEnabled(True)
        self.isDoneTutorialCheckBox.setEnabled(True)
        self.isMissionCheckBox.setEnabled(True)
        self.isSSRGachaCheckBox.setEnabled(True)

    def resetButtonFunction(self):
        self.resetButton.setEnabled(False)
        self.logs.append("-" * 50)
        self.logs.append("초기화!!")
        self.logs.append("-" * 50)
        try:
            path = "./Saved_Data/" + str(self.InstancePort) + ".uma"
            os.remove(path)
        except Exception:
            pass

    def isDoneTutorialCheckBoxFunction(self):
        self.logs.append("-" * 50)
        if self.isDoneTutorialCheckBox.isChecked():
            self.logs.append("튜토리얼 스킵 활성화!!")
        else:
            self.logs.append("튜토리얼 진행 (다소 렉 유발)")
        self.logs.append("-" * 50)

    def isMissionCheckBoxFunction(self):
        self.logs.append("-" * 50)
        if self.isMissionCheckBox.isChecked():
            self.logs.append("미션 수령!!")
        else:
            self.logs.append("미션 수령 안함!!")
        self.logs.append("-" * 50)

    def isSSRGachaCheckBoxFunction(self):
        self.logs.append("-" * 50)
        if self.isSSRGachaCheckBox.isChecked():
            self.logs.append("SSR 확정권 사용!!")
        else:
            self.logs.append("SSR 확정권 사용안함!!")
        self.logs.append("-" * 50)
