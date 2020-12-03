import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator

from application_gui.manage_trackers.functions import TrackerManagerFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class TrackerManagerWindow(qtw.QMainWindow, TrackerManagerFunctions):
    def __init__(self, parent):
        super(TrackerManagerWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Manage Trackers")

        # Populate the panel
        self.createTableWidget(self.mainLayout)
        #self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(350,275)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['tracker_manager'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------------
    # Generate the table display for the trackers
    def createTableWidget(self, parentWidget):

        # Generate the widget
        self.trackerSettingsWidget = qtw.QWidget()
        self.trackerSettingsLayout = qtw.QVBoxLayout(self.trackerSettingsWidget)

        # Generate the table of servers
        self.trackersTable = qtw.QTableWidget(0, 4)
        self.trackersTable.setHorizontalHeaderLabels( ['', 'Name', '', ''] )

        self.trackersTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.trackersTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        self.trackersTable.setShowGrid(False)
        self.trackersTable.setMinimumHeight(100)
        self.trackerSettingsLayout.addWidget(self.trackersTable)

        # Populate the widget
        self.fillTrackerTable()

        # Display the widget
        self.trackerSettingsWidget.setLayout(self.trackerSettingsLayout)
        parentWidget.addWidget(self.trackerSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionWidget = qtw.QWidget()
        self.userActionLayout = qtw.QGridLayout(self.userActionWidget)

        # Add the button to import a tracker
        current_row = 0
        self.importButton = qtw.QPushButton("Import")
        self.importButton.clicked.connect(self.importTracker)
        self.importButton.setStatusTip("Import a tracker from a file.")
        self.importButton.setFixedWidth(125)
        self.userActionLayout.addWidget(self.importButton, current_row, 0)

        # Add the button to create a new tracker
        self.newButton = qtw.QPushButton("New")
        self.newButton.clicked.connect(self.makeNewTracker)
        self.newButton.setStatusTip("Create a new tracker.")
        self.newButton.setFixedWidth(125)
        self.userActionLayout.addWidget(self.newButton, current_row, 1)

        # Add the button to export a tracker
        current_row += 1
        self.exportButton = qtw.QPushButton("Export")
        self.exportButton.clicked.connect(self.exportTracker)
        self.exportButton.setStatusTip("Export a tracker to a file.")
        self.exportButton.setFixedWidth(125)
        self.userActionLayout.addWidget(self.exportButton, current_row, 0)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionLayout.addWidget(self.closeButton, current_row, 1)

        # Display the widget
        self.userActionWidget.setLayout(self.userActionLayout)
        parentWidget.addWidget(self.userActionWidget)
