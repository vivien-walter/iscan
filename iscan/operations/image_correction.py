import numpy as np

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -------------------------------------------------------
# Rescale the image intensity to apply the given contrast
def rescaleContrast(initialArray, minPV, maxPV, displayedMaxPV):

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

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------
# Rescale the intensity of the image
def contrastCorrection(imageStack):

    # Retrieve the values
    minPV = imageStack.min_pv
    maxPV = imageStack.max_pv
    maxValue = imageStack.max_value

    # Rescale the contrast of the image
    imageArray = np.copy( imageStack.frame.raw )
    contrastArray = rescaleContrast(imageArray, minPV, maxPV, 256)

    # Adjust the intensity for display
    scaledArray = contrastArray * maxValue

    return scaledArray

# ------------------------------------
# Simple correction of the image stack
def backgroundCorrection(
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
