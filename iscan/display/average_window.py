from math import ceil, floor
import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR FRAME AVERAGING
##-/-/-/-/-/-/-/-/-/-/-/-/-/

class frameAveragingPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(frameAveragingPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Frame Averaging")

        # Populate the panel
        self.createAverageSettings(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createDisplayCalculation(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createAverageActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.initializeOutput()
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['average'] = None

    # ---------------------------------------------
    # Generate the settings for the frame averaging
    def createAverageSettings(self, parentWidget):

        # Generate the widget
        self.averageSettingsWidget = qtw.QWidget()
        self.averageSettingsLayout = qtw.QGridLayout(self.averageSettingsWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Average Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.averageSettingsLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Average type
        currentRow += 1
        averageLabel = qtw.QLabel("Average Type")
        self.averageComboBox = qtw.QComboBox()
        self.averageComboBox.addItem("Running")
        self.averageComboBox.addItem("Group")
        self.averageComboBox.activated.connect(self.updateOutput)
        self.averageComboBox.setStatusTip(
            "Select the type of average."
        )
        self.averageSettingsLayout.addWidget(averageLabel, currentRow, 0)
        self.averageSettingsLayout.addWidget(self.averageComboBox, currentRow, 1)

        # Number of frames to average on
        currentRow += 1
        frameLabel = qtw.QLabel("Average on: (frames)")
        self.frameNumberEntry = qtw.QLineEdit()
        self.frameNumberEntry.editingFinished.connect(self.updateOutput)
        self.frameNumberEntry.setStatusTip("Enter the number of frames to average on.")
        self.averageSettingsLayout.addWidget(frameLabel, currentRow, 0)
        self.averageSettingsLayout.addWidget(self.frameNumberEntry, currentRow, 1)

        # Use the median
        currentRow += 1
        self.medianCheckBox = qtw.QCheckBox("Calculate the median")
        self.medianCheckBox.setChecked(False)
        self.averageSettingsLayout.addWidget(self.medianCheckBox, currentRow, 0, 1, -1)

        # Use all frames
        currentRow += 1
        self.allFramesCheckBox = qtw.QCheckBox("Estimate out of range frames")
        self.allFramesCheckBox.setChecked(True)
        self.allFramesCheckBox.stateChanged.connect(self.updateOutput)
        self.averageSettingsLayout.addWidget(self.allFramesCheckBox, currentRow, 0, 1, -1)

        # Average on both sides
        currentRow += 1
        self.frameAfterCheckBox = qtw.QCheckBox("Average on frames after")
        self.frameAfterCheckBox.setChecked(False)
        self.averageSettingsLayout.addWidget(self.frameAfterCheckBox, currentRow, 0, 1, -1)

        # Display the widget
        self.averageSettingsWidget.setLayout(self.averageSettingsLayout)
        parentWidget.addWidget(self.averageSettingsWidget)

    # ---------------------------------------------
    # Generate the settings for the frame averaging
    def createDisplayCalculation(self, parentWidget):

        # Generate the widget
        self.averageOutputWidget = qtw.QWidget()
        self.averageOutputLayout = qtw.QGridLayout(self.averageOutputWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Output")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.averageOutputLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Output of the averaging
        currentRow += 1
        frameLabel = qtw.QLabel("Output number of frames:")
        self.frameNumberOutput = qtw.QLineEdit()
        self.frameNumberOutput.setEnabled(False)
        self.frameNumberOutput.setStatusTip("Total number of frames in the output stack.")
        self.averageOutputLayout.addWidget(frameLabel, currentRow, 0)
        self.averageOutputLayout.addWidget(self.frameNumberOutput, currentRow, 1)

        # Display the widget
        self.averageOutputWidget.setLayout(self.averageOutputLayout)
        parentWidget.addWidget(self.averageOutputWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createAverageActions(self, parentWidget):

        # Generate the widget
        self.averageActionsWidget = qtw.QWidget()
        self.averageActionsLayout = qtw.QHBoxLayout(self.averageActionsWidget)

        # Auto contrast and histogram crop
        self.processButton = qtw.QPushButton("Process")
        self.processButton.clicked.connect(self.processAveraging)
        self.processButton.setStatusTip("Process the frame averaging.")
        self.averageActionsLayout.addWidget(self.processButton)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.averageActionsLayout.addWidget(self.closeButton)

        # Display the widget
        self.averageActionsWidget.setLayout(self.averageActionsLayout)
        parentWidget.addWidget(self.averageActionsWidget)

    ##-\-\-\-\-\-\-\-\-\-\
    ## CALCULATE THE OUTPUT
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Recalculate the output number of frames
    def updateOutput(self):

        # Retrieve all the informations
        averageType = self.averageComboBox.currentText().lower()
        allFrames = self.allFramesCheckBox.isChecked()
        n_frames = self.frameNumberEntry.text()

        # Check the format of the input
        checkedText = string2Int(n_frames, convert=False)

        # Reinitialize the value if the input text is not an integer
        if checkedText == False:
            self.frameNumberEntry.setText( str(self.n_frames) )

        else:
            # Coerce the number of frames to aveage
            self.n_frames = floor( coerceValue(checkedText, self.frame_number/2, min=2) )

            # Calculate the number of frames in the output
            if averageType == 'group':
                if allFrames:
                    outputNumber = ceil(self.frame_number / self.n_frames)
                else:
                    outputNumber = self.frame_number // self.n_frames

            elif averageType == 'running':
                if allFrames:
                    outputNumber = self.frame_number
                else:
                    outputNumber = self.frame_number - (self.n_frames - 1)

            # Update the display
            self.frameNumberOutput.setText( str(outputNumber) )
            self.frameNumberEntry.setText( str(self.n_frames) )

    # ---------------------------------
    # Initialize the output calculation
    def initializeOutput(self):

        # Get the number of frames in the stack
        currentTab, _ = self.parent.getCurrentTab()
        self.array = np.copy( currentTab.image.stack.array )
        self.frame_number = currentTab.image.stack.n_frames
        self.n_frames = round(self.frame_number * .2)

        # Update the display
        self.frameNumberEntry.setText( str(self.n_frames) )
        self.updateOutput()

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## PERFORM THE FRAME AVERAGING
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------
    # Do the frame averaging
    def processAveraging(self):

        # Retrieve the informations
        averageType = self.averageComboBox.currentText().lower()
        allFrames = self.allFramesCheckBox.isChecked()
        useMedian = self.medianCheckBox.isChecked()
        onlyAfter = self.frameAfterCheckBox.isChecked()
        n_frames = self.frameNumberEntry.text()

        # Check the format of the input
        n_frames = string2Int(n_frames, convert=False)

        # Reinitialize the value if the input text is not an integer
        if n_frames == False:
            self.frameNumberEntry.setText( str(self.n_frames) )

        else:
            # Update the number of frames to average on
            self.n_frames = n_frames

            # Do the group averaging
            if averageType == 'group':
                outputArray = groupFrameAverage(self.array, self.n_frames, use_median=useMedian, all_frames=allFrames)

            # Do the running average
            elif averageType == 'running':
                outputArray = runningFrameAverage(self.array, self.n_frames, use_median=useMedian, all_frames=allFrames, after_only=onlyAfter)

            # Save all the properties of the current tab to transfer to new one
            currentTab, _ = self.parent.getCurrentTab()
            tabProperties = currentTab.saveProperties()
            if averageType == 'group':
                tabProperties['frame_rate'] = tabProperties['frame_rate'] / n_frames

            # Open a new tab with the corrected image
            imageName = currentTab.name + "_averaged"
            self.parent.addImageTab(outputArray, name=imageName)

            # Rescale the contrast
            currentTab, _ = self.parent.getCurrentTab()
            currentTab.loadProperties(tabProperties)
            currentTab.image.updateArrays()

            # Close the window at the end
            self.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.image_calculation import groupFrameAverage, runningFrameAverage
from iscan.operations.general_functions import string2Int, coerceValue
