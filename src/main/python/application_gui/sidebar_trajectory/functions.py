import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from trajectory.processing import deletePath
from trajectory.trajectory_class import startManager

from application_gui.common_gui_functions import openWindow
from application_gui.messageboxes.display import errorMessage, errorMessageNoImage, warningMessage
from application_gui.settings_track_display.display import TrackDisplaySettingsWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class TrajectoryControlsFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## MANAGE LOCATION
    ##-/-/-/-/-/-/-/-/

    # ----------------------------------------------------
    # Detect the change of location of the trajectory dock
    def detectLocationChange(self, event=None):

        # Check if the dock is floating
        is_floating = event

        # Get the window parent size
        main_width, main_height = self.parent.size().width(), self.parent.size().height()
        dock_width = self.size().width()

        # Calculate the new width
        if is_floating:
            main_width -= dock_width
        else:
            main_width += dock_width

        # Resize the main window
        self.parent.resize(main_width, main_height)

    ##-\-\-\-\-\-\-\-\
    ## REFRESH DISPLAY
    ##-/-/-/-/-/-/-/-/

    # ------------------------
    # Refresh the main display
    def refreshDisplay(self):

        # Refresh the button status
        _is_not_all = self.pathSelectionEntry.comboBox.currentText() != 'All'
        self.deletePathButton.setEnabled(_is_not_all)

        # Refresh the display
        tab_id = self.parent.imageTabDisplay.currentIndex()
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## TRAJECTORY MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/-/

    # -------------------------------------
    # Enable/disable the trajectory display
    def toggleDisplay(self):

        # Update the status
        self.parent.show_trajectory = self.viewCheckBox.isChecked()

        # Refresh the display
        self.refreshDisplay()

    # --------------------------------------
    # Set the information of the current tab
    def setDisplay(self):

        # Retrieve the current tab
        tab_id = self.parent.imageTabDisplay.currentIndex()
        crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

    # ------------------------
    # Delete the selected path
    def deleteSelectedPath(self):

        # Get the selection
        crt_selection = self.pathSelectionEntry.comboBox.currentText()

        if crt_selection != 'All':
            crt_selection = int(crt_selection)

            # Retrieve the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Delete the selected path
            deletePath(crt_selection, crt_class.trajectory)

            # Refresh the display
            self.parent.imageTabDisplay.displayedTabs[tab_id].refreshPathList()
            self.refreshDisplay()

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # ----------------------------------------
    # Open the window for the display settings
    def callDisplaySettingsWindow(self):
        openWindow(self.parent, TrackDisplaySettingsWindow, 'track_display_settings')

    ##-\-\-\-\-\-\-\-\
    ## FILE MANAGEMENT
    ##-/-/-/-/-/-/-/-/

    # -----------------------------
    # Save the trajectory in a file
    def saveTrajectoryFile(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Retrieve the current tab ID
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_traj = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.trajectory

            # Save the trajectory in a file
            if crt_traj is not None:

                # Get the file name
                trajectory_file, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Trajectory...", "","Hierarchical Data (*.xml);;Comma-Separated Value (*.csv)")

                if trajectory_file != "":
                    crt_traj.save(file_name=trajectory_file)

            # Display message if there are no trajectory opened
            else:
                errorMessage("No Trajectory","There is no loaded trajectory to be saved in a file.")

        else:
            errorMessageNoImage()

    # -------------------------------
    # Load the trajectory from a file
    def loadTrajectoryFile(self):

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

            # Refresh the display
            self.parent.imageTabDisplay.displayedTabs[tab_id].refreshPathList()
            self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

        else:
            errorMessageNoImage()
