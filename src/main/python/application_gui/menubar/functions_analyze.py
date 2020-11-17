import os
from pathlib import Path

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from trajectory.trajectory_class import startManager

from application_gui.common_gui_functions import openWindow

from application_gui.analysis_detection.display import particleDetectionWindow
from application_gui.messageboxes.display import errorMessageNoImage, errorMessageNoTrajectory
from application_gui.settings_scale.display import SetScaleWindow
from application_gui.manage_trackers.display import TrackerManagerWindow
from application_gui.analysis_signal.display import analyseSignalWindow
from application_gui.correction_center.display import cropCenterWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarAnalyzeFunctions(object):

    ##-\-\-\-\-\-\
    ## ANALYZE MENU
    ##-/-/-/-/-/-/

    # -----------------------------
    # Detect particles in the image
    def callParticleDetectionWindow(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Call the window
            openWindow(self.parent, particleDetectionWindow, 'particle_analysis', image_class=crt_class)

        else:
            errorMessageNoImage()

    # --------------------------------------
    # Load a trajectory in the current image
    def callLoadTrajectory(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Open the load file browser
            trajectoryFile, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Load Trajectory File...", "","Hierarchical Data (*.xml);;All Files (*)")

            # Retrieve the current tab ID
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Load the trajectory in the session
            if trajectoryFile != "":
                self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.trajectory = startManager(trajectoryFile)

                # Check that the length matches
                n_traj = len(self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.trajectory.positions['frame'].unique())
                n_frames = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.n_frames

                # Display a warning
                if n_traj != n_frames:
                    warningMessage("Different Number of Frames","The number of frames in the image stack and the number of frames in the trajectory do not match. This could lead to issues for displaying the positions of the particles.")

                # Open the trajectory side bar
                self.callTrajectoryManagerDock()

                # Refresh the display
                self.parent.imageTabDisplay.displayedTabs[tab_id].refreshPathList()
                self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

        else:
            errorMessageNoImage()

    # -------------------------------------
    # Call the window to center and crop on
    def callCenterCropWindow(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Check if there is a trajectory
            if crt_class.trajectory is not None:

                # Get the selection from the dock
                if self.parent.docks["tracking"] is not None:
                    _path_id = self.parent.docks["tracking"].pathSelectionEntry.comboBox.currentText()
                else:
                    _path_id = 'All'

                # Prompt the user if a specific path is not selected
                is_ok = True
                if _path_id == 'All':
                    path_list = crt_class.trajectory.listTracks().astype(str)
                    _path_id, is_ok = qtw.QInputDialog.getItem( self.parent, 'Path Selection', 'Path to Center on:', path_list, 0, False )

                if is_ok:
                    openWindow(self.parent, cropCenterWindow, 'crop_center', image_class=crt_class, path_id=int(_path_id))

            else:
                errorMessageNoTrajectory()

        else:
            errorMessageNoImage()

    # ----------------------------------------------------------
    # Call the window to manage the trackers saved in the memory
    def callTrackerManagerWindow(self):
        openWindow(self.parent, TrackerManagerWindow, 'tracker_manager')

    # -------------------------------------
    # Call the window to analyse the signal
    def callSignalAnalysisWindow(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Check if there is a trajectory
            if crt_class.trajectory is not None:
                openWindow(self.parent, analyseSignalWindow, 'measure_signals', image_class=crt_class)

            else:
                errorMessageNoTrajectory()

        else:
            errorMessageNoImage()

    # --------------------------------
    # Open the window to set the scale
    def callSetScaleWindow(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Call the window
            openWindow(self.parent, SetScaleWindow, 'set_scale', image_class=crt_class)

        else:
            errorMessageNoImage()
