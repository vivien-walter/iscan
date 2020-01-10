import os
import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class interactiveBackgroundWidget(qtw.QLabel):
    def __init__(self, parent):
        super(interactiveBackgroundWidget, self).__init__(parent)

        # Initialise the image
        self.parent = parent
        pathName = os.path.abspath( os.path.dirname(sys.argv[0]) )
        imagePath = os.path.join(pathName, "iscan", "static_images", "background.png")

        # Set the background image
        self.backgroundPixmap = qtg.QPixmap(imagePath)
        self.setPixmap(self.backgroundPixmap)

        # Allows the drag and drop event on the background
        self.setAcceptDrops(True)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## DRAG AND DROP FILES/FOLDERS HANDLING
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------------------
    # Other passive functions required to run the drag and drop events
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    # ----------------------------------------
    # Load the image on a drag and drop action
    def dropEvent(self, event):

        # Proceed if the dragged object has a path
        if event.mimeData().hasUrls:

            # Retrieve the path of all the objects being dragged
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))

            # Check the type of the item
            dataType, item = checkItemType(self.parent, links)

            # Call the appropriate function
            if dataType == "folder":
                loadImageFolder(self.parent, item)

            elif dataType == "file":
                loadImageFile(self.parent, item)

        # Do not do anything otherwise
        else:
            event.ignore()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.input_output.check_files import checkItemType
from iscan.input_output.open_images import loadImageFolder, loadImageFile
