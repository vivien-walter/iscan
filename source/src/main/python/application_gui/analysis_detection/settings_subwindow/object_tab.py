import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class objectSettingsFunctions:

    def createObjectSettings(self):

        # Generate the widget
        self.objectSettingsWidget = qtw.QWidget()
        self.objectSettingsLayout = qtw.QGridLayout(self.objectSettingsWidget)

        # Setting for the maximum size
        current_row = 0
        self.maxSizeCheckBox = qtw.QCheckBox('Set maximum size?')
        self.maxSizeCheckBox.clicked.connect(self.updateMaxSize)
        self.objectSettingsLayout.addWidget(self.maxSizeCheckBox, current_row, 0)
        self.maxSizeEntry = qtw.QLineEdit()
        #self.maxSizeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.maxSizeEntry.editingFinished.connect(self.editMaxSize)
        self.objectSettingsLayout.addWidget(self.maxSizeEntry, current_row, 1)

        # Setting for the separation
        current_row += 1
        self.separationCheckBox = qtw.QCheckBox('Set separation?')
        self.separationCheckBox.clicked.connect(self.updateSeparation)
        self.objectSettingsLayout.addWidget(self.separationCheckBox, current_row, 0)
        self.separationEntry = qtw.QLineEdit()
        #self.separationEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.separationEntry.editingFinished.connect(self.editSeparation)
        self.objectSettingsLayout.addWidget(self.separationEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.objectSettingsLayout.addWidget(qtw.QLabel("Percentile"), current_row, 0)
        self.percentileEntry = qtw.QLineEdit()
        #self.percentileEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.percentileEntry.editingFinished.connect(self.editPercentile)
        self.objectSettingsLayout.addWidget(self.percentileEntry, current_row, 1)

        # Empty widget for display formatting
        current_row += 1
        self.objectSettingsLayout.addWidget(qtw.QWidget(), current_row, 0)

        # Display the widget
        self.objectSettingsWidget.setLayout(self.objectSettingsLayout)
        return self.objectSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # -----------------------------
    # Update the maximum size entry
    def updateMaxSize(self):

        # Toggle the status of the entry
        self.maxSizeEntry.setEnabled( self.maxSizeCheckBox.isChecked() )

        # Edit the session
        self.editMaxSize()

    # ---------------------------
    # Update the separation entry
    def updateSeparation(self):

        # Toggle the status of the entry
        self.separationEntry.setEnabled( self.separationCheckBox.isChecked() )

        # Edit the session
        self.editSeparation()

    ##-\-\-\-\-\-\-\
    ## UPDATE SESSION
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Edit the maximum size settings
    def editMaxSize(self):

        # Save the content of the entry
        if self.maxSizeCheckBox.isChecked():
            self.detection_session.maxsize = float( self.maxSizeEntry.text() )
        else:
            self.detection_session.maxsize = None

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # ----------------------------
    # Edit the separation settings
    def editSeparation(self):

        # Save the content of the entry
        if self.separationCheckBox.isChecked():
            self.detection_session.separation = float( self.separationEntry.text() )
        else:
            self.detection_session.separation = None

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # ----------------------------
    # Edit the percentile settings
    def editPercentile(self):
        self.detection_session.percentile = float( self.percentileEntry.text() )

        # Refresh display if needed
        self.emitSignalLiveUpdate()
