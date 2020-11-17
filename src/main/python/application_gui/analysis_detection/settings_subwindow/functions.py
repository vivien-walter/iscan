import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class particleDetectionSettingsFunctions(object):

    ##-\-\-\-\-\-\-\-\-\
    ## INITIALISE DISPLAY
    ##-/-/-/-/-/-/-/-/-/

    # --------------------------------------------------
    # Initialise the display with the settings in memory
    def initialiseSettings(self):

        # Update the object settings
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

        # Update the status of all elements
        self.updateMaxSize()
        self.updateSeparation()
        self.updateSmoothingSize()
        self.updateThreshold()
        self.updateBrightestFeatures()

    # --------------------------------
    # Send a signal to the main window
    def emitSignalLiveUpdate(self):
        self.parent.subWindows['particle_analysis'].doLiveUpdate()
