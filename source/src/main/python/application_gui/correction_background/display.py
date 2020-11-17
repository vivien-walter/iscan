import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CLabelledLineEdit
from application_gui.correction_background.functions import backgroundCorrectionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class backgroundCorrectionWindow(qtw.QMainWindow, backgroundCorrectionFunctions):
    def __init__(self, parent, image_array=None):
        super(backgroundCorrectionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_array = image_array
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Background Correction")

        # Populate the panel
        self.createCorrectionSettings(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createCorrectionOptions(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

        # Update the panel with image content
        self.analyseStack()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['background_correction'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------------------
    # Generate the controls for the correction settings
    def createCorrectionSettings(self, parentWidget):

        # Generate the widget
        self.correctionSettingsWidget = qtw.QWidget()
        self.correctionSettingsLayout = qtw.QVBoxLayout(self.correctionSettingsWidget)

        self.correctionSettingsLayout.addWidget(CLabel("Correction settings:"))

        # Get the correction type
        self.correctionTypeComboBox = qtw.QComboBox()
        self.correctionTypeComboBox.addItem('Division')
        self.correctionTypeComboBox.addItem('Subtraction')
        self.correctionSettingsLayout.addWidget(self.correctionTypeComboBox)

        # Get the background type
        self.backgroundTypeComboBox = qtw.QComboBox()
        self.backgroundTypeComboBox.addItem('Median')
        self.backgroundTypeComboBox.addItem('Mean')
        self.correctionSettingsLayout.addWidget(self.backgroundTypeComboBox)

        # Add the checkbox for intensity fluctuations corrections
        self.correctFluctuationsCheckBox = qtw.QCheckBox("Correct intensity fluctuations")
        self.correctFluctuationsCheckBox.setChecked(True)
        self.correctionSettingsLayout.addWidget(self.correctFluctuationsCheckBox)

        # Display the widget
        self.correctionSettingsWidget.setLayout(self.correctionSettingsLayout)
        parentWidget.addWidget(self.correctionSettingsWidget)

    # -------------------------------------------------
    # Generate the controls for the correction settings
    def createCorrectionOptions(self, parentWidget):

        # Generate the widget
        self.correctionOptionsWidget = qtw.QWidget()
        self.correctionOptionsLayout = qtw.QVBoxLayout(self.correctionOptionsWidget)

        self.correctionOptionsLayout.addWidget(CLabel("Options:"))

        # Crop selection
        self.cropCheckBox = qtw.QCheckBox('Crop the image?')
        self.cropCheckBox.setEnabled(False)
        self.correctionOptionsLayout.addWidget( self.cropCheckBox)

        # Crop size selection
        cropSizeEntry_l, self.cropSizeEntry = CLabelledLineEdit("Crop size (px):", bold=False)
        self.cropSizeEntry.setText( str(self.parent.config.crop_size) )
        self.correctionOptionsLayout.addWidget(cropSizeEntry_l)

        # Signed bit correction
        self.signCorrectionCheckBox = qtw.QCheckBox('Correct signed bits?')
        self.signCorrectionCheckBox.setEnabled(False)
        self.correctionOptionsLayout.addWidget( self.signCorrectionCheckBox)

        # Signed bit correction
        self.replaceTabCheckBox = qtw.QCheckBox('Replace current tab?')
        self.replaceTabCheckBox.setChecked(True)
        self.correctionOptionsLayout.addWidget( self.replaceTabCheckBox)

        # Display the widget
        self.correctionOptionsWidget.setLayout(self.correctionOptionsLayout)
        parentWidget.addWidget(self.correctionOptionsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Apply")
        self.applyButton.clicked.connect(self.processImage)
        self.applyButton.setStatusTip("Apply the background correction.")
        self.applyButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.applyButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
