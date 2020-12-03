import numpy as np

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from settings.tracker_settings import loadTrackerConfig, listTrackerConfigs, editTrackerConfig
from trajectory.management import generateTrajectory

from application_gui.common_gui_functions import openWindow

from application_gui.messageboxes.display import warningProceedMessage, errorMessage
from application_gui.analysis_detection.settings_subwindow.display import particleDetectionSettingsSubWindow
from application_gui.analysis_detection.stack_subwindow.display import stackDetectionSubWindow
from application_gui.sidebar_trajectory.display import TrajectoryControlsPanel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class particleDetectionFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## DETECT PARTICLES
    ##-/-/-/-/-/-/-/-/

    # ---------------------------------
    # Initialize the particle detection
    def initializeDetection(self, tracker_name = None):

        # Get the tracker name
        if tracker_name is None:
            tracker_name = self.parent.config.tracker
        self.current_tracker = tracker_name

        # Start the session
        self.trajectory_session = loadTrackerConfig( tracker_name )
        self.detection_session = self.trajectory_session.session

        # Update the display
        self.minIntensityEntry.setText( str(self.detection_session.minmass) )
        self.diameterEntry.setText( str(self.detection_session.diameter) )
        self.darkSpotCheckBox.setChecked( self.detection_session.invert )

        # Do a first preview
        self.previewDetection()

    # ------------------------------------------------------
    # Preview the particle detection with the given settings
    def previewDetection(self):

        # Update the settings
        self.updateDetectionSession()

        # Get the current frame
        frame_id = self.image_class.frame
        crt_frame = self.image_class.image.display[frame_id]

        # Make the detection
        crt_positions = self.detection_session.locate(crt_frame)

        # Refine the data into an array
        crt_positions = crt_positions[['y','x']].to_numpy()

        # Refresh the display
        tab_id = self.parent.imageTabDisplay.currentIndex()
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage(particles=crt_positions, diameter=self.detection_session.diameter)

    ##-\-\-\-\-\-\-\-\-\
    ## TRACKER MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/

    # ------------------------------------------------
    # Open the context menu for the tracker management
    def openTrackerMenu(self):

        # Display the context menu
        trackerManagementMenu = qtw.QMenu()

        # Load tracker
        loadTrackerAction = trackerManagementMenu.addAction('Load Tracker')
        loadTrackerAction.triggered.connect(self.loadTracker)

        trackerManagementMenu.addSeparator()

        # Save current
        saveCurrentTrackerAction = trackerManagementMenu.addAction('Save current...')
        saveCurrentTrackerAction.triggered.connect(self.editTracker)

        # Save as new
        saveNewTrackerAction = trackerManagementMenu.addAction('Save as New')
        saveNewTrackerAction.triggered.connect(self.newTracker)

        # Get the position of the button
        button_position = self.pos() + self.mainWidget.pos() + self.settingsGridWidget.pos() + self.manageTrackerButton.pos()
        button_pos_x, button_pos_y = button_position.x(), button_position.y() + 2*self.manageTrackerButton.height()
        button_position = qtc.QPoint(button_pos_x, button_pos_y)

        # Display the menu
        action = trackerManagementMenu.exec_(button_position)

    # ----------------
    # Load the tracker
    def loadTracker(self):

        # Get the list of trackers
        trackers_list = listTrackerConfigs()

        # Get the initial index
        _default_tracker = self.current_tracker
        init_index = trackers_list.index(_default_tracker)

        # Get the tracker to load
        tracker_name, ok = qtw.QInputDialog.getItem(self, "Tracker Selection", "Tracker to load?", trackers_list, init_index, False)

        if ok:

            # Refresh the memory and window
            self.initializeDetection(tracker_name = tracker_name)

    # --------------------------------------------------
    # Save the new settings of the tracker in the memory
    def editTracker(self):

        # Raise an error if the 'Default' tracker is selected
        if self.current_tracker == 'Default':
            errorMessage('Forbidden Action',"The settings of the Default tracker cannot be edited.")

        else:
            if warningProceedMessage('Overwrite Tracker','Are you sure you want to replace the settings of the tracker '+self.current_tracker+' in the memory?'):

                # Update the selection
                self.updateDetectionSession()

                # Edit the tracker settings
                self.trajectory_session.modified = True
                editTrackerConfig(self.trajectory_session)

    # ------------------------------------
    # Save the settings into a new tracker
    def newTracker(self):

        # Prompt the user for the file name
        tracker_name, ok = qtw.QInputDialog.getText(self, "Tracker Name", "Name of the new tracker?")

        if ok:

            # Raise an error if the 'Default' tracker is selected
            if tracker_name == 'Default':
                errorMessage('Forbidden Action',"The settings of the Default tracker cannot be edited.")

            else:

                # Check if the name is in the list
                _write = True
                trackers_list = listTrackerConfigs()
                if tracker_name in trackers_list:
                    _write = warningProceedMessage('Existing Tracker','The selected tracker name ('+tracker_name+') is already in the memory. Do you want to replace it?')

                if _write:

                    # Update the selection
                    self.updateDetectionSession()

                    # Collect the settings
                    self.current_tracker = tracker_name
                    self.trajectory_session.name = tracker_name
                    self.trajectory_session.modified = True

                    # Save the tracker session in file
                    editTrackerConfig(self.trajectory_session)

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # -------------------------------------------------
    # Update the detection session with the given input
    def updateDetectionSession(self):

        # Load the parameter values in the class
        self.detection_session.minmass = float( self.minIntensityEntry.text() )
        self.detection_session.diameter = int( self.diameterEntry.text() )
        self.detection_session.invert = self.darkSpotCheckBox.isChecked()

    # -------------------------------
    # Do the live update if requested
    def doLiveUpdate(self):

        # Check if process is permitted
        if self.livePreviewCheckBox.isChecked():
            self.previewDetection()

    ##-\-\-\-\-\-\
    ## USER ACTION
    ##-/-/-/-/-/-/

    # -------------------------------------
    # Open the advanced settings sub-window
    def openAdvancedSettings(self):
        openWindow(self.parent, particleDetectionSettingsSubWindow, 'particle_advanced', detection_session=self.detection_session)

    # -------------------------------------------------
    # Use the given settings to process the whole stack
    def processParticleDetection(self):

        # Update the selection
        self.updateDetectionSession()

        # Process the whole stack
        if self.image_class.n_frames > 1:
            openWindow(self.parent, stackDetectionSubWindow, 'particle_stack', detection_session=self.trajectory_session)

        # Process a single frame
        else:

            # Get the current frame
            crt_frame = self.image_class.image.display[ self.image_class.frame ]
            crt_positions = self.detection_session.locate(crt_frame)

            # Format the trajectory
            crt_trajectory = generateTrajectory(crt_positions)

            # Save the trajectory in the class
            tab_id = self.parent.imageTabDisplay.currentIndex()
            self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.trajectory = crt_trajectory

            # Close the window
            self.close()

            # Open the dock
            _open_dock = True
            if "tracking" in self.parent.docks.keys():
                if self.parent.docks["tracking"] is not None:
                    _open_dock = False

            if _open_dock:
                self.parent.docks["tracking"] = TrajectoryControlsPanel("Trajectory Controller", self.parent)
                self.parent.addDockWidget(qtc.Qt.RightDockWidgetArea, self.parent.docks["tracking"])

                # Set the size and attach the dock
                self.parent.docks["tracking"].setFloating(True)
                self.parent.docks["tracking"].detectLocationChange()
                self.parent.docks["tracking"].setFloating(False)

            # Refresh the display
            self.parent.imageTabDisplay.displayedTabs[tab_id].refreshPathList()
            self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()
