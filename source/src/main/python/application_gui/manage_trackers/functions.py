from copy import deepcopy
from functools import partial

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow
from application_gui.messageboxes.display import warningProceedMessage, notificationFileSaved, errorMessage
from application_gui.settings_tracker.display import TrackerSettingsWindow

from settings.tracker_settings import listTrackerConfigs, loadTrackerConfig, deleteTracker
from trajectory.tracker_class import startSession

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class TrackerManagerFunctions(object):

    ##-\-\-\-\-\-\-\-\
    ## UPDATE THE TABLE
    ##-/-/-/-/-/-/-/-/

    # ------------------
    # Populate the table
    def fillTrackerTable(self):

        # Get the list of trackers
        all_trackers = listTrackerConfigs()
        self.tracker_list = [x for x in all_trackers if x != 'Default']

        # Reinialise the table
        rowCount = self.trackersTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.trackersTable.removeRow(0)

        # Fill the table
        i = -1
        self.checkbox_list = []
        if len(self.tracker_list) > 0:
            for i, name in enumerate(self.tracker_list):
                self._make_row(i, name)

        # Add the default tracker
        self.tracker_list.append('Default')
        self._make_row(i+1, 'Default', add_button=False)

        # Resize the columns
        header = self.trackersTable.horizontalHeader()
        for i in range( 4 ):
            header.setSectionResizeMode(i, qtw.QHeaderView.ResizeToContents)

        # Tick the box
        self._get_current_selection()

    # -----------------------------------
    # Update the status of the checkboxes
    def updateCheckBoxes(self, box_id=0):

        # Set the current tracker in the settings
        self.parent.config.tracker = self.tracker_list[box_id]

        # Save the settings to the file
        self.parent.config.save()

        # Refresh the selection
        self._get_current_selection()

    # ----------------------
    # Add a row in the table
    def _make_row(self, i, name, add_button=True):

        # Fill the rows
        self.trackersTable.insertRow(i)

        # Prepare the checkbox
        trackerSelectCheckbox = qtw.QCheckBox("Use?")
        trackerSelectCheckbox.clicked.connect(partial(self.updateCheckBoxes, box_id=i))
        self.checkbox_list.append(trackerSelectCheckbox)

        # Prepare the edit and delete buttons
        if add_button:
            trackerEditButton = qtw.QPushButton("Edit")
            trackerEditButton.clicked.connect(partial(self.editTracker, tracker_id=i))
            trackerEditButton.setFixedWidth(75)

            trackerDeleteButton = qtw.QPushButton("Delete")
            trackerDeleteButton.clicked.connect(partial(self.deleteTracker, tracker_id=i))
            trackerDeleteButton.setFixedWidth(75)

        # Keep empty
        else:
            trackerEditButton = qtw.QWidget()
            trackerDeleteButton = qtw.QWidget()

        # Fill the columns
        self.trackersTable.setCellWidget(i, 0, trackerSelectCheckbox)
        self.trackersTable.setItem(i, 1,  qtw.QTableWidgetItem(name))
        self.trackersTable.setCellWidget(i, 2, trackerEditButton)
        self.trackersTable.setCellWidget(i, 3, trackerDeleteButton)

    # ----------------------------------------
    # Check the box with the current selection
    def _get_current_selection(self):

        # Get the current tracker in the memory
        crt_tracker = self.parent.config.tracker

        # Get the index of the checbox
        crt_index = self.tracker_list.index(crt_tracker)

        # Update the status of the checkbox
        for box_id, box in enumerate(self.checkbox_list):
            box.setChecked( box_id == crt_index )

    ##-\-\-\-\-\-\
    ## USER ACTIONS
    ##-/-/-/-/-/-/

    # -------------------------
    # Edit the selected tracker
    def editTracker(self, tracker_id=0):

        # Get the name of the tracker
        tracker_name = self.tracker_list[tracker_id]

        # Load the selected tracker
        tracker_session = loadTrackerConfig(tracker_name)
        tracker_session = deepcopy( tracker_session )

        # Open the window
        openWindow(self.parent, TrackerSettingsWindow, 'tracker_settings', detection_session=tracker_session)

    # --------------------------------
    # Delete a tracker from the memory
    def deleteTracker(self, tracker_id=0):

        # Get the name of the tracker
        tracker_name = self.tracker_list[tracker_id]

        # Change the current tracker
        if self.parent.config.tracker == tracker_name:

            # Set the selected tracker to Default
            self.parent.config.tracker = 'Default'

            # Save the settings to the file
            self.parent.config.save()

        # Ask for confirmation
        if warningProceedMessage("Delete Tracker?","Are you sure you want to delete the selected tracker ("+tracker_name+")?"):

            # Delete the tracker
            deleteTracker(tracker_name)

            # Refresh the display
            self.fillTrackerTable()

    # ----------------------
    # Generate a new tracker
    def makeNewTracker(self):

        # Make a blank tracker
        blank_session = loadTrackerConfig('Default')
        blank_session = deepcopy( blank_session )

        # Open the window
        openWindow(self.parent, TrackerSettingsWindow, 'tracker_settings', detection_session=blank_session)

    # -----------------------------------
    # Import the tracker from a JSON file
    def importTracker(self):

        # Get the file name
        tracker_file, _ = qtw.QFileDialog.getOpenFileName(self.parent, "Load Tracker...", "","JSON Archive (*.json)")

        if tracker_file != "":

            # Prompt the user for the file name
            tracker_name, ok = qtw.QInputDialog.getText(self, "Tracker Name", "Name of the new tracker?")

            if ok:

                # Initialise a new session
                import_session = startSession()

                # Load the parameters in the session
                import_session.load(tracker_file)

                # Load the tracker in the class
                blank_session = loadTrackerConfig('Default')
                blank_session.name = tracker_name
                blank_session.session = import_session

                # Save the tracker in the memory
                blank_session.save()

                # Refresh the display
                self.fillTrackerTable()

    # --------------------------------------------
    # Export the selected tracker into a JSON file
    def exportTracker(self):

        # Prepare the list of exportable settings
        all_trackers = listTrackerConfigs()
        tracker_list = [x for x in all_trackers if x != 'Default']

        # Proceed if there are enough trackers in the memory
        if len(tracker_list) >= 1:

            # Get the tracker to export
            tracker_name, ok = qtw.QInputDialog.getItem(self, "Tracker Selection", "Tracker to export?", tracker_list, 0, False)

            # Export the selection
            if ok:

                # Get the file name
                tracker_file, _ = qtw.QFileDialog.getSaveFileName(self.parent, "Save Tracker...", "","JSON Archive (*.json)")

                if tracker_file != "":

                    # Load the selection
                    export_session = loadTrackerConfig(tracker_name)

                    # Save the selection in file
                    export_session.session.save(tracker_file)

                    # Message to confirm the export
                    notificationFileSaved(tracker_file)


        # Display an error message if there are nothing
        else:
            errorMessage("No Tracker","There is no tracker to export in the memory.")
