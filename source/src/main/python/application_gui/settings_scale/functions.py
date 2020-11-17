##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class SetScaleFunctions(object):

    # -------------------
    # Apply the new scale
    def applyScale(self):

        # Retrieve the information
        pixel_distance = self.pixelDistanceEntry.text()
        real_distance = self.knownDistanceEntry.text()
        space_scale = float(pixel_distance) / float(real_distance)
        space_unit = self.lengthUnitEntry.text()
        frame_rate = float( self.frameRateEntry.text() )

        # Apply the change to everything open in iSCAN
        if self.globalScaleCheckBox.isChecked():

            # Edit the scale saved in the main window
            self.parent.space_scale = space_scale
            self.parent.space_unit = space_unit
            self.parent.frame_rate = frame_rate

            # Loop over all the open tabs
            for image_tab in self.parent.imageTabDisplay.displayedTabs:
                crt_class = image_tab.image_class

                # Edit the settings
                crt_class.scale.space_scale = space_scale
                crt_class.scale.space_unit = space_unit
                crt_class.scale.frame_rate = frame_rate

        # Apply the change to the current image only
        else:
            self.image_class.scale.space_scale = space_scale
            self.image_class.scale.space_unit = space_unit
            self.image_class.scale.frame_rate = frame_rate

        # Close the window
        self.close()
