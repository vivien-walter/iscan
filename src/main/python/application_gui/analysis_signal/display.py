import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator

from application_gui.analysis_signal.functions import analyseSignalFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class analyseSignalWindow(qtw.QMainWindow, analyseSignalFunctions):
    def __init__(self, parent, image_class=None):
        super(analyseSignalWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class

        self.single = True
        self.all_checkboxes = []
        self.values = []
        self.errors = []

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Measure Signals")

        # Populate the panel
        self.createProcessSelection(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createPropertiesTable(self.mainLayout)
        self.createResultDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setMinimumSize(550,475)

        # Initialise
        if self.image_class.trajectory.signals is None:
            self.getProperties()
        else:
            self.populateTable()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['measure_signals'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------
    # Generate the selection widgets to process the signal
    def createProcessSelection(self, parentWidget):

        # Generate the widget
        self.processSelectionWidget = qtw.QWidget()
        self.processSelectionLayout = qtw.QHBoxLayout(self.processSelectionWidget)

        # Generate the radio buttons
        self.selectionTypeGroupWidget = qtw.QWidget()
        self.selectionTypeGroupLayout = qtw.QVBoxLayout(self.selectionTypeGroupWidget)

        self.selectionTypeGroupButton = qtw.QButtonGroup(self.selectionTypeGroupWidget)

        self.singleFrameRadiobutton = qtw.QRadioButton("Single Frame")
        self.singleFrameRadiobutton.setChecked( True )
        self.selectionTypeGroupButton.addButton(self.singleFrameRadiobutton)
        self.selectionTypeGroupLayout.addWidget(self.singleFrameRadiobutton)

        self.allFramesRadiobutton = qtw.QRadioButton("All Frames")
        self.selectionTypeGroupButton.addButton(self.allFramesRadiobutton)
        self.selectionTypeGroupLayout.addWidget(self.allFramesRadiobutton)

        self.selectionTypeGroupWidget.setLayout(self.selectionTypeGroupLayout)
        self.selectionTypeGroupWidget.setContentsMargins(0, 0, 0, 0)
        self.processSelectionLayout.addWidget(self.selectionTypeGroupWidget)

        # Generate the control block
        self.processButtonGroupWidget = qtw.QWidget()
        self.processButtonGroupLayout = qtw.QVBoxLayout(self.processButtonGroupWidget)

        # Generate the process button
        self.processButton = qtw.QPushButton("PROCESS")
        self.processButton.clicked.connect(self.processSignals)
        self.processButton.setFixedHeight(50)
        self.processButtonGroupLayout.addWidget(self.processButton)

        # Reprocess checkbox
        self.reloadCheckbox = qtw.QCheckBox("Compute again?")
        self.processButtonGroupLayout.addWidget(self.reloadCheckbox)

        self.processButtonGroupWidget.setLayout(self.processButtonGroupLayout)
        self.processButtonGroupWidget.setContentsMargins(0, 0, 0, 0)
        self.processSelectionLayout.addWidget(self.processButtonGroupWidget)

        # Display the widget
        self.processSelectionWidget.setLayout(self.processSelectionLayout)
        parentWidget.addWidget(self.processSelectionWidget)

    # --------------------------------------------------
    # Generate the table to show the detailed properties
    def createPropertiesTable(self, parentWidget):

        # Generate the widget
        self.contentTableWidget = qtw.QWidget()
        self.contentTableLayout = qtw.QVBoxLayout(self.contentTableWidget)

        # Generate the table of servers
        self.contentTable = qtw.QTableWidget(0, 6)
        self.contentTable.setHorizontalHeaderLabels( ['', 'Particle', '# Frames', 'Contrast', 'SNR', 'Noise'] )

        self.contentTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.contentTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        #self.contentTable.setShowGrid(False)
        self.contentTable.setMinimumHeight(125)
        self.contentTableLayout.addWidget(self.contentTable)

        # Display the widget
        self.contentTableWidget.setLayout(self.contentTableLayout)
        parentWidget.addWidget(self.contentTableWidget)

    # ----------------------------------------
    # Generate the display to show the results
    def createResultDisplay(self, parentWidget):

        # Generate the widget
        self.resultDisplayWidget = qtw.QWidget()
        self.resultDisplayLayout = qtw.QGridLayout(self.resultDisplayWidget)

        current_row = 0
        self.resultDisplayLayout.addWidget( CLabel('RESULTS'), current_row, 0, 1, 2 )

        # Contrast
        current_row += 1
        self.resultDisplayLayout.addWidget( CLabel('- Contrast:'), current_row, 0)
        self.contrastLabel = qtw.QLabel("")
        self.resultDisplayLayout.addWidget( self.contrastLabel, current_row, 1)

        # Signal-to-noise ratio
        current_row += 1
        self.resultDisplayLayout.addWidget( CLabel('- SNR:'), current_row, 0)
        self.snrLabel = qtw.QLabel("")
        self.resultDisplayLayout.addWidget( self.snrLabel, current_row, 1)

        # Noise
        current_row += 1
        self.resultDisplayLayout.addWidget( CLabel('- Noise:'), current_row, 0)
        self.noiseLabel = qtw.QLabel("")
        self.resultDisplayLayout.addWidget( self.noiseLabel, current_row, 1)

        # Display the widget
        self.resultDisplayWidget.setLayout(self.resultDisplayLayout)
        parentWidget.addWidget(self.resultDisplayWidget, alignment=qtc.Qt.AlignLeft)

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
