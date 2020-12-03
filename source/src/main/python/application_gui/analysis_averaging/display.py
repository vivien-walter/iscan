from pyqtgraph import PlotWidget
import pyqtgraph as pg

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CRangeSelection

from application_gui.analysis_averaging.functions import signalAveragingFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class signalAveragingWindow(qtw.QMainWindow, signalAveragingFunctions):
    def __init__(self, parent, image_class=None):
        super(signalAveragingWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.averaging_result = None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Signal vs. Averaging")

        # Populate the panel
        self.createPathSelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createAveragingSelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createGraphDisplay(self.mainLayout)
        self.createSignalSelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setMinimumSize(600,650)
        self.resize(600,650)

        # Initialise
        self.initialiseDisplay()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['average_signals'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------
    # Generate the selection widgets to process the signal
    def createPathSelection(self, parentWidget):

        # Generate the widget
        self.pathSelectionWidget = qtw.QWidget()
        self.pathSelectionLayout = qtw.QHBoxLayout(self.pathSelectionWidget)

        # Add the path selection combobox
        self.pathSelectionLayout.addWidget(CLabel('Analyse path:'))
        self.pathSelectionBox = qtw.QComboBox()
        self.pathSelectionLayout.addWidget( self.pathSelectionBox )

        # Display the widget
        self.pathSelectionWidget.setLayout(self.pathSelectionLayout)
        parentWidget.addWidget(self.pathSelectionWidget, alignment=qtc.Qt.AlignLeft)

    # -------------------------------
    # Generate the average to perform
    def createAveragingSelection(self, parentWidget):

        # Generate the widget
        self.averageSelectionWidget = qtw.QWidget()
        self.averageSelectionLayout = qtw.QGridLayout(self.averageSelectionWidget)

        # Average type
        self.averageSelectionLayout.addWidget(CLabel("Type:"), 0, 0)
        self.averagingTypeComboBox = qtw.QComboBox()
        self.averagingTypeComboBox.addItem('Standard Average')
        self.averagingTypeComboBox.addItem('Running Average')
        self.averagingTypeComboBox.setFixedWidth(200)
        self.averageSelectionLayout.addWidget(self.averagingTypeComboBox, 1, 0)

        # Process button
        self.processButton = qtw.QPushButton("PROCESS")
        self.processButton.setFixedHeight(50)
        self.processButton.setFixedWidth(100)
        self.processButton.clicked.connect(self.processAveraging)
        self.averageSelectionLayout.addWidget(self.processButton, 0, 1, 2, 1)

        # Range selection
        self.averageSelectionLayout.addWidget( qtw.QLabel('Processing range:'), 2, 0, 1, 2)
        self.frameRangeSelection = CRangeSelection()
        self.frameRangeSelection.setMin(2)
        self.frameRangeSelection.setMax(3)
        self.frameRangeSelection.setRange(2,3)
        self.frameRangeSelection.setFixedWidth(550)
        self.averageSelectionLayout.addWidget( self.frameRangeSelection, 3, 0, 1, 2, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.averageSelectionWidget.setLayout(self.averageSelectionLayout)
        parentWidget.addWidget(self.averageSelectionWidget)

    # ----------------------------------
    # Generate the display for the graph
    def createGraphDisplay(self, parentWidget):

        # Generate the widget
        self.plotGraphWidget = qtw.QWidget()
        self.plotGraphLayout = qtw.QVBoxLayout(self.plotGraphWidget)

        self.graphWidget = pg.PlotWidget()
        self.plotGraphLayout.addWidget(self.graphWidget)

        # Display the widget
        self.plotGraphWidget.setLayout(self.plotGraphLayout)
        parentWidget.addWidget(self.plotGraphWidget)

    # -----------------------------------------
    # Generate the display for signal selection
    def createSignalSelection(self, parentWidget):

        # Generate the widget
        self.signalSelectionWidget = qtw.QWidget()
        self.signalSelectionLayout = qtw.QHBoxLayout(self.signalSelectionWidget)

        self.signalSelectionGroupButton = qtw.QButtonGroup(self.signalSelectionLayout)

        self.showContrastRadiobutton = qtw.QRadioButton("Contrast")
        self.showContrastRadiobutton.clicked.connect(self.plotFluctuations)
        self.signalSelectionGroupButton.addButton(self.showContrastRadiobutton)
        self.signalSelectionLayout.addWidget(self.showContrastRadiobutton)

        self.showNoiseRadiobutton = qtw.QRadioButton("Noise")
        self.showNoiseRadiobutton.setChecked( True )
        self.showNoiseRadiobutton.clicked.connect(self.plotFluctuations)
        self.signalSelectionGroupButton.addButton(self.showNoiseRadiobutton)
        self.signalSelectionLayout.addWidget(self.showNoiseRadiobutton)

        self.showSNRRadiobutton = qtw.QRadioButton("SNR")
        self.showSNRRadiobutton.clicked.connect(self.plotFluctuations)
        self.signalSelectionGroupButton.addButton(self.showSNRRadiobutton)
        self.signalSelectionLayout.addWidget(self.showSNRRadiobutton)

        # Display the widget
        self.signalSelectionWidget.setLayout(self.signalSelectionLayout)
        parentWidget.addWidget(self.signalSelectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.saveButton = qtw.QPushButton("Save in File")
        self.saveButton.clicked.connect(self.saveResults)
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
