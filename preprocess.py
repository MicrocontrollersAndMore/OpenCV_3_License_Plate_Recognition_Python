# preprocess.py

import cv2.cv as cv
import cv2

# module variables ################################################################################
SMOOTH_FILTER_SIZE = 5
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

###################################################################################################
def preprocess(imgOriginal):
    tupSize = cv.GetSize(imgOriginal)

    imgValueGrayscale = extractValue(imgOriginal)

    imgMaxContrastGrayscale = maximizeContrast(imgValueGrayscale)                                       # maximise contrast

    # cv.ShowImage("imgMaxContrastGrayscale", imgMaxContrastGrayscale)
    # cv.WaitKey()

    # imgGrayscale = cv.CreateImage((imgOriginal.width, imgOriginal.height), cv.IPL_DEPTH_8U, 1)
    # cv.CvtColor(imgOriginal, imgGrayscale, cv.CV_RGB2GRAY)
    # imgMaxContrastGrayscale = imgGrayscale

    imgBlur = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)                 # a bit of smoothing to reduce noise
    cv.Smooth(imgMaxContrastGrayscale, imgBlur, cv.CV_GAUSSIAN, SMOOTH_FILTER_SIZE)

    imgThresh = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)

    cv.AdaptiveThreshold(imgBlur, imgThresh, 255, cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    return imgValueGrayscale, imgThresh
# end func

###################################################################################################
def extractValue(imgOriginal):                           # convert an RGB image to HSV and extract the V component
    tupSize = cv.GetSize(imgOriginal)

    imgHueSatVal = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 3)
    imgValue = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)

    cv.CvtColor(imgOriginal, imgHueSatVal, cv.CV_RGB2HSV)   # convert to HSV
    cv.SetImageCOI(imgHueSatVal, 3)                         # set channel of interest to 3rd channel (value)
    cv.Copy(imgHueSatVal, imgValue)                         # get value

    # imgHue = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)
    # imgSat = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)
    #
    # cv.SetImageCOI(imgHueSatVal, 1)
    # cv.Copy(imgHueSatVal, imgHue)
    #
    # cv.SetImageCOI(imgHueSatVal, 2)
    # cv.Copy(imgHueSatVal, imgSat)
    #
    # cv.ShowImage("imgOriginal", imgOriginal)
    # cv.ShowImage("imgHueSatVal", imgHueSatVal)
    # cv.ShowImage("imgHue", imgHue)
    # cv.ShowImage("imgSat", imgSat)
    # cv.ShowImage("imgValue", imgValue)
    #
    # imgGrayscale = cv.CreateImage((imgOriginal.width, imgOriginal.height), cv.IPL_DEPTH_8U, 1)
    # cv.CvtColor(imgOriginal, imgGrayscale, cv.CV_RGB2GRAY)
    #
    # cv.ShowImage("imgGrayscale", imgGrayscale)
    # cv.ShowImage("imgValue", imgValue)
    #
    # cv.WaitKey()

    return imgValue
# end func

###################################################################################################
def maximizeContrast(imgGrayscale):                        # maximise the contrast of an image using top hat and black hat filters
    tupSize = cv.GetSize(imgGrayscale)

    imgTopHat = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)         # declare 4 images
    imgBlackHat = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)       #
    imgGrayscalePlusTopHat = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)                #
    imgGrayscalePlusTopHatMinusBlackHat = cv.CreateImage(tupSize, cv.IPL_DEPTH_8U, 1)                #

    structuringElement = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_ELLIPSE)

    cv.MorphologyEx(imgGrayscale, imgTopHat, None, structuringElement, cv.CV_MOP_TOPHAT, 1)
    cv.MorphologyEx(imgGrayscale, imgBlackHat, None, structuringElement, cv.CV_MOP_BLACKHAT, 1)

    cv.Add(imgGrayscale, imgTopHat, imgGrayscalePlusTopHat)
    cv.Sub(imgGrayscalePlusTopHat, imgBlackHat, imgGrayscalePlusTopHatMinusBlackHat)
    
    # cv.ShowImage("imgGrayscale", imgGrayscale)
    # cv.ShowImage("imgBlackHat", imgBlackHat)
    # cv.ShowImage("imgTopHat", imgTopHat)
    # cv.ShowImage("imgGrayscalePlusTopHat", imgGrayscalePlusTopHat)
    # cv.ShowImage("imgGrayscalePlusTopHatMinusBlackHat", imgGrayscalePlusTopHatMinusBlackHat)
    #
    # cv.WaitKey()

    return imgGrayscalePlusTopHatMinusBlackHat
# end func








