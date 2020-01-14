import numpy as np
from PIL import ImageQt

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WIDGET TO DISPLAY IMAGES IN A TAB
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageWidget(qtw.QWidget):
    def __init__(self, parent, name, imageStack, calibration):
        super(imageWidget, self).__init__()

        # Store the widget informations
        self.parent = parent
        self.main_parent = parent.parent
        self.name = name
        self.stack = imageStack

        # Set the calibration of th estack
        self.spatial_calibration = calibration[0]
        self.time_calibration = calibration[1]

        # Store the profiles properties
        self.profile_active = None
        self.profile_saved = []
        self.path_active = None
        self.path_saved = []

        # Define the default settings for the auto-tracking
        self.tracking_settings = {
        'crop_size': 200,
        'particle_size':45,
        'min_mass':20,
        'min_frame':10,
        'memory':3
        }
        self.default_settings = self.tracking_settings.copy()

        # Generate the display
        self.createStackDisplay()

    # --------------------------------------
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
        self.updateArrays()

        # Save the initial size of the image
        imageSize = self.scrollAreaImage.size()
        self.initialWidth, self.initialHeight = imageSize.width(), imageSize.height()

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## MODIFICATION OF THE DISPLAYED IMAGE
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------------------
    # Update the arrays and the main display of the software
    def updateArrays( self, preview_tracking=None ):

        # Extract the required values
        zoom = self.stack.zoom

        # Update the array
        self.stack.changeFrame()
        self.initialWidth, self.initialHeight = self.stack.frame.display.shape

        # Generate the pixmap
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt( self.stack.frame.pil_image ))
        )

        # Rescale the pixmap
        width, height = (
            int(self.initialWidth * zoom),
            int(self.initialHeight * zoom),
        )
        self.pixmapToDisplay = self.pixmapSource.scaled(width, height)

        # Plot the profiles and paths
        if preview_tracking is None:
            if self.main_parent.docks['tracking'] is not None:
                self.drawPaths()
            if self.main_parent.docks['profiling'] is not None:
                self.drawProfiles()

        # Plot preview of profiles being tracked
        else:
            self.drawParticlePosition(preview_tracking)

        # Update the display
        self.scrollAreaImage.setPixmap( self.pixmapToDisplay )
        self.scrollAreaImage.adjustSize()

    # ------------------------------------------------------
    # Update the arrays and the main display of the software
    def updateSingleArray( self ):

        # Extract the required values
        zoom = self.stack.zoom

        # Update the array
        self.stack.rescaleFrame()
        self.initialWidth, self.initialHeight = self.stack.frame.display.shape

        # Generate the pixmap
        self.pixmapSource = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt( self.stack.frame.pil_image ))
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

    # -----------------------------------
    # Draw the profile(s) line and circle
    def drawProfileLine(self, profile, colour="yellow"):

        # Retrieve the elements for the profile
        frame = profile.frame
        lineLimits = profile.line
        circleLimits = profile.circle

        # Check if the frame can be displayed
        if frame != self.stack.i_frame:
            return 0

        # Set the colour
        if colour == "yellow":
            colour = qtc.Qt.yellow
        elif colour == "black":
            colour = qtc.Qt.black
        elif colour == "blue":
            colour = qtc.Qt.blue

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)
        painter.setPen(qtg.QPen(colour, 2, qtc.Qt.SolidLine))

        # Draw the elements
        zoomValue = self.stack.zoom
        painter.drawEllipse(*[i * zoomValue for i in circleLimits])
        painter.drawLine(*[i * zoomValue for i in lineLimits])
        painter.end()

    # -----------------
    # Draw all profiles
    def drawProfiles(self):

        # Plot the active profile
        if self.profile_active is not None:
            self.drawProfileLine( self.profile_active )

        # Plot the saved profiles
        if len(self.profile_saved) > 0:
            for profile in self.profile_saved:
                self.drawProfileLine( profile, colour=profile.colour )

    # -----------------------------------
    # Draw the profile(s) line and circle
    def drawPathLine(self, path, colour="yellow"):

        # Retrieve the required parameters
        zoomValue = self.stack.zoom
        currentFrame = self.stack.i_frame

        # Set the colour
        if colour == "yellow":
            colour = qtc.Qt.yellow
        elif colour == "blue":
            colour = qtc.Qt.blue

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)

        # Check that positions exist
        positions = path.positions
        if positions is None:
            return 0

        # Draw all the different elements
        for i, (t, x, y) in enumerate(positions):

            # Rescale the object position
            x *= zoomValue
            y *= zoomValue

            # Edit the point size
            size = 6
            if t == currentFrame:
                size = 10

            # Check the display in time options
            drawPoint = True
            drawLine = True

            if path.time_option == 'single':
                if t != currentFrame:
                    drawPoint = False
                drawLine = False

            elif path.time_option == 'reduced':
                if t not in np.arange(currentFrame-3, currentFrame+1):
                    drawPoint = False
                if t not in np.arange(currentFrame-2, currentFrame+1):
                    drawLine = False

            # Draw the point on the canvas
            if drawPoint:
                painter.setPen(qtg.QPen(colour, size*zoomValue, qtc.Qt.SolidLine))
                painter.drawPoint(x,y)

            # Draw the line on the canvas
            if i > 0 and drawLine:
                painter.setPen(qtg.QPen(colour, 2*zoomValue, qtc.Qt.SolidLine))
                painter.drawLine(x,y,positions[i-1,1]* zoomValue,positions[i-1,2]* zoomValue)

        painter.end()

    # ----------------------------------------
    # Draw the particle positions in a preview
    def drawParticlePosition(self, particle_positions):

        # Retrieve the required parameters
        zoomValue = self.stack.zoom

        # Initialise the painter
        painter = qtg.QPainter()
        painter.begin(self.pixmapToDisplay)
        painter.setRenderHint(qtg.QPainter.Antialiasing)

        # Draw all the different elements
        for x, y in particle_positions:

            # Rescale the object position
            x *= zoomValue
            y *= zoomValue

            # Draw the point on the canvas
            painter.setPen(qtg.QPen(qtc.Qt.yellow, 6*zoomValue, qtc.Qt.SolidLine))
            painter.drawPoint(x,y)

        painter.end()

    # ---------------------
    # Draw all trajectories
    def drawPaths(self):

        # Plot the active profile
        if self.path_active is not None:
            self.drawPathLine( self.path_active )

        # Plot the saved profiles
        showAll = self.main_parent.docks['tracking'].allPathRadiobutton.isChecked()

        for path in self.path_saved:
            if self.path_active != path and showAll:
                self.drawPathLine( path, colour="blue" )

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## INTENSITY PROFILE MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------
    # Generate a new intensity profile
    def createProfile(self, position, angle, length, imageSize=None, radius=30):

        # Get the image size
        if imageSize is None:
            imageSize = self.stack.frame.raw.shape

        # Get the line and circle definitions
        circleLimits, lineLimits, p1, p2 = circleAndLineComputation(
            position, length, angle, imageSize, radius=radius
        )

        # Append to the memory and refresh the display
        self.profile_active = profile(self.stack.i_frame, lineLimits, circleLimits)
        self.updateArrays()

        return p1, p2

    # -----------------------------
    # Extract the intensity profile
    def extractProfile(self, p1, p2, center):

        # REMEMBER: x and y are inverted from image to array
        # Generate the coordinates
        numberPoints = int(np.hypot(p2[1] - p1[1], p2[0] - p1[0]))
        x, y = ( np.linspace(p1[1], p2[1], numberPoints) , np.linspace(p1[0], p2[0], numberPoints) )

        # Get the profile
        profile = self.stack.frame.raw[x.astype(np.int), y.astype(np.int)]
        self.profile_active.profile = profile

        # Generate the radius
        distance = np.sqrt((x - center[1]) ** 2 + (y - center[0]) ** 2) * np.sign(x - center[1])
        self.profile_active.distance = distance

        return distance, profile

    # ------------------------------------------------------
    # Save all the profiles informations stored in the table
    def saveProfileTable(self):

        # Check if profiles are stored in the memory
        if len(self.profile_saved) == 0:
            errorMessage("ERROR: No data in memory", "There is no profile to save in the memory.")
            return 0

        # Save all the profiles in a file
        saveTable( self.main_parent, self.profile_saved )

    # ------------------------------------------
    # Save all the profiles stored in the memory
    def saveAllProfiles(self):

        # Check if profiles are stored in the memory
        if len(self.profile_saved) == 0:
            errorMessage("ERROR: No data in memory", "There is no profile to save in the memory.")
            return 0

        # Get the directory to save the files in
        proceed, useDefault, path = getFileOrFolder(self.main_parent)
        if not proceed:
            return 0

        # Save all profiles in separated files
        for i, profile in enumerate(self.profile_saved):

            # Generate the name of the file to save
            if useDefault:
                file_name = path + profile.name + '.csv'
            else:
                file_name = path + '_' + str(i+1) + '.csv'

            # Save the profile in file
            saveProfile( self.main_parent, profile, file_name )

        messageFileSaved()

    # --------------------------------------------
    # Delete all the profiles stored in the memory
    def clearAllProfiles(self):

        # Check if profiles are stored in the memory
        if self.profile_active is None and len(self.profile_saved) == 0:
            errorMessage("ERROR: No data in memory", "There is no profile to erase in the memory.")
            return 0

        # Ask for user confirmation
        if checkSavedData():

            # Delete all saved profiles
            self.profile_saved.clear()
            self.profile_saved = []

            # Empty the rest and refresh the display
            if self.main_parent.docks['profiling'] is not None:
                self.main_parent.docks['profiling'].updateOnTabChange()
            else:
                self.profile_active = None

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## PARTICLE TRACKING MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------------
    # Delete all the profiles stored in the memory
    def clearAllPaths(self):

        # Check if profiles are stored in the memory
        if self.path_active is None and len(self.path_saved) == 0:
            errorMessage("ERROR: No data in memory", "There is no path to erase in the memory.")
            return 0

        # Ask for user confirmation
        if checkSavedData():

            # Delete all saved profiles
            self.path_saved.clear()
            self.path_saved = []

            # Empty the rest and refresh the display
            if self.main_parent.docks['tracking'] is not None:
                self.main_parent.docks['tracking'].updateOnTabChange()
            else:
                self.path_active = None

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## MANAGE INTERACTIONS ON CLICK
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Interact with the image on a mouse click
    def actionOnClick(self, event=None):

        # Retrieve the mouse position on click
        mousePosition = np.array([event.pos().x(), event.pos().y()])
        mousePosition = (mousePosition / self.stack.zoom).astype(int)

        # Are the particle bright or dark
        brightSpot = self.main_parent.controlPanel.brightSpotCheckBox.isChecked()

        # Check what to do
        interactionType = self.main_parent.interaction_type

        # ---------------------------
        # Track the particle position
        if interactionType == 'tracking':

            # Check that the dock is open
            if self.main_parent.docks['tracking'] is None:
                self.main_parent.callTrackingDock()

            # Require an active path to interact
            if self.path_active is None:
                errorMessage('ERROR: No active path', 'An active path is required to interact with the image')

            else:
                # Get the tracking type
                trackingDock = self.main_parent.docks['tracking']
                manualTracking = trackingDock.isManualTrackingOn()

                # Manual tracking
                if manualTracking:

                    # Get the required parameters
                    canEdit, moveFrame = trackingDock.getManualParameters()
                    generateManualPath(self.path_active, mousePosition, self.stack.i_frame, canEdit=canEdit)

                    # Move to the next frame if tolerated
                    if moveFrame:
                        self.main_parent.controlPanel.nextFrame()
                    else:
                        self.updateArrays()

                # Automatic tracking
                else:

                    # Check if a path is already saved in the memory
                    doAutoTracking = True
                    if self.path_active.positions is not None:
                        doAutoTracking = checkMessage("WARNING: Path in the memory", """Frames have a saved position for this path. Performing an automatic tracking will erase all existing frames.
Are you sure want to proceed?""")

                    # Do the automatic tracking
                    if doAutoTracking:

                        # Get the required parameters
                        trackingParameters = trackingDock.getAutomaticParameters()
                        trackingParameters['invert'] = not brightSpot

                        # Track the particles
                        generateAutomaticSinglePath(self.stack.array, self.path_active, mousePosition, self.stack.i_frame, tracking_option=trackingParameters)
                        self.updateArrays()

                # Update the path completion display
                try:
                    trackingDock.numberFrameDoneOutput.setText( str(self.path_active.positions.shape[0]) )
                except:
                    pass

        # ----------------
        # Plot the profile
        elif interactionType == 'profiling':

            # Check that the dock is open
            if self.main_parent.docks['profiling'] is None:
                self.main_parent.callProfilingDock()

            # Auto-position using trackpy
            if self.main_parent.controlPanel.autoPositionCheckBox.isChecked():
                try:
                    mousePosition = findSingleParticle(self.stack.frame.raw, mousePosition, invert= not brightSpot)
                except:
                    pass

            # Update the profile menu
            try:
                self.main_parent.docks['profiling'].updateOnClick(mousePosition)
            except:
                pass

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIMPLE CLASS TO HANDLE TABS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageTab:
    def __init__(self, parent, name, imageArray, calibration):

        # General informations
        self.name = name
        self.parent = parent

        # Widget and layout
        self.widget = qtw.QWidget()
        self.layout = qtw.QVBoxLayout()

        # Image stack
        self.image = imageWidget(self, name, imageStack(imageArray), calibration )
        self.saved_data = False

        # Populate the tab
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.image)
        self.widget.setLayout(self.layout)

    ##-\-\-\-\-\-\-\-\-\-\
    ## TRANSFER PROPERTIES
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------
    # Save the properties of the tab in a dictionary
    def saveProperties(self):

        # Extract the stack
        stack = self.image.stack

        # Save the properties in a dictionnary
        properties = {
        'zoom': stack.zoom,
        'i_frame': stack.i_frame,
        'min_pv': stack.min_pv,
        'max_pv': stack.max_pv,
        'max_value': stack.max_value,
        'frame_rate': stack.frame_rate
        }

        return properties

    # ---------------------------------
    # Load properies from a dictionnary
    def loadProperties(self, properties):

        # Load all the properties into their variables
        self.image.stack.zoom = properties['zoom']
        self.image.stack.i_frame = properties['i_frame']
        self.image.stack.min_pv = properties['min_pv']
        self.image.stack.max_pv = properties['max_pv']
        self.image.stack.max_value = properties['max_value']
        self.image.stack.frame_rate = properties['frame_rate']

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import checkSavedData, errorMessage, messageFileSaved, checkMessage
from iscan.input_output.check_files import getFileOrFolder
from iscan.operations.general_functions import circleAndLineComputation
from iscan.operations.image_class import imageStack
from iscan.operations.intensity_profiling import profile, saveTable, saveProfile
from iscan.operations.particle_tracking import findSingleParticle, generateManualPath, generateAutomaticSinglePath
