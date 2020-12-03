import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator

from application_gui.settings_track_display.functions import TrackDisplaySettingsFunctions
from application_gui.settings_track_display.positions_tab import positionsDisplayFunctions
from application_gui.settings_track_display.path_tab import pathDisplayFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class TrackDisplaySettingsWindow(qtw.QMainWindow, TrackDisplaySettingsFunctions, positionsDisplayFunctions, pathDisplayFunctions):
    def __init__(self, parent):
        super(TrackDisplaySettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Track Display Settings")

        # Populate the panel
        self.createTabDisplay(self.mainLayout)
        #self.mainLayout.addWidget( CHorizontalSeparator() )
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
        self.parent.subWindows['track_display_settings'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------
    # Generate the tab display
    def createTabDisplay(self, parentWidget):

        # Generate the widget
        self.tabWidget = qtw.QTabWidget()

        # Add the positions display
        self.tabWidget.addTab(self.createPositionsDisplaySettings(), "Positions")

        # Add the paths display
        self.tabWidget.addTab(self.createPathsDisplaySettings(), "Paths")

        parentWidget.addWidget(self.tabWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionWidget = qtw.QWidget()
        self.userActionLayout = qtw.QHBoxLayout(self.userActionWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Apply")
        self.applyButton.clicked.connect(self.saveTrackDisplaySettings)
        self.applyButton.setStatusTip("Apply the display settings.")
        self.applyButton.setFixedWidth(125)
        self.userActionLayout.addWidget(self.applyButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionWidget.setLayout(self.userActionLayout)
        parentWidget.addWidget(self.userActionWidget)
