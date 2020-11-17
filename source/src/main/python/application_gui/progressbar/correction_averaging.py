import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.averaging import averageStack

from application_gui.progressbar.streams import Stream

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class AverageImageProgressBarWindow(qtw.QMainWindow):
    def __init__(self, parent, image_class=None, window=2, average_type='block', include_partial=False, scheduler=None):
        super(AverageImageProgressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.window = window
        self.average_type = average_type
        self.include_partial = include_partial
        self.scheduler = scheduler
        self.setWindowTitle("Averaging Images...")
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
        self.resize(450, 175)
        self.show()
        self.setFixedSize(self.size())

        # Start the job
        self.parent.application.processEvents()
        self.startJob()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        sys.stdout = sys.__stdout__
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

    ##-\-\-\-\-\-\
    ## JOB HANDLING
    ##-/-/-/-/-/-/

    # -------------
    # Start the job
    def startJob(self):

        # Start the listener
        sys.stdout = Stream(newText=self.updateProgress)

        # Run the job
        thread = AverageImageJobThread(self.parent, self.image_class, self.window, self.average_type, self.include_partial)
        thread.release_array.connect(self.getImageArray)

    # -----------------
    # Update the window
    def updateProgress(self, text):

        try:
            # Read the output
            crt_frame, n_frames = text.split("/")

            # Format the frames
            crt_frame = int(crt_frame)
            n_frames = int(n_frames)

            # Set the text
            label_text = 'Processing frame ' + str(crt_frame)+'/'+str(n_frames)

            # Set the index
            index = crt_frame * 100 / n_frames

            # Update the display
            self.progressBarLabel.setText(label_text)
            self.progressBarWidget.setValue(index)

        except:
            pass

    # -----------------------------------
    # Get the image class from the thread
    def getImageArray(self, image_array):

        # Close the progress bar window
        self.close()
        self.scheduler.averageCompleted(image_array)

# --------------------------
# Class to handle the thread
class AverageImageJobThread(qtc.QThread):

    release_array = qtc.pyqtSignal(object)

    # Initialise
    def __init__(self, parent, image_array, window, average_type, include_partial):
        super(AverageImageJobThread, self).__init__(parent)

        # Get the parameters
        self.image_array = image_array
        self.window = window
        self.average_type = average_type
        self.include_partial = include_partial

        # Start the event
        self.start()

    # ----------------------
    # Run the periodic event
    def run(self):

        # Process the trajectory
        crt_array = averageStack(self.image_array, self.window, average_type=self.average_type, include_partial=self.include_partial)

        # Return the result
        self.release_array.emit(crt_array)

        # Interrupt the process
        self.stop()

    # -----------------------
    # Stop the periodic event
    def stop(self):
        self.quit()
