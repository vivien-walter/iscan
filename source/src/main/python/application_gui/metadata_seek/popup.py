import time

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import emptyLayout, openWindow
from application_gui.metadata_seek.display import seekMetadataWindow

from metadata.read_data import readMetadataFile

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class seekMetadataPopup(qtw.QMainWindow):
    def __init__(self, parent, files_list=None):
        super(seekMetadataPopup, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.all_files = files_list
        self.n_files = len(files_list)

        self.type_dict = {
        'Experiment Metadata':'experiment',
        'Fast Record Metadata':'fast_record'
        }

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Process Metadata")

        # Populate the panel
        self.createTypeSelection(self.mainLayout)
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
        self.parent.subWindows['seek_metadata_popup'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------------
    # Generate the controls for the metadata selection
    def createTypeSelection(self, parentWidget):

        # Generate the widget
        self.typeSelectionWidget = qtw.QWidget()
        self.typeSelectionLayout = qtw.QVBoxLayout(self.typeSelectionWidget)

        # Add the info label
        numberFileLabel = qtw.QLabel(str(len(self.all_files))+' files have been found.')
        self.typeSelectionLayout.addWidget(numberFileLabel, alignment=qtc.Qt.AlignCenter)

        # Add the type combo box
        self.dataTypeComboBox = qtw.QComboBox()
        for type_name in list( self.type_dict.keys() ):
            self.dataTypeComboBox.addItem(type_name)
        self.typeSelectionLayout.addWidget(self.dataTypeComboBox)

        # Display the widget
        self.typeSelectionWidget.setLayout(self.typeSelectionLayout)
        parentWidget.addWidget(self.typeSelectionWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.loadButton = qtw.QPushButton("Load Files")
        self.loadButton.clicked.connect(self.readAndLoadFiles)
        self.loadButton.setStatusTip("Load the files found in the folder.")
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

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # ---------------------------------------
    # Replace the display with a progress bar
    def changeToProgressBar(self):

        # Empty the layout
        emptyLayout(self.mainLayout)

        # Add the label
        self.progressLabel = qtw.QLabel('Processing file 1/'+ str(self.n_files) )
        self.mainLayout.addWidget(self.progressLabel, alignment=qtc.Qt.AlignCenter)

        # Add the bar
        self.progressBarWidget = qtw.QProgressBar()
        self.mainLayout.addWidget(self.progressBarWidget)

        # Adjust the display
        self.mainLayout.setAlignment(qtc.Qt.AlignCenter)

    # -------------------------------------
    # Update the status of the progress bar
    def updateProgressBar(self, current_value):

        # Update the text display
        if current_value < self.n_files:
            self.progressLabel.setText( 'Processing file '+ str(current_value+1) +'/'+ str(self.n_files) )
        else:
            self.progressLabel.setText( 'All files have been processed' )

        # Update the status of the progress bar
        _bar_value = current_value * 100 / self.n_files
        self.progressBarWidget.setValue(_bar_value)

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -------------------------------------------
    # Read and load the files found in the folder
    def readAndLoadFiles(self):

        # Replace the display
        self.changeToProgressBar()
        self.parent.application.processEvents()

        # Get the type of file to read
        file_type = self.dataTypeComboBox.currentText()
        file_type = self.type_dict[file_type]

        # Process all the files
        selected_files = {}
        for i, file_path in enumerate(self.all_files):

            # Read the file
            try:
                current_type, current_content = readMetadataFile(file_path)

                # Add to the list
                if current_type == file_type:
                    selected_files[file_path] = current_content
            except:
                pass

            # Update the status of the progress bar
            self.updateProgressBar(i+1)
            self.parent.application.processEvents()

        # Open the new window
        if len(list( selected_files.keys() )) == 0:
            pass # NOTE: Add error message here

        else:
            openWindow(self.parent, seekMetadataWindow, 'seek_metadata', metadata_type=file_type, file_contents=selected_files)

        # Close the window
        self.close()
