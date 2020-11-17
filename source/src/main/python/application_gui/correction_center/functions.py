from PIL import Image, ImageQt

import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.modifications import cropImage
from image_processing.image_class import ImageCollection
from trajectory.modifications import centerCrop

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class cropCenterFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## INITIALISE THE WINDOW
    ##-/-/-/-/-/-/-/-/-/-/-/

    # -------------------------------
    # Get the centered path and array
    def getCenteredPath(self):

        # Get the cropped array
        self.array = centerCrop( self.image_class.image.display, self.image_class.trajectory, self.path_id )

        # Get the display array
        self.source_array = self.array[ self.image_class.frame ]
        self.display_array = np.copy(self.source_array)

        # Refresh the controls
        self.sizeSlider.setMaximum(self.source_array.shape[0])
        self.sizeSlider.setValue(self.source_array.shape[0])
        self.sizeEntry.setText(str(self.source_array.shape[0]))
        self.maxLabel.setText(str(self.source_array.shape[0]))

        # Prepare the display
        self.displayImage()

    ##-\-\-\-\-\-\-\-\-\
    ## DISPLAY THE IMAGE
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Display the selected image in the tab
    def displayImage(self):

        # Crop the new image
        _size = int(self.sizeEntry.text())
        self.display_array = cropImage(np.reshape(self.source_array, (1,self.source_array.shape[0],self.source_array.shape[1])), (_size, _size))
        self.display_array = self.display_array[0]

        # Compute the required values
        initial_height, initial_width = self.display_array.shape
        zoom = 256 / initial_height

        # Generate the pixmap
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt( Image.fromarray( self.display_array.astype(np.uint8) ) ))
        )

        # Rescale the pixmap
        width, height = (
            int(initial_height * zoom),
            int(initial_width * zoom),
        )
        self.pixmapToDisplay = self.pixmapSource.scaled(width, height)

        # Update the display
        self.scrollAreaImage.setPixmap( self.pixmapToDisplay )
        self.scrollAreaImage.adjustSize()

    ##-\-\-\-\-\-\-\-\-\
    ## USER INTERACTIONS
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------------
    # Update the display when the value of the slider is changed
    def updateSlider(self, value=None):

        # Update the text box
        self.sizeEntry.setText(str(value))

        # Update the image
        self.displayImage()

    # -------------------------------------------------------------
    # Update the display when the value of the entry box is changed
    def updateEntry(self):

        # Get the text
        _value = int(self.sizeEntry.text())
        self.sizeSlider.setValue(_value)

        # Update the image
        self.displayImage()

    # ---------------------------------
    # Apply the crop and open a new tab
    def applyCrop(self):

        # Get the final crop value
        crop_size = int(self.sizeEntry.text())

        # Crop the array
        array = centerCrop( self.image_class.image.source, self.image_class.trajectory, self.path_id )
        new_array = cropImage(array, (crop_size, crop_size))

        # Prepare the new array
        new_name = self.image_class.name + ' ('+str(self.path_id)+')'
        space_scale = self.image_class.scale.space_scale
        space_unit = self.image_class.scale.space_unit
        frame_rate = self.image_class.scale.frame_rate

        # Generate the class
        new_class = ImageCollection(new_array, name=new_name, space_scale=space_scale, space_unit=space_unit, frame_rate=frame_rate)

        # Open the new tab
        self.parent.imageTabDisplay.newTab(new_class)

        # Close the image
        self.close()
