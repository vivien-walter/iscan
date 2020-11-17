import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.image_class import ImageCollection

from application_gui.common_gui_functions import openWindow
from application_gui.progressbar.correction_averaging import AverageImageProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class frameAveragingFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\
    ## CALCULATE PROPERTIES
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------
    # Calculate the properties
    def calculateInfos(self):

        # Get the values
        avg_type = self.averagingTypeComboBox.currentText()
        n_frames = int( self.numberFrameEntry.text() )

        # Calculate a standard average
        if avg_type == 'Standard Average':

            # Calculate the number of frames after average
            n_frames_avg = self.max_n // n_frames

            # Check for partial data
            if self.partialDataCheckBox.isChecked():
                if self.max_n % n_frames != 0:
                    n_frames_avg += 1
                n_frames_lost = 0
            else:
                n_frames_lost = self.max_n - (n_frames_avg * n_frames)

        # Calculate a running average
        elif avg_type == 'Running Average':

            # Check for partial data
            if self.partialDataCheckBox.isChecked():
                n_frames_avg = self.max_n
                n_frames_lost = 0
            else:
                n_frames_avg = self.max_n - (n_frames-1)
                n_frames_lost = self.max_n - n_frames_avg

        # Edit the display
        self.frameAfterLabel.setText(str( n_frames_avg ))
        self.frameLostLabel.setText(str( n_frames_lost ))

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # --------------------------------------------
    # Update the display when the slider is edited
    def sliderIsEdited(self, value=None):

        # Edit the entry
        self.numberFrameEntry.setText( str(value) )

        # Refresh
        self.calculateInfos()

    # -------------------------------------------
    # Update the display when the entry is edited
    def entryIsEdited(self):

        # Get the value
        new_value = int( self.numberFrameEntry.text() )

        # Coerce the value
        if new_value < 2:
            new_value = 2
            self.numberFrameEntry.setText( str(new_value) )
        if new_value > self.max_n:
            new_value = self.max_n

        # Edit the slider
        self.numberFrameSlider.setValue(new_value)

        # Refresh
        self.calculateInfos()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ---------------------------
    # Process the frame averaging
    def processAveraging(self):

        # Get the averaging parameters
        avg_type = self.averagingTypeComboBox.currentText()
        n_frames = int( self.numberFrameEntry.text() )
        include_partial = self.partialDataCheckBox.isChecked()

        # Convert the average type
        type_conversion = {
        "Standard Average":'block',
        "Running Average":'running',
        }
        avg_type = type_conversion[avg_type]

        # Open the progress bar window
        openWindow(self.parent, AverageImageProgressBarWindow, 'progress_bar', image_class=self.image_array, window=n_frames, average_type=avg_type, include_partial=include_partial, scheduler=self)

    # -------------------------------------------
    # Open the new tab once the averaging is done
    def averageCompleted(self, averaged_array):

        # Get the current tab
        tab_id = self.parent.imageTabDisplay.currentIndex()
        old_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

        # Load the array in a file
        new_class = ImageCollection(averaged_array, name=old_class.name.strip()+' (Averaged)', space_scale=old_class.scale.space_scale, space_unit=old_class.scale.space_unit, frame_rate=old_class.scale.frame_rate)

        # Update the current tab
        if self.replaceTabCheckBox.isChecked():
            new_class.name = old_class.name
            self.parent.imageTabDisplay.replaceTab(tab_id, new_class)
            self.parent.animationControl.setNFrames(new_class.n_frames)

        # Create a new tab
        else:
            self.parent.imageTabDisplay.newTab(new_class)

        # Close the window
        self.close()
