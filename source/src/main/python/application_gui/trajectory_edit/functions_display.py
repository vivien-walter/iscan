from functools import partial
import numpy as np
from PIL import Image, ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.messageboxes.display import warningProceedMessage

from image_processing.modifications import cropMiniature

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class PathEditorDisplayFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## INITIALISE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/

    # -----------------------
    # Initialise the displays
    def initialiseDisplay(self):

        # Get the dimension of the current scroll areas
        widget_width = self.scrollArea.frameGeometry().width()
        widget_height = self.scrollArea.frameGeometry().height()

        mini_widget_width = self.miniScrollArea.frameGeometry().width()
        mini_widget_height = self.miniScrollArea.frameGeometry().height()

        # Get the dimension of the image
        image_height, image_width = self.image_class.size.tuple

        # Get the zoom factor
        self.zoom = np.amin( [widget_width / image_width, widget_height / image_height] )
        self.mini_zoom = np.amin( [mini_widget_width / 25, mini_widget_height / 25] )

    ##-\-\-\-\-\-\-\-\-\
    ## DISPLAY THE IMAGE
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Display the selected image in the tab
    def displayImage(self):

        # Get the image to display
        self.image_array = self.image_class.image.display[ self.current_frame ]
        self.image_frame = Image.fromarray( self.image_array.astype(np.uint8) )

        # Extract the required values
        zoom = self.zoom
        mini_zoom = self.mini_zoom
        self.initialHeight, self.initialWidth = self.image_class.size.tuple

        # Crop the miniature
        if self.new_position is not None:
            self.miniature_array, self.mini_cursor = cropMiniature(self.new_position, self.image_array)
            self.miniature_frame = Image.fromarray( self.miniature_array.astype(np.uint8) )
            self.miniHeight, self.miniWidth = self.miniature_array.shape

        # Generate the pixmap
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt( self.image_frame ))
        )

        # Rescale the pixmap
        width, height = (
            int(self.initialWidth * zoom),
            int(self.initialHeight * zoom),
        )

        self.pixmapToDisplay = self.pixmapSource.scaled(width, height)

        # Generate the miniature pixmap
        if self.new_position is not None:

            self.miniPixmapSource = qtg.QPixmap.fromImage(
                qtg.QImage(ImageQt.ImageQt( self.miniature_frame ))
            )

            mini_width, mini_height = (
                int(self.miniWidth * mini_zoom),
                int(self.miniHeight * mini_zoom),
            )

            self.miniPixmapToDisplay = self.miniPixmapSource.scaled(mini_width, mini_height)

        # Paint the position
        if self.new_position is not None:
            self.drawPosition()
            self.drawCursor()

        # Update the display
        self.scrollAreaImage.setPixmap( self.pixmapToDisplay )
        self.scrollAreaImage.adjustSize()

        if self.new_position is not None:
            self.miniScrollAreaImage.setPixmap( self.miniPixmapToDisplay )
            self.miniScrollAreaImage.adjustSize()

    # --------------------------------
    # Draw the particles on the screen
    def drawPosition(self, diameter=40):

        # Extract the zoom value
        zoom = self.zoom

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)

        # Draw the object
        y, x  = self.new_position

        # Rescale the object position
        x *= zoom
        y *= zoom

        # Get the circle limits
        radius = diameter/2 * zoom
        xmin, ymin = x - radius, y - radius

        # Draw the point on the canvas
        painter.setPen(qtg.QPen(qtc.Qt.red, 6*zoom, qtc.Qt.SolidLine))
        painter.drawEllipse(xmin,ymin,2*radius,2*radius)

        painter.end()

    # -----------------------------
    # Draw the cursor on the screen
    def drawCursor(self):

        # Extract the zoom value
        zoom = self.mini_zoom

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.miniPixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)

        # Draw the object
        y, x  = self.mini_cursor

        # Rescale the object position
        x *= zoom
        y *= zoom

        # Draw the lines on the canvas
        painter.setPen(qtg.QPen(qtc.Qt.yellow, .5*zoom, qtc.Qt.SolidLine))

        painter.drawLine(0,y,self.miniature_array.shape[1]*zoom,y)
        painter.drawLine(x,0,x,self.miniature_array.shape[0]*zoom)

        painter.end()

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## INTERACT WITH THE IMAGE
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Interact with the image on a mouse click
    def actionOnClick(self, event=None):

        # Get the click position
        x, y = event.pos().x(), event.pos().y()

        # Extract the zoom value
        zoom = self.zoom

        # Correct the zoom
        x = x / zoom
        y = y / zoom

        # Save the values
        self.new_position = np.array([y, x])

        # Refresh the image
        self.displayImage()
