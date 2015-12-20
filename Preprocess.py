# Preprocess.py

import cv2
import numpy as np
import math

# module level variables ##########################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

###################################################################################################
def preprocess(imgOriginal, imgGrayscale, imgThresh):
    imgGrayscale = extractValue(imgOriginal)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

    height, width = imgGrayscale.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)

    cv2.GaussianBlur(imgMaxContrastGrayscale, imgBlurred, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    cv2.adaptiveThreshold(imgBlurred, imgThresh, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
# end function

###################################################################################################
def extractValue(imgOriginal):

    height, width, numChannels = imgOriginal.shape

    imgHSV = np.zeros((height, width, 3), np.uint8)

    cv2.cvtColor(imgOriginal, imgHSV, cv2.COLOR_BGR2HSV)

    imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

    return imgValue
# end function

###################################################################################################
def maximizeContrast(imgGrayscale):

    height, width = imgGrayscale.shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    cv2.morphologyEx(imgGrayscale, imgTopHat, cv2.MORPH_TOPHAT, structuringElement)
    cv2.morphologyEx(imgGrayscale, imgBlackHat, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = imgGrayscale + imgTopHat
    imgGrayscalePlusTopHatMinusBlackHat = imgGrayscalePlusTopHat - imgBlackHat

    return imgGrayscalePlusTopHatMinusBlackHat
# end function










