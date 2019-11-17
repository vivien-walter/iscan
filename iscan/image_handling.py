from math import ceil, floor
import numpy as np
import pims
import scipy.ndimage as simg

import iscan.math_functions as mfunc

##-\-\-\-\-\-\-\-\
## IMAGE CORRECTION
##-/-/-/-/-/-/-/-/

# --------------------------------------------------------
# Rescale the image intensity to apply the given contrast
def _rescaleContrast(initialArray, minPV, maxPV, displayedMaxPV):

    imageArray = np.copy(initialArray).astype(float)

    # Crop the values
    imageArray[imageArray < minPV] = minPV
    imageArray[imageArray > maxPV] = maxPV

    # Shift to 0
    imageArray = imageArray - minPV

    # Rescale the maximal value
    maxPV -= minPV
    imageArray = imageArray * displayedMaxPV / maxPV

    return imageArray


# --------------------------
# Gaussian blur on an image
def _gaussianBlur(imageArray, sigma=5, order=0):
    return simg.filters.gaussian_filter(imageArray, sigma, order=order)


##-\-\-\-\
## CLASSES
##-/-/-/-/

# ----------------------------------------
# Class to handle the single image object
class iscatImage:
    def __init__(self, imageSequence):
        self.raw = imageSequence


# --------------------------
# Class to handle the stack
class iscatStack:
    def __init__(self, imageStack):

        # Get the image and the relevant informations
        self.image = iscatImage(imageStack)
        self.size = self.image.raw[0].shape
        self.frames = len(self.image.raw)


##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------------
# Open the image stack in the given folder
def loadStack(stackPath):

    # Open the images
    frames = iscatStack(pims.ImageSequence(stackPath))

    return frames


# -----------------------------------
# Rescale the intensity of the image
def contrastCorrection(imageArray, maxValue=1.0, minPV=None, maxPV=None):

    # Calculate the limits of the contrast if required
    if minPV is None:
        minPV = np.amin(imageArray)
    if maxPV is None:
        maxPV = np.amax(imageArray)

    # Rescale the contrast of the image
    contrastArray = _rescaleContrast(imageArray, minPV, maxPV, 256)

    # Adjust the intensity for display
    scaledArray = contrastArray * maxValue

    return scaledArray


# -----------------------------------------------------------
# Extract the pixel values distribution from the given array
def getPixelValueDistribution(imageArray):

    # Get the pixel values distribution
    pixelValues = np.ravel(np.array(imageArray))

    # Calculate the bins to use
    minBin = 10 ** (floor(np.log10(np.amin(pixelValues))))
    maxBin = 10 ** (ceil(np.log10(np.amax(pixelValues))))
    bins = np.logspace(np.log10(minBin), np.log10(maxBin), 1000)

    # Generate the histogram
    count, bins = np.histogram(imageArray, bins=bins)
    bins = (bins[0:-1] + bins[1::]) / 2

    return pixelValues, (count, bins), (minBin, maxBin)


# ---------------------------------
# Extract a caption from the image
def cropArray(position, array, size=50):

    # Extract the index from cursor position
    column, row = position

    # Get the subarray limits
    a, b = mfunc.limitCalculation(row, size, array.shape[0])
    c, d = mfunc.limitCalculation(column, size, array.shape[1])

    # Extract the subarray
    return array[a:b, c:d]


# ------------------------------------
# Adjust the position to local maxima
def positionAdjustment(imageArray, cursorPosition, areaSize=30):

    # Extract the index from cursor position
    column, row = cursorPosition

    # Extract the subarray
    subArray = cropArray(cursorPosition, imageArray, size=areaSize)
    smoothedArray = _gaussianBlur(subArray)

    # Find the local minima to recenter the subarray
    subRow, subColumn = np.unravel_index(
        np.argmax(smoothedArray, axis=None), smoothedArray.shape
    )
    subRow += row - areaSize
    subColumn += column - areaSize

    # Extract a new centered subarray
    subArray2 = cropArray((subColumn, subRow), imageArray, size=areaSize)
    smoothedArray2 = _gaussianBlur(subArray2)

    # Make a gaussian 2D fit on the data
    try:
        fitParameters, _ = mfunc.gaussian2DFit(smoothedArray2)
        fittedRow, fittedColumn = fitParameters[1:3]
    except:
        fittedRow, fittedColumn = row, column

    return (
        int(round(fittedColumn, 0)) + subColumn - areaSize,
        int(round(fittedRow, 0)) + subRow - areaSize,
    )


# -------------------------------------
# Simple correction of the image stack
def imageCorrection(
    array, averageType="median", correctionType="division", bitDepth=16, signedBits=True
):

    # Remove the signed values
    if signedBits:
        unsignedArray = np.copy(array) - (2 ** (bitDepth - 1) - 1)
    else:
        unsignedArray = np.copy(array)

    # Calculate the average image
    if averageType == "median":
        averageArray = np.reshape(
            np.median(unsignedArray, axis=0), (1, array.shape[1], array.shape[2])
        )
    elif averageType == "mean":
        averageArray = np.reshape(
            np.mean(unsignedArray, axis=0), (1, array.shape[1], array.shape[2])
        )
    correctionArray = np.repeat(averageArray, array.shape[0], axis=0)

    # Apply the correction
    if correctionType == "division":
        correctedArray = unsignedArray / correctionArray
    elif correctionType == "subtraction":
        correctedArray = unsignedArray - correctionArray

    return correctedArray
