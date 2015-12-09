# detect.py

import cv2.cv as cv
import cv2

import math
import os

import preprocess
import possible_char

# module variables ################################################################################
MAX_CHAR_DIST_FACTOR = 1.5
MAX_CHAR_GRADIENT_DIFF = 0.1
MIN_NUMBER_OF_MATCHING_CHARS = 3

###################################################################################################
def detectPlates(imgOriginal):

    # cv.ShowImage("image", image)

    imgGrayscale, imgThresh = preprocess.preprocess(imgOriginal)

    # cv.ShowImage("imgGrayscale", imgGrayscale)
    # cv.ShowImage("imgThresh", imgThresh)
    # cv.WaitKey()

    # ------------------------------------------------------------------

    listOfPossibleChars = findPossibleChars(imgGrayscale, imgThresh)

    # print "len of listOfPossibleChars = " + str(len(listOfPossibleChars))     # 246

    # for possibleChar in listOfPossibleChars:
    #     imageToDrawContourOn = cv.CreateImage(cv.GetSize(imgGrayscale), cv.IPL_DEPTH_8U, 1)
    #     cv.DrawContours(imageToDrawContourOn, possibleChar.contour, 255, 255, 1000, 2)
    #     cv.ShowImage("imageToDrawContourOn", imageToDrawContourOn)
    #     cv.WaitKey()
    # # end for

    # imageToDrawContourOn = cv.CreateImage(cv.GetSize(imgGrayscale), cv.IPL_DEPTH_8U, 1)
    #
    # for possibleChar in listOfPossibleChars:
    #     cv.DrawContours(imageToDrawContourOn, possibleChar.contour, 255, 255, 1000, 1)
    # # end for
    #
    # cv.ShowImage("imageToDrawContourOn", imageToDrawContourOn)
    # cv.WaitKey()

    # ------------------------------------------------------------------

    listOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleChars)

    # print "len of listOfListsOfMatchingChars = " + str(len(listOfListsOfMatchingChars))

    # ------------------------------------------------------------------

    imgListOfPlates = []

    for listOfListsOfMatchingChars in listOfListsOfMatchingChars:
        imgPlate = extractPlate(imgOriginal, listOfListsOfMatchingChars)
        if imgPlate is not None:
            imgListOfPlates.append(imgPlate)
        # end if
    # end for

    # debugCount = 0
    # for plate in listOfPlates:
    #     cv.ShowImage("plate" + str(debugCount), plate)
    #     debugCount = debugCount + 1
    # # end for
    #
    # cv.WaitKey()

    return imgListOfPlates
# end func

###################################################################################################
def findPossibleChars(imgGrayscale, imgThresh):

    # cv.ShowImage("gray", gray)
    # cv.WaitKey()

    storage = cv.CreateMemStorage()
    #contours = cv.FindContours(bw, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_NONE)
    #contours = cv.FindContours(bw, storage, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)
    contours = cv.FindContours(imgThresh, storage, cv.CV_RETR_LIST, cv.CV_CHAIN_APPROX_SIMPLE)

    # while contours is not None:
    #
    #     arcLength = cv.ArcLength(contours)
    #     print "arcLength = " + str(arcLength)
    #     contour = cv.ApproxPoly(contours, storage, cv.CV_POLY_APPROX_DP, arcLength * 0.02)
    #
    #     imageToDrawContourOn = cv.CreateImage(cv.GetSize(gray), cv.IPL_DEPTH_8U, 1)
    #     cv.DrawContours(imageToDrawContourOn, contour, 255, 255, 1000, 2)
    #     cv.ShowImage("imageToDrawContourOn", imageToDrawContourOn)
    #     print "---"
    #     cv.WaitKey()
    #     contours = contours.h_next()
    # # end while
    #
    # contours = cv.FindContours(bw, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_NONE)

    listOfPossibleChars = []

    countOfPossibleChars = 0
    countOfValidPossibleChars = 0

    while contours is not None:

        countOfPossibleChars = countOfPossibleChars + 1

        possibleChar = possible_char.PossibleChar(contours)           # declare a PossibleChar, call constructor

        if possibleChar.checkIfValid():

            countOfValidPossibleChars = countOfValidPossibleChars + 1

            possibleChar.calcAvgAndStdDev(imgGrayscale)

            listOfPossibleChars.append(possibleChar)
            # print "--------------------------------------------------------------"
            # print "possibleChar.intCenterX = " + str(possibleChar.intCenterX)
            # print "possibleChar.intCenterY = " + str(possibleChar.intCenterY)
            # imageToDrawContourOn = cv.CreateImage(cv.GetSize(gray), cv.IPL_DEPTH_8U, 1)
            # cv.DrawContours(imageToDrawContourOn, possibleChar.contour, 255, 255, 1000, 2)
            # cv.ShowImage("imageToDrawContourOn", imageToDrawContourOn)
            # cv.WaitKey()

        # end if
        contours = contours.h_next()
    # end while

    # print "countOfPossibleChars = " + str(countOfPossibleChars)                 # 2115
    # print "countOfValidPossibleChars = " + str(countOfValidPossibleChars)       # 246
    #
    # print "len of listOfPossibleChars = " + str(len(listOfPossibleChars))       # 246

    return listOfPossibleChars
# end func

