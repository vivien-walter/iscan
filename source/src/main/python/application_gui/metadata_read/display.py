import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CHorizontalSeparator
from application_gui.metadata_read.functions import readMetadataFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class readMetadataWindow(qtw.QMainWindow, readMetadataFunctions):
    def __init__(self, parent, file_path=None):
        super(readMetadataWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.file_path = file_path

        # Load the file
        self.loadFromFile(file_path)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Read Metadata")

        # Populate the panel
        self.createGeneralContentDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createContentTable(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()

        # Set the size
        if self.data_type == 'experiment':
            self.setMinimumSize(700,600)
        elif self.data_type == 'fast_record':
            self.setMinimumSize(500,600)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['read_metadata'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------
    # Generate the display of the general information
    def createGeneralContentDisplay(self, parentWidget):

        # Generate the widget
        self.generalInfosWidget = qtw.QWidget()
        self.generalInfosLayout = qtw.QVBoxLayout(self.generalInfosWidget)

        # Populate the content of the section
        self.populateGeneral()

        # Display the widget
        self.generalInfosWidget.setLayout(self.generalInfosLayout)
        parentWidget.addWidget(self.generalInfosWidget)

    # --------------------------
    # Generate the content table
    def createContentTable(self, parentWidget):

        # Generate the widget
        self.contentTableWidget = qtw.QWidget()
        self.contentTableLayout = qtw.QVBoxLayout(self.contentTableWidget)

        # Generate the table of servers
        self.contentTable = qtw.QTableWidget(0, self.n_columns)
        self.contentTable.setHorizontalHeaderLabels( self.column_names )

        self.contentTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.contentTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        #self.contentTable.setShowGrid(False)
        self.contentTable.setMinimumHeight(125)
        self.contentTableLayout.addWidget(self.contentTable)

        # Populate the content of the table
        self.populateTable()

        # Display the widget
        self.contentTableWidget.setLayout(self.contentTableLayout)
        parentWidget.addWidget(self.contentTableWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.loadButton = qtw.QPushButton("Open New File")
        self.loadButton.clicked.connect(self.getNewFile)
        self.loadButton.setStatusTip("Close the current window.")
        self.loadButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.loadButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(150)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
