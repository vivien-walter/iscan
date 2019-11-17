import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from iscan.image_handling import imageCorrection

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/


class backgroundCorrectionPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(backgroundCorrectionPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Background Correction")

        # Populate the panel
        self.createCorrectionSettings(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createImageSettings(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createCorrectionActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event):
        event.accept()
        self.parent.correctionWindow = None

    # ----------------------------------------------------
    # Generate the settings for the background correction
    def createCorrectionSettings(self, parentWidget):

        # Generate the widget
        self.correctionSettingsWidget = qtw.QWidget()
        self.correctionSettingsLayout = qtw.QGridLayout(self.correctionSettingsWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Correction Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.correctionSettingsLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Average
        currentRow += 1
        averageLabel = qtw.QLabel("Average Type")
        self.averageComboBox = qtw.QComboBox()
        self.averageComboBox.addItem("Median")
        self.averageComboBox.addItem("Mean")
        self.averageComboBox.setStatusTip(
            "Select the type of average to calculate the image average."
        )
        self.correctionSettingsLayout.addWidget(averageLabel, currentRow, 0)
        self.correctionSettingsLayout.addWidget(self.averageComboBox, currentRow, 1)

        # Correction
        currentRow += 1
        correctionLabel = qtw.QLabel("Correction Type")
        self.correctionComboBox = qtw.QComboBox()
        self.correctionComboBox.addItem("Division")
        self.correctionComboBox.addItem("Subtraction")
        self.correctionComboBox.setStatusTip(
            "Select the type of background correction to compute."
        )
        self.correctionSettingsLayout.addWidget(correctionLabel, currentRow, 0)
        self.correctionSettingsLayout.addWidget(self.correctionComboBox, currentRow, 1)

        # Display the widget
        self.correctionSettingsWidget.setLayout(self.correctionSettingsLayout)
        parentWidget.addWidget(self.correctionSettingsWidget)

    # -----------------------------------
    # Generate the settings of the image
    def createImageSettings(self, parentWidget):

        # Generate the widget
        self.imageSettingsWidget = qtw.QWidget()
        self.imageSettingsLayout = qtw.QGridLayout(self.imageSettingsWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Image Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.imageSettingsLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Bit depth
        currentRow += 1
        bitDepthLabel = qtw.QLabel("Bit Depth")
        self.bitDepthComboBox = qtw.QComboBox()
        self.bitDepthComboBox.addItem("16-bit")
        self.bitDepthComboBox.addItem("12-bit")
        self.bitDepthComboBox.addItem("10-bit")
        self.bitDepthComboBox.addItem("8-bit")
        self.bitDepthComboBox.setStatusTip("Select the camera bit depth.")
        self.imageSettingsLayout.addWidget(bitDepthLabel, currentRow, 0)
        self.imageSettingsLayout.addWidget(self.bitDepthComboBox, currentRow, 1)

        # Unsigned
        currentRow += 1
        self.signedCheckBox = qtw.QCheckBox("Signed bit depth")
        self.signedCheckBox.setChecked(True)
        self.signedCheckBox.setStatusTip(
            "Specify if the pixel values are taken from a signed bit depth."
        )
        self.imageSettingsLayout.addWidget(self.signedCheckBox, currentRow, 0, 1, -1)

        # Display the widget
        self.imageSettingsWidget.setLayout(self.imageSettingsLayout)
        parentWidget.addWidget(self.imageSettingsWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createCorrectionActions(self, parentWidget):

        # Generate the widget
        self.correctionActionsWidget = qtw.QWidget()
        self.correctionActionsLayout = qtw.QHBoxLayout(self.correctionActionsWidget)

        # Auto contrast and histogram crop
        self.processButton = qtw.QPushButton("Process")
        self.processButton.clicked.connect(self.runBackgroundCorrection)
        self.processButton.setStatusTip("Process the image correction.")
        self.correctionActionsLayout.addWidget(self.processButton)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.correctionActionsLayout.addWidget(self.closeButton)

        # Display the widget
        self.correctionActionsWidget.setLayout(self.correctionActionsLayout)
        parentWidget.addWidget(self.correctionActionsWidget)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## START THE BACKGROUND CORRECTION
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------------
    # Run the background correction on the current image
    def runBackgroundCorrection(self):

        # Retrieve all the settings
        averageType = self.averageComboBox.currentText().lower()
        correctionType = self.correctionComboBox.currentText().lower()
        bitDepth = self.bitDepthComboBox.currentText().lower()
        signedBits = self.signedCheckBox.isChecked()

        # Prepare the process parameters
        bitDepth = int(bitDepth.split("-")[0])

        # Process the image correction
        tabIndex = self.parent.centralWidget.currentIndex()
        previousArray = np.array(self.parent.imageTabsImage[tabIndex].array)
        newArray = imageCorrection(
            previousArray,
            averageType=averageType,
            correctionType=correctionType,
            bitDepth=bitDepth,
            signedBits=signedBits,
        )

        # Create a new tab with the image
        newName = self.parent.imageTabsImage[tabIndex].name + "_corrected"
        self.parent.addImageTab(newArray, name=newName, minPV=0.5, maxPV=1.5)
        self.parent.centralWidget.setCurrentIndex(self.parent.centralWidget.count() - 1)

        # Close the window at the end
        self.close()
