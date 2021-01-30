import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from input_output.folder_management import convertFolders2Stacks

from application_gui.progressbar.streams import Stream

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class ConvertFolderProgressBarWindow(qtw.QMainWindow):
    def __init__(self, parent, folder_list=None, delete_folders=True, scheduler=None):
        super(ConvertFolderProgressBarWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.folder_list = folder_list
        self.delete_folders = delete_folders
        self.scheduler = scheduler
        self.setWindowTitle("Converting Folders...")
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

        # Show the progress bar for folders
        self.folderProgressBarWidget = qtw.QProgressBar()
        parentWidget.addWidget(self.folderProgressBarWidget)

        # Show the progress bar for images
        self.imagesProgressBarWidget = qtw.QProgressBar()
        parentWidget.addWidget(self.imagesProgressBarWidget)

    ##-\-\-\-\-\-\
    ## JOB HANDLING
    ##-/-/-/-/-/-/

    # -------------
    # Start the job
    def startJob(self):

        # Start the listener
        sys.stdout = Stream(newText=self.updateProgress)

        # Run the job
        thread = ConvertFoldersJobThread(self.parent, self.folder_list, self.delete_folders)
        thread.convertionComplete.connect(self.convertionComplete)

    # -----------------
    # Update the window
    def updateProgress(self, text):

        try:
            # Read the output
            crt_frame, n_frames = text.split("/")

            # Read folder
            if 'folder' in crt_frame:

                # Format the tolder
                crt_folder = int(crt_frame.split('folder')[1])
                n_folders = int(n_frames)

                # Set the text
                label_text = 'Processing folder ' + str(crt_folder)+'/'+str(n_folders)

                # Set the index
                index = crt_folder * 100 / n_folders

                # Update the display
                self.progressBarLabel.setText(label_text)
                self.folderProgressBarWidget.setValue(index)

            # Read files
            else:

                # Format the frames
                crt_frame = int(crt_frame)
                n_frames = int(n_frames)

                # Set the text
                label_text = 'Opening frame ' + str(crt_frame)+'/'+str(n_frames)

                # Set the index
                index = crt_frame * 100 / n_frames

                # Update the display
                self.progressBarLabel.setText(label_text)
                self.imagesProgressBarWidget.setValue(index)

        except:
            pass

    # ----------------------------------------------------
    # Send a signal that the convertion has been completed
    def convertionComplete(self):

        # Close the progress bar window
        self.scheduler.resetDisplay()
        self.close()

# --------------------------
# Class to handle the thread
class ConvertFoldersJobThread(qtc.QThread):

    convertionComplete = qtc.pyqtSignal()

    # Initialise
    def __init__(self, parent, folder_list, delete_folders):
        super(ConvertFoldersJobThread, self).__init__(parent)

        # Get the parameters
        self.folder_list = folder_list
        self.delete_folders = delete_folders

        # Start the event
        self.start()

    # ----------------------
    # Run the periodic event
    def run(self):

        # Process the trajectory
        convertFolders2Stacks(self.folder_list, delete_folders=self.delete_folders)

        # Return the result
        self.convertionComplete.emit()

        # Interrupt the process
        self.stop()

    # -----------------------
    # Stop the periodic event
    def stop(self):
        self.quit()
