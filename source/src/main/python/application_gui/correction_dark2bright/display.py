import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CLabelledLineEdit
from application_gui.correction_dark2bright.functions import darkToBrightCorrectionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class darkToBrightCorrectionWindow(qtw.QMainWindow, darkToBrightCorrectionFunctions):
    def __init__(self, parent):
        super(darkToBrightCorrectionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        #self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Dark Particles to Bright")

        # Populate the panel
        self.createCorrectionSettings(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

        # Initialise the display
        self.initialiseDisplay()
        self.refreshFrameDisplay()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['dark_to_bright'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------------------
    # Generate the controls for the correction settings
    def createCorrectionSettings(self, parentWidget):

        # Generate the widget
        self.correctionSettingsWidget = qtw.QWidget()
        self.correctionSettingsLayout = qtw.QVBoxLayout(self.correctionSettingsWidget)

        self.correctionSettingsLayout.addWidget(CLabel("Background type:"))

        # Get the background type
        self.backgroundTypeComboBox = qtw.QComboBox()
        self.backgroundTypeComboBox.addItem('Median')
        self.backgroundTypeComboBox.addItem('Mean')
        self.backgroundTypeComboBox.activated.connect(self.refreshFrameDisplay)
        self.correctionSettingsLayout.addWidget(self.backgroundTypeComboBox)

        # Add the checkbox for intensity fluctuations corrections
        self.previewCheckBox = qtw.QCheckBox("Preview?")
        self.previewCheckBox.setChecked(True)
        self.previewCheckBox.clicked.connect(self.refreshFrameDisplay)
        self.correctionSettingsLayout.addWidget(self.previewCheckBox)

        # Display the widget
        self.correctionSettingsWidget.setLayout(self.correctionSettingsLayout)
        parentWidget.addWidget(self.correctionSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Apply")
        self.applyButton.clicked.connect(self.applySettings)
        self.applyButton.setStatusTip("Apply the correction.")
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
