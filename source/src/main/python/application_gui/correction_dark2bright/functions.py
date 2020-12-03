import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class darkToBrightCorrectionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------
    # Initialise the display
    def initialiseDisplay(self):

        # Set the value of the checkbox
        _index_background = self.backgroundTypeComboBox.findText(self.parent.config.background_type.capitalize(), qtc.Qt.MatchFixedString)
        if _index_background >= 0:
             self.backgroundTypeComboBox.setCurrentIndex(_index_background)

    # -----------------------
    # Update the main display
    def refreshFrameDisplay(self):

        # Get the correction type
        _do_median = self.backgroundTypeComboBox.currentText().lower() == 'median'

        # Get the current tab
        tab_id = self.parent.imageTabDisplay.currentIndex()

        # Refresh with the selected settings
        if self.previewCheckBox.isChecked():
            self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.dark2BrightTest(correction=True, median=_do_median)

        # Refresh with the current settings
        else:
            self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.dark2BrightTest()

        # Update the display
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ------------------
    # Apply the settings
    def applySettings(self):

        # Get the current the tab
        tab_id = self.parent.imageTabDisplay.currentIndex()

        # Apply the correction
        _do_median = self.backgroundTypeComboBox.currentText().lower() == 'median'
        self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.dark2BrightDisplay(median=_do_median)

        # Refresh the display
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

        # Close the window
        self.close()
