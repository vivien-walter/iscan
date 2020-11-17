import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CPathSelection
from application_gui.sidebar_trajectory.functions import TrajectoryControlsFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class TrajectoryControlsPanel(qtw.QDockWidget, TrajectoryControlsFunctions):
    def __init__(self, name, parent):
        super(TrajectoryControlsPanel, self).__init__(name, parent)

        # Initialise the subwindow
        self.parent = parent
        self.trajectory = None
        self.setAllowedAreas( qtc.Qt.LeftDockWidgetArea | qtc.Qt.RightDockWidgetArea )

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Populate the panel
        self.createVisualisationDisplay(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createPathSelectionDisplay(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createTrajectoryFileActions(self.mainLayout)

        # Display the panel
        self.mainLayout.setAlignment(qtc.Qt.AlignTop)
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)
        #self.show()
        #self.setFixedSize(self.size())

        # Add listeners
        self.topLevelChanged.connect(self.detectLocationChange)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.removeDockWidget(self.parent.docks["tracking"])
        self.parent.docks["tracking"] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Generate the widget to select a path
    def createVisualisationDisplay(self, parentWidget):

        self.trajectoryViewWidget = qtw.QWidget()
        self.trajectoryViewLayout = qtw.QVBoxLayout(self.trajectoryViewWidget)

        # Add the checkbox for displaying trajectory
        self.viewCheckBox = qtw.QCheckBox('Display trajectories?')
        self.viewCheckBox.setChecked( self.parent.show_trajectory )
        self.viewCheckBox.clicked.connect(self.toggleDisplay)
        self.trajectoryViewLayout.addWidget(self.viewCheckBox)

        # Add the button for display settings
        self.displaySettingsButton = qtw.QPushButton('Display Settings')
        self.displaySettingsButton.clicked.connect(self.callDisplaySettingsWindow)
        self.trajectoryViewLayout.addWidget(self.displaySettingsButton)

        self.trajectoryViewWidget.setLayout(self.trajectoryViewLayout)
        parentWidget.addWidget(self.trajectoryViewWidget)

    # -------------------------------
    # Generate the widget for display
    def createPathSelectionDisplay(self, parentWidget):

        self.pathSelectionWidget = qtw.QWidget()
        self.pathSelectionLayout = qtw.QVBoxLayout(self.pathSelectionWidget)

        # Add the label
        self.pathSelectionLayout.addWidget( CLabel("Path selection:") )

        # Add the checkbox for displaying trajectory
        self.pathSelectionEntry = CPathSelection()
        self.pathSelectionEntry.connectChange(self.refreshDisplay)
        self.pathSelectionLayout.addWidget(self.pathSelectionEntry)

        # Add the options
        self.deletePathButton = qtw.QPushButton("Delete Path")
        self.deletePathButton.setEnabled(False)
        self.deletePathButton.clicked.connect(self.deleteSelectedPath)
        self.pathSelectionLayout.addWidget(self.deletePathButton)

        self.pathSelectionWidget.setLayout(self.pathSelectionLayout)
        parentWidget.addWidget(self.pathSelectionWidget)

    # -------------------------------------------------
    # Generate the display for saving and loading files
    def createTrajectoryFileActions(self, parentWidget):

        self.fileActionsWidget = qtw.QWidget()
        self.fileActionsLayout = qtw.QVBoxLayout(self.fileActionsWidget)

        # Add the button to save the trajectory in a file
        self.saveTrajectoryButton = qtw.QPushButton('Save')
        self.saveTrajectoryButton.clicked.connect(self.saveTrajectoryFile)
        self.fileActionsLayout.addWidget(self.saveTrajectoryButton)

        # Add the button to load a trajectory from a file
        self.loadTrajectoryButton = qtw.QPushButton('Load')
        self.loadTrajectoryButton.clicked.connect(self.loadTrajectoryFile)
        self.fileActionsLayout.addWidget(self.loadTrajectoryButton)

        self.fileActionsWidget.setLayout(self.fileActionsLayout)
        parentWidget.addWidget(self.fileActionsWidget)
