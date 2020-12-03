import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.corrections import backgroundCorrection, intensityCorrection, correctSignedBits
from image_processing.image_class import ImageCollection
from image_processing.modifications import cropImage
from input_output.image_management import getArrayInfos

from application_gui.common_gui_functions import openWindow
from application_gui.progressbar.correction_background import ImageCorrectionProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class backgroundCorrectionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## PRE-ANALYSE IMAGE
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Analyse the stack to get recommendations
    def analyseStack(self):

        # Get the image informations
        self.image_infos = getArrayInfos(self.image_array)

        # Set the combo boxes settings
        _index_correction = self.correctionTypeComboBox.findText(self.parent.config.correction_type.capitalize(), qtc.Qt.MatchFixedString)
        if _index_correction >= 0:
             self.correctionTypeComboBox.setCurrentIndex(_index_correction)

        _index_background = self.backgroundTypeComboBox.findText(self.parent.config.background_type.capitalize(), qtc.Qt.MatchFixedString)
        if _index_background >= 0:
             self.backgroundTypeComboBox.setCurrentIndex(_index_background)

        # Set the correction suggestions
        self.correctFluctuationsCheckBox.setChecked( self.parent.config.correct_intensity )

        _do_crop = self.parent.config.crop_image and self.image_infos['do_crop']
        self.cropCheckBox.setEnabled( _do_crop )
        self.cropCheckBox.setChecked( _do_crop )

        _do_signed_bits = self.parent.config.correct_signed and self.image_infos['do_sign_correction']
        #self.signCorrectionCheckBox.setEnabled( _do_signed_bits )
        self.signCorrectionCheckBox.setChecked( _do_signed_bits )

        # Set the new tab option
        self.replaceTabCheckBox.setChecked( not self.parent.config.correct_newtab )

    ##-\-\-\-\-\-\-\
    ## PROCESS IMAGE
    ##-/-/-/-/-/-/-/

    # ----------------------------------------------
    # Process the background correction of the image
    def processImage(self):

        # Retrieve the user selection
        do_division = self.correctionTypeComboBox.currentText() == 'Division'
        do_median = self.backgroundTypeComboBox.currentText() == 'Median'
        do_intensity_correction = self.correctFluctuationsCheckBox.isChecked()
        do_crop = self.cropCheckBox.isChecked()
        crop_size = int(self.cropSizeEntry.text())
        do_bit_correction = self.signCorrectionCheckBox.isChecked()
        replace_tab = self.replaceTabCheckBox.isChecked()

        # Crop the image - if required
        if do_crop:
            self.image_array = cropImage(self.image_array, (crop_size,crop_size))

        # Correct signed bits image - if required
        if do_bit_correction:
            self.image_array = correctSignedBits(self.image_array)

        # Open the progress window
        openWindow(self.parent, ImageCorrectionProgressBarWindow, 'progress_bar')

        # Apply the background correction
        self.image_array = backgroundCorrection(self.image_array, median=do_median, divide=do_division)

        # Apply the intensity fluctuation correction - if required
        if do_intensity_correction:
            _intensity_correction_type = self.parent.config.intensity_correction_type.lower()
            self.image_array = intensityCorrection(self.image_array, correction=_intensity_correction_type)

        # Get the current tab
        tab_id = self.parent.imageTabDisplay.currentIndex()
        old_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

        # Load the array in a file
        new_class = ImageCollection(self.image_array, name=old_class.name.strip()+' (Corrected)', space_scale=old_class.scale.space_scale, space_unit=old_class.scale.space_unit, frame_rate=old_class.scale.frame_rate)

        # Update the current tab
        if replace_tab:
            new_class.name = old_class.name
            self.parent.imageTabDisplay.replaceTab(tab_id, new_class)

        # Create a new tab
        else:
            self.parent.imageTabDisplay.newTab(new_class)

        # Close the progress window
        self.parent.subWindows['progress_bar'].close()
        self.parent.application.processEvents()

        # Close the window
        self.close()
