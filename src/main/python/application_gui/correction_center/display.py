import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator
from application_gui.correction_center.functions import cropCenterFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class cropCenterWindow(qtw.QMainWindow, cropCenterFunctions):
    def __init__(self, parent, image_class=None, path_id=0):
        super(cropCenterWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.path_id = path_id
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Crop and Center")

        # Populate the panel
        self.createMiniDisplay(self.mainLayout)
        self.createSizeControl(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(375,600)

        # Update the panel with image content
        self.getCenteredPath()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['crop_center'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Generate the display of the mini-image
    def createMiniDisplay(self, parentWidget):

        # Define the scrollable widget
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setMinimumWidth(256)
        self.scrollArea.setMinimumHeight(256)

        # Define the image label
        self.scrollAreaImage = qtw.QLabel(self.scrollArea)
        self.scrollAreaImage.setScaledContents(True)
        self.scrollArea.setWidget(self.scrollAreaImage)

        # Display the widget
        parentWidget.addWidget(self.scrollArea)

    # -------------------------------------
    # Generate the control of the crop size
    def createSizeControl(self, parentWidget):

        # Generate the widget
        self.sizeControlWidget = qtw.QWidget()
        self.sizeControlLayout = qtw.QGridLayout(self.sizeControlWidget)

        current_row = 0
        self.sizeControlLayout.addWidget(CLabel('Crop size'), current_row, 0, 1, 3)

        # Slider to change the size
        current_row += 1
        self.sizeSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.sizeSlider.setMinimum(4)
        self.sizeSlider.sliderMoved.connect(self.updateSlider)
        self.sizeControlLayout.addWidget(self.sizeSlider, current_row, 0, 1, 3)

        # Add labels and controls
        current_row += 1
        minLabel = qtw.QLabel('4')
        minLabel.setAlignment(qtc.Qt.AlignLeft)
        self.sizeControlLayout.addWidget(minLabel, current_row, 0)

        self.sizeEntry = qtw.QLineEdit()
        self.sizeEntry.setFixedWidth(100)
        self.sizeEntry.setAlignment(qtc.Qt.AlignCenter)
        self.sizeEntry.editingFinished.connect(self.updateEntry)
        self.sizeControlLayout.addWidget(self.sizeEntry, current_row, 1)

        self.maxLabel = qtw.QLabel('')
        self.maxLabel.setAlignment(qtc.Qt.AlignRight)
        self.sizeControlLayout.addWidget(self.maxLabel, current_row, 2)

        # Display the widget
        self.sizeControlWidget.setLayout(self.sizeControlLayout)
        parentWidget.addWidget(self.sizeControlWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Apply")
        self.applyButton.clicked.connect(self.applyCrop)
        self.applyButton.setStatusTip("Crop and center the image.")
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
