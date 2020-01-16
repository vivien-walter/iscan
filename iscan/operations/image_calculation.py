import bottleneck as bn
from math import ceil, floor
import numpy as np
from skimage import exposure, img_as_uint, img_as_float

##-\-\-\-\-\-\-\-\
## FRAME AVERAGING
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Frame averaging using running average
def runningFrameAverage(stackArray, n_frames, use_median=False, all_frames=True, after_only=False):

    # Initialize the output array
    outputArray = []

    # Loop over all the frames
    numberFrames = stackArray.shape[0]
    for i in range( numberFrames ):

        # Calculate the range to average on
        if after_only:
            averageRange = ( i , i+n_frames )
        else:
            averageRange = ( i-floor(n_frames/2) , i+ceil(n_frames/2) )

        # Check if it's free to proceed
        if averageRange[0] >= 0 and averageRange[1] <= numberFrames:
            proceed = True

        elif all_frames:
            proceed = True
            if averageRange[0] < 0:
                averageRange = ( i , i+n_frames )
            elif averageRange[1] >= numberFrames:
                averageRange = ( i-n_frames , i )

        else:
            proceed = False

        # Calculate the average
        if proceed:

            # Extract the array to calculate
            currentStack = stackArray[averageRange[0]:averageRange[1]]

            # Do the required average
            if use_median:
                averagedArray = bn.nanmedian(currentStack, axis=0)
            else:
                averagedArray = bn.nanmean(currentStack, axis=0 )

            # Append the array to the output array
            outputArray.append( np.copy(averagedArray) )

    return np.array(outputArray)

# -------------------------------------
# Frame averaging using group averaging
def groupFrameAverage(stackArray, n_frames, use_median=False, all_frames=True):

    # Initialize the output array
    outputArray = []

    # Initialize the loop
    numberFrames = stackArray.shape[0]

    # Loop over all the frames
    for i in range( 0, numberFrames, n_frames ):

        # Calculate the range to average on
        averageRange = ( i , i+n_frames )

        # Check if it's free to proceed
        if averageRange[1] <= numberFrames:
            proceed = True

        elif all_frames:
            proceed = True
            averageRange = ( numberFrames - n_frames , numberFrames )

        else:
            proceed = False

        # Calculate the average
        if proceed:

            # Extract the array to calculate
            currentStack = stackArray[averageRange[0]:averageRange[1]]

            # Do the required average
            if use_median:
                averagedArray = bn.nanmedian( currentStack, axis=0 )
            else:
                averagedArray = bn.nanmean( currentStack, axis=0 )

            # Append the array to the output array
            outputArray.append( np.copy(averagedArray) )

    return np.array(outputArray)

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## STATISTICS ON PIXEL VALUES
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------------------------------
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

##-\-\-\-\-\-\-\-\-\
## IMAGE MODIFICATION
##-/-/-/-/-/-/-/-/-/

# --------------------------------
# Extract a caption from the image
def cropImage(position, array, size=50):

    # Extract the index from cursor position
    column, row = position

    # Check if it's a stack or not
    i = len(array.shape) - 2

    # Get the subarray limits
    a, b = limitCalculation(row, size, array.shape[i])
    c, d = limitCalculation(column, size, array.shape[i+1])

    # Extract the subarray
    if i == 0:
        return array[a:b, c:d]
    elif i == 1:
        return array[:, a:b, c:d]

# --------------------------------
# Center the image on a trajectory
def centerImage(imageArray, particlePath, frameSize):

    # Process everyframe
    newImageArray = []
    for i, (t, x, y) in enumerate(particlePath):

        # Crop the array
        croppedArray = imageArray[i][y-frameSize:y+frameSize, x-frameSize:x+frameSize]
        newImageArray.append( np.copy(croppedArray) )

    newImageArray = np.array(newImageArray)

    return newImageArray

# ------------------------------------------
# Convert the image to an 8 or 16 bits image
def changeBitDepth(image, to8bits=True, signedBits=False):

    # Select the conversion to apply
    if to8bits:
        max = 255
        dataType = np.uint8
    else:
        max = 65535
        dataType = np.uint16

    # Correct for signed bits
    if signedBits:
        image = np.copy(image) - np.amin(image)

    # Change the array bit depth
    newImage = np.copy(image).astype(np.float32) / np.amax(image)
    newImage = newImage * max
    newImage = newImage.astype(dataType)

    return newImage

##-\-\-\-\-\-\-\-\-\
## STACK MODIFICATION
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------------------
# Select only a reduced number of frames in the stack
def cropStack(imageArray, frame_range):

    # Get a copy of the array
    newArray = np.copy(imageArray)

    # Select only the desired frames of the array
    newArray = newArray[frame_range]

    return newArray

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.general_functions import limitCalculation
