import numpy as np
from PIL import Image
from skimage import io

##-\-\-\-\-\-\-\-\-\-\-\
## IMAGE ARRAY EXTRACTION
##-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------
# Return the array to be saved
def getArrayToSave(imageStack, saveSingle=True, saveRaw=True):

    # Deal with single frame
    if saveSingle:
        if saveRaw:
            imageArray = np.copy( imageStack.frame.raw )
        else:
            imageArray = np.copy( imageStack.frame.display )

    # Get the whole stack
    else:

        # Get the array
        imageArray = np.copy( imageStack.array )

        # Adapt if needed
        if not saveRaw:

            # Retrieve the values
            minPV = imageStack.min_pv
            maxPV = imageStack.max_pv
            maxValue = imageStack.max_value

            # Rescale the contrast
            imageArray = rescaleContrast(imageArray, minPV, maxPV, 256)
            imageArray = imageArray * maxValue

    return imageArray

##-\-\-\-\-\-\-\-\
## SAVE IMAGE FILE
##-/-/-/-/-/-/-/-/

# --------------------
# Save the whole stack
def saveStack(fileName, imageArray, extension='.tif'):

    # Save the .tif stack normally
    try:
        if extension == '.gif':
            im = [Image.fromarray(img) for img in imageArray]
            im[0].save(fileName, save_all=True, append_images=im[1:])

        # Save the gif animation
        else:
            io.imsave(fileName, imageArray)

        messageFileSaved()
        return True

    except:
        errorFileSaved()
        return False

# ------------------------
# Save a single image only
def saveImage(fileName, imageArray):

    # Save the image
    try:
        io.imsave(fileName, imageArray)
        messageFileSaved()
        return True

    # Return an error if it failed
    except:
        errorFileSaved()
        return False

# ------------------------------
# Save the displayed image stack
def saveFrames(parent, imageStack, saveSingle=False, extension='.tif', saveRaw=True, convert8Bit=True, signedBits=False):

    # Get the array to save
    imageArray = getArrayToSave(imageStack, saveSingle=saveSingle, saveRaw=saveRaw)

    # Convert to the required bit depth
    arrayToSave = changeBitDepth(imageArray, to8bits=convert8Bit, signedBits=signedBits)

    # Get the file name
    process, fileName = getFileToCreate(parent, extension=extension)

    # Save the stack or image
    if process:

        if saveSingle:
            isSaved = saveImage(fileName, arrayToSave)
        else:
            isSaved = saveStack(fileName, arrayToSave, extension=extension)
        return isSaved

    # Keep the window open if the user did not select a name
    else:
        return False

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import messageFileSaved, errorFileSaved
from iscan.input_output.check_files import getFileToCreate
from iscan.operations.image_calculation import changeBitDepth
from iscan.operations.image_correction import rescaleContrast
