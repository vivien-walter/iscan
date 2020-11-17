import numpy as np
from PIL import ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.modifications import cropImage
from image_processing.image_class import ImageCollection

from application_gui.messageboxes.display import errorMessage

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class imageCropFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## MANAGE THE IMAGE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Display the selected image in the tab
    def displayImage(self):

        # Extract the required values
        zoom = self.zoom
        self.initialHeight, self.initialWidth = self.image_class.size.tuple

        # Generate the pixmap
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt( self.image_class.image.frame ))
        )

        # Rescale the pixmap
        width, height = (
            int(self.initialWidth * zoom),
            int(self.initialHeight * zoom),
        )
        self.pixmapToDisplay = self.pixmapSource.scaled(width, height)

        # Update the display
        self.scrollAreaImage.setPixmap( self.pixmapToDisplay )
        self.scrollAreaImage.adjustSize()

    # -------------------------------
    # Draw the rectangle on the image
    def drawRectangleSelection(self):

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        painter.setPen(qtg.QPen(qtc.Qt.yellow, 3*self.zoom, qtc.Qt.SolidLine))

        # Draw the rectangle
        painter.drawRect( qtc.QRect(self.selection_pointA, self.selection_pointB).normalized() )

        # End the painter
        painter.end()

        # Refresh
        self.scrollAreaImage.setPixmap( self.pixmapToDisplay )

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## INTERACTION WITH THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------------------
    # Coerce the selected point
    def _coerce_point(self, point):

        # Get the coordinates
        x, y = point.x(), point.y()
        x_max, y_max = self.pixmapToDisplay.width(), self.pixmapToDisplay.height()

        # Coerce low limit
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        # Coerce the highest limit
        if x >= x_max:
            x = x_max-1
        if y >= y_max:
            y = y_max-1

        # Convert back into a point
        point = qtc.QPoint(x,y)

        return point

    # ----------------------------------------
    # Interact with the image on a mouse click
    def actionOnClick(self, event=None):

        # Start drawing
        if event.button() == qtc.Qt.LeftButton:
            self.drawing = True

            # Reset the display
            self.displayImage()

            # Set the first point
            self.selection_pointA = self._coerce_point(event.pos())

            # Display the rubber band
            self.rubberband.setGeometry( qtc.QRect(self.selection_pointA, qtc.QSize()) )
            self.rubberband.show()

        # Open the context menu
        elif event.button() == qtc.Qt.RightButton:
            self.showZoomMenu(event)

    # -------------------------------------------------
    # Interact with the image when the mouse is dragged
    def actionOnMove(self, event=None):

        # Draw the rectangle
        if self.drawing and self.rubberband.isVisible():
            self.rubberband.setGeometry( qtc.QRect(self.selection_pointA, self._coerce_point(event.pos())).normalized() )

    # --------------------------------------------------
    # Interact with the image when the mouse is released
    def actionOnRelease(self, event=None):

        # Interrupt the selection
        if event.button() == qtc.Qt.LeftButton and self.drawing:

            # Disable the rubber band
            self.drawing = False
            self.rubberband.hide()

            # Set the last point
            self.selection_pointB = self._coerce_point(event.pos())

            # Draw the rectangle selection on the image
            self.drawRectangleSelection()

    ##-\-\-\-\-\
    ## ZOOM MENU
    ##-/-/-/-/-/

    # --------------------------
    # Define the key press event
    def keyPressEvent(self, event):

        # Zoom In
        if event.key() == qtc.Qt.Key_Plus:
            self.changeZoom(zoom_in=True)

        # Zoom Out
        elif event.key() == qtc.Qt.Key_Minus:
            self.changeZoom(zoom_in=False)

    # ------------------------
    # Display the control menu
    def showZoomMenu(self, event):

        # Display the menu
        contextMenu = qtw.QMenu()

        # Rename the selected tab
        if self.selection_pointA is not None or self.selection_pointB is not None:
            resetSelectionAction = contextMenu.addAction("Reset selection")
            resetSelectionAction.triggered.connect(self.resetSelection)

            contextMenu.addSeparator()

        # Zoom actions
        zoomInAction = contextMenu.addAction("Zoom In (+)")
        zoomInAction.triggered.connect(lambda : self.changeZoom(zoom_in=True))

        zoomFitAction = contextMenu.addAction("Zoom to fit")
        zoomFitAction.triggered.connect(self.initialiseZoom)

        zoomOutAction = contextMenu.addAction("Zoom Out (-)")
        zoomOutAction.triggered.connect(lambda : self.changeZoom(zoom_in=False))

        action = contextMenu.exec_(qtg.QCursor.pos())

    # ---------------------------
    # Reset the current selection
    def resetSelection(self):

        # Remove the selection
        self.selection_pointA = None
        self.selection_pointB = None

        # Refresh the display
        self.displayImage()

    # -----------------------------
    # Increase or decrease the zoom
    def changeZoom(self, zoom_in=True):

        # Remove the selection
        self.selection_pointA = None
        self.selection_pointB = None

        # Modify the zoom value
        if zoom_in:
            self.zoom = self.zoom * 1.05
        else:
            self.zoom = self.zoom * .95

        # Refresh the display
        self.displayImage()

    # --------------------------------------------------------
    # Set the initial zoom to fit the image in the scroll area
    def initialiseZoom(self):

        # Remove the selection
        self.selection_pointA = None
        self.selection_pointB = None

        # Get the dimension of the current tab
        widget_width = self.scrollArea.frameGeometry().width()
        widget_height = self.scrollArea.frameGeometry().height()

        # Get the dimension of the image
        image_height, image_width = self.image_class.size.tuple

        # Get the zoom factor
        self.zoom = np.amin( [widget_width / image_width, widget_height / image_height] )

        # Refresh the display
        self.displayImage()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ----------------------------------
    # Crop the image using the selection
    def cropImage(self):

        # Raise an error if there is no selection
        if self.selection_pointA is None or self.selection_pointB is None:
            errorMessage("No Selection","A selection is required to crop the image.")

        # Crop the image
        else:

            # Get the selection
            selection = qtc.QRect(self.selection_pointA, self.selection_pointB)
            origin = int(selection.x()/self.zoom), int(selection.y()/self.zoom)
            dimensions = int(selection.width()/self.zoom), int(selection.height()/self.zoom)

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            old_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Crop the array
            new_array = cropImage(old_class.image.source, dimensions, origin=origin)

            # Load the array in a file
            new_class = ImageCollection(new_array, name=old_class.name, space_scale=self.parent.space_scale, space_unit=self.parent.space_unit, frame_rate=self.parent.frame_rate)

            # Replace the array in the tab
            self.parent.imageTabDisplay.replaceTab(tab_id, new_class)

            # Close the image
            self.close()
