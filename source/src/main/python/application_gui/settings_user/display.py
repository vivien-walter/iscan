import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CLabelledLineEdit
from application_gui.settings_user.functions import userSettingsFunctions
from application_gui.settings_user.tab_general import userGeneralSettingsTab
from application_gui.settings_user.tab_image import imageSettingsTab
from application_gui.settings_user.tab_scale import scaleSettingsTab

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class userSettingsWindow(qtw.QMainWindow, userSettingsFunctions, userGeneralSettingsTab, imageSettingsTab, scaleSettingsTab):
    def __init__(self, parent):
        super(userSettingsWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("User Settings")

        # Populate the panel
        self.createTabDisplay(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['user_settings'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------
    # Generate the tab widget for display
    def createTabDisplay(self, parentWidget):

        # Define the widget
        self.tabWidget = qtw.QTabWidget()

        # Add the basic user settings tab
        self.tabWidget.addTab(self.createGeneralSettings(), "I/O")

        # Add the image settings
        self.tabWidget.addTab(self.createImageSettings(), "Image")

        # Add the scale settings
        self.tabWidget.addTab(self.createScaleSettings(), "Scale")

        # Load the widget
        parentWidget.addWidget(self.tabWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveServerSettings)
        self.saveButton.setStatusTip("Save the settings.")
        self.saveButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.saveButton)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
