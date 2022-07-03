import win32gui
import win32ui
from ctypes import windll
from PIL import Image

def screenshot(hwnd, isExport):
    
    # Change the line below depending on whether you want the whole window
    # or just the client area.    
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top
    
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    
    saveDC.SelectObject(saveBitMap)
    
    # Change the line below depending on whether you want the whole window
    # or just the client area. 0, 1, 2, 3 원하는 이미지 찾아 시도해볼 것
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    
    if result == 1:
        # PrintWindow Succeeded
        if isExport:
            im.save("test.png") # 이미지 파일로 내보내기
        
        return im
    else:
        return False
    
    
if __name__ == "__main__": # 이미지 추출 테스트
    hwndMain = win32gui.FindWindow(None, "Bluestacks Dev")
    screenshot(hwndMain, True)