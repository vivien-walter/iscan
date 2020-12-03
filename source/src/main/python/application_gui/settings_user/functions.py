##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class userSettingsFunctions(object):

    # --------------------------------
    # Display the user settings window
    def saveServerSettings(self):

        # - Refresh the status
        # General
        self.parent.config.single_images = self.singleFileRadiobutton.isChecked()
        self.parent.config.autoload_images = self.autoOpenImageCheckBox.isChecked()
        #self.parent.config.dark_theme = self.darkThemeCheckBox.isChecked()
        self.parent.config.auto_background = self.autoBackgroundCorrectionCheckBox.isChecked()
        # Image
        self.parent.config.crop_image = self.cropImageCheckBox.isChecked()
        self.parent.config.crop_size = int( self.cropSizeEntry.text() )
        self.parent.config.correct_signed = self.correctSignedBitsCheckBox.isChecked()
        self.parent.config.correction_type = self.correctionTypeComboBox.currentText()
        self.parent.config.background_type = self.backgroundTypeComboBox.currentText()
        self.parent.config.correct_intensity = self.correctFluctuationsCheckBox.isChecked()
        self.parent.config.intensity_correction_type = self.fluctuationCorrectionTypeComboBox.currentText()
        self.parent.config.correct_newtab = self.newTabCheckBox.isChecked()
        # Scale
        pixel_distance = self.pixelDistanceEntry.text()
        real_distance = self.knownDistanceEntry.text()
        self.parent.config.space_scale = float(pixel_distance) / float(real_distance)
        self.parent.config.space_unit = self.lengthUnitEntry.text()
        self.parent.config.frame_rate = float( self.frameRateEntry.text() )

        # Save the config
        self.parent.config.save()

        # Close the window
        self.close()
