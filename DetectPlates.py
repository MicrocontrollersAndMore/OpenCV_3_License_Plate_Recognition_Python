# DetectPlates.py

import cv2
import numpy as np
import math
import Main
import random

# module level variables ##########################################################################
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5

###################################################################################################
def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []                   # this will be the return value

    height, width, numChannels = imgOriginal.shape

    imgGrayscaleScene = np.zeros((height, width, 1), np.uint8)
    imgThreshScene = np.zeros((height, width, 1), np.uint8)
    imgContours = np.zeros((height, width, 3), np.uint8)

    cv2.destroyAllWindows()

    if Main.showSteps == True:
        cv2.imshow("0", imgOriginalScene)
    # end if

    Preprocess.preprocess(imgOriginalScene, imgGrayscaleScene, imgThreshScene)

    if Main.showSteps == True:
        cv2.imshow("1a", imgGrayscaleScene)
        cv2.imshow("1b", imgThreshScene)
    # end if

    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)

    if Main.showSteps == True:
        print "step 2 - listOfPossibleCharsInScene.Count = " + str(listOfPossibleCharsInScene.len()) + "\n"

        imgContours = np.zeros((height, width, 3), np.uint8)

        contours = []

        for possibleChar in listOfPossibleCharsInScene:
            contours.append(possibleChar)
        # end for

        cv2.drawContours(imgContours, contours, -1, Main.SCALAR_WHITE)
        cv2.imshow("2b", imgContours)
    # end if

    listOfListsOfMatchingCharsInScene = findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    if Main.showSteps == True:
        print "step 3 - listOfListsOfMatchingCharsInScene.Count = " + str(len(listOfListsOfMatchingCharsInScene)) + "\n"    # 13 with MCLRNF1 image

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
    # end if

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)

        if possiblePlate.imgPlate.empty() == False:
            listOfPossiblePlates.append(possiblePlate)
        # end if
    # end for

    print "\n" + len(listOfPossiblePlates) + " possible plates found\n"

    if Main.showSteps == True:
        print "\n"
        cv2.imshow("4a", imgContours)

        for i in range(0, len(listOfPossiblePlates)):
            p2fRectPoints = []

            listOfPossiblePlates[i].rrLocationOfPlateInScene.points(p2fRectPoints)

            cv2.line(imgContours, p2fRectPoints[0], p2fRectPoints[1], Main.SCALAR_RED, 2)
            cv2.line(imgContours, p2fRectPoints[1], p2fRectPoints[2], Main.SCALAR_RED, 2)
            cv2.line(imgContours, p2fRectPoints[2], p2fRectPoints[3], Main.SCALAR_RED, 2)
            cv2.line(imgContours, p2fRectPoints[3], p2fRectPoints[4], Main.SCALAR_RED, 2)

            cv2.imshow("4a", imgContours)

            print "possible plate " + str(i) + ", click on any image and press a key to continue . . .\n"

            cv2.imshow("4b", vectorOfPossiblePlates[i].imgPlate)
            cv2.waitKey(0)
        # end for

        print "\nplate detection complete, click on any image and press a key to begin char recognition . . .\n\n"
        cv2.waitKey(0)
    # end if

    return listOfPossiblePlates
# end function

###################################################################################################
def findPossibleCharsInScene(imgThresh):

    listOfPossibleChars



    return listOfPossibleChars
# end function


###################################################################################################
def extractPlate(imgOriginal, listOfMatchingChars):

    possiblePlate = PossiblePlate()


    return possiblePlate
# end function








