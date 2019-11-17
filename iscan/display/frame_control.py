import numpy as np

from PIL import Image, ImageQt

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

import iscan.image_handling as img
from iscan.display.tracking_control import trackingControlPanel

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
        #self.widgetLayout.setSizeConstraint(qtw.QLayout.SetFixedSize)
        self.setWidget(self.mainWidget)
        self.setFloating(False)

    # --------------------------------------
    # Generate the control of the image zoom
    def createImageZoom(self, parentWidget):

        # Generate the widget
        self.zoomSettingsWidget = qtw.QWidget()
        self.zoomSettingsLayout = qtw.QGridLayout(self.zoomSettingsWidget)
        #self.zoomSettingsWidget.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Zoom Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.zoomSettingsLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Zoom modification
        currentRow += 1
        self.decreaseZoomButton = qtw.QPushButton(" - ")
        self.decreaseZoomButton.clicked.connect(self.decreaseZoom)
        self.decreaseZoomButton.setStatusTip(
            "Decrease the image scale by 5%."
        )
        self.resetZoomButton = qtw.QPushButton("100%")
        self.resetZoomButton.clicked.connect(self.resetZoom)
        self.resetZoomButton.setStatusTip(
            "Reinitialise the scale to the actual image size."
        )
        self.increaseZoomButton = qtw.QPushButton(" + ")
        self.increaseZoomButton.clicked.connect(self.increaseZoom)
        self.increaseZoomButton.setStatusTip(
            "Increase the image scale by 5%."
        )
        self.zoomSettingsLayout.addWidget(self.decreaseZoomButton, currentRow, 0, 1, 2)
        self.zoomSettingsLayout.addWidget(self.resetZoomButton, currentRow, 2, 1, 2)
        self.zoomSettingsLayout.addWidget(self.increaseZoomButton, currentRow, 4, 1, 2)

        # Zoom display
        currentRow += 1
        self.zoomValueLabel = qtw.QLabel("Current zoom:")
        self.currentZoomEntry = qtw.QLineEdit()
        self.currentZoomEntry.returnPressed.connect(self.setZoomValue)
        self.zoomSettingsLayout.addWidget(self.zoomValueLabel, currentRow, 0, 1, 3)
        self.zoomSettingsLayout.addWidget(self.currentZoomEntry, currentRow, 3, 1, 3)

        # Display the widget
        self.zoomSettingsWidget.setLayout(self.zoomSettingsLayout)
        parentWidget.addWidget(self.zoomSettingsWidget)

    # --------------------------------------------
    # Generate the control of the position in time
    def createFrameNavigation(self, parentWidget):

        # Generate the widget
        self.frameNavigationWidget = qtw.QWidget()
        self.frameNavigationLayout = qtw.QGridLayout(self.frameNavigationWidget)
        #self.frameNavigationLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Frame Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.frameNavigationLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Frame number display and selection
        currentRow += 1
        self.frameSelectionEntry = qtw.QLineEdit()
        self.frameSelectionEntry.returnPressed.connect(self.moveToFrame)
        self.frameSelectionEntry.setStatusTip(
            "Current frame being displayed. Type a number to go directly to the given frame."
        )
        self.frameNumberDisplay = qtw.QLineEdit()
        self.frameNumberDisplay.setEnabled(False)
        self.frameNumberDisplay.setStatusTip(
            "Total number of frames in the image stack."
        )
        self.frameNavigationLayout.addWidget(self.frameSelectionEntry, currentRow, 0)
        self.frameNavigationLayout.addWidget(self.frameNumberDisplay, currentRow, 1)

        # Navigation buttons
        currentRow += 1
        self.previousFrameButton = qtw.QPushButton("<")
        self.previousFrameButton.clicked.connect(self.previousFrame)
        self.previousFrameButton.setStatusTip(
            "Move to the previous frame."
        )
        self.nextFrameButton = qtw.QPushButton(">")
        self.nextFrameButton.clicked.connect(self.nextFrame)
        self.nextFrameButton.setStatusTip(
            "Move to the next frame."
        )
        self.frameNavigationLayout.addWidget(self.previousFrameButton, currentRow, 0)
        self.frameNavigationLayout.addWidget(self.nextFrameButton, currentRow, 1)

        # Display the widget
        self.frameNavigationWidget.setLayout(self.frameNavigationLayout)
        parentWidget.addWidget(self.frameNavigationWidget)

    # -----------------------------------------------------
    # Generate the mode selection for the image interaction
    def createModeSelection(self, parentWidget):

        # Generate the widget
        self.modeSelectionWidget = qtw.QWidget()
        self.modeSelectionLayout = qtw.QVBoxLayout(self.modeSelectionWidget)
        #self.modeSelectionLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Mode Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.modeSelectionLayout.addWidget(widgetName)

        # Create the button group
        self.modeSelectionButtonGroup = qtw.QButtonGroup()

        self.trackingModeButton = qtw.QPushButton("Tracking")
        self.modeSelectionLayout.addWidget(self.trackingModeButton)
        self.modeSelectionButtonGroup.addButton(self.trackingModeButton)
        self.trackingModeButton.setCheckable(True)
        self.trackingModeButton.setStatusTip(
            "Set mouse interaction with the image to Particle Tracking."
        )
        self.trackingModeButton.clicked.connect(self.displayTrackingMenu)

        self.profilingModeButton = qtw.QPushButton("Profiling")
        self.modeSelectionLayout.addWidget(self.profilingModeButton)
        self.modeSelectionButtonGroup.addButton(self.profilingModeButton)
        self.profilingModeButton.setCheckable(True)
        self.profilingModeButton.setChecked(True)
        self.profilingModeButton.setStatusTip(
            "Set mouse interaction with the image to Intensity Profiling."
        )

        # Display the widget
        self.modeSelectionWidget.setLayout(self.modeSelectionLayout)
        parentWidget.addWidget(self.modeSelectionWidget)

    # ----------------------------------------------------
    # Generate the option selections for the tracking mode
    def createModeOptions(self, parentWidget):

        # Generate the widget
        self.modeOptionsWidget = qtw.QWidget()
        self.modeOptionsLayout = qtw.QVBoxLayout(self.modeOptionsWidget)
        #self.modeOptionsLayout.setContentsMargins(0, 0, 0, 0)

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

        self.sincFrameCheckBox = qtw.QCheckBox("Synchronise tabs")
        self.sincFrameCheckBox.setChecked(True)
        self.sincFrameCheckBox.setStatusTip(
            "Synchronise the frame being displayed on all tabs."
        )
        self.generalOptionsLayout.addWidget(self.sincFrameCheckBox)

        self.generalOptionsGroup.setLayout(self.generalOptionsLayout)
        self.modeOptionsLayout.addWidget(self.generalOptionsGroup)

        # Tracking options
        self.trackingOptionsGroup = qtw.QGroupBox("Tracking options")
        self.trackingOptionsLayout = qtw.QVBoxLayout(self.trackingOptionsGroup)

        self.manualTrackingCheckBox = qtw.QCheckBox("Manual tracking")
        self.manualTrackingCheckBox.setChecked(False)
        self.trackingOptionsLayout.addWidget(self.manualTrackingCheckBox)

        self.trackingOptionsGroup.setLayout(self.trackingOptionsLayout)
        self.modeOptionsLayout.addWidget(self.trackingOptionsGroup)

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

    ##-\-\-\-\-\-\-\-\
    ## OTHER DOCK MENU
    ##-/-/-/-/-/-/-/-/

    #-------------------------------
    # Start the tracking docking menu
    def displayTrackingMenu(self):

        # WARNING: Update or remove this function after release of the tracking functions
        trackingControlPanel(self.parent)
        self.profilingModeButton.setChecked(True)

    #--------------------------------------------
    # Return the current interaction type selected
    def getInteractionType(self):

        # Lists
        modes = np.array(['tracking', 'profiling'])
        buttonState = np.array([self.trackingModeButton.isChecked(), self.profilingModeButton.isChecked()])

        # Get the enabled mode
        modeIndex = np.where(buttonState == True)[0]

        return modes[modeIndex[0]]

    ##-\-\-\-\-\-\-\-\-\
    ## IMAGE MODIFICATION
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Change the frame displayed on the screen
    def changeFrame(self, increment=1, frame=None):

        # Check the tabs synchronicity
        sincTabs = self.sincFrameCheckBox.isChecked()

        # Only change the displayed tab image
        if not sincTabs:
            tabIndex = self.parent.centralWidget.currentIndex()
            newFrame = self.parent.imageTabsImage[tabIndex].changeFrame(increment=increment, frame=frame)

        # Update all tabs
        else:
            for i in range( len(self.parent.imageTabsImage) ):
                newFrame = self.parent.imageTabsImage[i].changeFrame(increment=increment, frame=frame)

        # Edit the entry box with the new frame index
        self.frameSelectionEntry.setText(str(newFrame))

    def previousFrame(self):
        self.changeFrame(increment=-1)

    def nextFrame(self):
        self.changeFrame()

    def moveToFrame(self):

        # Retrieve the text from the entry box
        frameText = self.frameSelectionEntry.text()

        # WARNING: Insert here correction of the text if not int

        self.changeFrame(frame=int(frameText))

    #-----------------------------------------------------
    # Change the zoom of the image displayed on the screen
    def changeZoom(self, factor=1.005, value=None):

        # Check the tabs synchronicity
        sincTabs = self.sincFrameCheckBox.isChecked()

        # Only change the displayed tab image
        if not sincTabs:
            tabIndex = self.parent.centralWidget.currentIndex()
            newFrame = self.parent.imageTabsImage[tabIndex].changeZoom(factor=factor, value=value)

        # Update all tabs
        else:
            for i in range( len(self.parent.imageTabsImage) ):
                newFrame = self.parent.imageTabsImage[i].changeZoom(factor=factor, value=value)

        # Edit the entry box with the new frame index
        self.currentZoomEntry.setText(str(newFrame))

    def decreaseZoom(self):
        self.changeZoom(factor=0.995)

    def resetZoom(self):
        self.changeZoom(value=1)

    def increaseZoom(self):
        self.changeZoom()

    def setZoomValue(self):

        # Retrieve the text from the entry box
        frameText = self.currentZoomEntry.text()

        # WARNING: Insert here correction of the text if not int

        self.changeZoom(value=float(frameText)/100)
