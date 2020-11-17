import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class filterSettingsFunctions:

    def createFilterSettings(self):

        # Generate the widget
        self.filterSettingsWidget = qtw.QWidget()
        self.filterSettingsLayout = qtw.QGridLayout(self.filterSettingsWidget)

        # Setting for the maximum size
        current_row = 0
        self.filterSettingsLayout.addWidget(qtw.QLabel("Noise size"), current_row, 0)
        self.noiseSizeEntry = qtw.QLineEdit()
        #self.noiseSizeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.noiseSizeEntry.editingFinished.connect(self.editNoiseSize)
        self.filterSettingsLayout.addWidget(self.noiseSizeEntry, current_row, 1)

        # Setting for the separation
        current_row += 1
        self.smoothingSizeCheckBox = qtw.QCheckBox('Set smoothing size?')
        self.smoothingSizeCheckBox.clicked.connect(self.updateSmoothingSize)
        self.filterSettingsLayout.addWidget(self.smoothingSizeCheckBox, current_row, 0)
        self.smoothingSizeEntry = qtw.QLineEdit()
        #self.smoothingSizeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.smoothingSizeEntry.editingFinished.connect(self.editSmoothingSize)
        self.filterSettingsLayout.addWidget(self.smoothingSizeEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.thresholdCheckBox = qtw.QCheckBox('Set threshold?')
        self.thresholdCheckBox.clicked.connect(self.updateThreshold)
        self.filterSettingsLayout.addWidget(self.thresholdCheckBox, current_row, 0)
        self.thresholdEntry = qtw.QLineEdit()
        #self.thresholdEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.thresholdEntry.editingFinished.connect(self.editThreshold)
        self.filterSettingsLayout.addWidget(self.thresholdEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.brightestFeaturesCheckBox = qtw.QCheckBox('Set brightest features?')
        self.brightestFeaturesCheckBox.clicked.connect(self.updateBrightestFeatures)
        self.filterSettingsLayout.addWidget(self.brightestFeaturesCheckBox, current_row, 0)
        self.brightestFeaturesEntry = qtw.QLineEdit()
        #self.brightestFeaturesEntry.setValidator(qtg.QIntValidator(999999,0))
        self.brightestFeaturesEntry.editingFinished.connect(self.editBrightestFeatures)
        self.filterSettingsLayout.addWidget(self.brightestFeaturesEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.preprocessCheckBox = qtw.QCheckBox('Preprocess?')
        self.preprocessCheckBox.clicked.connect(self.editPreprocess)
        self.filterSettingsLayout.addWidget(self.preprocessCheckBox, current_row, 0)

        # Display the widget
        self.filterSettingsWidget.setLayout(self.filterSettingsLayout)
        return self.filterSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # -------------------------------
    # Update the smoothing size entry
    def updateSmoothingSize(self):

        # Toggle the status of the entry
        self.smoothingSizeEntry.setEnabled( self.smoothingSizeCheckBox.isChecked() )

        # Edit the session
        self.editSmoothingSize()

    # --------------------------
    # Update the threshold entry
    def updateThreshold(self):

        # Toggle the status of the entry
        self.thresholdEntry.setEnabled( self.thresholdCheckBox.isChecked() )

        # Edit the session
        self.editThreshold()

    # -----------------------------------
    # Update the brightest features entry
    def updateBrightestFeatures(self):

        # Toggle the status of the entry
        self.brightestFeaturesEntry.setEnabled( self.brightestFeaturesCheckBox.isChecked() )

        # Edit the session
        self.editBrightestFeatures()

    ##-\-\-\-\-\-\-\
    ## UPDATE SESSION
    ##-/-/-/-/-/-/-/

    # ----------------------------
    # Edit the noise size settings
    def editNoiseSize(self):
        self.detection_session.noise_size = float( self.noiseSizeEntry.text() )

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # --------------------------------
    # Edit the smoothing size settings
    def editSmoothingSize(self):

        # Save the content of the entry
        if self.smoothingSizeCheckBox.isChecked():
            self.detection_session.smoothing_size = float( self.smoothingSizeEntry.text() )
        else:
            self.detection_session.smoothing_size = None

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # ---------------------------
    # Edit the threshold settings
    def editThreshold(self):

        # Save the content of the entry
        if self.thresholdCheckBox.isChecked():
            self.detection_session.threshold = float( self.thresholdEntry.text() )
        else:
            self.detection_session.threshold = None

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # ------------------------------------
    # Edit the brightest features settings
    def editBrightestFeatures(self):

        # Save the content of the entry
        if self.brightestFeaturesCheckBox.isChecked():
            self.detection_session.topn = int( self.brightestFeaturesEntry.text() )
        else:
            self.detection_session.topn = None

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # ----------------------------
    # Edit the preprocess settings
    def editPreprocess(self):
        self.detection_session.preprocess = self.preprocessCheckBox.isChecked()

        # Refresh display if needed
        self.emitSignalLiveUpdate()
