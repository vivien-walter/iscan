import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

sns.set(style="darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 1.0})

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR STATISTICS ON PROFILES
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class diffusitivityMeasurementPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(diffusitivityMeasurementPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        self.saved_paths = currentTab.image.path_saved
        self.max_frame = currentTab.image.stack.n_frames
        self.ignore_index = []
        self.micron_per_pixel = 1.
        self.frame_per_second = 1.

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Diffusitivity Measurement")

        # Populate the panel
        self.createMsdDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createPathTable(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createDiffusitivityButtons(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)

        # Extract the data
        self.extractData()

        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event = None):
        event.accept()
        self.parent.subWindows['diffusion'] = None

    # --------------------------------------------
    # Generate the statistics histogram and values
    def createMsdDisplay(self, parentWidget):

        # Generate the widget
        self.msdDisplayWidget = qtw.QWidget()
        self.msdDisplayLayout = qtw.QGridLayout(self.msdDisplayWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Mean Square Displacement")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.msdDisplayLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Histogram in a matplotlib figure
        currentRow += 1
        self.msdFigure = plt.Figure(figsize=(5, 3), dpi=75)
        self.msdCanvas = FigureCanvas(self.msdFigure)
        self.msdCanvas.setStatusTip("Plot of the mean square displacement.")

        # Initialise the graph
        self.msdAxis = self.msdFigure.add_subplot(111)
        self.msdAxis.clear()
        self.msdFigure.subplots_adjust(0, 0, 1, 1)
        self.msdAxis.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        self.msdAxis.tick_params(
            axis="y", which="both", left=False, right=False, labelleft=False
        )

        self.msdDisplayLayout.addWidget(self.msdCanvas, currentRow, 0, 1, -1)

        # Diffusitivity
        currentRow += 1
        self.msdDisplayLayout.addWidget(qtw.QLabel("Diffusitivity"), currentRow, 0)
        self.diffusionOutput = qtw.QLineEdit()
        self.diffusionOutput.setEnabled(False)
        self.diffusionOutput.setStatusTip("Mean value of the diffusitivity.")
        self.msdDisplayLayout.addWidget(self.diffusionOutput, currentRow, 1)

        # Exponent of the power law
        currentRow += 1
        self.msdDisplayLayout.addWidget(qtw.QLabel("Power law"), currentRow, 0)
        self.powerLawOutput = qtw.QLineEdit()
        self.powerLawOutput.setEnabled(False)
        self.powerLawOutput.setStatusTip("Form of the fitted power law for the diffusitivity measurement.")
        self.msdDisplayLayout.addWidget(self.powerLawOutput, currentRow, 1)

        # Use calibration for the measurement
        currentRow += 1
        self.calibrationSelection = qtw.QCheckBox("Use spatial and time calibration")
        self.calibrationSelection.toggled.connect(self.setCalibration)
        self.calibrationSelection.setStatusTip(
            "Use the spatial and time calibration in the memory for the measurements."
        )
        self.msdDisplayLayout.addWidget(
            self.calibrationSelection, currentRow, 0, 1, -1
        )

        # Display the widget
        self.msdDisplayWidget.setLayout(self.msdDisplayLayout)
        parentWidget.addWidget(self.msdDisplayWidget)

    # ---------------------------------------------
    # Generate the display of the result of the fit
    def createPathTable(self, parentWidget):

        # Generate the widget
        self.pathDisplayWidget = qtw.QWidget()
        self.pathDisplayLayout = qtw.QVBoxLayout(self.pathDisplayWidget)
        self.pathDisplayLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Path Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.pathDisplayLayout.addWidget(widgetName)

        # Table for the results
        self.pathTable = qtw.QTableWidget(0, 4)
        self.pathTable.setHorizontalHeaderLabels(
            [
                "Index",
                "Diffusitivity",
                "Power law",
                "Use?",
            ]
        )
        self.pathTable.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.pathTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.pathTable.cellDoubleClicked.connect(self.tableIsDoubleClicked)
        self.pathDisplayLayout.addWidget(self.pathTable)

        # Display the widget
        self.pathDisplayWidget.setLayout(self.pathDisplayLayout)
        parentWidget.addWidget(self.pathDisplayWidget)

    # ---------------------------
    # Generate the action buttons
    def createDiffusitivityButtons(self, parentWidget):

        # Generate the widget
        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QGridLayout(self.buttonWidget)

        # Buttons
        currentRow = 0
        # Create the radiobuttons for path selection
        self.saveSelectionGroup = qtw.QGroupBox("Save...")
        self.saveSelectionLayout = qtw.QGridLayout(self.saveSelectionGroup)

        currentSubRow = 0
        self.saveMeanMsdButton = qtw.QPushButton("Mean MSD")
        self.saveMeanMsdButton.clicked.connect(self.saveMeanMSD)
        self.saveMeanMsdButton.setStatusTip("Save the mean MSD of all selected paths.")
        self.saveSelectionLayout.addWidget(self.saveMeanMsdButton, currentSubRow, 0)

        self.saveDiffusitivyButton = qtw.QPushButton("Diffusitivity")
        self.saveDiffusitivyButton.clicked.connect(self.saveDiffusitivity)
        self.saveDiffusitivyButton.setStatusTip("Save the mean value of the diffusitivity.")
        self.saveSelectionLayout.addWidget(self.saveDiffusitivyButton, currentSubRow, 1)

        currentSubRow += 1
        self.saveAllMsdButton = qtw.QPushButton("Single MSDs")
        self.saveAllMsdButton.clicked.connect(self.saveAllMSD)
        self.saveAllMsdButton.setStatusTip("Save the individual MSDs of all selected paths.")
        self.saveSelectionLayout.addWidget(self.saveAllMsdButton, currentSubRow, 0)

        self.saveSelectionGroup.setLayout(self.saveSelectionLayout)
        self.buttonLayout.addWidget(self.saveSelectionGroup, currentRow, 0,1,-1)

        # Close the window
        currentRow += 1
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the window.")
        self.buttonLayout.addWidget(self.closeButton, currentRow, 1)

        # Display the widget
        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)

    ##-\-\-\-\-\-\-\-\-\-\
    ## UPDATE PROFILE PLOT
    ##-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Plot the MSD and the fit in the canvas
    def plotMSD(self):

        # Reset the graph
        self.msdAxis.clear()

        # Plot the MSD
        sns.relplot(x='lagt', y='msd', kind='line', data=self.computed_msd, ax=self.msdAxis)

        # Plot the fit for the diffusitivity
        tau_fit = np.arange(0, self.max_frame/2)
        if self.calibrationSelection.isChecked():
            tau_fit = tau_fit / self.frame_per_second
        msd_fit = powerlaw(tau_fit, *self.law_power)

        self.msdAxis.plot( tau_fit, msd_fit, 'r--' )

        # Refresh the canvas
        self.msdCanvas.draw()

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------
    # Update the main display fields
    def updateFields(self):

        # Extract the values
        diff = self.diffusitivity
        diffErr = self.diffusitivity_error
        factorLaw, exponentLaw = self.law_power

        # Prepare the texts
        diffusionText = str(round(diff,3)) + ' ± ' + str(round(diffErr,3))
        powerLawText = str(round(factorLaw,3)) + ' * tau ^ ' + str(round(exponentLaw,3))

        # Add the unit
        if self.calibrationSelection.isChecked():
            diffusionText += ' micron^2/s'
        else:
            diffusionText += ' pixel^2/frame'

        # Update the different fields
        self.diffusionOutput.setText(diffusionText)
        self.powerLawOutput.setText(powerLawText)

    # -----------------------
    # Populate the data table
    def populateTable(self):

        # Delete the values
        rowCount = self.pathTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.pathTable.removeRow(0)

        # Populate row by row
        for i, path_index in enumerate(self.processed_paths.keys()):

                # Fill the rows
                self.pathTable.insertRow(i)

                # Current path
                tmp_path = self.processed_paths[path_index]

                # Fill the columns
                indexItem = qtw.QTableWidgetItem( str(path_index) )
                self.pathTable.setItem(i, 0, indexItem)
                diffusionItem = qtw.QTableWidgetItem( str(round(tmp_path['D'],2)) + ' ± ' + str(round(tmp_path['D_error'],2)) )
                self.pathTable.setItem(i, 1, diffusionItem)
                powerLawItem = qtw.QTableWidgetItem( str(round(tmp_path['power_law'][0],2)) + ' * tau ^ ' + str(round(tmp_path['power_law'][1],2)) )
                self.pathTable.setItem(i, 2, powerLawItem)
                displayItem = qtw.QTableWidgetItem( str(tmp_path['display']) )
                self.pathTable.setItem(i, 3, displayItem)

    ##-\-\-\-\-\-\-\-\
    ## TABLE MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # ------------------------------
    # Edit the table on double click
    def tableIsDoubleClicked(self, row, column):

        # Modify the select path
        oneTrue = False
        for i, path_index in enumerate(self.processed_paths.keys()):
            if i == row:
                oldStatus = self.processed_paths[path_index]['display']
                self.processed_paths[path_index]['display'] = not oldStatus

            # Check that at least one status is kept True
            if self.processed_paths[path_index]['display'] == True:
                oneTrue = True

        # Refresh the table
        if oneTrue:
            self.populateTable()
            self.checkIndex()
        else:
            self.tableIsDoubleClicked(row, column)

    ##-\-\-\-\-\-\-\-\
    ## DATA MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # --------------------------------------------
    # Extract all the required data from the paths
    def extractData(self):

        # Import all the trajectories into a panda dataframe
        processed_paths = {}
        for i, path in enumerate(self.saved_paths):

            # Check that the path can be processed
            if path.positions is not None:
                if path.positions.shape[0] == self.max_frame:

                    # Get all the positions in the path
                    tmp_dataframe = pd.DataFrame({
                    'frame':path.positions[:,0],
                    'x':path.positions[:,1],
                    'y':path.positions[:,2]
                    })

                    # Append the path to the dictionnary
                    processed_paths[i] = {'trajectory':tmp_dataframe, 'display':True, 'index':i}

        # Calculate all the MSDs
        calculateMSD(processed_paths, int(self.max_frame/2), micron_per_pixel = self.micron_per_pixel, fps=self.frame_per_second)

        # Save the results
        self.processed_paths = processed_paths

        # Update the display
        self.computeDiffusitivity(do_all=True)

    # --------------------------------------
    # Calculate the coefficient of diffusion
    def computeDiffusitivity(self, do_all=False):

        # Generate the dataframe with all MSDs
        self.computed_msd = mergeMSD(self.processed_paths, self.ignore_index)

        # Calculate all the diffusitivity
        diff, powerlaw = calculateDiffusion(self.processed_paths, self.ignore_index, do_all=do_all)

        # Save the results
        self.diffusitivity = diff[0]
        self.diffusitivity_error = diff[1]
        self.law_power = powerlaw[0]
        self.law_power_error = powerlaw[1]

        # Update the display
        self.populateTable()
        self.updateFields()
        self.plotMSD()

    # --------------------------------------------
    # Check which path can be used for the display
    def checkIndex(self):

        # List the index that should not be displayed
        self.ignore_index = []
        for path_index in self.processed_paths.keys():
            if self.processed_paths[path_index]['display'] == False:
                self.ignore_index.append(self.processed_paths[path_index]['index'])

        # Refresh the display
        self.computeDiffusitivity()

    # ------------------------------------
    # Set the spatial and time calibration
    def setCalibration(self):

        # Check which calibration to apply
        if self.calibrationSelection.isChecked():

            # Retrieve the current tab being displayed
            currentTab, _ = self.parent.getCurrentTab()
            self.micron_per_pixel = currentTab.image.spatial_calibration
            self.frame_per_second = 1/currentTab.image.time_calibration

        # Set everything to 1
        else:
            self.micron_per_pixel = 1.
            self.frame_per_second = 1.

        # Refresh the display
        self.extractData()

    ##-\-\-\-\-\-\
    ## SAVE RESULTS
    ##-/-/-/-/-/-/

    # --------------------------------
    # Save the mean MSD in a data file
    def saveMeanMSD(self):

        # Get the data
        dataframe = self.computed_msd

        # Fit the values
        fit_msd = powerlaw(np.array(dataframe['lagt']), *self.law_power)

        # Create the array for the values
        valueArray = np.array( [dataframe['lagt'],dataframe['msd'], fit_msd] ).T

        # Generate the header
        if self.calibrationSelection.isChecked():
            columnName = ['tau (s)','msd (micron^2)','fit msd (micron^2)']
        else:
            columnName = ['tau (frame)','msd (pixel^2)','fit msd (pixel^2)']

        # Save the msd
        saveDataFile(self.parent, valueArray, name_array=columnName)

    # ----------------------------
    # Save all the individual MSDs
    def saveAllMSD(self):

        # Generate the header
        if self.calibrationSelection.isChecked():
            columnName = ['tau (s)','msd (micron^2)','fit msd (micron^2)']
        else:
            columnName = ['tau (frame)','msd (pixel^2)','fit msd (pixel^2)']

        # Ask for the folder to save files in
        process, folder_name = getFolderToSaveIn(self.parent)
        if not process:
            return 0

        # Process all the paths
        for path_index in self.processed_paths.keys():
            if self.processed_paths[path_index]['display'] == True:
                current_path = self.processed_paths[path_index]

                # Retrieve the required elements
                tmp_index = current_path['index']
                tmp_msd = current_path['msd']
                tmp_parameters = current_path['power_law']

                # Fit the values
                tmp_fit_msd = powerlaw(np.array(tmp_msd['lagt']), *tmp_parameters)

                # Create the array for the values
                tmp_array = np.array( [tmp_msd['lagt'],tmp_msd['msd'], tmp_fit_msd] ).T

                # Generate the file name
                tmp_file_name = os.path.join(folder_name, 'msd_path_'+str(tmp_index))

                # Save the msd
                saveDataFile(self.parent, tmp_array, name_array=columnName, file_name=tmp_file_name, confirm_message=False)

        # Confirm all files have been saved
        messageFileSaved()

    # -------------------------------------------
    # Save the fitted diffusitivity and power law
    def saveDiffusitivity(self):

        # Retrieve the data
        diff = self.diffusitivity
        diffErr = self.diffusitivity_error
        factorLaw = self.law_power[0]
        factorLawErr = self.law_power_error[0]
        exponentLaw = self.law_power[1]
        exponentLawErr = self.law_power_error[1]

        # Generate the text to save
        dataText = 'Diffusitivity: ' + str(diff) + ' ± ' +str(diffErr)

        # Add the unit
        if self.calibrationSelection.isChecked():
            dataText += ' micron^2/s\n'
        else:
            dataText += ' pixel^2/frame\n'

        dataText += 'Power law: (' + str(factorLaw) + ' ± ' + str(factorLawErr) + ') * tau ^ ('
        dataText += str(exponentLaw) + ' ± ' + str(exponentLawErr) + ')'

        # Save the file
        saveTextFile(self.parent, dataText, extension='.dat')

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import messageFileSaved
from iscan.input_output.check_files import getFolderToSaveIn
from iscan.input_output.data_files import saveDataFile, saveTextFile
from iscan.operations.general_functions import powerlaw
from iscan.operations.particle_tracking import calculateMSD, mergeMSD, calculateDiffusion
