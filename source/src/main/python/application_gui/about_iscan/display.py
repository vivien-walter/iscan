import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class aboutHelpWindow(qtw.QMainWindow):
    def __init__(self, parent):
        super(aboutHelpWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setWindowModality(qtc.Qt.ApplicationModal)

        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle('About...')

        # Get the logo path
        if self.parent.compiler == 'fbs':
            image_path = self.parent.appctxt.get_resource('iscan_logo.png')
        else:
            image_path = os.path.join("resources","iscan_logo.png")

            if os.name == 'posix':
                image_path = resource_path(image_path)

        # Get the image form path
        image = qtg.QPixmap( image_path )

        # Show the logo
        imageWidget = qtw.QLabel()
        imageWidget.setPixmap(image)
        self.mainLayout.addWidget(imageWidget, alignment=qtc.Qt.AlignCenter)

        # Show the title
        titleText = CLabel(self.parent.title + " - " + self.parent.version)
        self.mainLayout.addWidget(titleText, alignment=qtc.Qt.AlignCenter)

        # Show the text
        aboutText = qtw.QLabel("""Release Date: 30/01/2021
Author: Vivien Walter
Contact: walter.vivien@gmail.com

More information and documentation can be found on the website of the software:
https://github.com/vivien-walter/iscan""")
        self.mainLayout.addWidget(aboutText)#, alignment=qtc.Qt.AlignCenter)

        # Exit button
        self.exitButton = qtw.QPushButton("Close")
        self.exitButton.setFixedWidth(125)
        self.exitButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.exitButton, alignment=qtc.Qt.AlignCenter)

        # Display the panel
        #self.mainLayout.setAlignment(qtc.Qt.AlignCenter)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.resize(300, 300)
        self.show()
        self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['about'] = None

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
