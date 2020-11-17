##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class TrackDisplaySettingsFunctions(object):

    # --------------------------------
    # Display the user settings window
    def saveTrackDisplaySettings(self):

        # - Refresh the status
        # Positions
        self.parent.disptrack_conf.show_positions = self.displayPositionsCheckbox.isChecked()
        self.parent.disptrack_conf.current_position = self.currentOnlyPositionsCheckbox.isChecked()
        self.parent.disptrack_conf.color_position = self.colorCurrentPositionCheckbox.isChecked()
        # Paths
        self.parent.disptrack_conf.show_paths = self.displayPathsCheckbox.isChecked()
        self.parent.disptrack_conf.current_path = self.currentOnlyPathCheckbox.isChecked()
        self.parent.disptrack_conf.color_path = self.colorCurrentPathCheckbox.isChecked()

        # Save the config
        self.parent.disptrack_conf.save()

        # Close the window
        self.close()

        # Refresh the current display
        tab_id = self.parent.imageTabDisplay.currentIndex()
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()
