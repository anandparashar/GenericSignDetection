import numpy as np
import cv2
from matplotlib import pyplot as plt
import os


def calcHist(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist(image, [0], None, [256], [0,256])
    # hist = cv2.normalize(hist, hist).flatten()
    # hist, bins = np.histogram(image.ravel(), 256, [0, 256])
    # print hist.shape
    # hist = cv2.GaussianBlur(hist, (3, 3), 1.25)
    # print hist

    # ret, hist = cv2.threshold(hist, 100, 255, cv2.THRESH_BINARY)

    # plt.plot(hist)
    # plt.xlim([0, 256])
    # plt.show()
    # plt.hist(image.ravel(),256,[0,256]); plt.show()
    return hist


def calcHistDistance(hist1, hist2):
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)


def calcDistance(image1, image2):
    return calcHistDistance(calcHist(image1), calcHist(image2))


def checksign(image):
    path = "./hist_match_candidates/"
    filelist = os.listdir("./hist_match_candidates/")
    for file in filelist:
        image1 = cv2.imread(path+file)
        if(calcDistance(image1, image) >0.7):
            return True
    return False



# print checksign(cv2.imread("D:/Study/CS-682ComputerVision/GenericSignDetection/GenericSignDetection/hist_match_candidates/10.jpg"))


#
# hist1 = calcHist(cv2.imread("D:/Study/CS-682ComputerVision/GenericSignDetection/GenericSignDetection/hist_match_candidates/1.jpg"))
# hist2 = calcHist(cv2.imread("D:/Study/CS-682ComputerVision/GenericSignDetection/GenericSignDetection/hist_match_candidates/10.jpg"))
#
# # zipped = zip(hist1, hist2)
# # print zipped
# # d=0
# eps = 1e-10
# # for (a, b) in zipped:
# #    d += ((a - b) ** 2)/(a + b + eps)
# #
# # d = 0.5 * d
# # print d
#
# # d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(hist1, hist2)])
#
# d = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
#
# print d
#
# # checksign()