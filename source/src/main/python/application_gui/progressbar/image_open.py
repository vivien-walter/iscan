import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from input_output.image_management import loadImages

from application_gui.progressbar.streams import Stream

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class OpenImageProgressBarWindow(qtw.QMainWindow):
    def __init__(self, parent, image_path=None, name="Untitled", open_range=None, crop=True, crop_size=512, correct_sign=True, scheduler=None):
        super(OpenImageProgressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_path = image_path
        self.name = name
        self.open_range = open_range
        self.crop = crop
        self.crop_size = crop_size
        self.correct_sign = correct_sign
        self.scheduler = scheduler
        self.setWindowTitle("Opening Images...")
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
        thread = OpenImageJobThread(self.parent, self.parent, self.image_path, self.name, self.open_range, self.crop, self.crop_size, self.correct_sign)
        thread.release_class.connect(self.getImageClass)

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
            label_text = 'Opening frame ' + str(crt_frame)+'/'+str(n_frames)

            # Set the index
            index = crt_frame * 100 / n_frames

            # Update the display
            self.progressBarLabel.setText(label_text)
            self.progressBarWidget.setValue(index)

        except:
            pass

    # -----------------------------------
    # Get the image class from the thread
    def getImageClass(self, image_class):

        # Save the trajectory in the class
        self.scheduler.image_class = image_class

        # Close the progress bar window
        self.close()
        self.scheduler.imageStackOpened()

# --------------------------
# Class to handle the thread
class OpenImageJobThread(qtc.QThread):

    release_class = qtc.pyqtSignal(object)

    # Initialise
    def __init__(self, parent, parent_scale, image_path, name, open_range, crop, crop_size, correct_sign):
        super(OpenImageJobThread, self).__init__(parent)

        # Get the parameters
        self.parent_scale = parent_scale
        self.image_path = image_path
        self.name = name
        self.open_range = open_range
        self.crop = crop
        self.crop_size = crop_size
        self.correct_sign = correct_sign

        # Start the event
        self.start()

    # ----------------------
    # Run the periodic event
    def run(self):

        # Process the trajectory
        crt_class = loadImages(self.image_path, name=self.name, open_range=self.open_range, crop=self.crop, crop_size=self.crop_size, correct_sign=self.correct_sign, space_scale=self.parent_scale.space_scale, space_unit=self.parent_scale.space_unit, frame_rate=self.parent_scale.frame_rate)

        # Return the result
        self.release_class.emit(crt_class)

        # Interrupt the process
        self.stop()

    # -----------------------
    # Stop the periodic event
    def stop(self):
        self.quit()
