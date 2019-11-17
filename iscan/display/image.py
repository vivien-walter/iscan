import numpy as np

from PIL import Image, ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

import iscan.image_handling as img
import iscan.math_functions as mfunc

##-\-\-\-\-\-\-\-\-\-\-\-\
## MENUBAR OF THE MAIN GUI
##-/-/-/-/-/-/-/-/-/-/-/-/

class imageWidget(qtw.QWidget):
    def __init__(self, parent, array, name, minPV=None, maxPV=None):
        super(imageWidget, self).__init__()

        # Store the widget parameters
        self.parent = parent
        self.name = name
        self.array = array
        self.zoom = 1
        self.minPV = minPV
        self.maxPV = maxPV

        # Store the profiles properties
        self.activeProfile = None
        self.savedProfiles = []
        self.savedData = []

        self.createStackDisplay()

    # ---------------------------------------
    # Create the display for the image stack
    def createStackDisplay(self):

        # Define the scrollable widget
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setMinimumWidth(630)
        self.scrollArea.setMaximumWidth(630)
        self.scrollAreaImage = qtw.QLabel(self.scrollArea)
        self.scrollAreaImage.setScaledContents(True)
        self.scrollAreaImage.mousePressEvent = self.actionOnClick
        self.scrollArea.setWidget(self.scrollAreaImage)
        self.scrollAreaLayout = qtw.QVBoxLayout()
        self.scrollAreaLayout.addWidget(self.scrollArea)
        self.setLayout(self.scrollAreaLayout)

        # Generate the array the first time
        self.updateArrays(frameNumber=0)

        # Save the initial size of the image
        imageSize = self.scrollAreaImage.size()
        self.initialWidth, self.initialalHeight = imageSize.width(), imageSize.height()

    # -------------------------------------------------------
    # Update the arrays and the main display of the software
    def updateArrays(self, frameNumber=None, maxValue=1., minPV=None, maxPV=None, zoomValue=None):

        # Retrieve or generate the values
        if frameNumber is None:
            frameNumber = self.currentFrame
        if zoomValue is None:
            zoomValue = self.zoom
        if minPV is None:
            if self.minPV is None:
                minPV= np.amin(self.array[frameNumber])
            else:
                minPV = self.minPV
        if maxPV is None:
            if self.maxPV is None:
                maxPV= np.amax(self.array[frameNumber])
            else:
                maxPV = self.maxPV
        self.minPV = minPV
        self.maxPV = maxPV

        # Update the array
        self.currentFrame = frameNumber
        self.currentArray = self.array[frameNumber]
        self.initialWidth, self.initialalHeight = self.currentArray.shape

        # Prepare the array and generate the image to display
        self.arrayToDisplay = img.contrastCorrection(
            np.copy(self.currentArray), maxValue=maxValue, minPV=self.minPV, maxPV=self.maxPV
        )
        self.imageToDisplay = Image.fromarray(self.arrayToDisplay.astype(np.uint8))
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt(self.imageToDisplay))
        )

        # Rescale the image size
        width, height = int(self.initialWidth*zoomValue), int(self.initialalHeight*zoomValue)
        self.pixmapToDisplay = self.pixmapSource.scaled(width, height)

        # Plot the saved profile if any
        if len(self.savedProfiles) > 0:
            for profile in [i for i in self.savedProfiles if i['frame'] == self.currentFrame]:
                self.drawProfileLine(profile['circle'], profile['line'], zoomValue, colour='black')

        # Plot the current profile is any
        if self.activeProfile is not None:
            if self.activeProfile['frame'] == self.currentFrame:
                self.drawProfileLine(self.activeProfile['circle'], self.activeProfile['line'], zoomValue)

        # Update the display
        self.scrollAreaImage.setPixmap(self.pixmapToDisplay)
        self.scrollAreaImage.adjustSize()

    #-------------------------------------
    # Change the frame currently displayed
    def changeFrame(self, increment=1, frame=None):

        # Get the new frame index
        if frame is None:
            frame = self.currentFrame + increment

        # Check that the new frame is within the range or correct
        maxFrame = len(self.array)
        if frame < 0:
            frame = 0
        elif frame >= maxFrame:
            frame = maxFrame -1

        # Update the display
        self.updateArrays(frameNumber = frame)

        return frame

    #-----------------------------
    # Modify the zoom on the image
    def changeZoom(self, factor=1.005, value=None, minImageSize = 16):

        # Get the rescaling value
        if value is None:
            value = self.zoom * factor

        # Calculate the new image size
        if self.initialWidth*value <= minImageSize or self.initialalHeight*value <= minImageSize:
            value = value * minImageSize / min(self.initialWidth*value, self.initialalHeight*value)

        # Save the zoom value and refresh the image
        self.zoom = value
        self.updateArrays(zoomValue=value)

        return round(self.zoom * 100, 2)

    #-------------------------------------------------------
    # Extract the intensity profile between two given points
    def extractProfile(self, p1, p2, center):

        # REMEMBER: x and y are inverted from image to arra
        # Generate the coordinates
        numberPoints = int(np.hypot(p2[1]-p1[1], p2[0]-p1[0]))
        x, y = np.linspace(p1[1], p2[1], numberPoints), np.linspace(p1[0], p2[0], numberPoints)

        # Get the profile
        profile = self.currentArray[x.astype(np.int), y.astype(np.int)]

        # Generate the radius
        distance = np.sqrt((x - center[1])**2 + (y - center[0])**2)*np.sign(x - center[1])

        return distance, profile

    ##-\-\-\-\-\-\-\-\
    ## PROFILE DRAWING
    ##-/-/-/-/-/-/-/-/

    #-------------------------------
    # Plot the profile on the screen
    def drawNewProfile(self, position, angle, length, radius=30):

        # Draw the elements
        imageSize = self.currentArray.shape
        p1, p2 = self.drawProfileElements(position, length, angle, imageSize, radius=radius)

        return p1, p2

    def drawProfileLine(self, circleLimits, lineLimits, zoomValue, colour='yellow'):

        # Set the colour
        if colour == 'yellow':
            colour = qtc.Qt.yellow
        elif colour == 'black':
            colour = qtc.Qt.black

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        painter.setPen(qtg.QPen(colour, 2, qtc.Qt.SolidLine))

        # Draw the elements
        painter.drawEllipse(*[i*zoomValue for i in circleLimits])
        painter.drawLine(*[i*zoomValue for i in lineLimits])
        painter.end()

    def drawProfileElements(self, position, length, angle, imageSize, radius=30, colour='yellow'):

        # Get the line and circle definitions
        circleLimits, lineLimits, p1, p2 = mfunc.circleAndLineComputation(position, length, angle, imageSize, radius=radius)

        # Append to the memory and refresh the display
        self.activeProfile = {'frame':self.currentFrame, 'circle':circleLimits, 'line':lineLimits}
        self.updateArrays()

        return p1, p2

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## HANDLE MOUSE INTERACTIONS WITH THE IMAGE
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    #--------------------------------------------
    # Action to perform when the image is clicked
    def actionOnClick(self, event):

        # Get the mouse position and rescale according to zoom
        mousePosition = np.array( [event.pos().x(), event.pos().y()] )
        mousePosition = (mousePosition / self.zoom).astype(int)

        # Get the current mode for the mouse interaction
        interactionType = self.parent.controlPanel.getInteractionType()

        # Proceed to the required interaction panel
        if interactionType == 'tracking':
            pass

        elif interactionType == 'profiling':

            # Check if the profiling panel has been already opened
            if self.parent.profilingPanel is None:
                self.parent.startProfilingMode()

            # Recalculate the position if required
            if self.parent.controlPanel.autoPositionCheckBox.isChecked():
                mousePosition = img.positionAdjustment(self.currentArray, mousePosition)

            # Update the profile menu
            self.parent.profilingPanel.updateOnClick(mousePosition, self.arrayToDisplay)
