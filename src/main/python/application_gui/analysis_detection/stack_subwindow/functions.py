import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from settings.tracker_settings import editTrackerConfig

from application_gui.common_gui_functions import openWindow

from application_gui.messageboxes.display import warningProceedMessage
from application_gui.progressbar.trackpy_batch import TrackpyProgressBarWindow
from application_gui.sidebar_trajectory.display import TrajectoryControlsPanel

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class stackDetectionFunctions(object):

    ##-\-\-\-\-\-\-\-\-\-\
    ## MANAGE THE SETTINGS
    ##-/-/-/-/-/-/-/-/-/-/

    # --------------------------------------------------
    # Initialise the display with the settings in memory
    def initialiseSettings(self):

        # Update the basic settings
        self.memoryEntry.setText( str(self.detection_session.memory) )

        self.searchRangeEntry.setText( str(self.detection_session.search_range) )

        self.adaptiveStepEntry.setText( str(self.detection_session.adaptive_step) )

        self.filterStubsEntry.setText( str(self.detection_session.filter_stubs) )

        # Update the advanced settings
        _is_adaptive_stop = self.detection_session.adaptive_stop is not None
        self.adaptiveStopCheckBox.setChecked( _is_adaptive_stop )
        if _is_adaptive_stop:
            self.adaptiveStopEntry.setText( str(self.detection_session.adaptive_stop) )

        name_neighbor_strategy = str(self.detection_session.neighbor_strategy)
        index_neighbor_strategy = self.neighborStrategyComboBox.findText(name_neighbor_strategy.capitalize(), qtc.Qt.MatchFixedString)
        if index_neighbor_strategy >= 0:
             self.neighborStrategyComboBox.setCurrentIndex(index_neighbor_strategy)

        name_link_strategy = str(self.detection_session.link_strategy)
        index_link_strategy = self.linkStrategyComboBox.findText(name_link_strategy.capitalize(), qtc.Qt.MatchFixedString)
        if index_link_strategy >= 0:
             self.linkStrategyComboBox.setCurrentIndex(index_link_strategy)

        # Update the status of all elements
        self.updateAdaptiveStop()

    # -------------------------
    # Save the current settings
    def saveSettings(self):

        # Save the basic options
        self.detection_session.memory = int( self.memoryEntry.text() )
        self.detection_session.search_range = float( self.searchRangeEntry.text() )
        self.detection_session.adaptive_step = float( self.adaptiveStepEntry.text() )
        self.detection_session.filter_stubs = int( self.filterStubsEntry.text() )

        # Save the advanced options
        if self.adaptiveStopCheckBox.isChecked():
            self.detection_session.adaptive_stop = float( self.adaptiveStopEntry.text() )
        else:
            self.detection_session.adaptive_stop = None

        _neighbor_strategy = self.neighborStrategyComboBox.currentText()
        if _neighbor_strategy == 'None':
            self.detection_session.neighbor_strategy = None
        else:
            self.detection_session.neighbor_strategy = _neighbor_strategy.lower()

        _link_strategy = self.linkStrategyComboBox.currentText()
        if _link_strategy == 'None':
            self.detection_session.link_strategy = None
        else:
            self.detection_session.link_strategy = _link_strategy.lower()

    ##-\-\-\-\-\-\-\-\-\
    ## PROCESS THE STACK
    ##-/-/-/-/-/-/-/-/-/

    # -----------------------------------------------#
    # Process the whole stack with the given settings
    def processStack(self):

        # Save the current settings in the class
        self.saveSettings()

        # Ask the user to save the new settings as well if needed
        if self.trajectory_session.modified:

            # Prompt
            if warningProceedMessage('Save Tracker','Do you want to save the batch settings of the tracker in the memory?'):
                editTrackerConfig(self.trajectory_session)

        # Retrieve the displayed stack
        tab_id = self.parent.imageTabDisplay.currentIndex()
        self.image_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

        # Open the progress bar window
        openWindow(self.parent, TrackpyProgressBarWindow, 'progress_bar', image_class=self.image_class, trackpy_session=self.detection_session, scheduler=self)

    # -----------------------------
    # Get the result of the process
    def stackProcessed(self):

        # Close the windows
        self.parent.subWindows['particle_analysis'].close()
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
        tab_id = self.parent.imageTabDisplay.currentIndex()
        self.parent.imageTabDisplay.displayedTabs[tab_id].refreshPathList()
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()
