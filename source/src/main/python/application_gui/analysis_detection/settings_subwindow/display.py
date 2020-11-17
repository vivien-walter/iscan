import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel
from application_gui.analysis_detection.settings_subwindow.functions import particleDetectionSettingsFunctions
from application_gui.analysis_detection.settings_subwindow.object_tab import objectSettingsFunctions
from application_gui.analysis_detection.settings_subwindow.filter_tab import filterSettingsFunctions
from application_gui.analysis_detection.settings_subwindow.other_tab import otherSettingsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class particleDetectionSettingsSubWindow(qtw.QMainWindow, particleDetectionSettingsFunctions, objectSettingsFunctions, filterSettingsFunctions, otherSettingsFunctions):
    def __init__(self, parent, detection_session=None):
        super(particleDetectionSettingsSubWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.detection_session = detection_session
        #self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Advanced Settings")

        # Populate the panel
        self.createTabDisplay(self.mainLayout)
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
        self.parent.subWindows['particle_advanced'] = None

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

        parentWidget.addWidget(self.tabWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.userActionsLayout.addWidget(qtw.QWidget(), alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
