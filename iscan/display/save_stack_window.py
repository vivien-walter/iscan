import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR AUTOTRACK ADVANCED SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class saveImagePanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(saveImagePanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Save Images")

        # Populate the panel
        self.createSettingsInput(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createSaveActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['save_image'] = None

    # ---------------------------------------------
    # Generate the control for the intensity limits
    def createSettingsInput(self, parentWidget):

        # Generate the widget
        self.saveSettingsWidget = qtw.QWidget()
        self.saveSettingsLayout = qtw.QVBoxLayout(self.saveSettingsWidget)

        # Name of the panel
        widgetName = qtw.QLabel("Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.saveSettingsLayout.addWidget(widgetName)

        # Prompt the file type
        typeLabel = qtw.QLabel("Image file type:")
        self.saveSettingsLayout.addWidget(typeLabel)

        self.fileTypeComboBox = qtw.QComboBox()
        self.fileTypeComboBox.addItems([".tif", ".gif"])
        self.fileTypeComboBox.setStatusTip(
            "Select the type of file to save."
        )
        self.saveSettingsLayout.addWidget(self.fileTypeComboBox)

        # Create the file type group
        self.fileTypeGroup = qtw.QGroupBox("File to save")
        self.fileTypeLayout = qtw.QVBoxLayout(self.fileTypeGroup)

        self.fileTypeGroupButton = qtw.QButtonGroup(self.fileTypeGroup)

        self.saveStackRadiobutton = qtw.QRadioButton("Image stack")
        self.saveStackRadiobutton.setChecked(True)
        self.saveStackRadiobutton.toggled.connect(self.updateComboBox)
        self.saveStackRadiobutton.setStatusTip(
            "Save the whole stack."
        )
        self.fileTypeGroupButton.addButton(self.saveStackRadiobutton)
        self.fileTypeLayout.addWidget(self.saveStackRadiobutton)

        self.saveSingleRadiobutton = qtw.QRadioButton("Single image")
        self.saveSingleRadiobutton.toggled.connect(self.updateComboBox)
        self.saveSingleRadiobutton.setStatusTip(
            "Save only the current frame."
        )
        self.fileTypeGroupButton.addButton(self.saveSingleRadiobutton)
        self.fileTypeLayout.addWidget(self.saveSingleRadiobutton)

        self.fileTypeGroup.setLayout(self.fileTypeLayout)
        self.saveSettingsLayout.addWidget(self.fileTypeGroup)

        # Create the source group
        self.sourceArrayGroup = qtw.QGroupBox("Source")
        self.sourceArrayLayout = qtw.QVBoxLayout(self.sourceArrayGroup)

        self.sourceArrayGroupButton = qtw.QButtonGroup(self.sourceArrayGroup)

        self.rawImageRadiobutton = qtw.QRadioButton("Raw Image")
        self.rawImageRadiobutton.setStatusTip(
            "Save the raw image."
        )
        self.sourceArrayGroupButton.addButton(self.rawImageRadiobutton)
        self.sourceArrayLayout.addWidget(self.rawImageRadiobutton)

        self.displayedImageRadiobutton = qtw.QRadioButton("Displayed image")
        self.displayedImageRadiobutton.setChecked(True)
        self.displayedImageRadiobutton.setStatusTip(
            "Save the displayed contrast."
        )
        self.sourceArrayGroupButton.addButton(self.displayedImageRadiobutton)
        self.sourceArrayLayout.addWidget(self.displayedImageRadiobutton)

        self.sourceArrayGroup.setLayout(self.sourceArrayLayout)
        self.saveSettingsLayout.addWidget(self.sourceArrayGroup)

        # Create the bit depth group
        self.bitDepthGroup = qtw.QGroupBox("Bit depth")
        self.bitDepthLayout = qtw.QVBoxLayout(self.bitDepthGroup)

        self.bitDepthGroupButton = qtw.QButtonGroup(self.bitDepthGroup)

        self.floatImageRadiobutton = qtw.QRadioButton("16-Bits")
        self.floatImageRadiobutton.setStatusTip(
            "Save the image as 16-Bits"
        )
        self.bitDepthGroupButton.addButton(self.floatImageRadiobutton)
        self.bitDepthLayout.addWidget(self.floatImageRadiobutton)

        self.intImageRadiobutton = qtw.QRadioButton("8-Bits")
        self.intImageRadiobutton.setChecked(True)
        self.intImageRadiobutton.setStatusTip(
            "Save the image as 8-Bits."
        )
        self.bitDepthGroupButton.addButton(self.intImageRadiobutton)
        self.bitDepthLayout.addWidget(self.intImageRadiobutton)

        self.bitDepthGroup.setLayout(self.bitDepthLayout)
        self.saveSettingsLayout.addWidget(self.bitDepthGroup)

        # Manage signed bits
        self.signedBitCheckBox = qtw.QCheckBox("The source uses unsigned bits")
        self.signedBitCheckBox.setChecked(False)
        self.saveSettingsLayout.addWidget(self.signedBitCheckBox)

        # Display the widget
        self.saveSettingsWidget.setLayout(self.saveSettingsLayout)
        parentWidget.addWidget(self.saveSettingsWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createSaveActions(self, parentWidget):

        # Generate the widget
        self.saveActionsWidget = qtw.QWidget()
        self.saveActionsLayout = qtw.QHBoxLayout(self.saveActionsWidget)

        # Auto contrast and histogram crop
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveSelection)
        self.saveButton.setStatusTip("Save the selection.")
        self.saveActionsLayout.addWidget(self.saveButton)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.saveActionsLayout.addWidget(self.closeButton)

        # Display the widget
        self.saveActionsWidget.setLayout(self.saveActionsLayout)
        parentWidget.addWidget(self.saveActionsWidget)

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # -----------------------------------------
    # Update the list of items in the combo box
    def updateComboBox(self):

        # Purge the box
        self.fileTypeComboBox.clear()

        # Re-populate the box
        if self.saveStackRadiobutton.isChecked():
            self.fileTypeComboBox.addItems([".tif", ".gif"])

        else:
            self.fileTypeComboBox.addItems([".tif", ".gif", ".png", ".bmp", ".jpg"])

    ##-\-\-\-\-\-\-\-\-\
    ## SAVE THE SELECTION
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------------
    # Save the images using the different settings
    def saveSelection(self):

        # Retrieve the settings
        saveSingle = self.saveSingleRadiobutton.isChecked()
        saveRaw = self.rawImageRadiobutton.isChecked()
        convert8Bit = self.intImageRadiobutton.isChecked()
        signedBits = self.signedBitCheckBox.isChecked()
        extension = self.fileTypeComboBox.currentText().lower()

        # Interrupt if impossible combinations are selected
        if extension == '.gif' and convert8Bit == False:
            errorMessage("ERROR: Incorrect Bit Depth","""Stack files in 16-Bits cannot be saved as .gif files.
Please select 8-bits to use this extension.""")
            return 0

        if (extension == ".bmp" or extension=='.jpg') and convert8Bit == False:
            errorMessage("ERROR: Incorrect Bit Depth","""Images in 16-Bits are only supported in .tif or .png formats.
Please select 8-bits to use other extensions.""")
            return 0

        # Get the current image
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image.stack

        # Select the type of save to do
        isSaved = saveFrames(self.parent, currentImage, saveSingle=saveSingle, extension=extension, saveRaw=saveRaw, convert8Bit=convert8Bit, signedBits=signedBits)

        # Close the current window
        if isSaved:
            self.close()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import errorMessage
from iscan.input_output.save_images import saveFrames
