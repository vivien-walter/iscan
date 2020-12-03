import numpy as np
import os
import pandas as pd
from pyqtgraph import plot
import pyqtgraph as pg

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from image_processing.scaling import getSpaceScale
from trajectory.trajectory_class import startManager
from trajectory.calculations import getMSD, getDiffusivity

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class particleDiffusionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------------
    # Initialise the display of the window
    def initialiseDisplay(self):

        # Check the input
        _image_on = self.image_class is not None

        # Get the scale
        if _image_on:
            tab_id = self.parent.imageTabDisplay.currentIndex()

            self.space_scale = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.scale.space_scale
            self.space_unit = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.scale.space_unit
            self.frame_rate = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.scale.frame_rate

        else:
            self.space_scale = self.parent.space_scale
            self.space_unit = self.parent.space_unit
            self.frame_rate = self.parent.frame_rate

        # Update the scale entry
        self.updateScaleDisplay()

        # Update the input selection
        self.fromFileButton.setChecked(not _image_on)
        self.fromImageButton.setChecked(_image_on)

        # Disable options if image is empty
        if not _image_on:
            self.fromFileButton.setEnabled(False)
            self.fromImageButton.setEnabled(False)

        # Set the graph style
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Contrast (%)')
        self.graphWidget.setLabel('bottom', '# Averaged frames')
        self.graphWidget.showGrid(x=False, y=False)

        if self.logScaleCheckbox.isChecked():
            self.graphWidget.setLogMode(True, True)
        else:
            self.graphWidget.setLogMode(False, False)

    # --------------------------------
    # Update the graph being displayed
    def updateGraph(self):

        if self.trajectory is not None:

            # Get the index of the graph to display
            graph_id = self.pathSelectionEntry.comboBox.currentIndex()

            # Reset the graph
            self.graphWidget.clear()

            # Update the graph widget
            pen = pg.mkPen(color=(0, 0, 0), width=6)
            self.graphWidget.plot(self.lagtime[graph_id], self.msd[graph_id], pen=pen)

            pen2 = pg.mkPen(color=(255, 0, 0), width=3)
            self.graphWidget.plot(self.fits[graph_id][0], self.fits[graph_id][1], pen=pen2)

            # Set the graph style
            self.graphWidget.setBackground('w')
            self.graphWidget.setLabel('left', 'MSD (µm^2)')
            self.graphWidget.setLabel('bottom', 'Lag time (s)')
            self.graphWidget.showGrid(x=False, y=False)

            if self.logScaleCheckbox.isChecked():
                self.graphWidget.setLogMode(True, True)
            else:
                self.graphWidget.setLogMode(False, False)

            # Update the D value being displayed
            self.diffusivityValueLabel.setText( "{:.5f}".format(self.diffusivity[graph_id]) + ' ± ' + "{:.5f}".format(self.diff_err[graph_id]) + ' µm^2/s' )

    # ---------------------------------------
    # Get the scales from the displayed image
    def getScaleFromImage(self):

        # Get the current tab
        tab_id = self.parent.imageTabDisplay.currentIndex()

        # Extract the scale
        self.space_scale = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.scale.space_scale
        self.space_unit = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.scale.space_unit
        self.frame_rate = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.scale.frame_rate

        # Update the display
        self.updateScaleDisplay()

    # ------------------------
    # Update the scale display
    def updateScaleDisplay(self):

        # Update the display
        self.spaceScaleEntry.setText( str(self.space_scale) )
        self.timeScaleEntry.setText( str(self.frame_rate) )
        self.spaceUnitEntry.setText( str(self.space_unit) )

    ##-\-\-\-\-\-\-\-\-\-\
    ## TRAJECTORY HANDLING
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------------
    # Browse the files on the computer to load a trajectory
    def browseTrajectory(self):

        # Open the load file browser
        trajectoryFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Load Trajectory File...", "","Hierarchical Data (*.xml);;All Files (*)")

        # Load the trajectory in the session
        if trajectoryFile != "":
            self.loaded_trajectory = trajectoryFile

        # Update the display
        self.browseEntry.setText(trajectoryFile)

    # ----------------------------------------
    # Load and process the selected trajectory
    def processTrajectory(self):
        _proceed = True

        # Load the selected trajectory - from file
        if self.fromFileButton.isChecked() and self.loaded_trajectory is not None:
            self.trajectory = startManager( self.loaded_trajectory )

        # Load the selected trajectory - from image tab
        elif self.fromImageButton.isChecked():
            tab_id = self.parent.imageTabDisplay.currentIndex()
            self.trajectory = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.trajectory

        else:
            _proceed = False

        # Process the loaded trajectory
        if _proceed:

            # Retrieve the scale
            self.space_scale = float( self.spaceScaleEntry.text() )
            self.frame_rate = float( self.timeScaleEntry.text() )
            self.space_unit = self.spaceUnitEntry.text()

            # Comvert the scale
            micron_per_pixel = getSpaceScale(self.space_scale, self.space_unit)

            # Get the list of paths
            self.path_list = list( self.trajectory.listTracks() )

            # Extract the MSDs
            self.lagtime = []
            self.msd = []

            # Get the combined MSD
            crt_lagtime, crt_msd = getMSD(self.trajectory.positions, micron_per_pixel, self.frame_rate)
            self.lagtime.append(crt_lagtime)
            self.msd.append(crt_msd)

            # Get the individual MSDs
            crt_lagtime, all_msd = getMSD(self.trajectory.positions, micron_per_pixel, self.frame_rate, path_id=self.path_list)

            for i in range(all_msd.shape[1]):
                self.lagtime.append(crt_lagtime)
                self.msd.append(all_msd[:,i])

            # Get all the diffusivity
            self.fits, self.diffusivity, self.diff_err = getDiffusivity(self.lagtime, self.msd)

            # Update the display
            self.path_list.insert(0, 'All')
            self.pathSelectionEntry.replaceList( [str(x) for x in self.path_list] )

            # Update the graph
            self.updateGraph()
            self.saveButton.setEnabled( True )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -------------------------------------
    # Save the analysed data in a .csv file
    def saveData(self):

        if self.trajectory is not None:

            # Format the output data
            output_data = pd.DataFrame(np.array( self.msd ).T, columns=[str(x) for x in self.path_list])

            # Add the lag time
            output_data.insert(loc=0, column='Lag time', value=self.lagtime[0])

            # Get the file name to save
            dataFile, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Data as...","signals","Comma-Separated Values (*.csv);;Microsoft Excel (*.xlsx)")

            # Proceed to save the file
            if dataFile:

                # Save the file in the appropriate format
                _, file_extension = os.path.splitext(dataFile)

                if file_extension == '.csv':
                    output_data.to_csv(dataFile)

                elif file_extension == '.xlsx':
                    with pd.ExcelWriter(dataFile) as writer:
                        output_data.to_excel(writer)
