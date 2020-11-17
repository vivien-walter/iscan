import numpy as np

import PyQt5.QtWidgets as qtw
from pyqtgraph import plot
import pyqtgraph as pg

from application_gui.common_gui_functions import openWindow
from application_gui.messageboxes.display import warningProceedMessage
from application_gui.progressbar.correction_background import ImageCorrectionProgressBarWindow

from image_processing.corrections import getFluctuations, intensityCorrection
from image_processing.image_class import ImageCollection

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class fluctuationCorrectionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## PLOT FLUCTUATIONS
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Analyse the stack and plot fluctuations
    def plotFluctuations(self):

        # Get the intensity fluctuations
        frame_values = np.arange(self.image_array.shape[0])
        mean_PVs = getFluctuations(self.image_array)

        # Update the graph widget
        pen = pg.mkPen(color=(0, 0, 0), width=3)
        self.graphWidget.plot(frame_values, mean_PVs, pen=pen)

        # Set the graph style
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Pixel Value Intensity (AU)')
        self.graphWidget.setLabel('bottom', 'Time (frame)')
        self.graphWidget.showGrid(x=True, y=True)

        # Update the stats
        self.meanValueLabel.setText(str( np.mean(mean_PVs) ))
        self.standardDeviationLabel.setText(str( np.std(mean_PVs) ))
        self.variations_value = np.std(mean_PVs) *100 / np.mean(mean_PVs)
        self.variationsLabel.setText( str(self.variations_value)+' %' )

        # Add warning
        if self.variations_value < 0.01:
            self.variationsLabel.setStyleSheet('color: red')

    ##-\-\-\-\-\-\-\-\-\
    ## PROCESS CORRECTION
    ##-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Correct the intensity fluctuations
    def correctFluctuations(self):

        # Check the fluctuations values
        do_correction = True
        if self.variations_value < 0.01:
            do_correction = warningProceedMessage('Low intensity fluctuations', 'The measured intensity fluctuations are below 0.01% of the mean intensity. Performing a correction might not improve the quality of the signal. Proceed anyway?')

        # Do the correction if accepted
        if do_correction:

            # Open the progress window
            openWindow(self.parent, ImageCorrectionProgressBarWindow, 'progress_bar')

            self.image_array = intensityCorrection(self.image_array)

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            use_name = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.name

            # Load the array in a file
            new_class = ImageCollection(self.image_array, name=use_name, space_scale=self.parent.space_scale, space_unit=self.parent.space_unit, frame_rate=self.parent.frame_rate)

            # Refresh the tab
            self.parent.imageTabDisplay.replaceTab(tab_id, new_class)

            # Close the progress window
            self.parent.subWindows['progress_bar'].close()
            self.parent.application.processEvents()

        # Close the window
        self.close()
