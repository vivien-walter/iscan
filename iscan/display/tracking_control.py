import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/


class trackingControlPanel(qtw.QDockWidget):
    def __init__(self, name, parent):
        super(trackingControlPanel, self).__init__(name, parent)

        # Initialize the display
        self.parent = parent

        # Get the number of frame in the stack
        currentTab, _ = self.parent.getCurrentTab()
        self.total_frame = currentTab.image.stack.n_frames

        # Initialize the parameters
        self.path_index = None
        self.settings = currentTab.image.tracking_settings

        # Generate the display
        self.mainWidget = qtw.QWidget()
        #self.mainWidget.setMinimumWidth(550)
        self.widgetLayout = qtw.QHBoxLayout(self.mainWidget)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        # -----------------------
        # Populate the left panel
        self.leftPanelWidget = qtw.QWidget()
        self.leftPanelLayout = qtw.QVBoxLayout(self.leftPanelWidget)
        # self.panelLayout.setContentsMargins(0, 0, 0, 0)

        self.createTrackType(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createPathSelection(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createDisplayType(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createPreviewSettings(self.leftPanelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget = qtw.QWidget()
        emptyWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.leftPanelLayout.addWidget(emptyWidget)

        self.leftPanelWidget.setLayout(self.leftPanelLayout)
        self.widgetLayout.addWidget(self.leftPanelWidget)

        self.widgetLayout.addWidget(self.parent.Vseparator())

        # ------------------------
        # Populate the right panel
        self.rightPanelWidget = qtw.QWidget()
        self.rightPanelLayout = qtw.QVBoxLayout(self.rightPanelWidget)
        # self.panelLayout.setContentsMargins(0, 0, 0, 0)

        self.createAutoSettings(self.rightPanelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget = qtw.QWidget()
        emptyWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.rightPanelLayout.addWidget(emptyWidget)

        self.rightPanelWidget.setLayout(self.rightPanelLayout)
        self.widgetLayout.addWidget(self.rightPanelWidget)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setWidget(self.mainWidget)
        self.setFloating(False)

        # Load the parameters
        self.loadSettings()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.docks['tracking'] = None
        self.parent.resizeWindowOnDockAction()

    #-----------------------------------------------------
    # Generate the display for the tracking type selection
    def createTrackType(self, parentWidget):

        # Generate the widget
        self.trackingTypeWidget = qtw.QWidget()
        self.trackingTypeLayout = qtw.QVBoxLayout(self.trackingTypeWidget)
        self.trackingTypeLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Tracking Type")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.trackingTypeLayout.addWidget(widgetName)

        # Create the radiobuttons
        self.typeGroupButton = qtw.QButtonGroup(self.trackingTypeWidget)

        self.automaticTrackingRadiobutton = qtw.QRadioButton("Automatic")
        self.automaticTrackingRadiobutton.setChecked(True)
        self.automaticTrackingRadiobutton.setStatusTip(
            "Automatic particle tracking on the given area."
        )
        self.manualTrackingRadiobutton = qtw.QRadioButton("Manual")
        self.manualTrackingRadiobutton.setStatusTip(
            "Manual particle tracking."
        )
        self.typeGroupButton.addButton(self.automaticTrackingRadiobutton)
        self.trackingTypeLayout.addWidget(self.automaticTrackingRadiobutton)
        self.typeGroupButton.addButton(self.manualTrackingRadiobutton)
        self.trackingTypeLayout.addWidget(self.manualTrackingRadiobutton)

        # Size for the automatic tracking
        self.trackingTypeLayout.addWidget(qtw.QLabel("Crop radius (px)"))

        self.cropSizeEntry = qtw.QLineEdit()
        self.cropSizeEntry.editingFinished.connect(self.checkSizeEntry)
        self.cropSizeEntry.setStatusTip("Radius of the area to crop for faster processing.")
        self.trackingTypeLayout.addWidget(self.cropSizeEntry)

        # Display the widget
        self.trackingTypeWidget.setLayout(self.trackingTypeLayout)
        parentWidget.addWidget(self.trackingTypeWidget)

    #-----------------------------------------------------
    # Generate the display for the tracking type selection
    def createPathSelection(self, parentWidget):

        # Generate the widget
        self.pathSelectionWidget = qtw.QWidget()
        self.pathSelectionLayout = qtw.QGridLayout(self.pathSelectionWidget)
        self.pathSelectionLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow=0
        widgetName = qtw.QLabel("Path Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.pathSelectionLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Path selection
        currentRow += 1
        self.previousPathButton = qtw.QPushButton("<")
        self.previousPathButton.setMaximumWidth(40)
        self.previousPathButton.setMaximumHeight(40)
        self.previousPathButton.clicked.connect(self.previousPath)
        self.previousPathButton.setStatusTip("Select the previous path.")
        self.pathSelectionLayout.addWidget(self.previousPathButton, currentRow, 0, 1, 3)

        self.pathIndexEntry = qtw.QLineEdit()
        self.pathIndexEntry.returnPressed.connect(self.setPath)
        self.pathIndexEntry.setStatusTip(
            "Current path being selected. Type a number to select directly the given path."
        )
        self.pathSelectionLayout.addWidget(self.pathIndexEntry, currentRow, 3, 1, 6)

        self.nextPathButton = qtw.QPushButton(">")
        self.nextPathButton.setMaximumWidth(40)
        self.nextPathButton.setMaximumHeight(40)
        self.nextPathButton.clicked.connect(self.nextPath)
        self.nextPathButton.setStatusTip("Select the next path.")
        self.pathSelectionLayout.addWidget(self.nextPathButton, currentRow, 9, 1, 3)

        # Path creation and destruction
        currentRow += 1
        self.newPathButton = qtw.QPushButton("New Path")
        self.newPathButton.clicked.connect(self.createPath)
        self.newPathButton.setStatusTip("Create a new path.")
        self.pathSelectionLayout.addWidget(self.newPathButton, currentRow, 0, 1, 6)

        self.deletePathButton = qtw.QPushButton("Delete Path")
        self.deletePathButton.clicked.connect(self.deletePath)
        self.deletePathButton.setStatusTip("Delete the current path.")
        self.pathSelectionLayout.addWidget(self.deletePathButton, currentRow, 6, 1, 6)

        # Number of frame done
        currentRow += 1
        self.numberFrameDoneOutput = qtw.QLineEdit()
        self.numberFrameDoneOutput.setEnabled(False)
        self.numberFrameDoneOutput.setStatusTip(
            "Number of frame already completed in the current path."
        )
        self.pathSelectionLayout.addWidget(self.numberFrameDoneOutput, currentRow, 0, 1, 4)

        slashLabel = qtw.QLabel("/")
        slashLabel.setAlignment(qtc.Qt.AlignCenter | qtc.Qt.AlignVCenter)
        self.pathSelectionLayout.addWidget(slashLabel, currentRow, 4, 1, 4)

        self.totalNumberFrameOutput = qtw.QLineEdit()
        self.totalNumberFrameOutput.setText( str(self.total_frame) )
        self.totalNumberFrameOutput.setEnabled(False)
        self.totalNumberFrameOutput.setStatusTip(
            "Total number of frame to populate."
        )
        self.pathSelectionLayout.addWidget(self.totalNumberFrameOutput, currentRow, 8, 1, 4)

        # Path completion
        currentRow += 1
        self.completePathButton = qtw.QPushButton("Path Completion")
        self.completePathButton.clicked.connect(self.completeMissingFrame)
        self.completePathButton.setStatusTip("Complete the missing frame of the path.")
        self.pathSelectionLayout.addWidget(self.completePathButton, currentRow, 0, 1, -1)

        # Path modification
        currentRow += 1
        self.pathModificationCheckBox = qtw.QCheckBox("Enable Path Modification")
        self.pathModificationCheckBox.setStatusTip(
            "Allow path modification by clicking on the image."
        )
        self.pathSelectionLayout.addWidget(self.pathModificationCheckBox, currentRow, 0, 1, -1)

        # Path modification
        currentRow += 1
        self.frameChangeCheckBox = qtw.QCheckBox("Move forward on click")
        self.frameChangeCheckBox.setChecked(True)
        self.frameChangeCheckBox.setStatusTip(
            "Move to the next frame when the image is clicked."
        )
        self.pathSelectionLayout.addWidget(self.frameChangeCheckBox, currentRow, 0, 1, -1)

        # Display the widget
        self.pathSelectionWidget.setLayout(self.pathSelectionLayout)
        parentWidget.addWidget(self.pathSelectionWidget)

    #---------------------------------------------------
    # Generate the display for the path display selection
    def createDisplayType(self, parentWidget):

        # Generate the widget
        self.displayTypeWidget = qtw.QWidget()
        self.displayTypeLayout = qtw.QVBoxLayout(self.displayTypeWidget)
        self.displayTypeLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Path Display")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.displayTypeLayout.addWidget(widgetName)

        # Create the radiobuttons for path selection
        self.pathSelectionGroup = qtw.QGroupBox("Path selection")
        self.pathSelectionLayout = qtw.QVBoxLayout(self.pathSelectionGroup)

        self.pathGroupButton = qtw.QButtonGroup(self.pathSelectionGroup)

        self.currentPathRadiobutton = qtw.QRadioButton("Show current path")
        self.currentPathRadiobutton.toggled.connect(self.refreshDisplay)
        self.currentPathRadiobutton.setStatusTip(
            "Display only the selected path."
        )
        self.allPathRadiobutton = qtw.QRadioButton("Show all paths")
        self.allPathRadiobutton.setChecked(True)
        self.allPathRadiobutton.toggled.connect(self.refreshDisplay)
        self.allPathRadiobutton.setStatusTip(
            "Display all the path in the memory."
        )
        self.pathGroupButton.addButton(self.currentPathRadiobutton)
        self.pathSelectionLayout.addWidget(self.currentPathRadiobutton)
        self.pathGroupButton.addButton(self.allPathRadiobutton)
        self.pathSelectionLayout.addWidget(self.allPathRadiobutton)

        self.pathSelectionGroup.setLayout(self.pathSelectionLayout)
        self.displayTypeLayout.addWidget(self.pathSelectionGroup)

        # Selection of the time range
        self.timeDisplayGroup = qtw.QGroupBox("Display time")
        self.timeDisplayLayout = qtw.QVBoxLayout(self.timeDisplayGroup)

        self.frameOnlyCheckBox = qtw.QCheckBox("Display frame only")
        self.frameOnlyCheckBox.toggled.connect( lambda: self.changeTimeDisplay(self.frameOnlyCheckBox) )
        self.frameOnlyCheckBox.setStatusTip(
            "Display only the position on the current frame."
        )
        self.timeDisplayLayout.addWidget(self.frameOnlyCheckBox)

        self.reducedFrameCheckBox = qtw.QCheckBox("Reduced frame range")
        self.reducedFrameCheckBox.toggled.connect( lambda: self.changeTimeDisplay(self.reducedFrameCheckBox) )
        self.reducedFrameCheckBox.setStatusTip(
            "Display a reduced time range around the current frame."
        )
        self.timeDisplayLayout.addWidget(self.reducedFrameCheckBox)

        self.timeDisplayGroup.setLayout(self.timeDisplayLayout)
        self.displayTypeLayout.addWidget(self.timeDisplayGroup)

        # Display the widget
        self.displayTypeWidget.setLayout(self.displayTypeLayout)
        parentWidget.addWidget(self.displayTypeWidget)

    # ------------------------------------
    # Generate the display for the preview
    def createPreviewSettings(self, parentWidget):

        # Generate the widget
        self.previewSettingsWidget = qtw.QWidget()
        self.previewSettingsLayout = qtw.QVBoxLayout(self.previewSettingsWidget)
        self.previewSettingsLayout.setContentsMargins(0, 0, 0, 0)

        # Advanced settings
        self.previewSettingsButton = qtw.QPushButton("Preview")
        self.previewSettingsButton.clicked.connect(self.previewSettings)
        self.previewSettingsButton.setStatusTip("Preview the selection on the current using the current settings.")
        self.previewSettingsLayout.addWidget(self.previewSettingsButton)

        # Display the widget
        self.previewSettingsWidget.setLayout(self.previewSettingsLayout)
        parentWidget.addWidget(self.previewSettingsWidget)

    #-----------------------------------------------------
    # Generate the display for the tracking type selection
    def createAutoSettings(self, parentWidget):

        # Generate the widget
        self.trackingSettingsWidget = qtw.QWidget()
        self.trackingSettingsLayout = qtw.QVBoxLayout(self.trackingSettingsWidget)
        self.trackingSettingsLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Advanced Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.trackingSettingsLayout.addWidget(widgetName)

        # Size options
        self.sizeOptionsGroup = qtw.QGroupBox("Object size")
        self.sizeOptionsLayout = qtw.QGridLayout(self.sizeOptionsGroup)

        currentRow = 0
        self.sizeOptionsLayout.addWidget(qtw.QLabel("Min size (px)"), currentRow, 0)
        self.sizeOptionsLayout.addWidget(qtw.QLabel("Max size (px)"), currentRow, 1)

        currentRow += 1
        self.particleSizeEntry = qtw.QLineEdit()
        self.particleSizeEntry.editingFinished.connect(self.checkParticleInput)
        self.particleSizeEntry.setStatusTip("Expected diameter of the particle.")
        self.sizeOptionsLayout.addWidget(self.particleSizeEntry, currentRow, 0)

        self.maximumSizeEntry = qtw.QLineEdit()
        self.maximumSizeEntry.editingFinished.connect(self.checkMaxSizeEntry)
        self.maximumSizeEntry.setStatusTip("Maximum radius-of-gyration of brightness.")
        self.sizeOptionsLayout.addWidget(self.maximumSizeEntry, currentRow, 1)

        currentRow += 1
        self.sizeOptionsLayout.addWidget(qtw.QLabel("Separation (px)"), currentRow, 0)

        currentRow += 1
        self.separationEntry = qtw.QLineEdit()
        self.separationEntry.editingFinished.connect(self.checkSeparationEntry)
        self.separationEntry.setStatusTip("Minimum separation between features.")
        self.sizeOptionsLayout.addWidget(self.separationEntry, currentRow, 0)

        self.sizeOptionsGroup.setLayout(self.sizeOptionsLayout)
        self.trackingSettingsLayout.addWidget(self.sizeOptionsGroup)

        # Brightness options
        self.brightnessOptionsGroup = qtw.QGroupBox("Object brightness")
        self.brightnessOptionsLayout = qtw.QGridLayout(self.brightnessOptionsGroup)

        currentRow = 0
        self.brightnessOptionsLayout.addWidget(qtw.QLabel("Min bright (AU)"), currentRow, 0)
        self.brightnessOptionsLayout.addWidget(qtw.QLabel("Threshold (AU)"), currentRow, 1)

        currentRow += 1
        self.minimumBrightnessEntry = qtw.QLineEdit()
        self.minimumBrightnessEntry.editingFinished.connect(self.checkMassEntry)
        self.minimumBrightnessEntry.setStatusTip("Minimum integrated brightness of the object.")
        self.brightnessOptionsLayout.addWidget(self.minimumBrightnessEntry, currentRow, 0)

        self.brightnessThresholdEntry = qtw.QLineEdit()
        self.brightnessThresholdEntry.editingFinished.connect(self.checkThresholdEntry)
        self.brightnessThresholdEntry.setStatusTip("Clip bandpass result below the threshold value.")
        self.brightnessOptionsLayout.addWidget(self.brightnessThresholdEntry, currentRow, 1)

        currentRow += 1
        self.brightnessOptionsLayout.addWidget(qtw.QLabel("Bright ratio (%)"), currentRow, 0)

        currentRow += 1
        self.percentileEntry = qtw.QLineEdit()
        self.percentileEntry.editingFinished.connect(self.checkRatioEntry)
        self.percentileEntry.setStatusTip("Features must have a peak brighter than pixels in the given percentile to be selected.")
        self.brightnessOptionsLayout.addWidget(self.percentileEntry, currentRow, 0)

        self.brightnessOptionsGroup.setLayout(self.brightnessOptionsLayout)
        self.trackingSettingsLayout.addWidget(self.brightnessOptionsGroup)

        # Gaussian filter options
        self.gaussianOptionsGroup = qtw.QGroupBox("Gaussian filter")
        self.gaussianOptionsLayout = qtw.QVBoxLayout(self.gaussianOptionsGroup)

        self.gaussianOptionsLayout.addWidget(qtw.QLabel("Kernel width (px)"))
        self.noiseWidthEntry = qtw.QLineEdit()
        self.noiseWidthEntry.editingFinished.connect(self.checkKernelEntry)
        self.noiseWidthEntry.setStatusTip("Width of the Gaussian blurring kernel to attenuate noise.")
        self.gaussianOptionsLayout.addWidget(self.noiseWidthEntry)

        self.gaussianOptionsLayout.addWidget(qtw.QLabel("Smoothing size (px)"))
        self.smoothingSizeEntry = qtw.QLineEdit()
        self.smoothingSizeEntry.editingFinished.connect(self.checkSmoothEntry)
        self.smoothingSizeEntry.setStatusTip("Size of the sides of the square kernel used in rolling average smoothing.")
        self.gaussianOptionsLayout.addWidget(self.smoothingSizeEntry)

        self.gaussianOptionsGroup.setLayout(self.gaussianOptionsLayout)
        self.trackingSettingsLayout.addWidget(self.gaussianOptionsGroup)

        # Gaussian filter options
        self.persistenceGroup = qtw.QGroupBox("Particle persistence")
        self.persistenceLayout = qtw.QVBoxLayout(self.persistenceGroup)

        self.persistenceLayout.addWidget(qtw.QLabel("Minimum time (frame)"))
        self.minFrameEntry = qtw.QLineEdit()
        self.minFrameEntry.editingFinished.connect(self.checkFrameNumberEntry)
        self.minFrameEntry.setStatusTip("Minimum time a path should last to be considered as a path.")
        self.persistenceLayout.addWidget(self.minFrameEntry)

        self.persistenceLayout.addWidget(qtw.QLabel("Frame memory (frame)"))
        self.frameMemoryEntry = qtw.QLineEdit()
        self.frameMemoryEntry.editingFinished.connect(self.checkMemoryEntry)
        self.frameMemoryEntry.setStatusTip("Number of frames a particle can disappear to still be considered as a path.")
        self.persistenceLayout.addWidget(self.frameMemoryEntry)

        self.persistenceGroup.setLayout(self.persistenceLayout)
        self.trackingSettingsLayout.addWidget(self.persistenceGroup)

        # Reset settings
        self.resetSettingsButton = qtw.QPushButton("Reset")
        self.resetSettingsButton.clicked.connect(self.resetSettings)
        self.resetSettingsButton.setStatusTip("Return the settings to the default values.")
        self.trackingSettingsLayout.addWidget(self.resetSettingsButton)

        # Display the widget
        self.trackingSettingsWidget.setLayout(self.trackingSettingsLayout)
        parentWidget.addWidget(self.trackingSettingsWidget)

    ##-\-\-\-\-\-\-\-\
    ## PATH MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    #-----------------------------------------------
    # Change the current path selected and displayed
    def changeCurrentPath(self, increment=1, pathNumber = None):

        # Stop the function if no path are in the memory
        if self.path_index is None:
            return 0

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Calculate the new path number
        self.path_index = calculateIndex( self.path_index , len(currentImage.path_saved)-1, increment=increment, frame=pathNumber, max2Zero=True )

        # Change the active path
        currentImage.path_active = currentImage.path_saved[ self.path_index ]
        self.pathIndexEntry.setText( str(self.path_index) )

        if currentImage.path_active.positions is not None:
            self.numberFrameDoneOutput.setText( str(currentImage.path_active.positions.shape[0]) )
        else:
            self.numberFrameDoneOutput.setText("0")

        currentImage.updateArrays()

    def previousPath(self):
        self.changeCurrentPath(increment=-1)

    def nextPath(self):
        self.changeCurrentPath()

    def setPath(self):

        # Retrieve the text from the entry box
        pathNumber = self.pathIndexEntry.text()

        # Check if the value is an integer
        checkedText = string2Int(pathNumber, convert=False)

        # Reinitialize the value if the input text is not an integer
        if checkedText == False:
            self.pathIndexEntry.setText( str(self.path_index) )

        else:
            self.changeCurrentPath(pathNumber=checkedText)

    #---------------------------
    # Create a new tracking path
    def createPath(self):

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Append the path to the list of saved path
        newPath = trajectory()
        currentImage.path_saved.append( newPath )
        currentImage.path_active = newPath

        # Update the display
        self.path_index = len(currentImage.path_saved)-1
        self.pathIndexEntry.setText( str( self.path_index ) )
        self.numberFrameDoneOutput.setText( "0" )
        currentImage.updateArrays()

    # -------------------------
    # Complete the current path
    def completeMissingFrame(self):

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Interrupt if there is no active path or no frame currently saved
        if currentImage.path_active is None:
            return 0
        if currentImage.path_active.positions is None:
            return 0

        # Complete the position
        completePath(currentImage.path_active, self.total_frame)
        self.numberFrameDoneOutput.setText( str(currentImage.path_active.positions.shape[0]) )

        # Refresh the display
        currentImage.updateArrays()

    # ------------------------------------
    # Save the current path in a data file
    def saveCurrentPath(self, file_type='csv'):

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Check if an active path exists and is filled
        if currentImage.path_active is None:
            return 0
        if currentImage.path_active.positions is None:
            return 0

        # Generate the required file
        saveTrajectoryInFile(self.parent, currentImage.path_active, file_type=file_type)

    #-----------------------
    # Delete the current path
    def deletePath(self):

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Remove the path from the list
        currentImage.path_active = None
        del currentImage.path_saved[ self.path_index ]

        # Update the path display to the previous path in the list
        if len(currentImage.path_saved) > 0:

            # Set equal to 0 if the path deleted was the first one
            if self.path_index != 0:
                self.path_index -= 1

            # Set the new current path as active
            currentImage.path_active = currentImage.path_saved[ self.path_index ]

            # Update the display
            self.pathIndexEntry.setText( str(self.path_index) )
            self.numberFrameDoneOutput.setText( str(currentImage.path_active.positions.shape[0]) )
            currentImage.updateArrays()

        # Create a new path if the last one of the list has been deleted
        else:
            self.createPath()

    ##-\-\-\-\-\-\-\-\
    ## DISPLAY OPTIONS
    ##-/-/-/-/-/-/-/-/

    # --------------------------
    # Change the display in time
    def changeTimeDisplay(self, checkbox):

        # Check all the checkboxes
        for tmp_checkbox in [self.frameOnlyCheckBox, self.reducedFrameCheckBox]:

            # Deselect the old checkbox if another one is selected
            if tmp_checkbox.isChecked() and checkbox.isChecked():
                tmp_checkbox.setChecked( tmp_checkbox == checkbox )

        # Change the type of time display
        statusArray = np.array( [
        [self.frameOnlyCheckBox.isChecked(), 'single'],
        [self.reducedFrameCheckBox.isChecked(), 'reduced']
        ] )

        selection = np.where(statusArray[:,0] == str(True))[0]
        if selection.shape[0] == 0:
            time_type = "all"
        else:
            time_type = statusArray[selection, 1][0]

        # Update the profiles
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        for path in currentImage.path_saved:
            path.time_option = time_type

        # Refresh the window
        currentImage.updateArrays()

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE DOCK
    ##-/-/-/-/-/-/-/-/

    # ------------------------------
    # Update when the tab is changed
    def updateOnTabChange(self):

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Change the number of frames in the tab
        self.total_frame = currentImage.stack.n_frames
        self.totalNumberFrameOutput.setText( str(self.total_frame) )

        # Reset the display if there is no path in the tab memory
        if len(currentImage.path_saved) == 0:

            # Select the index
            self.path_index = None

            # Reset the display
            self.pathIndexEntry.setText( "" )
            self.numberFrameDoneOutput.setText( "" )

        # Load the informations stored in the memory
        else:

            # Select the index and path
            self.path_index = 0
            currentImage.path_active = currentImage.path_saved[0]

            # Update the display
            self.pathIndexEntry.setText( "0" )

            pathPosition = currentImage.path_active.positions
            if pathPosition is not None:
                self.numberFrameDoneOutput.setText( str(pathPosition.shape[0]) )
            else:
                self.numberFrameDoneOutput.setText( "0" )

    # -------------------
    # Refresh the display
    def refreshDisplay(self):

        # Update the profiles
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.updateArrays()

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## RETRIEVE TRACKING INTERACTION
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Check if the manual tracking is on
    def isManualTrackingOn(self):

        return self.manualTrackingRadiobutton.isChecked()

    # -------------------------------------
    # Return parameters for manual tracking
    def getManualParameters(self):

        # Retrieve the options
        canEdit = self.pathModificationCheckBox.isChecked()
        moveFrame = self.frameChangeCheckBox.isChecked()

        return canEdit, moveFrame

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## GET TRACKING PARAMETERS
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkSizeEntry(self, event=None):

        # Retrieve the text from the entry box
        cropSizeText = self.cropSizeEntry.text()

        # Check if the value is an integer
        cropSizeText = string2Int(cropSizeText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if cropSizeText == False:
            self.cropSizeEntry.setText( str(self.settings['crop_size']) )

        else:
            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['crop_size'] = cropSizeText
            self.settings['crop_size'] = cropSizeText

    # -------------------------------------
    # Check the entry for the particle size
    def checkParticleInput(self, event=None):

        # Retrieve the text from the entry box
        particleSizeText = self.particleSizeEntry.text()

        # Check if the value is an integer
        particleSizeText = string2Int(particleSizeText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if particleSizeText == False:
            self.particleSizeEntry.setText( str(self.settings['particle_size']) )

        else:
            # Turn even numbers into odd ones
            if particleSizeText % 2 == 0:
                particleSizeText += 1
                self.particleSizeEntry.setText( str(particleSizeText) )

            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['particle_size'] = particleSizeText
            self.settings['particle_size'] = particleSizeText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkMaxSizeEntry(self, event=None):

        # Retrieve the text from the entry box
        maxSizeText = self.maximumSizeEntry.text()

        # Get the current tab
        currentTab, _ = self.parent.getCurrentTab()

        # Process if None
        if maxSizeText.lower() == "none":
            currentTab.image.tracking_settings['max_size'] = None
            self.settings['max_size'] = None

        else:
            # Check if the value is an integer
            maxSizeText = string2Int(maxSizeText, convert=False)

            # Reinitialize the value if the input text is not an integer
            if maxSizeText == False:
                self.maximumSizeEntry.setText( str(self.settings['max_size']) )

            else:
                # Save the results
                currentTab.image.tracking_settings['max_size'] = maxSizeText
                self.settings['max_size'] = maxSizeText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkSeparationEntry(self, event=None):

        # Retrieve the text from the entry box
        separationText = self.separationEntry.text()

        # Get the current tab
        currentTab, _ = self.parent.getCurrentTab()

        # Process if None
        if separationText.lower() == "none":
            currentTab.image.tracking_settings['separation'] = None
            self.settings['separation'] = None

        else:
            # Check if the value is an integer
            separationText = string2Int(separationText, convert=False)

            # Reinitialize the value if the input text is not an integer
            if separationText == False:
                self.separationEntry.setText( str(self.settings['separation']) )

            else:
                # Save the results
                currentTab.image.tracking_settings['separation'] = separationText
                self.settings['separation'] = separationText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkMassEntry(self, event=None):

        # Retrieve the text from the entry box
        minMassText = self.minimumBrightnessEntry.text()

        # Check if the value is an integer
        minMassText = string2Int(minMassText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if minMassText == False:
            self.minimumBrightnessEntry.setText( str(self.settings['min_mass']) )

        else:
            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['min_mass'] = minMassText
            self.settings['min_mass'] = minMassText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkThresholdEntry(self, event=None):

        # Retrieve the text from the entry box
        thresholdText = self.brightnessThresholdEntry.text()

        # Get the current tab
        currentTab, _ = self.parent.getCurrentTab()

        # Process if None
        if thresholdText.lower() == "none":
            currentTab.image.tracking_settings['threshold'] = None
            self.settings['threshold'] = None

        else:
            # Check if the value is an integer
            thresholdText = string2Int(thresholdText, convert=False)

            # Reinitialize the value if the input text is not an integer
            if thresholdText == False:
                self.brightnessThresholdEntry.setText( str(self.settings['threshold']) )

            else:
                # Save the results
                currentTab.image.tracking_settings['threshold'] = thresholdText
                self.settings['threshold'] = thresholdText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkRatioEntry(self, event=None):

        # Retrieve the text from the entry box
        ratioText = self.percentileEntry.text()

        # Check if the value is an integer
        ratioText = string2Int(ratioText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if ratioText == False:
            self.percentileEntry.setText( str(self.settings['percentile']) )

        else:
            # Coerce the value
            ratioText = coerceValue(ratioText, 100)
            self.percentileEntry.setText( str(ratioText) )

            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['percentile'] = ratioText
            self.settings['percentile'] = ratioText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkKernelEntry(self, event=None):

        # Retrieve the text from the entry box
        noiseText = self.noiseWidthEntry.text()

        # Check if the value is an integer
        noiseText = string2Int(noiseText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if noiseText == False:
            self.noiseWidthEntry.setText( str(self.settings['noise_size']) )

        else:
            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['noise_size'] = noiseText
            self.settings['noise_size'] = noiseText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkSmoothEntry(self, event=None):

        # Retrieve the text from the entry box
        smoothingText = self.smoothingSizeEntry.text()

        # Get the current tab
        currentTab, _ = self.parent.getCurrentTab()

        # Process if None
        if smoothingText.lower() == "none":
            currentTab.image.tracking_settings['smoothing_size'] = None
            self.settings['smoothing_size'] = None

        else:
            # Check if the value is an integer
            smoothingText = string2Int(smoothingText, convert=False)

            # Reinitialize the value if the input text is not an integer
            if smoothingText == False:
                self.smoothingSizeEntry.setText( str(self.settings['smoothing_size']) )

            else:
                # Save the results
                currentTab.image.tracking_settings['smoothing_size'] = smoothingText
                self.settings['smoothing_size'] = smoothingText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkFrameNumberEntry(self, event=None):

        # Retrieve the text from the entry box
        frameNumberText = self.minFrameEntry.text()

        # Check if the value is an integer
        frameNumberText = string2Int(frameNumberText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if frameNumberText == False:
            self.minFrameEntry.setText( str(self.settings['min_frame']) )

        else:
            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['min_frame'] = frameNumberText
            self.settings['min_frame'] = frameNumberText

    # ---------------------------------------
    # Check the entry of the crop size widget
    def checkMemoryEntry(self, event=None):

        # Retrieve the text from the entry box
        memoryText = self.frameMemoryEntry.text()

        # Check if the value is an integer
        memoryText = string2Int(memoryText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if memoryText == False:
            self.frameMemoryEntry.setText( str(self.settings['memory']) )

        else:
            # Save the results
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.image.tracking_settings['memory'] = memoryText
            self.settings['memory'] = memoryText

    # ----------------------------------------
    # Return parameters for automatic tracking
    def loadSettings(self):

        # Get the number of frame in the stack
        currentTab, _ = self.parent.getCurrentTab()
        self.settings = currentTab.image.tracking_settings

        # Load settings for crop
        self.cropSizeEntry.setText( str(self.settings['crop_size']) )

        # Load settings for size
        self.particleSizeEntry.setText( str(self.settings['particle_size']) )
        self.maximumSizeEntry.setText( str(self.settings['max_size']) )
        self.separationEntry.setText( str(self.settings['separation']) )

        # Load settings for brightness
        self.minimumBrightnessEntry.setText( str(self.settings['min_mass']) )
        self.brightnessThresholdEntry.setText( str(self.settings['threshold']) )
        self.percentileEntry.setText( str(self.settings['percentile']) )

        # Load settings for the filter
        self.noiseWidthEntry.setText( str(self.settings['noise_size']) )
        self.smoothingSizeEntry.setText( str(self.settings['smoothing_size']) )

        # Load settings for the memory
        self.minFrameEntry.setText( str(self.settings['min_frame']) )
        self.frameMemoryEntry.setText( str(self.settings['memory']) )

    # ------------------------------------------------------
    # Load the default parameters for the automatic tracking
    def resetSettings(self):

        # Load the tab and settings
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.tracking_settings = currentTab.image.default_settings.copy()

        # Reset the settings
        self.loadSettings()

    ##-\-\-\-\-\-\-\-\-\
    ## PREVIEW GENERATION
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------------------------
    # Generate a preview of the particle tracking using the current settings
    def previewSettings(self):

        # Retrieve the current settings
        brightSpot = self.parent.controlPanel.brightSpotCheckBox.isChecked()

        # Get the current frame
        currentTab, _ = self.parent.getCurrentTab()
        currentArray = currentTab.image.stack.frame.raw

        # Find all particles in the image
        particlePositions = locateParticle(currentArray,
        invert=not brightSpot,
        particle_size = self.settings['particle_size'],
        min_mass = self.settings['min_mass'],
        max_size = self.settings['max_size'],
        separation = self.settings['separation'],
        noise_size = self.settings['noise_size'],
        smoothing_size = self.settings['smoothing_size'],
        threshold = self.settings['threshold'],
        percentile = self.settings['percentile']
        )

        # Display the result
        currentTab.image.updateArrays(preview_tracking=particlePositions)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import errorAlreadyOpen
from iscan.operations.general_functions import calculateIndex, string2Int, coerceValue
from iscan.operations.particle_tracking import trajectory, completePath, saveTrajectoryInFile, locateParticle
