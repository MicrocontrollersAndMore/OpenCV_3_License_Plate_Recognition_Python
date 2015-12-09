# contour

import math
import cv2.cv as cv

import GlobalCounters

###################################################################################################
class PossibleChar(object):

    # member variables ############################################################################
    MIN_PIXELS = 8              # contour filter criteria
    MIN_WIDTH = 2
    MIN_HEIGHT = 8
    MAX_WIDTH = 50
    MAX_HEIGHT = 50
    MIN_ASPECT = 0.1
    MAX_ASPECT = 3.0
    MIN_AREA = 20
    MIN_DENSITY = 0.01

    MAX_HEIGHT_DIFF = 8         # similarity criteria
    MAX_WIDTH_DIFF = 8
    MAX_AVG_FACTOR = 0.2
    MAX_SDV_FACTOR = 0.2

    MIN_DIST_FACTOR = 0.3       # match criteria
    MAX_DIST_FACTOR = 10.0
    MAX_ANGLE = math.pi/4

    # blnValid = False
    contour = None

    intX1 = 0
    intY1 = 0
    intX2 = 0
    intY2 = 0

    intWidth = 0
    intHeight = 0

    intCenterX = 0
    intCenterY = 0

    fltDiameter = 0.0
    fltAspect = 0.0
    intArea = 0
    fltDensity = 0.0

    fltAvg = 0.0
    fltStdDev = 0.0

    # constructor #################################################################################
    def __init__(self, _contour):
        # self.contour = _contour          # save the contour

        storage = cv.CreateMemStorage()

        arcLength = cv.ArcLength(_contour)
        self.contour = cv.ApproxPoly(_contour, storage, cv.CV_POLY_APPROX_DP, arcLength * 0.001)
    # end func

    ##############################################################################################
    def checkIfValid(self):

        # print "--------------------"
        #
        # GlobalCounters.intNumTimesInCheckIfValid = GlobalCounters.intNumTimesInCheckIfValid + 1
        # print "GlobalCounters.intNumTimesInCheckIfValid = " + str(GlobalCounters.intNumTimesInCheckIfValid)

        if len(self.contour) < self.MIN_PIXELS:
            return False
        # end if

        # GlobalCounters.intNumTimesPastFirstIf = GlobalCounters.intNumTimesPastFirstIf + 1
        # print "GlobalCounters.intNumTimesPastFirstIf = " + str(GlobalCounters.intNumTimesPastFirstIf)

        listOfXPoints = []
        listOfYPoints = []

        for point in self.contour:
            listOfXPoints.append(point[0])
            listOfYPoints.append(point[1])
        # end for

        self.intX1 = min(listOfXPoints)        # left
        self.intY1 = min(listOfYPoints)        # top
        self.intX2 = max(listOfXPoints)        # right
        self.intY2 = max(listOfYPoints)        # bottom

        self.intWidth = self.intX2 - self.intX1              # intWidth
        self.intHeight = self.intY2 - self.intY1             # intHeight

        if self.intWidth < self.MIN_WIDTH or self.intWidth > self.MAX_WIDTH:
            return False
        # end if

        if self.intHeight < self.MIN_HEIGHT or self.intHeight > self.MAX_HEIGHT:
            return False
        # end if

        # GlobalCounters.intNumTimesPastWidthAndHeight = GlobalCounters.intNumTimesPastWidthAndHeight + 1
        # print "GlobalCounters.intNumTimesPastWidthAndHeight = " + str(GlobalCounters.intNumTimesPastWidthAndHeight)

        self.intCenterX = (self.intX1 + self.intX2) / 2             # center
        self.intCenterY = (self.intY1 + self.intY2) / 2

        # print "type of self.intCenterX = " + str(type(self.intCenterX))
        # print "type of self.intCenterY = " + str(type(self.intCenterY))

        self.fltDiameter = math.sqrt((self.intWidth * self.intWidth) + (self.intHeight * self.intHeight))       # diagonal size

        self.fltAspect = float(self.intWidth) / float(self.intHeight)                          # fltAspect
        if self.fltAspect < self.MIN_ASPECT or self.fltAspect > self.MAX_ASPECT:
            return False
        # end if

        self.intArea = self.intWidth * self.intHeight                    # intArea

        # print "self.intArea = " + str(self.intArea)

        if self.intArea < self.MIN_AREA:
            return False
        # end if

        self.fltDensity = len(self.contour) / float(self.intArea)            # fltDensity

        if self.fltDensity < self.MIN_DENSITY:
            return False
        # end if

        # print "type of self.fltDensity = " + str(type(self.fltDensity))
        
                                    # if we get here, the contour is valid
        # self.blnValid = True                            # mark current obj flag as valid
        return True                                     # and return True

    ###############################################################################################
    def calcAvgAndStdDev(self, imgGrayscale):
        cv.SetImageROI(imgGrayscale, (self.intX1, self.intY1, self.intWidth, self.intHeight))
        self.fltAvg, self.fltStdDev = cv.AvgSdv(imgGrayscale)
        self.fltAvg = self.fltAvg[0]
        self.fltStdDev = self.fltStdDev[0]

        # print "self.fltAvg = " + str(self.fltAvg)

        # print "-------------------------------------"
        # print "type of self.intX1 = " + str(type(self.intX1))
        # print "type of self.intY1 = " + str(type(self.intY1))
        # print "type of self.intWidth = " + str(type(self.intWidth))
        # print "type of self.intHeight = " + str(type(self.intHeight))
        # print "type of self.fltAvg = " + str(type(self.fltAvg))
        # print "type of self.fltStdDev = " + str(type(self.fltStdDev))

        cv.ResetImageROI(imgGrayscale)
    # end func

    ###############################################################################################
    def distanceTo(self, otherPossibleChar):                                # called by ??
        x = self.intCenterX - otherPossibleChar.intCenterX
        y = self.intCenterY - otherPossibleChar.intCenterY

        # print "type of self.intCenterX = " + str(type(self.intCenterX))
        # print "type of self.intCenterY = " + str(type(self.intCenterY))
        
        return math.sqrt((x * x) + (y * y))
    # end func

    ###############################################################################################
    def gradientTo(self, otherPossibleChar):

        if self.intCenterX > otherPossibleChar.intCenterX:
            greaterXPossibleChar = self
            lesserXPossibleChar = otherPossibleChar
        else: # elif otherPossibleChar.intCenterX <= self.intCenterX:
            greaterXPossibleChar = otherPossibleChar
            lesserXPossibleChar = self
        # end else if

        fltXDifference = float(greaterXPossibleChar.intCenterX - lesserXPossibleChar.intCenterX)
        fltYDifference = float(greaterXPossibleChar.intCenterY - lesserXPossibleChar.intCenterY)

        return fltYDifference / fltXDifference
    # end func

    ###############################################################################################
    def angleTo(self, otherPossibleChar):
        fltAdj = float(abs(self.intCenterX - otherPossibleChar.intCenterX))
        fltOpp = float(abs(self.intCenterY - otherPossibleChar.intCenterY))
        fltHyp = float(math.sqrt((fltAdj * fltAdj) + (fltOpp * fltOpp)))

        # print "-------------------------------------"
        # print "adj = " + str(fltAdj) + ", type of adj = " + str(type(fltAdj))
        # print "opp = " + str(fltOpp) + ", type of opp = " + str(type(fltOpp))
        # print "hyp = " + str(fltHyp) + ", type of hyp = " + str(type(fltHyp))

        return math.asin(fltOpp / fltHyp)
    # end func

    ###############################################################################################
    def findListOfMatchingChars(self, listOfPossibleChars):

        listOfMatchingChars = []

        for otherPossibleChar in listOfPossibleChars:
            if otherPossibleChar != self:
                fltDistanceTo = self.distanceTo(otherPossibleChar)
                if (fltDistanceTo > (self.fltDiameter * self.MIN_DIST_FACTOR) and
                    fltDistanceTo < (self.fltDiameter * self.MAX_DIST_FACTOR) and
                    abs(self.intWidth - otherPossibleChar.intWidth) < self.MAX_WIDTH_DIFF and
                    abs(self.intHeight - otherPossibleChar.intHeight) < self.MAX_HEIGHT_DIFF and
                    ((self.fltAvg - otherPossibleChar.fltAvg) / self.fltAvg) < self.MAX_AVG_FACTOR and
                    ((self.fltStdDev - otherPossibleChar.fltStdDev) / self.fltStdDev) < self.MAX_SDV_FACTOR and
                    self.angleTo(otherPossibleChar) < self.MAX_ANGLE):

                                            # if all the above are true, then self and otherPossibleChar are a "match",
                                            # so add it to our list, also add distance between self and otherPossibleChar
                    listOfMatchingChars.append(otherPossibleChar)
                # end if
            # end if
        # end for

        return listOfMatchingChars
    # end func

# end class















