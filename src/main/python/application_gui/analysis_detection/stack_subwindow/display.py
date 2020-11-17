import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.analysis_detection.stack_subwindow.functions import stackDetectionFunctions
from application_gui.analysis_detection.stack_subwindow.basic_tab import basicSettingsFunctions
from application_gui.analysis_detection.stack_subwindow.advanced_tab import advancedSettingsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class stackDetectionSubWindow(qtw.QMainWindow, stackDetectionFunctions, basicSettingsFunctions, advancedSettingsFunctions):
    def __init__(self, parent, detection_session=None):
        super(stackDetectionSubWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.trajectory_session = detection_session
        self.detection_session = self.trajectory_session.session
        #self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Process Stack")

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
        self.parent.subWindows['particle_stack'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------
    # Generate the controls for the stack processing
    def createTabDisplay(self, parentWidget):

        # Generate the widget
        self.tabWidget = qtw.QTabWidget()

        # Add the object settings
        self.tabWidget.addTab(self.createBasicSettings(), "Basic")

        # Add the filter settings
        self.tabWidget.addTab(self.createAdvancedSettings(), "Advanced")

        parentWidget.addWidget(self.tabWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.processButton = qtw.QPushButton("Process")
        self.processButton.clicked.connect(self.processStack)
        self.processButton.setStatusTip("Process the whole stack with the given settings.")
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
