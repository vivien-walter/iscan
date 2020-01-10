import time

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR FRAME CONTROL
##-/-/-/-/-/-/-/-/-/-/-/-/-/


class frameControlPanel(qtw.QDockWidget):
    def __init__(self, name, parent):
        super(frameControlPanel, self).__init__(name, parent)

        # Generate the display
        self.parent = parent
        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        # Initialize the properties
        self.image_widget = None
        self.animationRun = False
        self.animationThread = None

        # Populate the panel
        self.createImageZoom(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createFrameNavigation(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createModeSelection(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createModeOptions(self.widgetLayout)

        # Fill the bottom of the panel with blank
        emptyWidget = qtw.QWidget()
        emptyWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.widgetLayout.addWidget(emptyWidget)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setWidget(self.mainWidget)
        self.setFeatures(qtw.QDockWidget.NoDockWidgetFeatures)

    # --------------------------------------
    # Generate the control of the image zoom
    def createImageZoom(self, parentWidget):

        # Generate the widget
        self.zoomSettingsWidget = qtw.QWidget()
        self.zoomSettingsLayout = qtw.QGridLayout(self.zoomSettingsWidget)
        self.zoomSettingsWidget.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Zoom Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.zoomSettingsLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Zoom modification and increase
        currentRow += 1

        self.zoomValueLabel = qtw.QLabel("Current:")
        self.zoomSettingsLayout.addWidget(self.zoomValueLabel, currentRow, 0, 1, 2)

        self.currentZoomEntry = qtw.QLineEdit()
        self.currentZoomEntry.editingFinished.connect(self.setZoomValue)
        self.currentZoomEntry.setStatusTip("Enter the desired image scale.")
        self.zoomSettingsLayout.addWidget(self.currentZoomEntry, currentRow, 2, 1, 2)

        self.increaseZoomButton = qtw.QPushButton(" + ")
        self.increaseZoomButton.setMaximumWidth(40)
        self.increaseZoomButton.setMaximumHeight(40)
        self.increaseZoomButton.clicked.connect(self.increaseZoom)
        self.increaseZoomButton.setStatusTip("Increase the image scale by 5%.")
        self.zoomSettingsLayout.addWidget(self.increaseZoomButton, currentRow, 4)

        # Zoom reset and decrease
        currentRow += 1

        self.fitZoomButton = qtw.QPushButton("Fit")
        self.fitZoomButton.clicked.connect(self.zoomToFit)
        self.fitZoomButton.setStatusTip(
            "Fit the image scale to the screen."
        )
        self.zoomSettingsLayout.addWidget(self.fitZoomButton, currentRow, 0, 1, 2)

        self.resetZoomButton = qtw.QPushButton("100%")
        self.resetZoomButton.clicked.connect(self.resetZoom)
        self.resetZoomButton.setStatusTip(
            "Reinitialise the scale to the actual image size."
        )
        self.zoomSettingsLayout.addWidget(self.resetZoomButton, currentRow, 2, 1, 2)

        self.decreaseZoomButton = qtw.QPushButton(" - ")
        self.decreaseZoomButton.setMaximumWidth(40)
        self.decreaseZoomButton.setMaximumHeight(40)
        self.decreaseZoomButton.clicked.connect(self.decreaseZoom)
        self.decreaseZoomButton.setStatusTip("Decrease the image scale by 5%.")
        self.zoomSettingsLayout.addWidget(self.decreaseZoomButton, currentRow, 4)

        # Display the widget
        self.zoomSettingsWidget.setLayout(self.zoomSettingsLayout)
        parentWidget.addWidget(self.zoomSettingsWidget)

    # --------------------------------------------
    # Generate the control of the position in time
    def createFrameNavigation(self, parentWidget):

        # Generate the widget
        self.frameNavigationWidget = qtw.QWidget()
        self.frameNavigationLayout = qtw.QGridLayout(self.frameNavigationWidget)
        self.frameNavigationLayout.setContentsMargins(15, 0, 15, 0)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Frame Navigation")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.frameNavigationLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Frame number display and selection
        currentRow += 1

        self.previousFrameButton = qtw.QPushButton("<")
        self.previousFrameButton.clicked.connect(self.previousFrame)
        self.previousFrameButton.setMaximumWidth(40)
        self.previousFrameButton.setMaximumHeight(40)
        self.previousFrameButton.setStatusTip("Move to the previous frame.")
        self.frameNavigationLayout.addWidget(self.previousFrameButton, currentRow, 0)

        self.frameSelectionEntry = qtw.QLineEdit()
        self.frameSelectionEntry.editingFinished.connect(self.moveToFrame)
        self.frameSelectionEntry.setStatusTip(
            "Current frame being displayed. Type a number to go directly to the given frame."
        )
        self.frameNavigationLayout.addWidget(self.frameSelectionEntry, currentRow, 1)

        slashLabel = qtw.QLabel("/")
        slashLabel.setAlignment(qtc.Qt.AlignCenter | qtc.Qt.AlignVCenter)
        self.frameNavigationLayout.addWidget(slashLabel, currentRow, 2)

        self.frameNumberDisplay = qtw.QLineEdit()
        self.frameNumberDisplay.setEnabled(False)
        self.frameNumberDisplay.setStatusTip(
            "Total number of frames in the image stack."
        )
        self.frameNavigationLayout.addWidget(self.frameNumberDisplay, currentRow, 3)

        self.nextFrameButton = qtw.QPushButton(">")
        self.nextFrameButton.setMaximumWidth(40)
        self.nextFrameButton.setMaximumHeight(40)
        self.nextFrameButton.clicked.connect(self.nextFrame)
        self.nextFrameButton.setStatusTip("Move to the next frame.")
        self.frameNavigationLayout.addWidget(self.nextFrameButton, currentRow, 4)

        # Frame animation
        currentRow += 1

        self.playButton = qtw.QPushButton("")
        self.playButton.setIcon( self.style().standardIcon( getattr(qtw.QStyle, 'SP_MediaPlay') ) )
        self.playButton.setMaximumWidth(40)
        self.playButton.setMaximumHeight(40)
        self.playButton.clicked.connect(self.playAnimation)
        self.playButton.setStatusTip("Start the animation.")
        self.frameNavigationLayout.addWidget(self.playButton, currentRow, 0)

        self.stopButton = qtw.QPushButton("")
        self.stopButton.setIcon( self.style().standardIcon( getattr(qtw.QStyle, 'SP_MediaStop') ) )
        self.stopButton.setMaximumWidth(40)
        self.stopButton.setMaximumHeight(40)
        self.stopButton.clicked.connect(self.stopAnimation)
        self.stopButton.setStatusTip("Stop the animation.")
        self.frameNavigationLayout.addWidget(self.stopButton, currentRow, 1)

        self.frameRateSelection = qtw.QLineEdit()
        self.frameRateSelection.editingFinished.connect(self.editFrameRate)
        self.frameRateSelection.setStatusTip(
            "Speed of the animation."
        )
        self.frameNavigationLayout.addWidget(self.frameRateSelection, currentRow, 2, 1, 2)

        speedLabel = qtw.QLabel("FPS")
        self.frameNavigationLayout.addWidget(speedLabel, currentRow, 4)

        # Frame navigation
        currentRow += 1

        self.navigationSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.navigationSlider.setMinimum(0)  # Set to a default 0 100 scale
        self.navigationSlider.setMaximum(100)
        self.navigationSlider.setValue(0)
        self.navigationSlider.sliderMoved.connect(self.sliderNavigation)
        self.navigationSlider.setStatusTip(
            "See or select the frame to display."
        )
        self.frameNavigationLayout.addWidget(self.navigationSlider, currentRow, 0, 1, -1)

        # Display the widget
        self.frameNavigationWidget.setLayout(self.frameNavigationLayout)
        parentWidget.addWidget(self.frameNavigationWidget)

    # -----------------------------------------------------
    # Generate the mode selection for the image interaction
    def createModeSelection(self, parentWidget):

        # Generate the widget
        self.modeSelectionWidget = qtw.QWidget()
        self.modeSelectionLayout = qtw.QVBoxLayout(self.modeSelectionWidget)
        # self.modeSelectionLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Mode Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.modeSelectionLayout.addWidget(widgetName)

        # Create the button group
        self.modeSelectionButtonGroup = qtw.QButtonGroup()

        self.trackingModeButton = qtw.QPushButton("Particle Tracking")
        self.modeSelectionLayout.addWidget(self.trackingModeButton)
        self.modeSelectionButtonGroup.addButton(self.trackingModeButton)
        self.trackingModeButton.setCheckable(True)
        self.trackingModeButton.setStatusTip(
            "Set mouse interaction with the image to Particle Tracking."
        )
        self.trackingModeButton.clicked.connect(self.openTrackingMenu)

        self.profilingModeButton = qtw.QPushButton("Intensity Profiling")
        self.modeSelectionLayout.addWidget(self.profilingModeButton)
        self.modeSelectionButtonGroup.addButton(self.profilingModeButton)
        self.profilingModeButton.setCheckable(True)
        self.profilingModeButton.setStatusTip(
            "Set mouse interaction with the image to Intensity Profiling."
        )
        self.profilingModeButton.clicked.connect(self.openProfilingMenu)

        self.noActionButton = qtw.QPushButton("Disable Mouse Click")
        self.modeSelectionLayout.addWidget(self.noActionButton)
        self.modeSelectionButtonGroup.addButton(self.noActionButton)
        self.noActionButton.setCheckable(True)
        self.noActionButton.setChecked(True)
        self.noActionButton.setStatusTip(
            "No interaction on mouse click on the image."
        )
        self.noActionButton.clicked.connect(self.closeDockMenus)

        # Display the widget
        self.modeSelectionWidget.setLayout(self.modeSelectionLayout)
        parentWidget.addWidget(self.modeSelectionWidget)

    # ----------------------------------------------------
    # Generate the option selections for the tracking mode
    def createModeOptions(self, parentWidget):

        # Generate the widget
        self.modeOptionsWidget = qtw.QWidget()
        self.modeOptionsLayout = qtw.QVBoxLayout(self.modeOptionsWidget)
        # self.modeOptionsLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Interactions Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.modeOptionsLayout.addWidget(widgetName)

        # General options
        self.generalOptionsGroup = qtw.QGroupBox("General options")
        self.generalOptionsLayout = qtw.QVBoxLayout(self.generalOptionsGroup)

        self.brightSpotCheckBox = qtw.QCheckBox("Bright spot")
        self.brightSpotCheckBox.setChecked(True)
        self.generalOptionsLayout.addWidget(self.brightSpotCheckBox)

        self.generalOptionsGroup.setLayout(self.generalOptionsLayout)
        self.modeOptionsLayout.addWidget(self.generalOptionsGroup)

        # Profiling options
        self.profilingOptionsGroup = qtw.QGroupBox("Profiling options")
        self.profilingOptionsLayout = qtw.QVBoxLayout(self.profilingOptionsGroup)

        self.autoPositionCheckBox = qtw.QCheckBox("Position adjustment")
        self.autoPositionCheckBox.setChecked(True)
        self.profilingOptionsLayout.addWidget(self.autoPositionCheckBox)

        self.liveFitCheckBox = qtw.QCheckBox("Live fit")
        self.liveFitCheckBox.setChecked(False)
        self.profilingOptionsLayout.addWidget(self.liveFitCheckBox)

        self.profilingOptionsGroup.setLayout(self.profilingOptionsLayout)
        self.modeOptionsLayout.addWidget(self.profilingOptionsGroup)

        # Display the widget
        self.modeOptionsWidget.setLayout(self.modeOptionsLayout)
        parentWidget.addWidget(self.modeOptionsWidget)

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## INTERACTION MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------
    # Manage the side docks
    def openTrackingMenu(self):
        self.parent.callTrackingDock()

    def openProfilingMenu(self):
        self.parent.callProfilingDock()

    def closeDockMenus(self):
        self.parent.closeAllDocks(keep = "none")

    ##-\-\-\-\-\-\-\-\-\
    ## IMAGE MODIFICATION
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------
    # Update the zoom of the stack
    def changeZoom(self, factor=1.005, value=None):

        # Calculate the minimum zoom
        imageSize = min(self.image_widget.stack.size)
        minZoom = 16 / imageSize # 16px is arbitrary here

        # Get the zoom and calculate the new value
        currentZoom = self.image_widget.stack.zoom
        newZoom = calculateValue(currentZoom, 40, min=minZoom, factor=factor, newValue=value)

        # Update the zoom entry
        self.currentZoomEntry.setText( str(newZoom*100) )

        # Update the frame display
        self.image_widget.stack.zoom = newZoom
        self.image_widget.updateArrays()

    def decreaseZoom(self, event=None):
        self.changeZoom(factor=0.995)

    def resetZoom(self, event=None):
        self.changeZoom(value=1)

    def increaseZoom(self, event=None):
        self.changeZoom()

    def zoomToFit(self, event=None):

        # Calculate the appropriate zoom
        imageSize = max(self.image_widget.stack.size)
        zoomValue = 610 / imageSize

        self.changeZoom(value=zoomValue)

    def setZoomValue(self, event=None):

        # Retrieve the text from the entry box
        frameText = self.currentZoomEntry.text()

        # Check if the value is a float
        checkedText = string2Float(frameText)

        # Reinitialize the value if the input text is not an integer
        if checkedText == False:
            self.currentZoomEntry.setText( str(self.image_widget.stack.zoom * 100) )

        else:
            self.changeZoom(value=checkedText / 100)

    # --------------------------------
    # Update the displayed frame stack
    def changeFrame(self, increment=1, frame=None):

        # Get the required values
        currentIndex = self.image_widget.stack.i_frame

        # Check the value of the index
        newIndex = calculateIndex(currentIndex, self.image_widget.stack.n_frames - 1, increment=increment, frame=frame)

        # Update the frame navigation
        self.frameSelectionEntry.setText( str(newIndex) )
        self.navigationSlider.setValue(newIndex)

        # Update the frame display
        self.image_widget.stack.i_frame = newIndex
        self.image_widget.updateArrays()

    def previousFrame(self, event=None):
        self.changeFrame(increment=-1)

    def nextFrame(self, event=None):
        self.changeFrame()

    def moveToFrame(self, event=None):

        # Retrieve the text from the entry box
        frameText = self.frameSelectionEntry.text()

        # Check if the value is an integer
        checkedText = string2Int(frameText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if checkedText == False:
            self.frameSelectionEntry.setText( str(self.image_widget.stack.i_frame) )

        else:
            self.changeFrame(frame=checkedText)

    def sliderNavigation(self, event=None):
        self.changeFrame(frame=event)

    # ---------------------------------
    # Play the stack as an animated gif
    def animateStack(self):

        # Initialise the timer
        timerBegin = time.time()

        while self.animationRun:

            # Change the display of the image
            self.image_widget.stack.i_frame = calculateIndex(self.image_widget.stack.i_frame, self.image_widget.stack.n_frames - 1, max2Zero=True)
            self.image_widget.updateArrays()

            # Update the display
            self.frameSelectionEntry.setText( str(self.image_widget.stack.i_frame) )
            self.navigationSlider.setValue(self.image_widget.stack.i_frame)

            # Calculate the loop time
            frameRate = self.image_widget.stack.frame_rate
            totalLoopTime = 1 / frameRate

            timerStop = time.time()
            realLoopTime = timerStop - timerBegin

            # Adjust to match the required frame rate
            if realLoopTime < totalLoopTime:
                time.sleep( totalLoopTime - realLoopTime )

            # Modify the frame rate if the required frame rate cannot be achieved
            elif realLoopTime > totalLoopTime*1.05:
                newFrameTime = round(1/realLoopTime)
                self.frameRateSelection.setText( str(newFrameTime) )
                self.image_widget.stack.frame_rate = newFrameTime

            # Reinitialize the timer
            timerBegin = time.time()

    def playAnimation(self):

        if not self.animationRun:
            self.animationRun = True
            self.animationThread = subThread(target=self.animateStack, name="_proc").start()

    def stopAnimation(self):
        self.animationRun = False

    def editFrameRate(self, event=None):

        # Retrieve the text from the entry box
        frameRateText = self.frameRateSelection.text()

        # Check if the value is an integer
        checkedText = string2Float(frameRateText)

        # Reinitialize the value if the input text is not an integer
        if checkedText == False:
            self.frameRateSelection.setText( str(self.image_widget.stack.frame_rate) )

        else:
            self.image_widget.stack.frame_rate = checkedText

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## UPDATE THE CONTROLLER
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Update the display when the tab is changed
    def updateTabChanged(self, imageWidget):

        # Update the linked image widget
        self.image_widget = imageWidget

        # Update the image scale selection
        self.currentZoomEntry.setText( str(imageWidget.stack.zoom * 100) )

        # Update the frame navigation
        self.frameSelectionEntry.setText( str(imageWidget.stack.i_frame) )
        self.frameNumberDisplay.setText( str(imageWidget.stack.n_frames - 1) )

        self.frameRateSelection.setText( str(imageWidget.stack.frame_rate) )

        self.navigationSlider.setMaximum(imageWidget.stack.n_frames - 1)
        self.navigationSlider.setValue(imageWidget.stack.i_frame)

        # Stop any running animation
        self.animationRun = False

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.general_functions import calculateIndex, calculateValue, string2Int, string2Float, subThread
