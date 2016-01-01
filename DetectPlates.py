# DetectPlates.py

import cv2
import numpy as np
import math
import Main
import random

import Preprocess
import DetectChars
import PossiblePlate
import PossibleChar
import Point

# module level variables ##########################################################################
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5

###################################################################################################
def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginalScene.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True: # show steps -------------------------------------------------------
        cv2.imshow("0", imgOriginalScene)
    # end if # show steps -------------------------------------------------------------------------

    imgGrayscaleScene, imgThreshScene = Preprocess.preprocess(imgOriginalScene)

    if Main.showSteps == True: # show steps -------------------------------------------------------
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)
    # end if # show steps -------------------------------------------------------------------------

    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    if Main.showSteps == True: # show steps -------------------------------------------------------
        print "step 2 - len(listOfPossibleCharsInScene) = " + str(len(listOfPossibleCharsInScene))         # 131 with MCLRNF1 image

        imgContours = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar.contour)
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("2b", imgContours)
    # end if # show steps -------------------------------------------------------------------------

    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    if Main.showSteps == True: # show steps -------------------------------------------------------
        print "step 3 - listOfListsOfMatchingCharsInScene.Count = " + str(len(listOfListsOfMatchingCharsInScene))    # 13 with MCLRNF1 image

        imgContours = np.zeros((height, width, 3), np.uint8)

        for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)

            contours = []

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
            # end for

            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
        # end for

        cv2.imshow("3", imgContours)
    # end if # show steps -------------------------------------------------------------------------

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)

        if possiblePlate.imgPlate is not None:
            listOfPossiblePlates.append(possiblePlate)
        # end if
    # end for

    print "\n" + str(len(listOfPossiblePlates)) + " possible plates found"          # 13 with MCLRNF1 image

    if Main.showSteps == True: # show steps -------------------------------------------------------
        print "\n"
        cv2.imshow("4a", imgContours)

        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = cv2.boxPoints(listOfPossiblePlates[i].rrLocationOfPlateInScene)

            cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), Main.SCALAR_RED, 2)
            cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)

            print "possible plate " + str(i) + ", click on any image and press a key to continue . . ."

            cv2.imshow("4b", listOfPossiblePlates[i].imgPlate)
            cv2.waitKey(0)
        # end for

        print "\nplate detection complete, click on any image and press a key to begin char recognition . . .\n"
        cv2.waitKey(0)
    # end if # show steps -------------------------------------------------------------------------

    return listOfPossiblePlates
# end function

###################################################################################################
def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []                # this will be the return value

    intCountOfPossibleChars = 0

    imgThreshCopy = imgThresh.copy()

    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    height, width = imgThresh.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    for i in range(0, len(contours)):

        if Main.showSteps == True: # show steps ###################################################
            cv2.drawContours(imgContours, contours, i, Main.SCALAR_WHITE)
        # end if # show steps #####################################################################

        possibleChar = PossibleChar.PossibleChar(contours[i])

        if DetectChars.checkIfPossibleChar(possibleChar):
            intCountOfPossibleChars = intCountOfPossibleChars + 1
            listOfPossibleChars.append(possibleChar)
        # end if
    # end for

    if Main.showSteps == True:
        print "\nstep 2 - len(contours) = " + str(len(contours))                       # 2362 with MCLRNF1 image
        print "step 2 - intCountOfPossibleChars = " + str(intCountOfPossibleChars)       # 131 with MCLRNF1 image
        cv2.imshow("2a", imgContours)
    # end if

    return listOfPossibleChars
# end function


