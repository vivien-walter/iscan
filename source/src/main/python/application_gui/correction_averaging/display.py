import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator
from application_gui.correction_averaging.functions import frameAveragingFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class frameAveragingWindow(qtw.QMainWindow, frameAveragingFunctions):
    def __init__(self, parent, image_array=None):
        super(frameAveragingWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_array = image_array
        self.max_n = self.image_array.shape[0]
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Frame Averaging")

        # Populate the panel
        self.createCorrectionSettings(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createInformationDisplay(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(300,350)

        # Update the panel with image content
        self.calculateInfos()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['frame_average'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------------------
    # Generate the controls for the correction settings
    def createCorrectionSettings(self, parentWidget):

        # Generate the widget
        self.correctionSettingsWidget = qtw.QWidget()
        self.correctionSettingsLayout = qtw.QGridLayout(self.correctionSettingsWidget)

        # Get the correction type
        current_row = 0
        self.averagingTypeComboBox = qtw.QComboBox()
        self.averagingTypeComboBox.addItem('Standard Average')
        self.averagingTypeComboBox.addItem('Running Average')
        self.averagingTypeComboBox.currentIndexChanged.connect(self.calculateInfos)
        self.correctionSettingsLayout.addWidget(self.averagingTypeComboBox, current_row, 0, 1, 2)

        # Add the entry for the number of frames
        current_row += 1
        self.correctionSettingsLayout.addWidget(CLabel('Number of frames:'), current_row, 0)
        self.numberFrameEntry = qtw.QLineEdit()
        self.numberFrameEntry.setText( str(2) )
        self.numberFrameEntry.setValidator(qtg.QIntValidator(2,self.max_n))
        self.numberFrameEntry.editingFinished.connect(self.entryIsEdited)
        self.correctionSettingsLayout.addWidget(self.numberFrameEntry, current_row, 1)

        # Add the slider for number of frames selection
        current_row += 1
        self.numberFrameSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.numberFrameSlider.setMinimum(2)
        self.numberFrameSlider.setMaximum( self.max_n )
        self.numberFrameSlider.setValue(2)
        self.numberFrameSlider.sliderMoved.connect(self.sliderIsEdited)
        self.correctionSettingsLayout.addWidget(self.numberFrameSlider, current_row, 0, 1, 2)

        # Add the checkbox for processing partial data
        current_row += 1
        self.partialDataCheckBox = qtw.QCheckBox("Add partial data?")
        self.partialDataCheckBox.setChecked(False)
        self.partialDataCheckBox.clicked.connect(self.calculateInfos)
        self.correctionSettingsLayout.addWidget(self.partialDataCheckBox, current_row, 0, 1, 2)

        # Add the checkbox for new tab
        current_row += 1
        self.replaceTabCheckBox = qtw.QCheckBox("Replace current tab?")
        self.replaceTabCheckBox.setChecked(False)
        self.correctionSettingsLayout.addWidget(self.replaceTabCheckBox, current_row, 0, 1, 2)

        # Display the widget
        self.correctionSettingsWidget.setLayout(self.correctionSettingsLayout)
        parentWidget.addWidget(self.correctionSettingsWidget)

    # ----------------------------------------------------------------
    # Generate the display of the information on the current selection
    def createInformationDisplay(self, parentWidget):

        # Generate the widget
        self.infoDisplayWidget = qtw.QWidget()
        self.infoDisplayLayout = qtw.QGridLayout(self.infoDisplayWidget)

        # Display the total number of frames
        current_row = 0
        self.infoDisplayLayout.addWidget(CLabel("Total # frames:"), current_row, 0)
        self.infoDisplayLayout.addWidget(qtw.QLabel( str( self.max_n ) ), current_row, 1)

        # Display the final number of frames after average
        current_row += 1
        self.infoDisplayLayout.addWidget(CLabel("# frames after averaging:"), current_row, 0)
        self.frameAfterLabel = qtw.QLabel("")
        self.infoDisplayLayout.addWidget(self.frameAfterLabel, current_row, 1)

        # Display the final number of frames after average
        current_row += 1
        self.infoDisplayLayout.addWidget(CLabel("# frames lost:"), current_row, 0)
        self.frameLostLabel = qtw.QLabel("")
        self.infoDisplayLayout.addWidget(self.frameLostLabel, current_row, 1)

        # Display the widget
        self.infoDisplayWidget.setLayout(self.infoDisplayLayout)
        parentWidget.addWidget(self.infoDisplayWidget, alignment=qtc.Qt.AlignLeft)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.processButton = qtw.QPushButton("Process")
        self.processButton.clicked.connect(self.processAveraging)
        self.processButton.setStatusTip("Process the selected frame averaging.")
        self.processButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.processButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
