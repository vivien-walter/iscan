import bottleneck as bn
import numpy as np

import PyQt5.QtWidgets as qtw
import pyqtgraph as pg

from application_gui.common_gui_functions import updateValue

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class contrastCorrectionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## PLOT FLUCTUATIONS
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------------------------
    # Analyse the image and plot the distribution
    def getDistribution(self):

        # Calculate the pixel mean value and standard deviation
        self.image_mean = bn.nanmean(self.analyzed_image)
        self.image_stdev = bn.nanstd(self.analyzed_image)
        pv_max = np.amax(self.analyzed_image)

        # Calculate the range
        self._factor = 1
        if pv_max < 50:
            hist_max = pv_max * 2
            self._factor = 1000
        elif pv_max > 2**10:
            hist_max = 2**16 - 1
        else:
            hist_max = 2**8 - 1
        hist_min = hist_max / ( 2**16 - 1 )

        self.hist_min = hist_min
        self.hist_max = hist_max

        # Get the intensity distribution
        self.histogram_values, histogram_bins = np.histogram(self.analyzed_image, bins=255, range=(hist_min, hist_max))
        self.histogram_bins = (histogram_bins[1:] + histogram_bins[:-1])/2
        self.histogram_max = np.amax(self.histogram_values)
        self.histogram_submax = self.histogram_max / 10

        # Initialise the values for the slider
        self.pv_min = np.amin(self.analyzed_image)
        self.pv_max = pv_max
        self.brightness = (self.pv_max + self.pv_min)/2
        self.contrast = self.pv_max - self.pv_min

        # Save the initial values for reset
        self.initial_min = self.pv_min
        self.initial_max = self.pv_max

        # Block signals
        self.minPVSlider.blockSignals(True)
        self.maxPVSlider.blockSignals(True)
        self.brightnessSlider.blockSignals(True)
        self.contrastSlider.blockSignals(True)

        # Initialise the slider positions and limits
        self.minPVSlider.setMinimum(self.hist_min * self._factor)
        self.maxPVSlider.setMinimum(self.hist_min * self._factor)
        self.brightnessSlider.setMinimum(self.hist_min * self._factor)
        self.contrastSlider.setMinimum(self.hist_min * self._factor)

        self.minPVSlider.setMaximum(self.hist_max * self._factor)
        self.maxPVSlider.setMaximum(self.hist_max * self._factor)
        self.brightnessSlider.setMaximum(self.hist_max * self._factor)
        self.contrastSlider.setMaximum(self.hist_max * self._factor)

        # Release signals
        self.minPVSlider.blockSignals(False)
        self.maxPVSlider.blockSignals(False)
        self.brightnessSlider.blockSignals(False)
        self.contrastSlider.blockSignals(False)

        # Update the display
        self.updateDisplay()

    # -------------------------------------------------------
    # Analyse the stack and plot the pixel value distribution
    def plotDistribution(self):

        # Reset the graph
        self.graphWidget.clear()

        # Get the width of the bars
        bar_width = self.histogram_bins[1] - self.histogram_bins[0]

        # Plot the bars
        self.histogram_plot = pg.BarGraphItem(x=self.histogram_bins, height=self.histogram_values, width=bar_width)
        self.graphWidget.addItem(self.histogram_plot)

        # Plot the line
        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot([self.pv_min, self.pv_max], [0, self.histogram_max], pen=pen)
        self.graphWidget.plot([self.pv_max, self.pv_max], [0, self.histogram_submax], pen=pen)

        # Set the graph style
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Count')
        self.graphWidget.setLabel('bottom', 'Pixel Value Intensity (AU)')

    ##-\-\-\-\-\-\-\-\-\-\
    ## REFRESH THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # --------------------------
    # Update the sliders display
    def updateDisplay(self):

        # Set the values of the sliders
        updateValue(self.minPVSlider, self.pv_min * self._factor)
        updateValue(self.maxPVSlider, self.pv_max * self._factor)
        updateValue(self.brightnessSlider, self.brightness * self._factor)
        updateValue(self.contrastSlider, self.contrast * self._factor)

        # Set the values of the label
        self.minValueLabel.setText( str(self.pv_min) )
        self.maxValueLabel.setText( str(self.pv_max) )

        # Plot the distribution
        self.plotDistribution()

        # Update the display if live preview
        if self.liveCheckBox.isChecked():
            self.refreshFrameDisplay()

    # -----------------------
    # Update the main display
    def refreshFrameDisplay(self):

        # Get the current tab
        tab_id = self.parent.imageTabDisplay.currentIndex()

        # Refresh with the selected settings
        if self.liveCheckBox.isChecked():
            self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.rescaleTest([self.pv_min, self.pv_max])

        # Refresh with the current settings
        else:
            self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.rescaleTest()

        # Update the display
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## MANAGE THE VALUE CHANGE
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Update the value of the min slider
    def _update_min(self):
        self.pv_min = self.brightness - self.contrast / 2

    # ----------------------------------
    # Update the value of the max slider
    def _update_max(self):
        self.pv_max = self.brightness + self.contrast / 2

    # -----------------------------------------
    # Update the value of the brightness slider
    def _update_brightness(self):
        self.brightness = (self.pv_max + self.pv_min)/2

    # ---------------------------------------
    # Update the value of the contrast slider
    def _update_contrast(self):
        self.contrast = self.pv_max - self.pv_min

    # ----------------------------------------------
    # Edit the display when the min value is changed
    def minChanged(self, new_value):

        # Rescale
        new_value /= self._factor

        # Coerce the value
        if new_value >= self.pv_max:
            new_value = self.pv_max - self.hist_min

        # Update the values
        self.pv_min = new_value
        self._update_brightness()
        self._update_contrast()

        # Update the slider
        self.updateDisplay()

    # ----------------------------------------------
    # Edit the display when the max value is changed
    def maxChanged(self, new_value):

        # Rescale
        new_value /= self._factor

        # Coerce the value
        if new_value <= self.pv_min:
            new_value = self.pv_min + self.hist_min

        # Update the values
        self.pv_max = new_value
        self._update_brightness()
        self._update_contrast()

        # Update the slider
        self.updateDisplay()

    # -----------------------------------------------------
    # Edit the display when the brightness value is changed
    def brightnessChanged(self, new_value):

        # Rescale
        new_value /= self._factor

        # Calculate the total range
        mid_range = self.contrast / 2

        # Coerce the value
        if new_value - mid_range < self.hist_min:
            new_value = self.hist_min + mid_range
        elif new_value + mid_range > self.hist_max:
            new_value = self.hist_max - mid_range

        # Update the value
        self.brightness = new_value
        self._update_min()
        self._update_max()

        # Update the slider
        self.updateDisplay()

    # ---------------------------------------------------
    # Edit the display when the contrast value is changed
    def contrastChanged(self, new_value):

        # Rescale
        new_value /= self._factor

        # Calculate the total range
        mid_range = new_value / 2

        # Coerce the value
        if self.brightness - mid_range < self.hist_min:
            new_value = (self.brightness - self.hist_min) * 2
        elif self.brightness + mid_range > self.hist_max:
            new_value = (self.hist_max - self.brightness) * 2

        # Update the value
        self.contrast = new_value
        self._update_min()
        self._update_max()

        # Update the slider
        self.updateDisplay()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # --------------------
    # Set to auto settings
    def setAutoValues(self):

        # Determine the limits based on the mean and standard deviation
        currentAttempt = self.auto_attempt + 1
        if currentAttempt < 5:

            # Calculate the factor for the standard deviation
            factorList = [0, 3, 2, 1, 0.5]
            factor = factorList[currentAttempt]

            # Calculate the limits
            limits = [self.image_mean - factor * self.image_stdev, self.image_mean + factor * self.image_stdev]

        # Cover the whole histogram
        elif currentAttempt == 5:
            limits = self.hist_min, self.hist_max

        # Reset to the initial values
        else:
            limits = self.initial_min, self.initial_max
            currentAttempt = 0
        self.auto_attempt = currentAttempt

        # Re-assign the initial values
        self.pv_min, self.pv_max = limits

        # Update the values
        self._update_brightness()
        self._update_contrast()

        # Update the slider
        self.updateDisplay()

    # ----------------
    # Reset the values
    def resetValues(self):

        # Re-assign the initial values
        self.pv_min = self.initial_min
        self.pv_max = self.initial_max

        # Update the values
        self._update_brightness()
        self._update_contrast()

        # Update the slider
        self.updateDisplay()

    # ------------------
    # Apply the settings
    def applySettings(self):

        # Get the current the tab
        tab_id = self.parent.imageTabDisplay.currentIndex()

        # Apply the correction
        self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.contrast_limits = [self.pv_min, self.pv_max]
        self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.rescaleForDisplay()

        # Refresh the display
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

        # Close the window
        self.close()
