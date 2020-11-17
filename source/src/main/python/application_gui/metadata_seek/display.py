import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CHorizontalSeparator
from application_gui.metadata_seek.functions import seekMetadataFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class seekMetadataWindow(qtw.QMainWindow, seekMetadataFunctions):
    def __init__(self, parent, metadata_type=None, file_contents=None):
        super(seekMetadataWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.all_contents = file_contents
        self.data_type = metadata_type

        # Load the files
        self.loadFromFolder(file_contents)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("List Metadata")

        # Populate the panel
        self.createDataSelection(self.mainLayout)
        self.createDataTableDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setMinimumSize(650,450)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['seek_metadata'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------
    # Generate the selection for the data
    def createDataSelection(self, parentWidget):

        # Generate the widget
        self.dataSelectionWidget = qtw.QWidget()
        self.dataSelectionLayout = qtw.QVBoxLayout(self.dataSelectionWidget)

        # Add the type combo box
        self.dataSelectionComboBox = qtw.QComboBox()
        for type_name in self.info_names:
            self.dataSelectionComboBox.addItem(type_name)
        self.dataSelectionComboBox.currentTextChanged.connect(self.generateTable)
        self.dataSelectionLayout.addWidget(self.dataSelectionComboBox)

        # Display the widget
        self.dataSelectionWidget.setLayout(self.dataSelectionLayout)
        parentWidget.addWidget(self.dataSelectionWidget)

    # ---------------------------------------
    # Generate the table display for the data
    def createDataTableDisplay(self, parentWidget):

        # Generate the widget
        self.contentTableWidget = qtw.QWidget()
        self.contentTableLayout = qtw.QVBoxLayout(self.contentTableWidget)

        # Generate the table of servers
        self.generateTable()

        # Display the widget
        self.contentTableWidget.setLayout(self.contentTableLayout)
        parentWidget.addWidget(self.contentTableWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to save the selection
        self.saveButton = qtw.QPushButton("Save Selection")
        self.saveButton.clicked.connect(self.saveContent)
        self.saveButton.setStatusTip("Save the current selection.")
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
