# Main.py

import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

###################################################################################################
def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()

    if blnKNNTrainingSuccessful:
        print "\n\nerror: error: KNN traning was not successful\n\n"
        return
    # end if

    imgOriginalScene  = cv2.imread("1.png")               # open image

    if imgOriginal is None:                             # if image was not read successfully
        print "\nerror: image not read from file \n\n"      # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit function (which exits program)

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if listOfPossiblePlates.empty():
        print "\nno license plates were detected\n"
    else:
                # if we get in here vector of possible plates has at leat one plate

                # sort the vector of possible plates in DESCENDING order (most number of chars to least number of chars)


        # left off here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




        pass
    # end if else




    return
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    pass
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    pass
# end function

###################################################################################################
if __name__ == "__main__":
    main()





