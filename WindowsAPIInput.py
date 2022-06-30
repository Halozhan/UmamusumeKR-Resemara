import win32api
import win32con
import win32gui
import time

def GetHwnd(windowName):
    hwnd = win32gui.FindWindow(None, windowName) # 윈도우 이름으로 hwnd 찾기
    return hwnd


def SetWindowSize(hwnd, width, height):
    rect = win32gui.GetWindowRect(hwnd) # 창 크기 받기
    if rect[2] == width and rect[3] == height: # 창 크기가 똑같은지
        win32gui.MoveWindow(hwnd, rect[0], rect[1], width, height, True) # 창 크기 변경
        return True
    else:
        return False


def WindowsAPIKeyboardInput(hwnd, contents):
    hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD) # hwnd의 하위

    for char in contents: # 입력할 내용
        win32api.PostMessage(hwndChild, win32con.WM_CHAR, ord(char), 0)


def WindowsAPIMouseClick(hwnd, x, y):
    
    # hwndChild = win32gui.FindWindowEx(hwndMain, None, "HD-Player", None)
    hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD) # hwnd의 하위
    # hwndChild = win32gui.FindWindowEx(hwndMain, None, None, None)
    print(hwndChild)
    
    position = win32api.MAKELONG(x, y)
    win32gui.PostMessage(hwndChild, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, position)
    win32gui.PostMessage(hwndChild, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, position)


if __name__ == "__main__":
    hwndMain = GetHwnd("BlueStacks Dev")
    
    SetWindowSize(hwndMain, 574, 994)
    # WindowsAPIMouseClick(hwndMain, 250, 250)
    WindowsAPIKeyboardInput(hwndMain, "입력할 내용")