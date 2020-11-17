import sys

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.progressbar.streams import Stream

##-\-\-\-\-\-\
## PROGRESS BAR
##-/-/-/-/-/-/

class progressBarModes:

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## INITIALISE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Initialise the display based on the mode
    def initMode(self):

        # Check the title
        title_modes = {
        'trackpy_batch':'Tracking Particles'
        }
        title = title_modes[self.mode]

        # Initialise the label
        label_modes = {
        'trackpy_batch':'Preprocessing stack...'
        }
        label = label_modes[self.mode]

        # Update the display
        self.setWindowTitle(title)
        self.progressBarLabel.setText(label)

        # Start console listeners
        if self.mode in ['trackpy_batch']:
            self.startConsoleListener()

        # Force update of the window
        self.parent.application.processEvents()

    # -----------------------------------
    # Listen to the output of the console
    def startConsoleListener(self):

        # Start the Stream listener
        sys.stdout = Stream(new_text=self.updateProgress)

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## UPDATE THE PROGRESS BAR
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Update the status of the progress bar
    def updateProgress(self, text=None, bar_progress=None):

        # Check the mode
        if self.mode == 'trackpy_batch':

            # Set the new text
            new_text = text.split(':')[2].strip()

            # Set the bar progress
            current_frame = int(text.split('Frame')[1].split(':')[0].strip())
            print(current_frame)

            bar_progress = int( 100 * (current_frame+1) / self.n_max )

        # Close the current window
        if bar_progress >= 100:
            self.close()

        # Update the text display
        self.progressBarLabel.setText( new_text )

        # Update the status of the progress bar
        self.progressBarWidget.setValue(bar_progress)