###################################################################################################
def extractPlate(imgOriginal, listOfMatchingChars):
    possiblePlate = PossiblePlate.PossiblePlate()           # this will be the return value

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right

            # calculate the center point of the plate
    fltPlateCenterX = (listOfMatchingChars[0].intCenterX + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterX) / 2.0
    fltPlateCenterY = (listOfMatchingChars[0].intCenterY + listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY) / 2.0

    ptPlateCenter = Point.Point(fltPlateCenterX, fltPlateCenterY)

            # calculate plate width and height
    intPlateWidth = int((listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectX + listOfMatchingChars[len(listOfMatchingChars) - 1].intBoundingRectWidth - listOfMatchingChars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)

    intTotalOfCharHeights = 0

    for matchingChar in listOfMatchingChars:
        intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
    # end for

    fltAverageCharHeight = intTotalOfCharHeights / len(listOfMatchingChars)

    intPlateHeight = int(fltAverageCharHeight * PLATE_HEIGHT_PADDING_FACTOR)

            # calculate correction angle of plate region
    fltOpposite = listOfMatchingChars[len(listOfMatchingChars) - 1].intCenterY - listOfMatchingChars[0].intCenterY
    fltHypotenuse = DetectChars.distanceBetweenChars(listOfMatchingChars[0], listOfMatchingChars[len(listOfMatchingChars) - 1])
    fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
    fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

    ptTopLeftBeforeRotation = Point.Point(ptPlateCenter.x - (intPlateWidth / 2), ptPlateCenter.y - (intPlateHeight / 2))
    ptTopRightBeforeRotation = Point.Point(ptPlateCenter.x + (intPlateWidth / 2), ptPlateCenter.y - (intPlateHeight / 2))
    ptBottomLeftBeforeRotation = Point.Point(ptPlateCenter.x - (intPlateWidth / 2), ptPlateCenter.y + (intPlateHeight / 2))
    ptBottomRightBeforeRotation = Point.Point(ptPlateCenter.x + (intPlateWidth / 2), ptPlateCenter.y + (intPlateHeight / 2))

    ptTopLeft = Point.Point()

    ptTopLeft.x = (ptTopLeftBeforeRotation.x * math.cos(fltCorrectionAngleInRad)) - (ptTopLeftBeforeRotation.y * math.sin(fltCorrectionAngleInRad))
    ptTopLeft.y = (ptTopLeftBeforeRotation.x * math.sin(fltCorrectionAngleInRad)) + (ptTopLeftBeforeRotation.y * math.cos(fltCorrectionAngleInRad))

    ptTopRight = Point.Point()

    ptTopRight.x = (ptTopRightBeforeRotation.x * math.cos(fltCorrectionAngleInRad)) - (ptTopRightBeforeRotation.y * math.sin(fltCorrectionAngleInRad))
    ptTopRight.y = (ptTopRightBeforeRotation.x * math.sin(fltCorrectionAngleInRad)) + (ptTopRightBeforeRotation.y * math.cos(fltCorrectionAngleInRad))

    ptBottomLeft = Point.Point()

    ptBottomLeft.x = (ptBottomLeftBeforeRotation.x * math.cos(fltCorrectionAngleInRad)) - (ptBottomLeftBeforeRotation.y * math.sin(fltCorrectionAngleInRad))
    ptBottomLeft.y = (ptBottomLeftBeforeRotation.x * math.sin(fltCorrectionAngleInRad)) + (ptBottomLeftBeforeRotation.y * math.cos(fltCorrectionAngleInRad))

    ptBottomRight = Point.Point()

    ptBottomRight.x = (ptBottomRightBeforeRotation.x * math.cos(fltCorrectionAngleInRad)) - (ptBottomRightBeforeRotation.y * math.sin(fltCorrectionAngleInRad))
    ptBottomRight.y = (ptBottomRightBeforeRotation.x * math.sin(fltCorrectionAngleInRad)) + (ptBottomRightBeforeRotation.y * math.cos(fltCorrectionAngleInRad))

    #platePoints = [ np.array([ [ [ptTopLeft.x, ptTopLeft.y]], [[ptTopRight.x, ptTopRight.y]], [[ptBottomRight.x, ptBottomRight.y]], [[ptBottomLeft.x, ptBottomLeft.y] ] ]) ]

    #print platePoints

    #possiblePlate.rrLocationOfPlateInScene = cv2.minAreaRect(platePoints)

    possiblePlate.rrLocationOfPlateInScene = ( (ptPlateCenter.x, ptPlateCenter.y), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

    rotationMatrix = cv2.getRotationMatrix2D((ptPlateCenter.x, ptPlateCenter.y), fltCorrectionAngleInDeg, 1.0)

    height, width, numChannels = imgOriginal.shape

    imgRotated = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))

    imgCropped = cv2.getRectSubPix(imgRotated, (intPlateWidth, intPlateHeight), (ptPlateCenter.x, ptPlateCenter.y))

    possiblePlate.imgPlate = imgCropped

    # print "len(listOfMatchingChars) = " + str(len(listOfMatchingChars))
    # print "fltPlateCenterX = " + str(fltPlateCenterX)
    # print "fltPlateCenterY = " + str(fltPlateCenterY)
    # print "intPlateWidth = " + str(intPlateWidth)
    # print "intPlateHeight = " + str(intPlateHeight)
    #
    # print "possiblePlate.rrLocationOfPlateInScene = " + str(possiblePlate.rrLocationOfPlateInScene)
    # print "rotationMatrix = " + str(rotationMatrix)
    #
    # cv2.imshow("imgOriginal", imgOriginal)
    # cv2.imshow("imgRotated", imgRotated)
    # cv2.imshow("imgCropped", imgCropped)
    # cv2.imshow("possiblePlate.imgPlate", possiblePlate.imgPlate)
    #
    # cv2.waitKey(0)

    return possiblePlate
# end function












