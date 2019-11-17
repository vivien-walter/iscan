import os
import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from iscan.input_output import checkItemType

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/


class interactiveBackgroundWidget(qtw.QLabel):
    def __init__(self, parent):
        super(interactiveBackgroundWidget, self).__init__(parent)

        # Initialise the image
        self.parent = parent
        pathName = os.path.abspath(os.path.dirname(sys.argv[0]))
        imagePath = pathName + "/iscan/images/background.png"

        # Set the background image
        self.backgroundPixmap = qtg.QPixmap(imagePath)
        self.setPixmap(self.backgroundPixmap)

        self.setAcceptDrops(True)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## DRAG AND DROP FILES/FOLDERS HANDLING
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(qtc.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(qtc.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            checkItemType(self.parent, links)

        else:
            event.ignore()
