import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CBrowse, CHorizontalSeparator
from application_gui.tools_converter.functions import convertStackFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR CONVERTING FOLDERS INTO STACK
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class convertStackWindow(qtw.QMainWindow, convertStackFunctions):
    def __init__(self, parent):
        super(convertStackWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.directory = None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Folders to Stacks...")

        # Populate the panel
        self.createDirectoryBrowsingDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createStackSelectionDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(550,450)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['convert_stacks'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Generate the display to browse the file
    def createDirectoryBrowsingDisplay(self, parentWidget):

        # Generate the widget
        self.browsingWidget = qtw.QWidget()
        self.browsingLayout = qtw.QVBoxLayout(self.browsingWidget)

        # Add the button to open a new file
        self.browseEntry = CBrowse()
        self.browseEntry.connectButton(self.browseDirectory)
        self.browsingLayout.addWidget(self.browseEntry)

        # Display the widget
        self.browsingWidget.setLayout(self.browsingLayout)
        parentWidget.addWidget(self.browsingWidget)

    # ---------------------------------
    # Generate the display of the image
    def createStackSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.folderInfoWidget = qtw.QWidget()
        self.folderInfoLayout = qtw.QVBoxLayout(self.folderInfoWidget)

        # Generate the table of folders
        self.foldersTable = qtw.QTableWidget(0, 4)
        self.foldersTable.setHorizontalHeaderLabels( ['', 'Name', '# Images', 'Bitness'] )

        self.foldersTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.foldersTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        self.foldersTable.setShowGrid(False)
        self.foldersTable.setMinimumHeight(100)
        self.folderInfoLayout.addWidget(self.foldersTable)

        # Add the delete folder checkbox
        self.deleteFoldersCheckbox = qtw.QCheckBox('Delete folder(s) after convertion?')
        self.deleteFoldersCheckbox.setChecked(True)
        self.folderInfoLayout.addWidget(self.deleteFoldersCheckbox)

        # Display the widget
        self.folderInfoWidget.setLayout(self.folderInfoLayout)
        parentWidget.addWidget(self.folderInfoWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.loadButton = qtw.QPushButton("Convert")
        self.loadButton.clicked.connect(self.convertFolders)
        self.loadButton.setStatusTip("Convert the selected image folders into image stacks.")
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
