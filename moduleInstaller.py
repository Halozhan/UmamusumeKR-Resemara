import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 관리자 권한 필요함
if __name__ == "__main__":
    install("pywin32")
    install("opencv-python")
    install("selenium")
    install("chromedriver_autoinstaller")
    install("pyautogui")
    install("pure-python-adb")
    install("pyqt5")
    install("psutil")
    install("pillow")
    install("regex")
    # install("wmi")
    # install("pywinauto")
    # install("pyinstaller")