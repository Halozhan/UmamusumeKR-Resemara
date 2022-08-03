import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 관리자 권한 필요함
if __name__ == "__main__":
    install("pywin32")
    install("opencv-python")
    install("selenium")
    install("webdriver_manager")
    # install("chromedriver_autoinstaller") 구버전, Deprecated
    install("pyautogui")
    install("pure-python-adb")
    install("pyqt5")
    install("psutil")
    install("pillow==9.0.1")
    install("regex")
    # install("wmi")
    # install("pywinauto")
    # install("pyinstaller")