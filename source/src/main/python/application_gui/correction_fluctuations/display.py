import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator
from application_gui.correction_fluctuations.functions import fluctuationCorrectionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class fluctuationCorrectionWindow(qtw.QMainWindow, fluctuationCorrectionFunctions):
    def __init__(self, parent, image_array=None):
        super(fluctuationCorrectionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_array = image_array
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Intensity Fluctuations...")

        # Populate the panel
        self.createGraphDisplay(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createStatisticsDisplay(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(450,450)

        # Update the panel with image content
        self.plotFluctuations()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['fluctuations_correction'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

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

    # ---------------------------------------
    # Generate the display for the statistics
    def createStatisticsDisplay(self, parentWidget):

        # Generate the widget
        self.statisticsWidget = qtw.QWidget()
        self.statisticsLayout = qtw.QVBoxLayout(self.statisticsWidget)

        # Populate all the informations
        self.statisticsGridWidget = qtw.QWidget()
        self.statisticsGridLayout = qtw.QGridLayout(self.statisticsGridWidget)

        # Mean PV
        current_row = 0
        self.statisticsGridLayout.addWidget( CLabel('Mean PV:'), current_row, 0)
        self.meanValueLabel = qtw.QLabel()
        self.statisticsGridLayout.addWidget( self.meanValueLabel, current_row, 1)

        # Standard Deviation
        current_row += 1
        self.statisticsGridLayout.addWidget( CLabel('St. Dev.:'), current_row, 0)
        self.standardDeviationLabel = qtw.QLabel()
        self.statisticsGridLayout.addWidget( self.standardDeviationLabel, current_row, 1)

        # Standard Deviation
        current_row += 1
        self.statisticsGridLayout.addWidget( CLabel('Variations:'), current_row, 0)
        self.variationsLabel = qtw.QLabel()
        self.statisticsGridLayout.addWidget( self.variationsLabel, current_row, 1)

        self.statisticsGridWidget.setLayout(self.statisticsGridLayout)
        self.statisticsLayout.addWidget( self.statisticsGridWidget, alignment=qtc.Qt.AlignLeft)

        # Display the widget
        self.statisticsWidget.setLayout(self.statisticsLayout)
        parentWidget.addWidget(self.statisticsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Correct")
        self.applyButton.clicked.connect(self.correctFluctuations)
        self.applyButton.setStatusTip("Apply the intensity fluctuations correction.")
        self.applyButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.applyButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
