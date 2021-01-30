import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CNavigation
from application_gui.messageboxes.display import warningProceedMessage
from application_gui.trajectory_edit.functions_display import PathEditorDisplayFunctions
from application_gui.trajectory_edit.functions_actions import PathEditorActionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class PathEditorWindow(qtw.QMainWindow, PathEditorDisplayFunctions, PathEditorActionFunctions):
    def __init__(self, parent, image_class=None, path_id=0):
        super(PathEditorWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Initialise the parameters
        self.current_path = path_id
        self.current_track = None
        self.current_frame = self.image_class.frame
        self.n_frames = self.image_class.n_frames
        self.zoom = 1

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Edit Paths")

        # Populate the panel
        self.createPathSelection(self.mainLayout)
        self.createNavigationWidget(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createTableWidget(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        #self.setFixedSize(350,275)

        # Initialise the display
        self.getPath(path_id = path_id)
        self.populateTable()
        self.initialiseDisplay()
        self.current_frame = -1
        self.changeFrame(frame_id=self.image_class.frame)

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Check if the modification has been saved yet
        proceed = True
        if not self.is_saved:
            proceed = warningProceedMessage('Modification not saved','The modification on the current path have not been saved yet. Are you sure you want to close?')

        if proceed:
            event.accept()
            self.parent.subWindows['paths_editor'] = None
        else:
            event.ignore()

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the controls for the user
    def createPathSelection(self, parentWidget):

        # Generate the widget
        self.pathSelectionWidget = qtw.QWidget()
        self.pathSelectionLayout = qtw.QHBoxLayout(self.pathSelectionWidget)

        # Add the path selection labels
        self.pathSelectionLayout.addWidget(CLabel('Current path:'), alignment=qtc.Qt.AlignRight)
        self.selectedPathLabel = qtw.QLabel(str(self.current_path))
        self.pathSelectionLayout.addWidget(self.selectedPathLabel, alignment=qtc.Qt.AlignLeft)

        # Add the button to save the changes
        self.pathSelectionBox = qtw.QComboBox()
        self.pathSelectionBox.addItems( self.image_class.trajectory.listTracks().astype(str) )
        #self.pathSelectionBox.setFixedWidth(150)
        self.pathSelectionLayout.addWidget(self.pathSelectionBox, alignment=qtc.Qt.AlignRight)

        # Initial the combobox settings
        _index_correction = self.pathSelectionBox.findText(str(self.current_path), qtc.Qt.MatchFixedString)
        if _index_correction >= 0:
             self.pathSelectionBox.setCurrentIndex(_index_correction)

        # Add the button to load path
        self.loadButton = qtw.QPushButton("Load path")
        self.loadButton.clicked.connect(self.changePath)
        self.loadButton.setFixedWidth(150)
        self.pathSelectionLayout.addWidget(self.loadButton, alignment=qtc.Qt.AlignRight)

        # Add the button to create new path
        self.newPathButton = qtw.QPushButton("New path")
        self.newPathButton.clicked.connect(self.createNewPath)
        self.newPathButton.setFixedWidth(150)
        self.pathSelectionLayout.addWidget(self.newPathButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.pathSelectionWidget.setLayout(self.pathSelectionLayout)
        parentWidget.addWidget(self.pathSelectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createNavigationWidget(self, parentWidget):

        # Generate the widget
        self.imageNavigationWidget = qtw.QWidget()
        self.imageNavigationLayout = qtw.QHBoxLayout(self.imageNavigationWidget)

        # Add the two subwidgets
        self.createMainNavigationWidget(self.imageNavigationLayout)
        self.createSubNavigationWidget(self.imageNavigationLayout)

        # Display the widget
        self.imageNavigationWidget.setLayout(self.imageNavigationLayout)
        parentWidget.addWidget(self.imageNavigationWidget)

    # ---------------------------------------
    # Create the main display of the position
    def createMainNavigationWidget(self, parentWidget):

        # Generate the left panel
        self.mainNavigationWidget = qtw.QWidget()
        self.mainNavigationLayout = qtw.QVBoxLayout(self.mainNavigationWidget)

        # Define the scrollable widget
        self.scrollArea = qtw.QScrollArea()
        self.scrollArea.setMinimumWidth(400)
        self.scrollArea.setMinimumHeight(400)

        # Define the image label
        self.scrollAreaImage = qtw.QLabel(self.scrollArea)
        self.scrollAreaImage.setScaledContents(True)

        # Define the interactions
        self.scrollAreaImage.mousePressEvent = self.actionOnClick
        #self.scrollAreaImage.mouseReleaseEvent = self.actionOnRelease

        # Add the widget
        self.scrollArea.setWidget(self.scrollAreaImage)
        self.mainNavigationLayout.addWidget(self.scrollArea)

        # Display the widget
        self.mainNavigationWidget.setLayout(self.mainNavigationLayout)
        parentWidget.addWidget(self.mainNavigationWidget, alignment=qtc.Qt.AlignTop)

    # -----------------------------------------
    # Create the miniature display and controls
    def createSubNavigationWidget(self, parentWidget):

        # Generate the right panel
        self.subNavigationWidget = qtw.QWidget()
        self.subNavigationLayout = qtw.QVBoxLayout(self.subNavigationWidget)

        # Add the display type checkbox
        self.miniatureTypeCheckbox = qtw.QCheckBox('Use profiles?')
        self.subNavigationLayout.addWidget(self.miniatureTypeCheckbox)

        # Define the scrollable widget
        self.miniScrollArea = qtw.QScrollArea()
        self.miniScrollArea.setMinimumWidth(225)
        self.miniScrollArea.setMinimumHeight(225)

        # Define the image label
        self.miniScrollAreaImage = qtw.QLabel(self.scrollArea)
        self.miniScrollAreaImage.setScaledContents(True)
        self.miniScrollArea.setWidget(self.miniScrollAreaImage)
        self.subNavigationLayout.addWidget(self.miniScrollArea)

        # Add the button to save the changes
        self.navigationController = CNavigation()
        self.navigationController.connectDirections(self.moveCursor)
        self.navigationController.connectCenter(self.resetCursor)
        self.subNavigationLayout.addWidget(self.navigationController, alignment=qtc.Qt.AlignCenter)

        # Add the button to save the position
        self.savePositionButton = qtw.QPushButton("Save Position")
        self.savePositionButton.clicked.connect(self.saveCursor)
        self.subNavigationLayout.addWidget(self.savePositionButton)

        # Add the button to delete the position
        self.deletePositionButton = qtw.QPushButton("Delete Position")
        self.deletePositionButton.clicked.connect(self.deletePosition)
        self.subNavigationLayout.addWidget(self.deletePositionButton)

        # Add the button to complete the position
        self.fillCurrentPositionButton = qtw.QPushButton("Fill missing frames?")
        self.fillCurrentPositionButton.clicked.connect(self.fillAllPositions)
        self.subNavigationLayout.addWidget(self.fillCurrentPositionButton)

        # Display the widget
        self.subNavigationWidget.setLayout(self.subNavigationLayout)
        parentWidget.addWidget(self.subNavigationWidget, alignment=qtc.Qt.AlignTop)

    # -------------------------------------------
    # Generate the table display for the trackers
    def createTableWidget(self, parentWidget):

        # Generate the widget
        self.frameDisplayWidget = qtw.QWidget()
        self.frameDisplayLayout = qtw.QVBoxLayout(self.frameDisplayWidget)

        # Generate the frame selection
        self.frameSelectionWidget = qtw.QWidget()
        self.frameSelectionLayout = qtw.QHBoxLayout(self.frameSelectionWidget)

        # Label
        self.frameSelectionLayout.addWidget(CLabel('Frame:'), alignment=qtc.Qt.AlignRight)

        # Selection
        self.frameSelectionEntry = qtw.QLineEdit()
        self.frameSelectionEntry.setText(str(self.current_frame+1))
        self.frameSelectionEntry.setFixedWidth(75)
        self.frameSelectionLayout.addWidget(self.frameSelectionEntry)

        # Frame number
        self.totalFrameLabel = qtw.QLabel("/ "+str(self.n_frames))
        self.frameSelectionLayout.addWidget(self.totalFrameLabel, alignment=qtc.Qt.AlignLeft)

        # Display the widget
        self.frameSelectionWidget.setLayout(self.frameSelectionLayout)
        self.frameDisplayLayout.addWidget(self.frameSelectionWidget, alignment=qtc.Qt.AlignLeft)

        # ----------

        # Generate the table of servers
        self.frameTable = qtw.QTableWidget(1, 6)
        self.frameTable.setHorizontalHeaderLabels( [''] )

        self.frameTable.setSelectionMode(qtw.QAbstractItemView.NoSelection)
        self.frameTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

        self.frameTable.setShowGrid(True)
        self.frameTable.setMinimumHeight(63)
        self.frameTable.setMaximumHeight(63)
        self.frameDisplayLayout.addWidget(self.frameTable)

        # Display the widget
        self.frameDisplayWidget.setLayout(self.frameDisplayLayout)
        parentWidget.addWidget(self.frameDisplayWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionWidget = qtw.QWidget()
        self.userActionLayout = qtw.QHBoxLayout(self.userActionWidget)

        # Add the button to save the changes
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.savePath)
        self.saveButton.setStatusTip("Export a tracker to a file.")
        self.saveButton.setFixedWidth(150)
        self.userActionLayout.addWidget(self.saveButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(150)
        self.userActionLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionWidget.setLayout(self.userActionLayout)
        parentWidget.addWidget(self.userActionWidget)
