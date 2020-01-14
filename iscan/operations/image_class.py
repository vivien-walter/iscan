import numpy as np
from PIL import Image, ImageSequence
import pims

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## FRAME CURRENTLY DISPLAYED
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageFrame:
    def __init__(self, array):

        # Extract the array of the current frame
        self.raw = array
        self.display = np.copy(array)

        # Initialize the other attributes
        self.pil_image = None

##-\-\-\-\-\-\-\-\-\-\
## STACK LOADED IN TAB
##-/-/-/-/-/-/-/-/-/-/

class imageStack:
    def __init__(self, array):

        # Stack properties
        self.array = array
        self.d_array = np.copy( array )
        self.size = self.array[0].shape
        self.n_frames = self.array.shape[0]

        # Animation properties
        self.frame_rate = 25

        # Load the first frame
        self.i_frame = 0
        self.frame = imageFrame( self.array[self.i_frame] )

        # Image properties
        self.zoom = 610 / max(self.size) # 610 is an arbitrary value
        self.min_pv = np.amin( self.frame.raw )
        self.max_pv = np.amax( self.frame.raw )
        self.max_value = 1.0

        # Rescale the array for display
        self.rescaleArray()

    # ---------------------------------
    # Correct the contrast of the array
    def rescaleArray(self):

        # Contrast correction
        self.d_array = contrastCorrection( self )

        # Generate the PIL image
        self.frame.display = self.d_array[self.i_frame]
        self.frame.pil_image = Image.fromarray( self.frame.display.astype(np.uint8) )

    # -----------------------------------------
    # Correct the contrast of the current frame
    def rescaleFrame(self):

        # Get the number of the array
        index = self.i_frame

        # Update the current frame
        self.frame.raw = np.copy( self.array[index] )
        self.frame.display = singleContrastCorrection(self)
        self.frame.pil_image = Image.fromarray( self.frame.display.astype(np.uint8) )

    # ------------------------------------
    # Change the frame currently displayed
    def changeFrame(self):

        # Get the number of the array
        index = self.i_frame

        # Update the current frame
        self.frame.raw = np.copy( self.array[index] )
        self.frame.display = np.copy( self.d_array[index] )
        self.frame.pil_image = Image.fromarray( self.frame.display.astype(np.uint8) )

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------------
# Open the image stack in the given folder
def loadStack(stackPath):

    # Open the images
    sequence = pims.ImageSequence(stackPath)
    stackArray = np.array(sequence)

    return stackArray

# ----------------
# Open a gif stack
def loadGifStack(filePath):

    # Open the gif
    sequence = Image.open(filePath)

    # Extract all frames
    stackArray = []
    for frame in ImageSequence.Iterator(sequence):
        stackArray.append( np.copy(np.array(frame)) )

    return np.array(stackArray)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.image_correction import contrastCorrection, singleContrastCorrection
