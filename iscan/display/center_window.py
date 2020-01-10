import numpy as np

from PIL import Image, ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR CENTERING ON PATH
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class centerPathPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(centerPathPanel, self).__init__(parent)

        self.parent = parent

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        self.current_image = currentTab.image

        # Get the main informations
        self.path = self.current_image.path_active
        self.array = self.current_image.stack.array
        self.index = self.current_image.stack.i_frame
        self.max_frame = self.current_image.stack.n_frames-1

        # Get the parameters for the crop
        self.image_size = self.current_image.stack.size
        self.max_size = getMaxCropSize(self.path.positions, self.image_size)
        self.box_size = self.max_size
        self.limits = {
        'x_min': np.amin(self.path.positions[:,1]) - self.max_size,
        'y_min': np.amin(self.path.positions[:,2]) - self.max_size,
        'x_max': np.amax(self.path.positions[:,1]) + self.max_size,
        'y_max': np.amax(self.path.positions[:,2]) + self.max_size
        }

        # Initialise the subwindow
        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Center Image")

        # Populate the panel
        self.createFrameDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createNavigationDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createFrameSelection(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createActionButtons(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)

        # Initialize the image
        self.generateArray()

        self.show()

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event = None):
        event.accept()
        self.parent.subWindows['center'] = None

    # -----------------------------------------
    # Create the display for the path centering
    def createFrameDisplay(self, parentWidget):

        # Generate the widget
        self.displayWidget = qtw.QWidget()
        self.displayLayout = qtw.QVBoxLayout(self.displayWidget)

        # Define the scrollable widget
        self.frameImage = qtw.QLabel(self.displayWidget)
        self.frameImage.setScaledContents(True)
        self.displayLayout.addWidget(self.frameImage)

        # Display the widget
        self.displayWidget.setLayout(self.displayLayout)
        parentWidget.addWidget(self.displayWidget)

    # --------------------------------------------------------------
    # Generate buttons to process the correction or close the window
    def createNavigationDisplay(self, parentWidget):

        # Generate the widget
        self.navigationWidget = qtw.QWidget()
        self.navigationLayout = qtw.QGridLayout(self.navigationWidget)

        # Buttons
        currentRow = 0
        self.previousFrameButton = qtw.QPushButton("<")
        self.previousFrameButton.clicked.connect(self.previousFrame)
        self.previousFrameButton.setStatusTip("Move to the previous frame.")
        self.navigationLayout.addWidget(self.previousFrameButton, currentRow, 0)

        self.nextFrameButton = qtw.QPushButton(">")
        self.nextFrameButton.clicked.connect(self.nextFrame)
        self.nextFrameButton.setStatusTip("Move to the next frame.")
        self.navigationLayout.addWidget(self.nextFrameButton, currentRow, 1)

        # Show the path on the caption
        currentRow += 1
        self.showPathSelection = qtw.QCheckBox("Show path")
        self.showPathSelection.setChecked(True)
        self.showPathSelection.toggled.connect(self.displayImage)
        self.showPathSelection.setStatusTip("Display the path on the caption.")
        self.navigationLayout.addWidget(self.showPathSelection, currentRow, 0, 1, -1)

        # Display the widget
        self.navigationWidget.setLayout(self.navigationLayout)
        parentWidget.addWidget(self.navigationWidget)

    # --------------------------------------------------------------
    # Generate buttons to process the correction or close the window
    def createFrameSelection(self, parentWidget):

        # Generate the widget
        self.frameSelectionWidget = qtw.QWidget()
        self.frameSelectionLayout = qtw.QGridLayout(self.frameSelectionWidget)

        # Modify the frame size
        currentRow = 0
        self.frameSelectionLayout.addWidget(qtw.QLabel("Frame size"), currentRow, 0, 1, -1)

        currentRow += 1
        self.frameSizeSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.frameSizeSlider.setMaximum(self.max_size)
        self.frameSizeSlider.setMinimum(16)
        self.frameSizeSlider.setValue(self.max_size)
        self.frameSizeSlider.valueChanged.connect(self.updateLimits)
        self.frameSizeSlider.setStatusTip(
            "Modify the size of the frame to crop."
        )
        self.frameSelectionLayout.addWidget(self.frameSizeSlider, currentRow, 0, 1, -1)

        # Show the new frame size
        currentRow += 1
        self.showLimitSelection = qtw.QCheckBox("Show new frame size")
        self.showLimitSelection.setChecked(True)
        self.showLimitSelection.toggled.connect(self.displayImage)
        self.showLimitSelection.setStatusTip("Display the new window size on the caption.")
        self.frameSelectionLayout.addWidget(self.showLimitSelection, currentRow, 0, 1, -1)

        # Display the widget
        self.frameSelectionWidget.setLayout(self.frameSelectionLayout)
        parentWidget.addWidget(self.frameSelectionWidget)

    # --------------------------------------------------------------
    # Generate buttons to process the correction or close the window
    def createActionButtons(self, parentWidget):

        # Generate the widget
        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QGridLayout(self.buttonWidget)

        # Buttons
        currentRow = 0
        self.centerButton = qtw.QPushButton("Center")
        self.centerButton.clicked.connect(self.processCentering)
        self.centerButton.setStatusTip("Center the image on the path.")
        self.buttonLayout.addWidget(self.centerButton, currentRow, 0)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the window.")
        self.buttonLayout.addWidget(self.closeButton, currentRow, 1)

        # Display the widget
        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## PREPARATION OF THE IMAGE CANVAS
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    #-------------------------------------
    # Generate the cropped array to center
    def generateArray(self):

        # Get the array and crop it
        self.current_array = self.array[self.index]
        self.cropped_array = self.current_array[self.limits['y_min']:self.limits['y_max']+1,self.limits['x_min']:self.limits['x_max']+1]

        # Update the image
        self.displayImage()

    # -------------------------------
    # Display the image in the window
    def displayImage(self):

        # Get the image display properties
        minPV = self.current_image.stack.min_pv
        maxPV = self.current_image.stack.max_pv
        maxValue = self.current_image.stack.max_value

        # Prepare the array
        temp_array = rescaleContrast(self.cropped_array, minPV, maxPV, 256)
        self.display_array = temp_array * maxValue

        # Prepare the image for display
        self.display_image = Image.fromarray(self.display_array.astype(np.uint8))
        self.pixmap_source = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt(self.display_image))
        )

        # Display the path (static)
        if self.showPathSelection.isChecked():
            self.drawTrackedPath()

        # Display the frame edges
        if self.showLimitSelection.isChecked():
            self.drawFrameBox()

        # Update the display
        self.pixmap_display = self.pixmap_source.scaledToWidth(200)
        self.frameImage.setPixmap(self.pixmap_display)
        self.frameImage.adjustSize()

    #---------------------------
    # Update the displayed frame
    def updateFrame(self, increment=1):

        # Calculate the new index
        self.index = coerceValue(self.index + increment, self.max_frame)

        # Update the display
        self.displayImage()

    def previousFrame(self):
        self.updateFrame(increment=-1)

    def nextFrame(self):
        self.updateFrame()

    ##-\-\-\-\-\-\-\-\
    ## DRAWING ELEMENTS
    ##-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Draw the path to center on on the canvas
    def drawTrackedPath(self):

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmap_source)
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        colour = qtc.Qt.yellow

        # Check that positions exist
        positions = self.path.positions

        # Draw all the different elements
        for i, (t, x, y) in enumerate(positions):

            # Shift accordingly
            x -= self.limits['x_min']
            y -= self.limits['y_min']

            # Draw the point on the canvas
            painter.setPen(qtg.QPen(colour, 12, qtc.Qt.SolidLine))
            painter.drawPoint(x,y)

            # Draw the line on the canvas
            if i > 0:
                painter.setPen(qtg.QPen(colour, 4, qtc.Qt.SolidLine))
                painter.drawLine(x,y,positions[i-1,1]-self.limits['x_min'],positions[i-1,2]-self.limits['y_min'])

        painter.end()

    #-----------------------------
    # Plot the frame on the screen
    def drawFrameBox(self):

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmap_source)
        painter.setRenderHint(qtg.QPainter.Antialiasing)

        # Check that positions exist
        positions = self.path.positions

        # Draw the elements
        for i, (t, x, y) in enumerate(positions):

            # Only draw if the current frame is selected
            if self.index == t:

                # Correct the position of the particle
                x -= self.limits['x_min']
                y -= self.limits['y_min']

                # Calculate the position of the box corner
                TLCorner = [x-self.box_size, y+self.box_size]
                TRCorner = [x+self.box_size, y+self.box_size]
                BRCorner = [x+self.box_size, y-self.box_size]
                BLCorner = [x-self.box_size, y-self.box_size]

                # Paint the lines
                painter.setPen(qtg.QPen(qtc.Qt.yellow, 4, qtc.Qt.DashLine))
                painter.drawLine(TLCorner[0],TLCorner[1],TRCorner[0], TRCorner[1])
                painter.drawLine(TRCorner[0],TRCorner[1],BRCorner[0], BRCorner[1])
                painter.drawLine(BRCorner[0],BRCorner[1],BLCorner[0], BLCorner[1])
                painter.drawLine(BLCorner[0],BLCorner[1],TLCorner[0], TLCorner[1])

        painter.end()

    ##-\-\-\-\-\-\-\-\-\-\
    ## UPDATE THE ELEMENTS
    ##-/-/-/-/-/-/-/-/-/-/

    #---------------------------------
    # Update the size of the frame box
    def updateLimits(self, event=None):

        self.box_size = self.frameSizeSlider.value()
        self.displayImage()

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## PROCESS THE CENTERING
    ##-/-/-/-/-/-/-/-/-/-/-/

    #-------------------------------------------------------
    # Center the image using the path and load the new image
    def processCentering(self):

        # Extract the informations
        path = self.path.positions
        imageArray = self.array
        boxSize = self.box_size

        # Center and crop the image array
        centeredArray = centerImage(imageArray, path, boxSize)

        # Get the image properties
        currentTab, _ = self.parent.getCurrentTab()
        minPV = currentTab.image.stack.min_pv
        maxPV = currentTab.image.stack.max_pv
        maxValue = currentTab.image.stack.max_value

        # Open a new tab with the cropped image
        imageName = currentTab.name + "_centered"
        self.parent.addImageTab(centeredArray, name=imageName)

        # Rescale the contrast
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.stack.min_pv = minPV
        currentTab.image.stack.max_pv = maxPV
        currentTab.image.stack.max_value = maxValue

        # Refresh the display
        currentTab.image.updateArrays()

        # Close the window
        self.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.image_calculation import centerImage
from iscan.operations.image_correction import rescaleContrast
from iscan.operations.general_functions import coerceValue
from iscan.operations.particle_tracking import getMaxCropSize
