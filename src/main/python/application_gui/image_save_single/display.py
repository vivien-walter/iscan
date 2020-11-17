import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator
from application_gui.image_save_single.functions import saveSingleImageFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class saveSingleImageWindow(qtw.QMainWindow, saveSingleImageFunctions):
    def __init__(self, parent, image_class=None):
        super(saveSingleImageWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Save Single Frame(s)...")

        # Populate the panel
        self.createSaveFileDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createSaveContentDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['save_single'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Generate the display to browse the file
    def createSaveFileDisplay(self, parentWidget):

        # Generate the widget
        self.saveSettingsWidget = qtw.QWidget()
        self.saveSettingsLayout = qtw.QGridLayout(self.saveSettingsWidget)

        # Format selection
        current_row = 0
        self.saveSettingsLayout.addWidget(CLabel("Format:"), current_row, 0)
        self.formatComboBox = qtw.QComboBox()
        self.formatComboBox.addItems(['Tiff','Jpeg','BMP','PNG'])
        self.saveSettingsLayout.addWidget(self.formatComboBox, current_row, 1)

        # Bitness selection
        self.bitnessSelectionGroupButton = qtw.QButtonGroup(self.saveSettingsWidget)

        current_row += 1
        self.saveSettingsLayout.addWidget(CLabel("Bitness:"), current_row, 0)
        self.bit16Radiobutton = qtw.QRadioButton("16-bits")
        self.bit16Radiobutton.setChecked( True )
        self.bitnessSelectionGroupButton.addButton(self.bit16Radiobutton)
        self.saveSettingsLayout.addWidget(self.bit16Radiobutton, current_row, 1)

        current_row += 1
        self.bit8Radiobutton = qtw.QRadioButton("8-bits")
        self.bitnessSelectionGroupButton.addButton(self.bit8Radiobutton)
        self.saveSettingsLayout.addWidget(self.bit8Radiobutton, current_row, 1)

        # Save all frames selection
        current_row += 1
        self.allFramesCheckbox = qtw.QCheckBox("Save all frames?")
        self.saveSettingsLayout.addWidget(self.allFramesCheckbox, current_row, 0, 1, 2)

        # Display the widget
        self.saveSettingsWidget.setLayout(self.saveSettingsLayout)
        parentWidget.addWidget(self.saveSettingsWidget, alignment=qtc.Qt.AlignLeft)

    # ----------------------------------
    # Generate the controls for the user
    def createSaveContentDisplay(self, parentWidget):

        # Generate the widget
        self.contentSelectionWidget = qtw.QWidget()
        self.contentSelectionLayout = qtw.QVBoxLayout(self.contentSelectionWidget)

        # Save raw data
        self.saveRawCheckbox = qtw.QCheckBox("Save raw data?")
        self.contentSelectionLayout.addWidget(self.saveRawCheckbox)

        # Save trajectory and positions
        self.saveTrajectoryCheckbox = qtw.QCheckBox("Save trajectory?")
        self.contentSelectionLayout.addWidget(self.saveTrajectoryCheckbox)

        # Save scale bar
        self.saveScaleBarCheckbox = qtw.QCheckBox("Save scale bar?")
        self.contentSelectionLayout.addWidget(self.saveScaleBarCheckbox)

        # Display the widget
        self.contentSelectionWidget.setLayout(self.contentSelectionLayout)
        parentWidget.addWidget(self.contentSelectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveInFile)
        self.saveButton.setStatusTip("Save the current tab.")
        self.saveButton.setFixedWidth(100)
        self.userActionsLayout.addWidget(self.saveButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(100)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
