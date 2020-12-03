from pyqtgraph import PlotWidget
import pyqtgraph as pg

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CPathSelection, CBrowse

from application_gui.analysis_diffusivity.functions import particleDiffusionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class particleDiffusionWindow(qtw.QMainWindow, particleDiffusionFunctions):
    def __init__(self, parent, image_class=None):
        super(particleDiffusionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.trajectory = None
        self.path_list = None
        self.loaded_trajectory = None
        self.image_class = image_class

        self.space_scale = None
        self.space_unit = None
        self.frame_rate = None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Mean Squared Displacement")

        # Populate the panel
        self.createTrajectorySelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createScaleSelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createGraphDisplay(self.mainLayout)
        #self.createSignalSelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setMinimumSize(575,675)
        self.resize(575,675)

        # Initialise
        self.initialiseDisplay()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['msd_analysis'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------
    # Generate the selection widgets to process the signal
    def createTrajectorySelection(self, parentWidget):

        # Generate the widget
        self.trajectorySelectionWidget = qtw.QWidget()
        self.trajectorySelectionLayout = qtw.QGridLayout(self.trajectorySelectionWidget)

        # Bitness selection
        self.sourceSelectionGroupButton = qtw.QButtonGroup(self.trajectorySelectionLayout)

        current_row = 0
        self.fromFileButton = qtw.QRadioButton("Load from File")
        self.sourceSelectionGroupButton.addButton(self.fromFileButton)
        self.trajectorySelectionLayout.addWidget(self.fromFileButton, current_row, 0, alignment=qtc.Qt.AlignLeft)

        self.browseEntry = CBrowse()
        self.browseEntry.lineEdit.setFixedWidth(250)
        self.browseEntry.connectButton(self.browseTrajectory)
        self.trajectorySelectionLayout.addWidget(self.browseEntry, current_row, 1, alignment=qtc.Qt.AlignRight)

        current_row += 1
        self.fromImageButton = qtw.QRadioButton("Load from Image")
        self.fromImageButton.clicked.connect(self.getScaleFromImage)
        self.sourceSelectionGroupButton.addButton(self.fromImageButton)
        self.trajectorySelectionLayout.addWidget(self.fromImageButton, current_row, 0, alignment=qtc.Qt.AlignLeft)

        self.processTrajectoryButton = qtw.QPushButton("PROCESS")
        self.processTrajectoryButton.clicked.connect(self.processTrajectory)
        self.processTrajectoryButton.setFixedWidth(150)
        self.trajectorySelectionLayout.addWidget(self.processTrajectoryButton, current_row, 1, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.trajectorySelectionWidget.setLayout(self.trajectorySelectionLayout)
        parentWidget.addWidget(self.trajectorySelectionWidget)

    # ----------------------------------------------------
    # Generate the selection widgets to process the signal
    def createScaleSelection(self, parentWidget):

        # Generate the widget
        self.scaleSelectionWidget = qtw.QWidget()
        self.scaleSelectionLayout = qtw.QGridLayout(self.scaleSelectionWidget)

        current_row = 0
        self.scaleSelectionLayout.addWidget(CLabel('Scale(s):'), current_row, 0, 1, 4)

        current_row += 1
        self.scaleSelectionLayout.addWidget(qtw.QLabel('Space scale (px/unit):'), current_row, 0)
        self.spaceScaleEntry = qtw.QLineEdit()
        self.scaleSelectionLayout.addWidget(self.spaceScaleEntry, current_row, 1)

        self.scaleSelectionLayout.addWidget(qtw.QLabel('Time scale (FPS):'), current_row, 2)
        self.timeScaleEntry = qtw.QLineEdit()
        self.scaleSelectionLayout.addWidget(self.timeScaleEntry, current_row, 3)

        current_row += 1
        self.scaleSelectionLayout.addWidget(qtw.QLabel('Space unit:'), current_row, 0)
        self.spaceUnitEntry = qtw.QLineEdit()
        self.scaleSelectionLayout.addWidget(self.spaceUnitEntry, current_row, 1)

        # Display the widget
        self.scaleSelectionWidget.setLayout(self.scaleSelectionLayout)
        parentWidget.addWidget(self.scaleSelectionWidget)

    # ----------------------------------
    # Generate the display for the graph
    def createGraphDisplay(self, parentWidget):

        # Generate the widget
        self.plotGraphWidget = qtw.QWidget()
        self.plotGraphLayout = qtw.QVBoxLayout(self.plotGraphWidget)

        # Add the graph
        self.graphWidget = pg.PlotWidget()
        self.plotGraphLayout.addWidget(self.graphWidget)

        # Add the path selector
        self.pathSelectionEntry = CPathSelection()
        self.pathSelectionEntry.connectChange(self.updateGraph)
        self.plotGraphLayout.addWidget(self.pathSelectionEntry, alignment=qtc.Qt.AlignCenter)

        # Add the diffusivity display
        self.diffusivityValueWidget = qtw.QWidget()
        self.diffusivityValueLayout = qtw.QHBoxLayout(self.diffusivityValueWidget)

        self.diffusivityValueLayout.addWidget(CLabel('Diffusivity:'))
        self.diffusivityValueLabel = qtw.QLabel()
        self.diffusivityValueLayout.addWidget( self.diffusivityValueLabel, alignment=qtc.Qt.AlignLeft )

        self.diffusivityValueWidget.setLayout(self.diffusivityValueLayout)
        self.plotGraphLayout.addWidget(self.diffusivityValueWidget)

        # Add log checkbox
        self.logScaleCheckbox = qtw.QCheckBox('Log scale?')
        self.logScaleCheckbox.setChecked(True)
        self.logScaleCheckbox.clicked.connect(self.updateGraph)
        self.plotGraphLayout.addWidget(self.logScaleCheckbox, alignment=qtc.Qt.AlignLeft)

        # Display the widget
        self.plotGraphWidget.setLayout(self.plotGraphLayout)
        parentWidget.addWidget(self.plotGraphWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = qtw.QPushButton("Save in File")
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.setStatusTip("Save the results in a file.")
        self.saveButton.setFixedWidth(150)
        self.saveButton.setEnabled( False )
        self.userActionsLayout.addWidget(self.saveButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
