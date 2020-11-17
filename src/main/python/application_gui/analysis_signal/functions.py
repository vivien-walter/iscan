import numpy as np
import os
import pandas as pd

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from signal_processing.measurement import readSignals

from application_gui.common_gui_functions import openWindow
from application_gui.progressbar.analyse_signals import ProcessSignalsProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class analyseSignalFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## INITIALISE THE ANALYSIS
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------------------
    # Get the signal properties when the image is loaded
    def getProperties(self):

        # Open the progress window
        openWindow(self.parent, ProcessSignalsProgressBarWindow, 'progress_bar')

        # Start the processing
        self.image_class.trajectory.signals = readSignals(self.image_class.image.source, self.image_class.trajectory)

        # Close the progress window
        self.parent.subWindows['progress_bar'].close()
        self.parent.application.processEvents()

        # Update the display
        self.populateTable()

    # -----------------------------------------
    # Check if the data needs to be reprocessed
    def processSignals(self):

        if self.reloadCheckbox.isChecked():
            self.getProperties()
        else:
            self.populateTable()

    ##-\-\-\-\-\-\-\-\-\
    ## POPULATE THE TABLE
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------
    # Process the signals taken from the trajectory
    def populateTable(self):

        # Delete the previous values
        rowCount = self.contentTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.contentTable.removeRow(0)

        # Check what to read
        _current_only = self.singleFrameRadiobutton.isChecked()
        self.single = _current_only

        # Read all the signals
        self.values = {
        'contrast':[],
        'noise':[],
        'snr':[],
        }
        self.errors = {
        'contrast':[],
        'noise':[],
        'snr':[],
        }
        self.all_checkboxes = []
        self.all_paths = []

        row_id = 0
        for path_id in self.image_class.trajectory.signals.keys():
            _add_path = True

            # Get the current signal
            crt_signal = self.image_class.trajectory.signals[path_id]

            # Process single frame
            if _current_only:
                if self.image_class.frame in crt_signal['frame']:
                    crt_frame_id = np.where(crt_signal['frame'] == int(self.image_class.frame))
                    crt_frame_id = crt_frame_id[0]
                    crt_n_frames = 1

                    # Get the value
                    crt_contrast = crt_signal['contrast'][crt_frame_id][0]
                    crt_noise = crt_signal['noise'][crt_frame_id][0]
                    crt_snr = crt_signal['snr'][crt_frame_id][0]

                    # Save the values
                    self.values['contrast'].append(crt_contrast)
                    self.values['noise'].append(crt_noise)
                    self.values['snr'].append(crt_snr)

                    # Generate the text
                    contrast_text = "{:.2f}".format(crt_contrast)
                    noise_text = "{:.2f}".format(crt_noise)
                    snr_text = "{:.2f}".format(crt_snr)

                else:
                    _add_path = False

            # Process the whole stack
            else:

                # Get the value
                crt_contrast = crt_signal['contrast']
                crt_noise = crt_signal['noise']
                crt_snr = crt_signal['snr']

                # Save the values
                self.values['contrast'].append(np.nanmean(crt_contrast))
                self.values['noise'].append(np.nanmean(crt_noise))
                self.values['snr'].append(np.nanmean(crt_snr))

                # Save the values
                self.errors['contrast'].append(np.nanstd(crt_contrast, ddof=1))
                self.errors['noise'].append(np.nanstd(crt_noise, ddof=1))
                self.errors['snr'].append(np.nanstd(crt_snr, ddof=1))

                # Generate the text
                contrast_text = "{:.2f}".format(np.nanmean(crt_contrast)) + ' ± ' + "{:.2f}".format(np.nanstd(crt_contrast, ddof=1))
                noise_text = "{:.2f}".format(np.nanmean(crt_noise)) + ' ± ' + "{:.2f}".format(np.nanstd(crt_noise, ddof=1))
                snr_text = "{:.2f}".format(np.nanmean(crt_snr)) + ' ± ' + "{:.2f}".format(np.nanstd(crt_snr, ddof=1))

                # Get the number of frames
                crt_n_frames = len(crt_contrast)

            # Write in the table
            if _add_path:

                # Fill the rows
                self.contentTable.insertRow(row_id)

                # Make the checkbox
                crt_checkbox = qtw.QCheckBox("Include?")
                crt_checkbox.clicked.connect(self.computeStatistics)
                crt_checkbox.setChecked(True)

                self.all_paths.append(path_id)
                self.all_checkboxes.append(crt_checkbox)

                # Add the content
                self.contentTable.setCellWidget(row_id, 0, crt_checkbox)
                self.contentTable.setItem(row_id, 1, qtw.QTableWidgetItem( str(path_id) ))
                self.contentTable.setItem(row_id, 2, qtw.QTableWidgetItem( str(crt_n_frames) ))
                self.contentTable.setItem(row_id, 3, qtw.QTableWidgetItem( contrast_text ))
                self.contentTable.setItem(row_id, 4, qtw.QTableWidgetItem( snr_text ))
                self.contentTable.setItem(row_id, 5, qtw.QTableWidgetItem( noise_text ))

                # Increment the counter
                row_id += 1

        # Resize the columns
        header = self.contentTable.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

        # Get the overall stats
        self.computeStatistics()

    # -----------------------------------------------
    # Compute the overall statistics on the selection
    def computeStatistics(self):

        # Read the values
        all_contrast = [ x for i,x in enumerate(self.values['contrast']) if self.all_checkboxes[i].isChecked() ]
        all_noises = [ x for i,x in enumerate(self.values['noise']) if self.all_checkboxes[i].isChecked() ]
        all_snr = [ x for i,x in enumerate(self.values['snr']) if self.all_checkboxes[i].isChecked() ]

        # Get the average values
        contrast_mean = np.nanmean(all_contrast)
        noise_mean = np.nanmean(all_noises)
        snr_mean = np.nanmean(all_snr)

        # Complete the statistics
        if self.single:

            # Get the errors
            contrast_err = np.nanstd(all_contrast, ddof=1)
            noise_err = np.nanstd(all_noises, ddof=1)
            snr_err = np.nanstd(all_snr, ddof=1)

        else:

            # Read the errors
            all_contrast_err = [ x for i,x in enumerate(self.errors['contrast']) if self.all_checkboxes[i].isChecked() ]
            all_contrast_err = np.array(all_contrast_err)**2

            all_noise_err = [ x for i,x in enumerate(self.errors['noise']) if self.all_checkboxes[i].isChecked() ]
            all_noise_err = np.array(all_noise_err)**2

            all_snr_err = [ x for i,x in enumerate(self.errors['snr']) if self.all_checkboxes[i].isChecked() ]
            all_snr_err = np.array(all_snr_err)**2

            # Get the mean of variances
            m_var_contrast = np.mean(all_contrast_err)
            m_var_noise = np.mean(all_noise_err)
            m_var_snr = np.mean(all_snr_err)

            # Get the variance of means
            v_mean_contrast = np.var(all_contrast, ddof=1)
            v_mean_noise = np.var(all_noises, ddof=1)
            v_mean_snr = np.var(all_snr, ddof=1)

            # Calculate the errors
            contrast_err = np.sqrt(m_var_contrast + v_mean_contrast)
            noise_err = np.sqrt(m_var_noise + v_mean_noise)
            snr_err = np.sqrt(m_var_snr + v_mean_snr)

        # Update the display
        self.contrastLabel.setText( "{:.2f}".format(contrast_mean) + ' ± ' + "{:.2f}".format(contrast_err) )
        self.noiseLabel.setText( "{:.2f}".format(noise_mean) + ' ± ' + "{:.2f}".format(noise_err) )
        self.snrLabel.setText( "{:.2f}".format(snr_mean) + ' ± ' + "{:.2f}".format(snr_err) )

    ##-\-\-\-\-\-\-\-\
    ## SAVE THE RESULTS
    ##-/-/-/-/-/-/-/-/

    # ---------------------------
    # Save all the data in a file
    def saveData(self):

        # Get all the data
        all_data = pd.DataFrame()

        # Process all the data
        for i, path_id in enumerate(self.all_paths):
            if self.all_checkboxes[i].isChecked():
                crt_signal = self.image_class.trajectory.signals[path_id]

                # Initialise the lists
                crt_data = pd.DataFrame({
                'frame':crt_signal['frame'],
                'contrast':crt_signal['contrast'],
                'noise':crt_signal['noise'],
                'snr':crt_signal['snr'],
                })
                crt_data['particle'] = [path_id] * len(crt_data['frame'])

                # Concatenate the dataframe
                all_data = pd.concat([all_data, crt_data], ignore_index=True)

        # Get the file name to save
        dataFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Data as...","selection","Comma-Separated Values (*.csv);;Microsoft Excel (*.xlsx)")

        # Proceed to save the file
        if dataFile:

            # Save the file in the appropriate format
            _, file_extension = os.path.splitext(dataFile)

            if file_extension == '.csv':
                all_data.to_csv(dataFile)

            elif file_extension == '.xlsx':
                with pd.ExcelWriter(dataFile) as writer:
                    all_data.to_excel(writer)
