import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# install("wmi")
# install("pyautogui")
# install("psutil")
# install("pywin32")
# install("pywinauto")
# install("opencv-python")
# install("pillow")
# install("pyinstaller")
# 관리자 권한 필요함