import numpy as np
import pims
import scipy.ndimage as simg

import iscan.math_functions as mfunc

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## INTENSITY PROFILES AND FIT
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# -----------------------------------
# Class to handle intensity profiles
class iScatSignal:
    def __init__(
        self,
        dataName,
        imageValues,
        frameNumber,
        positionAndSetup,
        fitType,
        fitParams,
        fitErrors,
        signal,
        fittedSignal,
    ):

        # General informations
        self.name = dataName
        self.frame = frameNumber
        self.fit = fitType

        # Image values
        (
            self.contrast,
            self.contrastErr,
            self.noise,
            self.noiseErr,
            self.snr,
            self.snrErr,
        ) = imageValues

        # Profile position
        self.x, self.y, self.angle, self.length = positionAndSetup

        # Profile fit
        self.amplitude, self.width, self.center, self.offset = fitParams
        self.aErr, self.wErr, self.cErr, self.oErr = fitErrors

        # Profile displays
        self.distance, self.profile = signal
        self.distanceFit, self.profileFit = fittedSignal

    # ------------------------------------
    # Return the data to use in the table
    def getData(self):

        dataList = [
            self.name,
            self.contrast,
            self.contrastErr,
            self.noise,
            self.noiseErr,
            self.snr,
            self.snrErr,
            self.frame,
            self.x,
            self.y,
            self.angle,
            self.length,
            self.fit,
            self.amplitude,
            self.aErr,
            self.center,
            self.cErr,
            self.width,
            self.wErr,
            self.offset,
            self.oErr,
        ]

        return dataList
