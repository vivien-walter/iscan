import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class ProcessSignalsProgressBarWindow(qtw.QMainWindow):
    def __init__(self, parent):
        super(ProcessSignalsProgressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setWindowTitle("Measuring Signals...")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Initialise the widget
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Set the display
        self.createProgressDisplay(self.mainLayout)

        # Close and minimize properties
        self.setWindowFlags(self.windowFlags() | qtc.Qt.CustomizeWindowHint)
        self.setWindowFlag(qtc.Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(qtc.Qt.WindowCloseButtonHint, False)

        # Display the panel
        self.mainLayout.setAlignment(qtc.Qt.AlignCenter)
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.resize(450, 150)
        self.show()
        self.setFixedSize(self.size())

        # Start the job
        self.parent.application.processEvents()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['progress_bar'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------
    # Generate the main display of the progress bar
    def createProgressDisplay(self, parentWidget):

        # Show the progress bar text
        self.progressTopLabel = CLabel('Signal analysis in progress.')
        parentWidget.addWidget(self.progressTopLabel, alignment=qtc.Qt.AlignCenter)

        self.progressBottomLabel = qtw.QLabel('This operation can take several minutes.')
        parentWidget.addWidget(self.progressBottomLabel, alignment=qtc.Qt.AlignCenter)
