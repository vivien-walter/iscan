import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CHorizontalSeparator

from application_gui.correction_crop.functions import imageCropFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class imageCropWindow(qtw.QMainWindow, imageCropFunctions):
    def __init__(self, parent, image_class=None):
        super(imageCropWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Initialise the display parameters
        self.zoom = 1
        self.frame = 0
        self.drawing = False
        self.selection_pointA = None
        self.selection_pointB = None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Crop Image(s)")

        # Populate the panel
        self.createImageDisplay(self.mainLayout)
        #self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

        # Initialise the display
        self.initialiseZoom()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['crop_image'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Generate the display for the image to crop
    def createImageDisplay(self, parentWidget):

        # Define the scrollable widget
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setMinimumWidth(256)
        self.scrollArea.setMinimumHeight(256)

        # Define the image label
        self.scrollAreaImage = qtw.QLabel(self.scrollArea)
        self.scrollAreaImage.setScaledContents(True)

        # Define the interactions
        self.scrollAreaImage.mousePressEvent = self.actionOnClick
        self.scrollAreaImage.mouseMoveEvent = self.actionOnMove
        self.scrollAreaImage.mouseReleaseEvent = self.actionOnRelease

        # Define the rubber band
        self.rubberband = qtg.QRubberBand(qtg.QRubberBand.Rectangle, self.scrollAreaImage)

        self.scrollArea.setWidget(self.scrollAreaImage)

        # Display the widget
        parentWidget.addWidget(self.scrollArea)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.cropButton = qtw.QPushButton("Crop")
        self.cropButton.clicked.connect(self.cropImage)
        self.cropButton.setStatusTip("Crop the image on the desired selection.")
        self.cropButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.cropButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
