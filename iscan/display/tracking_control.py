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
        self.crop_size = currentTab.image.tracking_settings['crop_size']

        # Generate the display
        self.mainWidget = qtw.QWidget()
        #self.mainWidget.setMinimumWidth(550)
        self.widgetLayout = qtw.QHBoxLayout(self.mainWidget)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        # ------------------------
        # Populate the left panel
        self.panelWidget = qtw.QWidget()
        self.panelLayout = qtw.QVBoxLayout(self.panelWidget)
        # self.panelLayout.setContentsMargins(0, 0, 0, 0)

        self.createTrackType(self.panelLayout)
        self.panelLayout.addWidget(self.parent.Hseparator())
        self.createPathSelection(self.panelLayout)
        self.panelLayout.addWidget(self.parent.Hseparator())
        self.createDisplayType(self.panelLayout)
        self.panelLayout.addWidget(self.parent.Hseparator())
        self.createAutoSettings(self.panelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget = qtw.QWidget()
        emptyWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.panelLayout.addWidget(emptyWidget)

        self.panelWidget.setLayout(self.panelLayout)
        self.widgetLayout.addWidget(self.panelWidget)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setWidget(self.mainWidget)
        self.setFloating(False)

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

    #-----------------------------------------------------
    # Generate the display for the tracking type selection
    def createAutoSettings(self, parentWidget):

        # Generate the widget
        self.trackingSettingsWidget = qtw.QWidget()
        self.trackingSettingsLayout = qtw.QGridLayout(self.trackingSettingsWidget)
        self.trackingSettingsLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow= 0
        widgetName = qtw.QLabel("Auto-Tracking Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.trackingSettingsLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Area to crop for faster processing
        currentRow += 1

        self.trackingSettingsLayout.addWidget(qtw.QLabel("Crop radius (px)"), currentRow, 0)

        self.cropSizeEntry = qtw.QLineEdit()
        self.cropSizeEntry.setText( str(self.crop_size) )
        self.cropSizeEntry.editingFinished.connect(self.checkSizeEntry)
        self.cropSizeEntry.setStatusTip("Radius of the area to crop for faster processing.")
        self.trackingSettingsLayout.addWidget(self.cropSizeEntry, currentRow, 1)

        # Advanced settings
        currentRow += 1
        self.advancedSettingsButton = qtw.QPushButton("ADVANCED SETTINGS")
        self.advancedSettingsButton.clicked.connect(self.openAdvancedWindow)
        self.advancedSettingsButton.setStatusTip("Advanced settings for the automatic tracking.")
        self.trackingSettingsLayout.addWidget(self.advancedSettingsButton, currentRow, 0, 1, -1)

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
            self.numberFrameDoneOutput.setText( str(currentImage.path_active.positions.shape[0]) )

    # -------------------
    # Refresh the display
    def refreshDisplay(self):

        # Update the profiles
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.updateArrays()

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
            self.cropSizeEntry.setText( str(self.crop_size) )

        else:
            self.crop_size = cropSizeText

    # ---------------------------------
    # Open the advanced settings window
    def openAdvancedWindow(self, event=None):

        if self.parent.subWindows['auto_settings'] is None:

            # Get the number of frame in the stack
            currentTab, _ = self.parent.getCurrentTab()
            settings = currentTab.image.tracking_settings

            self.parent.subWindows['auto_settings'] = autotrackSettingsPanel(self.parent, settings)

        else:
            errorAlreadyOpen()

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

    # ----------------------------------------
    # Return parameters for automatic tracking
    def getAutomaticParameters(self):

        # Get the number of frame in the stack
        currentTab, _ = self.parent.getCurrentTab()
        settings = currentTab.image.tracking_settings

        # Write the dictionnary
        trackingOptions = {
        'crop_size': int(self.cropSizeEntry.text()),
        'particle_size': settings['particle_size'],
        'min_mass': settings['min_mass'],
        'min_frame': settings['min_frame'],
        'memory': settings['memory']
        }

        return trackingOptions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.autosettings_window import autotrackSettingsPanel
from iscan.display.error_messages import errorAlreadyOpen
from iscan.operations.general_functions import calculateIndex, string2Int
from iscan.operations.particle_tracking import trajectory, completePath, saveTrajectoryInFile
