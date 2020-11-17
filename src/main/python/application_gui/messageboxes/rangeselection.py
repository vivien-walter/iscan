import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CRangeSelection

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class rangeSelectionWindow(qtw.QMainWindow):
    def __init__(self, parent, n_frames=None):
        super(rangeSelectionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.n_frames = n_frames

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Range Selection...")

        # Populate the panel
        self.createRangeSelectionDisplay(self.mainLayout)
        #self.mainLayout.addWidget(CHorizontalSeparator())
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
        self.parent.subWindows['range_selection'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Generate the display of the image
    def createRangeSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.imageInfoWidget = qtw.QWidget()
        self.imageInfoLayout = qtw.QVBoxLayout(self.imageInfoWidget)

        self.imageInfoLayout.addWidget( CLabel('Open range:') )

        # Range selection
        self.frameRangeSelection = CRangeSelection()
        self.frameRangeSelection.setMin(1)
        self.frameRangeSelection.setMax(self.n_frames)
        self.frameRangeSelection.setRange(1,self.n_frames)
        self.imageInfoLayout.addWidget( self.frameRangeSelection )

        # Display the widget
        self.imageInfoWidget.setLayout(self.imageInfoLayout)
        parentWidget.addWidget(self.imageInfoWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.acceptButton = qtw.QPushButton("Ok")
        #self.loadButton.clicked.connect(self.getImageFromPath)
        self.acceptButton.setStatusTip("Use the selected range.")
        self.acceptButton.setFixedWidth(150)
        self.acceptButton.setEnabled(False)
        self.userActionsLayout.addWidget(self.acceptButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.cancelButton = qtw.QPushButton("Cancel")
        #self.cancelButton.clicked.connect(self.close)
        self.cancelButton.setStatusTip("Cancel and open the whole range.")
        self.cancelButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.cancelButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/
