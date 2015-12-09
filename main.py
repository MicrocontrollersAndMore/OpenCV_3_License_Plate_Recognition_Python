# main.py

import Tkinter as tk
import tkFileDialog
import tkFont

import cv2.cv as cv
import cv2

import os

import detect_plates
import preprocess

# module level variables ##########################################################################
frmMain = tk.Tk()                   # declare form
btnOpenFile = tk.Button(frmMain)      # declare button

previousChosenDirectory = "C:\OpenCV_pics\license_plate_scenes"

###################################################################################################
def main():
    frmMain.title("LPR")

    btnOpenFile.configure(text = "Open File", command = onBtnOpenFileClick)
    btnOpenFile.pack()

    updatedFont = tkFont.Font(font = btnOpenFile['font'])       # make the button font bigger so we don't have to squint
    updatedFont['size'] = int(float(updatedFont['size']) * 1.6)
    btnOpenFile.configure(font = updatedFont)

    frmMain.mainloop()

    cv2.destroyAllWindows()                     # remove windows from memory

    return
# end main

###################################################################################################
def onBtnOpenFileClick():

    cv2.destroyAllWindows()

    global  previousChosenDirectory

    chosenFile = tkFileDialog.askopenfilename(initialdir = previousChosenDirectory)       # get chosen file name

    previousChosenDirectory = getDirectoryFromDirectoryAndFileName(chosenFile)

    counter = 0

    try:
        imgOriginal = cv.LoadImage(chosenFile)
    except:
        print "error: unable to open file \n\n"        # print error message to std out
        return                                              # and exit function (which exits program)

    if imgOriginal is None:                             # if image was not read successfully
        print "error: image not read from file \n\n"        # print error message to std out
        return                                              # and exit function (which exits program)

    print "-------------------------------"
    print "detecting plates . . ."

    imgListOfPlates = detect_plates.detectPlates(imgOriginal)

    if len(imgListOfPlates) == 0:
        print "\nno license plates were detected\n"
        #print "-------------------------------"
        return
    # end if

    print "plate detection complete, " + str(len(imgListOfPlates)) + " possible plates found"

    for imgPlate in imgListOfPlates:

        imgGrayscale, imgThresh = preprocess.preprocess(imgPlate)

        imgBiggerPlate = cv.CreateImage((int(imgPlate.width * 1.6), int(imgPlate.height * 1.6)), cv.IPL_DEPTH_8U, 1)

        cv.Resize(imgThresh, imgBiggerPlate)

        imgThresh = imgBiggerPlate

        strOutputImageName = "output" + str(counter) + ".png"

        cv.SaveImage(strOutputImageName, imgThresh)        # save image to file, increment number in file name each time through for loop

        cv.ShowImage(strOutputImageName, imgThresh)

        # call OCR stuff here

        counter = counter+1
    # end for

    cv.ShowImage("imgOriginal", imgOriginal)

# end func

###################################################################################################
def getDirectoryFromDirectoryAndFileName(directoryAndFileName):
    indexOfLastSlash = directoryAndFileName.rfind("/")
    directoryAndFileName = directoryAndFileName[:indexOfLastSlash]
    return directoryAndFileName
# end func

###################################################################################################
if __name__ == "__main__":
    main()


















