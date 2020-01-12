import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR SELECTING TIME RANGE
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class timeRangePanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(timeRangePanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Make Substack")

        # Populate the panel
        self.timeRangeInput(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createSubstackActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['time_range'] = None

    # -----------------------------------------------------------
    # Generate the manual input and display of the fit parameters
    def timeRangeInput(self, parentWidget):

        # Generate the widget
        self.timeRangeInputWidget = qtw.QWidget()
        self.timeRangeInputLayout = qtw.QVBoxLayout(self.timeRangeInputWidget)
        self.timeRangeInputLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Time range selection:")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.timeRangeInputLayout.addWidget(widgetName)

        # Particle size
        self.rangeSelectionEntry = qtw.QLineEdit()
        self.rangeSelectionEntry.setStatusTip("Time range for the new substack.")
        self.timeRangeInputLayout.addWidget(self.rangeSelectionEntry)

        # Instructions
        instructions = qtw.QLabel("""You can specify range using e.g. 0-5 or list frames
e.g. 6,8,10 or a combination of both
e.g. 0-5,7,15-47
Note that in a range the last frame specified
is not included, i.e. 0-5 will select frames
0,1,2,3 and 4 only.""")
        self.timeRangeInputLayout.addWidget(instructions)

        # Display the widget
        self.timeRangeInputWidget.setLayout(self.timeRangeInputLayout)
        parentWidget.addWidget(self.timeRangeInputWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createSubstackActions(self, parentWidget):

        # Generate the widget
        self.correctionActionsWidget = qtw.QWidget()
        self.correctionActionsLayout = qtw.QHBoxLayout(self.correctionActionsWidget)

        # Auto contrast and histogram crop
        self.processButton = qtw.QPushButton("Process")
        self.processButton.clicked.connect(self.generateSubstack)
        self.processButton.setStatusTip("Process the image correction.")
        self.correctionActionsLayout.addWidget(self.processButton)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.correctionActionsLayout.addWidget(self.closeButton)

        # Display the widget
        self.correctionActionsWidget.setLayout(self.correctionActionsLayout)
        parentWidget.addWidget(self.correctionActionsWidget)

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE SUBSTACK
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Extract the substack using the given range
    def generateSubstack(self):

        # Extract the input
        rangeText = self.rangeSelectionEntry.text()

        # Convert the input into indices
        indicesArray = string2Indices(rangeText)

        # Get the current tab
        currentTab, _ = self.parent.getCurrentTab()
        currentStack = currentTab.image.stack

        # Generate the new array
        currentArray = currentStack.array[indicesArray]

        # Get the parameters
        minPV = currentStack.min_pv
        maxPV = currentStack.max_pv
        maxValue = currentStack.max_value

        # Open a new tab with the cropped image
        imageName = currentTab.name + "_substack"
        self.parent.addImageTab(currentArray, name=imageName)

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

from iscan.operations.general_functions import string2Indices
