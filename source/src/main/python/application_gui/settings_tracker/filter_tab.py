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
        self.noiseSizeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.filterSettingsLayout.addWidget(self.noiseSizeEntry, current_row, 1)

        # Setting for the separation
        current_row += 1
        self.smoothingSizeCheckBox = qtw.QCheckBox('Set smoothing size?')
        self.smoothingSizeCheckBox.clicked.connect(self.updateSmoothingSize)
        self.filterSettingsLayout.addWidget(self.smoothingSizeCheckBox, current_row, 0)
        self.smoothingSizeEntry = qtw.QLineEdit()
        self.smoothingSizeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.filterSettingsLayout.addWidget(self.smoothingSizeEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.thresholdCheckBox = qtw.QCheckBox('Set threshold?')
        self.thresholdCheckBox.clicked.connect(self.updateThreshold)
        self.filterSettingsLayout.addWidget(self.thresholdCheckBox, current_row, 0)
        self.thresholdEntry = qtw.QLineEdit()
        self.thresholdEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.filterSettingsLayout.addWidget(self.thresholdEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.brightestFeaturesCheckBox = qtw.QCheckBox('Set brightest features?')
        self.brightestFeaturesCheckBox.clicked.connect(self.updateBrightestFeatures)
        self.filterSettingsLayout.addWidget(self.brightestFeaturesCheckBox, current_row, 0)
        self.brightestFeaturesEntry = qtw.QLineEdit()
        self.brightestFeaturesEntry.setValidator(qtg.QIntValidator(999999,0))
        self.filterSettingsLayout.addWidget(self.brightestFeaturesEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.preprocessCheckBox = qtw.QCheckBox('Preprocess?')
        self.filterSettingsLayout.addWidget(self.preprocessCheckBox, current_row, 0)

        # Empty widget for display formatting
        for i in range(4):
            current_row += 1
            self.filterSettingsLayout.addWidget(qtw.QWidget(), current_row, 0)

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
        self.smoothingSizeEntry.setEnabled( self.smoothingSizeCheckBox.isChecked() )

    # --------------------------
    # Update the threshold entry
    def updateThreshold(self):
        self.thresholdEntry.setEnabled( self.thresholdCheckBox.isChecked() )

    # -----------------------------------
    # Update the brightest features entry
    def updateBrightestFeatures(self):
        self.brightestFeaturesEntry.setEnabled( self.brightestFeaturesCheckBox.isChecked() )
