import os

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from input_output.image_management import saveStack

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class saveImageStackFunctions(object):

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # --------------------------------------
    # Update the display for the radiobutton
    def updateRadioButton(self):

        # Get the selection
        if self.formatComboBox.currentText() == 'Gif':

            # Check the 8-bit button
            self.bit8Radiobutton.setChecked( True )

            # Disable the display
            self.bit16Radiobutton.setEnabled( False )
            self.bit8Radiobutton.setEnabled( False )

        # Reset the display
        else:
            self.bit16Radiobutton.setEnabled( True )
            self.bit8Radiobutton.setEnabled( True )

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## SAVE IMAGE(S) IN FILE
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Save the current image using the selection
    def saveInFile(self):

        # Retrieve the selection
        _file_format = self.formatComboBox.currentText()
        save_raw = self.saveRawCheckbox.isChecked()
        save_trj = self.saveTrajectoryCheckbox.isChecked()
        save_scale = self.saveScaleBarCheckbox.isChecked()

        # Get bit depth
        if self.bit16Radiobutton.isChecked():
            bit_depth = 16
        else:
            bit_depth = 8

        # Get the image type and extension
        format_list = {
        'Tiff':'Tagged Image File (*.tif)',
        'Gif':'Graphics Interchange Format (*.gif)',
        }
        format_extension = {
        'Tiff':'.tif',
        'Gif':'.gif',
        }
        save_format = format_list[_file_format]
        file_ext = format_extension[_file_format]

        # Get the window title
        _window_title = "Save Stack as..."

        # Browse for the image type
        _base_name, _ = os.path.splitext(self.image_class.name)
        dataFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, _window_title, _base_name, save_format)

        # Get the selection to save
        if save_raw:
            array = self.image_class.image.source
        else:
            array = self.image_class.image.display

        # Check the extension
        dataFile, _ = os.path.splitext(dataFile)
        dataFile += file_ext

        # Save the image
        saveStack(array, dataFile, bit_depth=bit_depth, rescale=not save_raw)

        # Close the window
        self.close()
