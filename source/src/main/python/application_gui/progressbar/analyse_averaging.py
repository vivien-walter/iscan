import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class AnalyseAveragingProgressBarWindow(qtw.QMainWindow):
    def __init__(self, parent):
        super(AnalyseAveragingProgressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.setWindowTitle("Averaging Signal...")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Initialise the widget
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)

        # Set the display
        self.createProgressBarDisplay(self.mainLayout)

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
    def createProgressBarDisplay(self, parentWidget):

        # Show the progress bar text
        self.progressBarLabel = qtw.QLabel('Starting...')
        parentWidget.addWidget(self.progressBarLabel, alignment=qtc.Qt.AlignCenter)

        # Show the progress bar
        self.progressBarWidget = qtw.QProgressBar()
        parentWidget.addWidget(self.progressBarWidget)

    # -----------------
    # Update the window
    def updateProgress(self, crt_avg, n_avg):

        # Set the text
        label_text = 'Frame averaging ' + str(crt_avg)+'/'+str(n_avg)

        # Set the index
        index = crt_avg * 100 / n_avg

        # Update the display
        self.progressBarLabel.setText(label_text)
        self.progressBarWidget.setValue(index)
