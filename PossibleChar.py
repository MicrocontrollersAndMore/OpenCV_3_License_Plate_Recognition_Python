# PossibleChar.py

import cv2
import numpy as np

###################################################################################################
class PossibleChar:

    # constructor #################################################################################
    def __init__(self, _contour):
        self.contour = _contour

        self.boundingRect = cv2.boundingRect(self.contour)

        self.intCenterX = (self.boundingRect.x + self.boundingRect.x + self.boundingRect.width) / 2
        self.intCenterY = (self.boundingRect.y + self.boundingRect.y + self.boundingRect.height) / 2

        self.fltDiagonalSize = sqrt((boundingRect.width ** 2) + (boundingRect.height ** 2))

        self.fltAspectRatio = boundingRect.width / boundingRect.height
    # end constructor

# end class



