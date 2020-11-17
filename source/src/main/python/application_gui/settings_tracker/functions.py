import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class TrackerSettingsFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## INITIALISE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------------------
    # Initialise the display with the settings in memory
    def initialiseSettings(self):

        # Update the tracker's name
        if self.detection_instance.name == 'Default':
            crt_name = 'New Tracker'
        else:
            crt_name = self.detection_instance.name
        self.nameSelectionEntry.setText( crt_name )

        # Update the object settings
        self.minIntensityEntry.setText( str(self.detection_session.minmass) )

        self.diameterEntry.setText( str(self.detection_session.diameter) )

        self.darkSpotCheckBox.setChecked( self.detection_session.invert )

        _is_max_size = self.detection_session.maxsize is not None
        self.maxSizeCheckBox.setChecked( _is_max_size )
        if _is_max_size:
            self.maxSizeEntry.setText( str(self.detection_session.maxsize) )

        _is_separation = self.detection_session.separation is not None
        self.separationCheckBox.setChecked( _is_separation )
        if _is_separation:
            self.separationEntry.setText( str(self.detection_session.separation) )

        self.percentileEntry.setText( str(self.detection_session.percentile) )

        # Update the filter settings
        self.noiseSizeEntry.setText( str(self.detection_session.noise_size) )

        _is_smoothing_size = self.detection_session.smoothing_size is not None
        self.smoothingSizeCheckBox.setChecked( _is_smoothing_size )
        if _is_smoothing_size:
            self.smoothingSizeEntry.setText( str(self.detection_session.smoothing_size) )

        _is_threshold = self.detection_session.threshold is not None
        self.thresholdCheckBox.setChecked( _is_threshold )
        if _is_threshold:
            self.thresholdEntry.setText( str(self.detection_session.threshold) )

        _is_bright_features = self.detection_session.topn is not None
        self.brightestFeaturesCheckBox.setChecked( _is_bright_features )
        if _is_bright_features:
            self.brightestFeaturesEntry.setText( str(self.detection_session.topn) )

        self.preprocessCheckBox.setChecked( self.detection_session.preprocess )

        # Update the other settings
        self.characterizeCheckBox.setChecked( self.detection_session.characterize )

        index = self.engineComboBox.findText(self.detection_session.engine.capitalize(), qtc.Qt.MatchFixedString)
        if index >= 0:
             self.engineComboBox.setCurrentIndex(index)

        # Update the trajectory settings
        self.memoryEntry.setText( str(self.detection_session.memory) )

        self.searchRangeEntry.setText( str(self.detection_session.search_range) )

        self.adaptiveStepEntry.setText( str(self.detection_session.adaptive_step) )

        self.filterStubsEntry.setText( str(self.detection_session.filter_stubs) )

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
        self.updateMaxSize()
        self.updateSeparation()
        self.updateSmoothingSize()
        self.updateThreshold()
        self.updateBrightestFeatures()
        self.updateAdaptiveStop()

    ##-\-\-\-\-\-\-\-\-\
    ## SAVE THE SETTINGS
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------------------------
    # Update the session based on the display
    def updateSession(self):

        # Save the name
        self.detection_instance.name = self.nameSelectionEntry.text()

        # Save the object settings
        self.detection_session.minmass = float( self.minIntensityEntry.text() )
        self.detection_session.diameter = int( self.diameterEntry.text() )
        self.detection_session.invert = self.darkSpotCheckBox.isChecked()
        self.detection_session.percentile = float( self.percentileEntry.text() )

        if self.maxSizeCheckBox.isChecked():
            self.detection_session.maxsize = float( self.maxSizeEntry.text() )
        else:
            self.detection_session.maxsize = None

        if self.separationCheckBox.isChecked():
            self.detection_session.separation = float( self.separationEntry.text() )
        else:
            self.detection_session.separation = None

        # Save the filter settings
        self.detection_session.noise_size = float( self.noiseSizeEntry.text() )
        self.detection_session.preprocess = self.preprocessCheckBox.isChecked()

        if self.smoothingSizeCheckBox.isChecked():
            self.detection_session.smoothing_size = float( self.smoothingSizeEntry.text() )
        else:
            self.detection_session.smoothing_size = None

        if self.thresholdCheckBox.isChecked():
            self.detection_session.threshold = float( self.thresholdEntry.text() )
        else:
            self.detection_session.threshold = None

        if self.brightestFeaturesCheckBox.isChecked():
            self.detection_session.topn = int( self.brightestFeaturesEntry.text() )
        else:
            self.detection_session.topn = None

        # Save the other settings
        self.detection_session.characterize = self.characterizeCheckBox.isChecked()
        self.detection_session.engine = self.engineComboBox.currentText().lower()

        # Save the trajectory settings
        self.detection_session.memory = int( self.memoryEntry.text() )
        self.detection_session.search_range = float( self.searchRangeEntry.text() )
        self.detection_session.adaptive_step = float( self.adaptiveStepEntry.text() )
        self.detection_session.filter_stubs = int( self.filterStubsEntry.text() )

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

    # --------------------------------
    # Save the tracker in the settings
    def saveSettings(self):

        # Update the content of the session with the user inputs
        self.updateSession()

        # Save the session in the setting file
        self.detection_instance.save()

        # Close the window once over
        self.close()

        # Refresh the list if open
        if self.parent.subWindows['tracker_manager'] is not None:
            self.parent.subWindows['tracker_manager'].fillTrackerTable()
