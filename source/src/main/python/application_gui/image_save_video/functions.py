import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from input_output.image_management import saveVideo

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class saveVideoFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## SAVE IMAGE(S) IN FILE
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Save the current image using the selection
    def saveInFile(self):

        # Retrieve the selection
        frame_rate = int(self.frameRateEntry.text())
        save_raw = self.saveRawCheckbox.isChecked()
        save_trj = self.saveTrajectoryCheckbox.isChecked()
        save_scale = self.saveScaleBarCheckbox.isChecked()

        # Get the window title
        _window_title = "Save Video as..."

        # Browse for the image type
        _base_name, _ = os.path.splitext(self.image_class.name)
        dataFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, _window_title, _base_name, 'Video MP4 (*.mp4)')

        # Get the selection to save
        if save_raw:
            array = self.image_class.image.source
        else:
            array = self.image_class.image.display

        # Check the extension
        dataFile, _ = os.path.splitext(dataFile)
        dataFile += ".mp4"

        # Save the image
        saveVideo(array, dataFile, fps=frame_rate)

        # Close the window
        self.close()
