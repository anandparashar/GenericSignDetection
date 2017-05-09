import numpy as np
import cv2

def clean(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    vmask = np.tile([[0, 0], [1, 0]], (gray.shape[0] / 2, gray.shape[1] / 2))

    noise = np.ma.array(gray, mask=vmask)

    filterKern = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) * (1.0 / 8.0)

    mfiltered = cv2.filter2D(gray, 0, filterKern).astype(np.uint8)

    mmasked = np.ma.array(mfiltered, mask=np.logical_not(vmask))

    cleaned = mmasked.filled(0) + noise.filled(0)

    #cv2.imshow('Cleaned', cleaned)
    return cleaned