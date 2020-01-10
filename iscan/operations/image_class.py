import numpy as np
from PIL import Image
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

    # ---------------------------------
    # Correct the contrast of the array
    def rescaleArray(self):

        # Contrast correction
        self.frame.display = contrastCorrection( self )

        # Generate the PIL image
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

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.image_correction import contrastCorrection
