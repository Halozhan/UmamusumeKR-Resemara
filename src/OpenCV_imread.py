import numpy as np
import cv2


def imreadUnicode(file):
    npFile = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npFile, cv2.IMREAD_UNCHANGED)  # img = array
    return img


# reference: https://kst1.tistory.com/39
