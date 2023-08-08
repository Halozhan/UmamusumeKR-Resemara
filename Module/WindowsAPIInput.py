import win32api
import win32con
import win32gui


def GetHwnd(windowName):
    try:
        hwnd = win32gui.FindWindow(None, windowName)  # 윈도우 이름으로 hwnd 찾기
        return hwnd
    except:
        pass


def SetWindowSize(hwnd, width, height):
    try:
        rect = win32gui.GetWindowRect(hwnd)  # 창 크기 받기
        if rect[2] == width and rect[3] == height:  # 창 크기가 똑같은지
            return False
        else:
            win32gui.MoveWindow(hwnd, rect[0], rect[1], width, height, True)  # 창 크기 변경
            return True
    except:
        return False


def WindowsAPIKeyboardInput(hwnd, key):
    try:
        hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)  # hwnd의 하위

        win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, key, 0)
        win32api.PostMessage(hwndChild, win32con.WM_KEYUP, key, 0)
    except:
        pass


def WindowsAPIKeyboardInputString(hwnd, contents):
    try:
        hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)  # hwnd의 하위

        for char in contents:  # 입력할 내용
            win32api.PostMessage(hwndChild, win32con.WM_CHAR, ord(char), 0)
    except:
        pass


def WindowsAPIMouseClick(hwnd, x, y):  # 미구현
    try:
        # hwndChild = win32gui.FindWindowEx(hwndMain, None, "HD-Player", None)
        hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)  # hwnd의 하위
        # hwndChild = win32gui.FindWindowEx(hwndMain, None, None, None)
        print(hwndChild)

        position = win32api.MAKELONG(x, y)
        win32gui.PostMessage(hwndChild, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, position)
        win32gui.PostMessage(hwndChild, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, position)
    except:
        pass


if __name__ == "__main__":
    hwndMain = GetHwnd("BlueStacks Dev")

    SetWindowSize(hwndMain, 574, 994)
    # WindowsAPIMouseClick(hwndMain, 250, 250)
    WindowsAPIKeyboardInputString(hwndMain, "입력할 내용")
