import numpy as np
from PIL import Image

from image_processing.corrections import correctSignedBits, contrastCorrection
from image_processing.modifications import cropImage

##-\-\-\-\-\
## SUBCLASSES
##-/-/-/-/-/

# -------------------------
# Hold the different arrays
class ImageArrays:
    def __init__(self, image_array):

        # Save the arrays
        self.source = image_array
        self.display = np.copy(image_array)
        self.frame = Image.fromarray( self.display[0].astype(np.uint8) )

# ----------------------------------
# Hold information on the image size
class ImageSize:
    def __init__(self, size):
        self.tuple = size
        self.x = size[1]
        self.y = size[0]

# -----------------------------
# Hold information on the scale
class Scales:
    def __init__(self, space_scale, space_unit, frame_rate):
        self.space_scale = space_scale
        self.space_unit = space_unit
        self.frame_rate = frame_rate

##-\-\-\-\-\
## MAIN CLASS
##-/-/-/-/-/

class ImageCollection:
    def __init__(self, image_array, name='Untitled', crop=False, crop_size=512, correct_sign=False, space_scale=44.9, space_unit="micron", frame_rate=150):

        # Apply corrections if needed
        if correct_sign:
            image_array = correctSignedBits(image_array)
        if crop:
            image_array = cropImage(image_array, (crop_size,crop_size))

        # Get the image array
        self.name = name
        self.frame = 0
        self.image = ImageArrays(image_array)

        # Get the image properties
        self.n_frames = image_array.shape[0]
        self.size = ImageSize(image_array.shape[1:])
        self.scale = Scales(space_scale, space_unit, frame_rate)
        self.zoom = 1.
        self.contrast_limits = [np.amin(image_array), np.amax(image_array)]

        if np.amax(image_array) > 256:
            self.bitness = np.uint16
        else:
            self.bitness = np.uint8

        # Initialise other properties
        self.trajectory = None
        self.path_list = None
        self.displayed_paths = None

        # Prepare the image for display
        self.rescaleForDisplay()

    ##-\-\-\-\-\-\
    ## IMAGE UPDATE
    ##-/-/-/-/-/-/

    # -----------------------------------------------
    # Correct the contrast of the array to display it
    def rescaleForDisplay(self):

        # Delete the previous array
        del self.image.display
        del self.image.frame

        # Apply the contrast correction
        self.image.display = contrastCorrection(self.image.source, 1.0, limits=self.contrast_limits)
        self.image.display = self.image.display.astype(np.uint8)

        # Set the current frame
        self.image.frame = Image.fromarray( self.image.display[ self.frame ] )

    # ---------------------------------------------------
    # Display a preview rescale for brightness correction
    def rescaleTest(self, pv_limits=None):

        # Delete the previous array
        del self.image.frame

        # Use the current settings
        if pv_limits is None:
            pv_limits = self.contrast_limits

        # Apply the contrast correction
        preview_display = contrastCorrection(self.image.source[ self.frame ], 1.0, limits=pv_limits)
        preview_display = preview_display.astype(np.uint8)

        # Set the current frame
        self.image.frame = Image.fromarray( preview_display )

    # ------------------------
    # Set the frame to display
    def setFrame(self, frame_id=0):

        # Coerce the value
        if frame_id < 0:
            frame_id = self.n_frames - 1
        elif frame_id >= self.n_frames:
            frame_id = 0

        # Set the frame
        self.frame = frame_id

        # Set the current frame
        self.image.frame = Image.fromarray( self.image.display[ self.frame ] )
