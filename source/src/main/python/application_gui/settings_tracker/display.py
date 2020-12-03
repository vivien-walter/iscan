import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel
from application_gui.settings_tracker.functions import TrackerSettingsFunctions
from application_gui.settings_tracker.object_tab import objectSettingsFunctions
from application_gui.settings_tracker.filter_tab import filterSettingsFunctions
from application_gui.settings_tracker.other_tab import otherSettingsFunctions
from application_gui.settings_tracker.trajectory_tab import trajectorySettingsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class TrackerSettingsWindow(qtw.QMainWindow, TrackerSettingsFunctions, objectSettingsFunctions, filterSettingsFunctions, otherSettingsFunctions, trajectorySettingsFunctions):
    def __init__(self, parent, detection_session=None):
        super(TrackerSettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.detection_instance = detection_session
        self.detection_session = detection_session.session
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Tracker Settings")

        # Populate the panel
        self.createTabDisplay(self.mainLayout)
        self.createNameSelection(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

        # Update the panel with class content
        self.initialiseSettings()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['tracker_settings'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the controls for the user
    def createTabDisplay(self, parentWidget):

        # Generate the widget
        self.tabWidget = qtw.QTabWidget()

        # Add the object settings
        self.tabWidget.addTab(self.createObjectSettings(), "Object")

        # Add the filter settings
        self.tabWidget.addTab(self.createFilterSettings(), "Filter")

        # Add the other settings
        self.tabWidget.addTab(self.createOtherSettings(), "Other(s)")

        # Add the trajectory settings
        self.tabWidget.addTab(self.createTrajectorySettings(), "Trajectory")

        parentWidget.addWidget(self.tabWidget)

    # ------------------------------------------
    # Generate the selection of the tracker name
    def createNameSelection(self, parentWidget):

        # Generate the widget
        self.nameSelectionWidget = qtw.QWidget()
        self.nameSelectionLayout = qtw.QHBoxLayout(self.nameSelectionWidget)

        # Add the label
        self.nameSelectionLayout.addWidget(CLabel('Tracker name'))

        # Add the entry
        self.nameSelectionEntry = qtw.QLineEdit()
        self.nameSelectionLayout.addWidget(self.nameSelectionEntry)

        # Display the widget
        self.nameSelectionWidget.setLayout(self.nameSelectionLayout)
        parentWidget.addWidget(self.nameSelectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveSettings)
        self.saveButton.setStatusTip("Save the current settings.")
        self.saveButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.saveButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Cancel the modifications.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
