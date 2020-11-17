import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CBrowse, CHorizontalSeparator
from application_gui.image_open.functions import openImageFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class makeSubstackWindow(qtw.QMainWindow, openImageFunctions):
    def __init__(self, parent):
        super(openImageWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_path = None

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Open Image or Stack...")

        # Populate the panel
        self.createFileBrowsingDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
        self.createImageInfosDisplay(self.mainLayout)
        self.mainLayout.addWidget(CHorizontalSeparator())
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
        self.parent.subWindows['open_image'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Generate the display to browse the file
    def createFileBrowsingDisplay(self, parentWidget):

        # Generate the widget
        self.browsingWidget = qtw.QWidget()
        self.browsingLayout = qtw.QVBoxLayout(self.browsingWidget)

        # Generate the radio buttons
        self.imageTypeButtonGroupWidget = qtw.QWidget()
        self.imageTypeButtonGroupLayout = qtw.QHBoxLayout(self.imageTypeButtonGroupWidget)

        self.imageTypeGroupButton = qtw.QButtonGroup(self.imageTypeButtonGroupWidget)

        self.singleFileRadiobutton = qtw.QRadioButton("Single File")
        self.singleFileRadiobutton.setChecked( self.parent.config.single_images )
        self.imageTypeGroupButton.addButton(self.singleFileRadiobutton)
        self.imageTypeButtonGroupLayout.addWidget(self.singleFileRadiobutton)

        self.imageFolderRadiobutton = qtw.QRadioButton("Images Folder")
        self.imageFolderRadiobutton.setChecked( not self.parent.config.single_images )
        self.imageTypeGroupButton.addButton(self.imageFolderRadiobutton)
        self.imageTypeButtonGroupLayout.addWidget(self.imageFolderRadiobutton)

        self.imageTypeButtonGroupWidget.setLayout(self.imageTypeButtonGroupLayout)
        self.imageTypeButtonGroupWidget.setContentsMargins(0, 0, 0, 0)
        self.browsingLayout.addWidget(self.imageTypeButtonGroupWidget)

        # Add the button to open a new file
        self.browseEntry = CBrowse()
        self.browseEntry.connectButton(self.browseImages)
        self.browsingLayout.addWidget(self.browseEntry)

        # Display the widget
        self.browsingWidget.setLayout(self.browsingLayout)
        parentWidget.addWidget(self.browsingWidget)

    # ---------------------------------
    # Generate the display of the image
    def createImageInfosDisplay(self, parentWidget):

        # Generate the widget
        self.imageInfoWidget = qtw.QWidget()
        self.imageInfoLayout = qtw.QVBoxLayout(self.imageInfoWidget)

        # Populate all the informations
        self.infoGridWidget = qtw.QWidget()
        self.infoGridLayout = qtw.QGridLayout(self.infoGridWidget)

        # Number of images
        self.imageNumberLabel = qtw.QLabel('')
        self.infoGridLayout.addWidget( CLabel('Number of image(s):'), 0, 0)
        self.infoGridLayout.addWidget( self.imageNumberLabel, 0, 1)

        # Image size
        self.imageSizeLabel = qtw.QLabel('')
        self.infoGridLayout.addWidget( CLabel('Image Size:'), 1, 0)
        self.infoGridLayout.addWidget( self.imageSizeLabel, 1, 1)

        # Image bitness
        self.imageBitsLabel = qtw.QLabel('')
        self.infoGridLayout.addWidget( CLabel('Image Bitness:'), 2, 0)
        self.infoGridLayout.addWidget( self.imageBitsLabel, 2, 1)

        # Display the grid
        self.infoGridWidget.setLayout(self.infoGridLayout)
        self.imageInfoLayout.addWidget( self.infoGridWidget, alignment=qtc.Qt.AlignLeft)

        # Crop selection
        self.cropCheckBox = qtw.QCheckBox('Crop the image?')
        self.cropCheckBox.setEnabled(False)
        self.imageInfoLayout.addWidget( self.cropCheckBox)

        # Signed bit correction
        self.signCorrectionCheckBox = qtw.QCheckBox('Correct signed bits?')
        self.signCorrectionCheckBox.setEnabled(False)
        self.imageInfoLayout.addWidget( self.signCorrectionCheckBox)

        # Signed bit correction
        self.backgroundCorrectionCheckBox = qtw.QCheckBox('Apply background correction?')
        self.backgroundCorrectionCheckBox.setEnabled(False)
        self.imageInfoLayout.addWidget( self.backgroundCorrectionCheckBox)

        # Display the widget
        self.imageInfoWidget.setLayout(self.imageInfoLayout)
        parentWidget.addWidget(self.imageInfoWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.loadButton = qtw.QPushButton("Load")
        self.loadButton.clicked.connect(self.getImageFromPath)
        self.loadButton.setStatusTip("Load the selected file or folder.")
        self.loadButton.setFixedWidth(150)
        self.loadButton.setEnabled(False)
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
