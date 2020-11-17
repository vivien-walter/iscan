import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel
from application_gui.progressbar.modes import progressBarModes

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class progressBarWindow(qtw.QMainWindow, progressBarModes):
    def __init__(self, parent, mode=None, n_max=None):
        super(progressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.mode = mode
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Other parameters
        self.n_max = None

        # Initialise the widget
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Set the display
        self.createProgressBarDisplay(self.mainLayout)

        # Close and minimize properties
        self.setWindowFlags(self.windowFlags() | qtc.Qt.CustomizeWindowHint)
        self.setWindowFlag(qtc.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(qtc.Qt.WindowCloseButtonHint, False)

        # Display the panel
        self.mainLayout.setAlignment(qtc.Qt.AlignCenter)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.resize(300, 175)
        self.show()
        self.setFixedSize(self.size())

        # Initialize with the mode
        self.initMode()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        sys.stdout = sys.__stdout__
        event.accept()
        self.parent.subWindows['progress_bar'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------
    # Generate the main display of the progress bar
    def createProgressBarDisplay(self, parentWidget):

        # Show the progress bar text
        self.progressBarLabel = CLabel("")
        parentWidget.addWidget(self.progressBarLabel, alignment=qtc.Qt.AlignCenter)

        # Show the progress bar
        self.progressBarWidget = qtw.QProgressBar()
        parentWidget.addWidget(self.progressBarWidget)
