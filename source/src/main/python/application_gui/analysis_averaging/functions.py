from math import floor
import numpy as np
import os
import pandas as pd

import PyQt5.QtWidgets as qtw
from pyqtgraph import plot
import pyqtgraph as pg

from image_processing.averaging import averageStack
from signal_processing.measurement import readSingle

from application_gui.common_gui_functions import openWindow
from application_gui.progressbar.analyse_averaging import AnalyseAveragingProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class signalAveragingFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Initialise the display of the window
    def initialiseDisplay(self):

        # Update the path selection
        path_list = self.image_class.trajectory.listTracks().astype(str)
        self.pathSelectionBox.addItems(path_list)

        # Update the range selection
        max_averaging = int(floor( self.image_class.n_frames / 2 ))
        self.frameRangeSelection.setMax(max_averaging)
        self.frameRangeSelection.setRange(2,max_averaging)

        # Set the graph style
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Contrast (%)')
        self.graphWidget.setLabel('bottom', '# Averaged frames')
        self.graphWidget.showGrid(x=True, y=True)

    # ---------------------------------------
    # Analyse the stack and plot fluctuations
    def plotFluctuations(self):

        # Check if data are in the memory
        if self.averaging_result is not None:

            # Get the value to display
            n_avg = self.averaging_result['averaged frames']

            if self.showContrastRadiobutton.isChecked():
                y_value = self.averaging_result['contrast']
                y_label = 'Contrast (%)'
            elif self.showNoiseRadiobutton.isChecked():
                y_value = self.averaging_result['noise']
                y_label = 'Noise (%)'
            else:
                y_value = self.averaging_result['snr']
                y_label = 'SNR'

            # Reset the graph
            self.graphWidget.clear()

            # Update the graph widget
            pen = pg.mkPen(color=(0, 0, 0), width=3)
            self.graphWidget.plot(n_avg, y_value, pen=pen)

            # Set the graph style
            self.graphWidget.setBackground('w')
            self.graphWidget.setLabel('left', y_label)
            self.graphWidget.setLabel('bottom', '# Averaged frames')
            self.graphWidget.showGrid(x=True, y=True)

    ##-\-\-\-\-\-\-\-\-\
    ## PROCESS AVERAGING
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Perform all the required calculation
    def processAveraging(self):

        # Get the information
        path_id = int( self.pathSelectionBox.currentText() )
        average_type = self.averagingTypeComboBox.currentText()
        min_avg, max_avg = self.frameRangeSelection.getRange()

        # Get the position to process
        crt_position = self.image_class.trajectory.positions
        crt_position = crt_position[crt_position['particle'] == path_id]
        _all_frames = crt_position['frame'].unique()
        object_position = crt_position[crt_position['frame'] == np.amin(_all_frames)]
        object_position = object_position[['y','x']].to_numpy()
        object_position = object_position[0]

        # Get the type of average
        type_conversion = {
        "Standard Average":'block',
        "Running Average":'running',
        }
        average_type = type_conversion[average_type]

        # Initialise the variables
        all_n_avg = []
        all_contrast = []
        all_noise = []
        all_snr = []

        # Open the progress window
        openWindow(self.parent, AnalyseAveragingProgressBarWindow, 'progress_bar')

        # Do the loop
        n_avg = (max_avg-min_avg)+1
        for i, n_frames in enumerate( range(min_avg, max_avg+1) ):

            # Update the progress bar
            self.parent.subWindows['progress_bar'].updateProgress(i+1, n_avg)
            self.parent.application.processEvents()

            print( str(i+1)+'/'+str(n_avg) )

            # Do the current averaging
            crt_average = averageStack(self.image_class.image.source, n_frames, average_type=average_type, include_partial=False, quiet=True)
            crt_frame = crt_average[0:2]

            # Measure the signal
            crt_profile = readSingle(crt_frame, object_position)

            # Save the values
            all_n_avg.append( n_frames )
            all_contrast.append( crt_profile['contrast'][0] )
            all_noise.append( crt_profile['noise'][0] )
            all_snr.append( crt_profile['snr'][0] )

        # Close the progress window
        self.parent.subWindows['progress_bar'].close()
        self.parent.application.processEvents()

        # Save in the memory
        self.averaging_result = {
        'averaged frames':all_n_avg,
        'contrast':all_contrast,
        'noise':all_noise,
        'snr':all_snr,
        }

        # Display the results
        self.plotFluctuations()

        # Update the display
        self.saveButton.setEnabled( True )

    ##-\-\-\-\-\-\-\-\
    ## SAVE THE RESULTS
    ##-/-/-/-/-/-/-/-/

    # --------------------------
    # Save the results in a file
    def saveResults(self):

        # Get all the data
        all_data = pd.DataFrame(self.averaging_result)

        # Get the file name to save
        dataFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Data as...","signals","Comma-Separated Values (*.csv);;Microsoft Excel (*.xlsx)")

        # Proceed to save the file
        if dataFile:

            # Save the file in the appropriate format
            _, file_extension = os.path.splitext(dataFile)

            if file_extension == '.csv':
                all_data.to_csv(dataFile)

            elif file_extension == '.xlsx':
                with pd.ExcelWriter(dataFile) as writer:
                    all_data.to_excel(writer)
