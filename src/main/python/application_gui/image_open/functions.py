import numpy as np
import os

import PyQt5.QtWidgets as qtw

from image_processing.corrections import backgroundCorrection, intensityCorrection
from image_processing.image_class import ImageCollection
from input_output.image_management import getImagesInfos, loadImages
from settings.recent_files_settings import appendRecentFiles

from application_gui.common_gui_functions import openWindow
from application_gui.messageboxes.display import errorMessage
from application_gui.progressbar.image_open import OpenImageProgressBarWindow
from application_gui.progressbar.correction_background import ImageCorrectionProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class openImageFunctions(object):

    ##-\-\-\-\-\-\
    ## BROWSE FILES
    ##-/-/-/-/-/-/

    # ---------------------------
    # Browse for a file or folder
    def browseImages(self):

        # Open the browser
        if self.singleFileRadiobutton.isChecked():
            imageFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Open Image(s)...", "","Image Files (*.tif;*.tiff;*.png;*.bmp;*.gif);;All Files (*)")
        else:
            imageFile = qtw.QFileDialog.getExistingDirectory(self.parent, "Open Image(s)...")

        # Process only if an image has been selected
        if imageFile:

            # Update the entry line
            self.image_path = imageFile
            self.browseEntry.setText(imageFile)

            # Get the image informations
            self.image_infos = getImagesInfos(imageFile)
            self.loadButton.setEnabled(True)

            # Update the display
            self.updateInformation()

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # --------------------------------------------------
    # Update the information of the image in the display
    def updateInformation(self):

        # Set the number of images
        self.imageNumberLabel.setText( str( self.image_infos['number'] ) )

        # Set the image size
        self.imageSizeLabel.setText( str( self.image_infos['size'][0] )+'x'+str( self.image_infos['size'][1] ) )

        # Set the bitness
        if self.image_infos['max_pv'] > 256:
            _bitness = '16 bits'
            _bitvalue = 65536
        else:
            _bitness = '8 bits'
            _bitvalue = 256

        if self.image_infos['do_sign_correction']:
            _bitness += ' signed'
        else:
            _bitness += ' unsigned'

        self.imageBitsLabel.setText( _bitness )

        # Set the range selection
        if int(self.image_infos['number']) > 1:
            self.frameRangeSelection.setMin(1)
            self.frameRangeSelection.setMax(self.image_infos['number'])
            self.frameRangeSelection.setRange(1,self.image_infos['number'])
            self.frameRangeSelection.setEnabled(True)
        else:
            self.frameRangeSelection.setMin(0)
            self.frameRangeSelection.setMax(1)
            self.frameRangeSelection.setRange(0,1)
            self.frameRangeSelection.setEnabled(False)

        # Set the correction suggestions
        _do_crop = self.parent.config.crop_image and self.image_infos['do_crop']
        self.cropCheckBox.setChecked( _do_crop )

        _do_signed_bits = self.parent.config.correct_signed and self.image_infos['do_sign_correction']
        self.signCorrectionCheckBox.setEnabled( _do_signed_bits )
        self.signCorrectionCheckBox.setChecked( _do_signed_bits )

        _do_background_correction = self.parent.config.auto_background and int(self.image_infos['number']) > 1
        self.backgroundCorrectionCheckBox.setEnabled( _do_background_correction )
        self.backgroundCorrectionCheckBox.setChecked( _do_background_correction )

    ##-\-\-\-\-\-\
    ## USER ACTION
    ##-/-/-/-/-/-/

    # -----------------------
    # Load the selected image
    def getImageFromPath(self):

        # Get the name of the file
        _, image_name = os.path.split(self.image_path)

        # Get the correction to apply
        _do_crop = self.cropCheckBox.isChecked()
        _crop_size = int( self.cropSizeEntry.text() )
        _do_sign_correction = self.signCorrectionCheckBox.isChecked()
        _start,_end = self.frameRangeSelection.getRange()
        _open_range = _start-1, _end

        # Check the crop size
        _proceed = True
        if _do_crop:
            if _crop_size > np.amin([self.image_infos['size'][0], self.image_infos['size'][1]]):
                errorMessage('Cropping Error','The requested crop size is greater than the image size.')
                _proceed = False

        # Load the image
        if _proceed:
            self.image_class = None

            # Open the progress bar window
            openWindow(self.parent, OpenImageProgressBarWindow, 'progress_bar', image_path=self.image_path, name=image_name, open_range=_open_range, crop=_do_crop, crop_size=_crop_size, correct_sign=_do_sign_correction, scheduler=self)

            # Add the image to the list of recent items
            appendRecentFiles(self.image_path)

    # -----------------------------
    # Proceed with the opened image
    def imageStackOpened(self):

        # Add in a new tab
        self.parent.imageTabDisplay.newTab(self.image_class)

        # Do background correction if required
        if self.backgroundCorrectionCheckBox.isChecked():

            # Open the progress window
            openWindow(self.parent, ImageCorrectionProgressBarWindow, 'progress_bar')

            # Get the settings in memory
            do_median = self.parent.config.background_type == 'Median'
            do_division = self.parent.config.correction_type == 'Division'
            do_intensity_correction = self.parent.config.correct_intensity
            replace_tab = not self.parent.config.correct_newtab

            # Apply the background correction
            corrected_array = backgroundCorrection(self.image_class.image.source, median=do_median, divide=do_division)

            # Apply the intensity fluctuation correction - if required
            if do_intensity_correction:
                corrected_array = intensityCorrection(corrected_array)

            # Load the array in a file
            new_class = ImageCollection(corrected_array, name=self.image_class.name.strip()+' (Corrected)', space_scale=self.parent.space_scale, space_unit=self.parent.space_unit, frame_rate=self.parent.frame_rate)

            # Update the current tab
            if replace_tab:
                # Get the current tab
                tab_id = self.parent.imageTabDisplay.currentIndex()

                # Update the tab
                new_class.name = self.image_class.name
                self.parent.imageTabDisplay.replaceTab(tab_id, new_class)

            # Create a new tab
            else:
                self.parent.imageTabDisplay.newTab(new_class)

            # Close the progress window
            self.parent.subWindows['progress_bar'].close()
            self.parent.application.processEvents()

        # Close the current window
        self.close()