###################################################################################################
def findListOfListsOfMatchingChars(listOfPossibleChars):

    # print "len of listOfPossibleChars = " + str(len(listOfPossibleChars))         # 246 first time in

    listOfListsOfMatchingChars = []

    for possibleChar in listOfPossibleChars:              # iterate over the set of contours, attempting to find the candidate that produces the largest setOfMatchingChars
        fltGradient = None                                     # line to fit the setOfMatchingChars to

        listOfPossibleMatchingChars = possibleChar.findListOfMatchingChars(listOfPossibleChars)         # get a list of contours that are similar to the candidate

        listOfMatchingChars = []                             # the listOfMatchingChars
        listOfMatchingChars.append(possibleChar)

        for otherPossibleChar in listOfPossibleMatchingChars:                         # iterate over each contour in the sorted list
            
            dists = []
            for possChar in listOfMatchingChars:
                dists.append(possChar.distanceTo(otherPossibleChar))
            # end for

            # print "------------"
            # print "len of dists = " + str(len(dists))

            if min(dists) < (otherPossibleChar.fltDiameter * MAX_CHAR_DIST_FACTOR):
                fltOtherGradient = possibleChar.gradientTo(otherPossibleChar)

                print "fltOtherGradient = " + str(fltOtherGradient)

                if fltGradient is None:
                    # print "in if"
                    fltGradient = fltOtherGradient
                elif abs(fltGradient - fltOtherGradient) < MAX_CHAR_GRADIENT_DIFF:
                    # print "in elif"
                    listOfMatchingChars.append(otherPossibleChar)
                # end else if

            # end if
        # end for

        if len(listOfMatchingChars) >= MIN_NUMBER_OF_MATCHING_CHARS:
            # print "in if"
            listOfListsOfMatchingChars.append(listOfMatchingChars)
        # end if
    # end for

    listOfListsOfMatchingChars.sort(key = lambda listOfPossibleChars: len(listOfPossibleChars))

    if len(listOfListsOfMatchingChars) > 0:
        bestListOfMatchingChars = listOfListsOfMatchingChars[-1]            # in the list of listOfListsOfMatchingChars, after sorting, the last listOfListsOfMatchingChars (the listOfListsOfMatchingChars with the most possible chars) is considered "best"

        for matchingChar in bestListOfMatchingChars:
            listOfPossibleChars.remove(matchingChar)
        # end for

        return [bestListOfMatchingChars] + findListOfListsOfMatchingChars(listOfPossibleChars)
    else:
        return []
    # end if
# end func

###################################################################################################
def extractPlate(imgOriginal, listOfMatchingChars):              # de-skew and extract a detected plate from an image
    # listOfMatchingChars = list(listOfMatchingChars)

    # cv.ShowImage("image", image)
    # cv2.waitKey()

    listOfMatchingChars.sort(key = lambda possibleChar: possibleChar.intCenterX)
    
    fltOpposite = float(listOfMatchingChars[-1].intCenterY - listOfMatchingChars[0].intCenterY)
    fltHypotenuse = float(listOfMatchingChars[0].distanceTo(listOfMatchingChars[-1]))

    # print "type of opp = " + str(type(fltOpposite))
    # print "type of hyp = " + str(type(fltHypotenuse))

    fltAngle = math.asin(fltOpposite / fltHypotenuse)

    # print "type of fltAngle = " + str(type(fltAngle))

    # print "fltOpposite = " + str(fltOpposite)           # 1.0
    # print "fltHypotenuse = " + str(fltHypotenuse)       # 124.004032193
    # print "fltAngle = " + str(fltAngle)                 # 0.00806434130677

    matrix = cv.CreateMat(2, 3, cv.CV_32FC1)

    fltCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[-1].intCenterX) / 2.0         # intCenterX, intCenterY is the center of the plate
    fltCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[-1].intCenterY) / 2.0

    # print "type of intCenterX = " + str(type(fltCenterX))
    # print "type of intCenterY = " + str(type(fltCenterY))

    # print "intCenterX = " + str(intCenterX)
    # print "intCenterY = " + str(intCenterY)

    cv.GetRotationMatrix2D((fltCenterX, fltCenterY), fltAngle * 180.0 / math.pi, 1, matrix)

    imgWarp = cv.CreateImage(cv.GetSize(imgOriginal), cv.IPL_DEPTH_8U, 3)

    cv.WarpAffine(imgOriginal, imgWarp, matrix)

    imgPlate = cv.CreateImage((int(fltHypotenuse + (listOfMatchingChars[0].fltDiameter * 3.0)), int(listOfMatchingChars[0].fltDiameter * 1.5)), cv.IPL_DEPTH_8U, 3)

    # cv.ShowImage("imgOriginal", imgOriginal)
    # cv.ShowImage("imgWarp", imgWarp)
    # cv.ShowImage("imgPlate", imgPlate)
    # cv.WaitKey()

    cv.GetRectSubPix(imgWarp, imgPlate, (fltCenterX, fltCenterY))

    # cv.ShowImage("imgOriginal", imgOriginal)
    # cv.ShowImage("imgWarp", imgWarp)
    # cv.ShowImage("imgPlate", imgPlate)
    # cv.WaitKey()

    # imgBiggerPlate = cv.CreateImage((imgPlate.width * 2, imgPlate.height * 2), cv.IPL_DEPTH_8U, 3)

    # cv.Resize(imgPlate, imgBiggerPlate)

    return imgPlate
# end func












