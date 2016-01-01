# Main.py

import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate
import Point

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = True

###################################################################################################
def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()

    if blnKNNTrainingSuccessful == False:
        print "\n\nerror: KNN traning was not successful\n\n"
        return
    # end if

    imgOriginalScene  = cv2.imread("1.png")               # open image

    if imgOriginalScene is None:                             # if image was not read successfully
        print "\nerror: image not read from file \n\n"      # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit function (which exits program)

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:
        print "\nno license plates were detected\n"
    else:
                # if we get in here vector of possible plates has at leat one plate

                # sort the vector of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reversed = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:
            print "\nno characters were detected\n\n"
            return
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)

        print "\nlicense plate read from image = " + licPlate.strChars + "\n"
        print "----------------------------------------"

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)

        cv2.imshow("imgOriginalScene", imgOriginalScene)

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

    # end if else

    cv2.waitKey(0)					# hold windows open until user presses a key

    return
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    cv2.boxPoints(licPlate.rrLocationOfPlateInScene, p2fRectPoints)

    cv2.line(imgOriginalScene, p2fRectPoints[0], p2fRectPoints[1], SCALAR_RED, 2)
    cv2.line(imgOriginalScene, p2fRectPoints[1], p2fRectPoints[2], SCALAR_RED, 2)
    cv2.line(imgOriginalScene, p2fRectPoints[2], p2fRectPoints[3], SCALAR_RED, 2)
    cv2.line(imgOriginalScene, p2fRectPoints[3], p2fRectPoints[4], SCALAR_RED, 2)
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextArea = Point.Point()
    ptLowerLeftTextOrigin = Point.Point()

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    dblFontScale = float(licPlate.imgPlate.rows) / 30.0
    intFontThickness = int(round(dblFontScale * 1.5))
    intBaseline = 0

    textSize = cv2.getTextSize(licPlate.strChars, intFontFace, dblFontScale, intFontThickness)

    ptCenterOfTextArea = Point.Point()

    ptCenterOfTextArea.x = int(licPlate.rrLocationOfPlateInScene.center.x)

    if licPlate.rrLocationOfPlateInScene.center.y < (imgOriginalScene.rows * 0.75):
        ptCenterOfTextArea.y = int(round(licPlate.rrLocationOfPlateInScene.center.y)) + int(round(licPlate.imgPlate.rows * 1.6))
    else:
        ptCenterOfTextArea.y = int(round(licPlate.rrLocationOfPlateInScene.center.y)) - int(round(licPlate.imgPlate.rows * 1.6))
    # end if

    ptLowerLeftTextOrigin.x = int(ptCenterOfTextArea.x - (textSize.width / 2))
    ptLowerLeftTextOrigin.y = int(ptCenterOfTextArea.y + (textSize.height / 2))

    cv2.putText(imgOriginalScene, licPlate.strChars, ptLowerLeftTextOrigin, intFontFace, dblFontScale, SCALAR_YELLOW, intFontThickness)
# end function

###################################################################################################
if __name__ == "__main__":
    main()


















