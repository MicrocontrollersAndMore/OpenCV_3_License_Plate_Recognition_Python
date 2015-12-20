# DetectChars.py

import cv2
import numpy as np
import math

# module level variables ##########################################################################

kNearest = cv2.ml.KNearest_create()

        # constants for checkIfPossibleChar, this checks one possible char only (does not compare to another char)
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

        # constants for comparing two chars
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

        # other constants
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100

###################################################################################################
def loadKNNDataAndTrainKNN():




    return True
# end function

###################################################################################################
def detectCharsInPlates(listOfPossiblePlates):




    return listOfPossiblePlates
# end function

###################################################################################################
def findPossibleCharsInPlate(imgGrayscale, imgThresh):

    listOfPossibleChars = []



    return listOfPossibleChars
# end function

###################################################################################################
def checkIfPossibleChar(possibleChar):



    return True
# end function

###################################################################################################
def findListOfListsOfMatchingChars(listOfPossibleChars):

    listOfListOfMatchingChars = []


    return listOfListOfMatchingChars
# end function

###################################################################################################
def findListOfMatchingChars(possibleChar, listOfChars):

    listOfMatchingChars = []



    return listOfMatchingChars
# end function

###################################################################################################
def distanceBetweenChars(firstChar, secondChar):

    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))
# end function

###################################################################################################
def angleBetweenChars(firstChar, secondChar):

    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    fltAngleInRad = math.atan(fltOpp / fltAdj)

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)

    return fltAngleInDeg
# end function

###################################################################################################
def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = []



    return listOfMatchingCharsWithInnerCharRemoved
# end function

###################################################################################################
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = ""





    return strChars
# end function








