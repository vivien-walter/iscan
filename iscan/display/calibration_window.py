import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR AUTOTRACK ADVANCED SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageCalibrationPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(imageCalibrationPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Image Calibration")

        # Retrieve the current calibration
        currentTab, _ = self.parent.getCurrentTab()
        self.current_image = currentTab.image
        self.spatial_calibration = self.current_image.spatial_calibration
        self.time_calibration = self.current_image.time_calibration

        # Populate the panel
        self.createCalibrationInput(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createCalibrationActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['calibration'] = None

    # -----------------------------------------------------------
    # Generate the manual input and display of the fit parameters
    def createCalibrationInput(self, parentWidget):

        # Generate the widget
        self.imageCalibrationWidget = qtw.QWidget()
        self.imageCalibrationLayout = qtw.QFormLayout(self.imageCalibrationWidget)
        self.imageCalibrationLayout.setContentsMargins(0, 0, 0, 0)

        # Spatial scale
        self.spatialCalibrationEntry = qtw.QLineEdit()
        self.spatialCalibrationEntry.returnPressed.connect(self.checkSpatialInput)
        self.spatialCalibrationEntry.setText( str( self.spatial_calibration ) )
        self.spatialCalibrationEntry.setStatusTip("Dimension of the image, using the given unit.")
        self.imageCalibrationLayout.addRow(qtw.QLabel("Image Scale (micron/px)"), self.spatialCalibrationEntry)

        # Time scale
        self.timeCalibrationEntry = qtw.QLineEdit()
        self.timeCalibrationEntry.returnPressed.connect(self.checkTimeInput)
        self.timeCalibrationEntry.setText( str(self.time_calibration) )
        self.timeCalibrationEntry.setStatusTip("Time between frames, using the given unit.")
        self.imageCalibrationLayout.addRow(qtw.QLabel("Time Scale (second/frame)"), self.timeCalibrationEntry)

        # Display the widget
        self.imageCalibrationWidget.setLayout(self.imageCalibrationLayout)
        parentWidget.addWidget(self.imageCalibrationWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createCalibrationActions(self, parentWidget):

        # Generate the widget
        self.calibrationActionsWidget = qtw.QWidget()
        self.calibrationActionsLayout = qtw.QGridLayout(self.calibrationActionsWidget)

        # Save and reset settings
        currentRow = 0
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.applyCalibration)
        self.saveButton.setStatusTip("Save the calibration.")
        self.calibrationActionsLayout.addWidget(self.saveButton, currentRow, 0)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.calibrationActionsLayout.addWidget(self.closeButton, currentRow, 1)

        # Apply changes to all windows
        currentRow += 1
        self.applyAllSelection = qtw.QCheckBox("Apply globally")
        self.applyAllSelection.setStatusTip("Apply the calibration to all windows.")
        self.calibrationActionsLayout.addWidget(self.applyAllSelection, currentRow, 0, 1, -1)

        # Display the widget
        self.calibrationActionsWidget.setLayout(self.calibrationActionsLayout)
        parentWidget.addWidget(self.calibrationActionsWidget)

    ##-\-\-\-\-\-\
    ## MANAGE INPUT
    ##-/-/-/-/-/-/

    # -------------------------------------
    # Check the entry for the particle size
    def checkSpatialInput(self, event=None):

        # Retrieve the text from the entry box
        spatialCalibration = self.spatialCalibrationEntry.text()

        # Check if the value is an integer
        spatialCalibration = string2Float(spatialCalibration)

        # Reinitialize the value if the input text is not an integer
        if spatialCalibration == False:
            self.spatialCalibrationEntry.setText( str(self.spatial_calibration) )

        else:
            self.spatial_calibration = spatialCalibration

    # -------------------------------------
    # Check the entry for the particle size
    def checkTimeInput(self, event=None):

        # Retrieve the text from the entry box
        timeCalibration = self.timeCalibrationEntry.text()

        # Check if the value is an integer
        timeCalibration = string2Float(timeCalibration)

        # Reinitialize the value if the input text is not an integer
        if timeCalibration == False:
            self.timeCalibrationEntry.setText( str(self.time_calibration) )

        else:
            self.time_calibration = timeCalibration

    ##-\-\-\-\-\-\-\-\-\
    ## APPLY THE CHANGES
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------
    # Apply the calibration
    def applyCalibration(self, event=None):

        # Retrieve all the settings
        self.spatial_calibration = string2Float( self.spatialCalibrationEntry.text() )
        self.time_calibration = string2Float( self.timeCalibrationEntry.text() )

        # Apply the changes on the current frame
        self.current_image.spatial_calibration = self.spatial_calibration
        self.current_image.time_calibration = self.time_calibration

        # Apply the changes globally if needed
        if self.applyAllSelection.isChecked():

            # Save in the intern memory for new image created
            self.parent.spatial_calibration = self.spatial_calibration
            self.parent.time_calibration = self.time_calibration

            # Modify all the open tabs
            numberTabs = self.parent.centralWidget.count()
            for i in range(numberTabs):
                tempImage = self.parent.imageTabs[i].image

                tempImage.spatial_calibration = self.spatial_calibration
                tempImage.time_calibration = self.time_calibration

        self.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.general_functions import string2Float
