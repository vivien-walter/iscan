import logging
import sys
import trackpy as tp

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.messageboxes.display import errorMessage
from application_gui.progressbar.streams import Stream

from trajectory.trajectory_class import startManager

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class TrackpyProgressBarWindow(qtw.QMainWindow):
    def __init__(self, parent, image_class=None, trackpy_session=None, scheduler=None):
        super(TrackpyProgressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.session = trackpy_session
        self.scheduler = scheduler
        self.setWindowTitle("Tracking Particles...")
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Initialise the parameters
        self.n_max = 0

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
        sys.stderr = sys.__stderr__
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

        # Prepare the parameters based on the session to read
        self.n_max = self.image_class.n_frames

        # Format the logger of trackpy batch
        trackpy_batch_logger = logging.getLogger('trackpy.feature')
        trackpy_batch_logger.addHandler( logging.StreamHandler(Stream(newText=self.updateProgress)) )
        trackpy_batch_logger.setLevel(logging.INFO)

        # Format the logger of trackpy link
        trackpy_find_logger = logging.getLogger('trackpy.linking.linking')
        trackpy_find_logger.addHandler( logging.StreamHandler(Stream(newText=self.updateProgress)) )
        trackpy_find_logger.setLevel(logging.INFO)

        # Start the listener
        sys.stderr = Stream(newText=self.handleErrors)

        # Run the job
        thread = BatchJobThread(self.parent, self.image_class, self.session)
        thread.release_trajectory.connect(self.getTrajectory)

    # -----------------
    # Update the window
    def updateProgress(self, text):

        try:
            # Read the output
            output_frame, output_features = text.split(":")
            if 'features' in output_features:
                output_type = 'trackpy.feature.batch'
            else:
                output_type = 'trackpy.linking.linking.link_iter'

            # Format the frames
            output_frame = int(output_frame.split('Frame')[1])

            # Set the text
            if output_type == 'trackpy.feature.batch':
                label_text = 'Reading frames ('
            else:
                label_text = 'Processing features ('
            label_text += str(output_frame)+'/'+str(self.n_max)+').' + output_features

            # Set the index
            index = output_frame * 100 / self.n_max

            # Update the display
            self.progressBarLabel.setText(label_text)
            self.progressBarWidget.setValue(index)

        except:
            pass

    # ----------------------------------
    # Get the trajectory from the thread
    def getTrajectory(self, trj):

        # Save the trajectory in the class
        self.image_class.trajectory = startManager(trj)

        # Close the progress bar window
        self.close()
        self.scheduler.stackProcessed()

    ##-\-\-\-\-\-\-\-\
    ## ERRORS HANDLING
    ##-/-/-/-/-/-/-/-/

    # -----------------------------
    # Interrupt in case of an error
    def handleErrors(self, text):

        # Handle subnetwork exceptions
        if "SubnetOversizeException" in text:
            self.close()
            errorMessage("Subnetwork Oversize","Too many points have been found in the subnetwork. Reduce the search range or increase the intensity threshold before trying again.")

# --------------------------
# Class to handle the thread
class BatchJobThread(qtc.QThread):

    release_trajectory = qtc.pyqtSignal(object)

    # Initialise
    def __init__(self, parent, image_class, session):
        super(BatchJobThread, self).__init__(parent)

        # Get the parameters
        self.image_class = image_class
        self.session = session

        # Start the event
        self.start()

    # ----------------------
    # Run the periodic event
    def run(self):

        # Process the trajectory
        crt_trajectory = self.session.batch(self.image_class.image.source, filter=True)

        # Return the result
        self.release_trajectory.emit(crt_trajectory)

        # Interrupt the process
        self.stop()

    # -----------------------
    # Stop the periodic event
    def stop(self):
        self.quit()
