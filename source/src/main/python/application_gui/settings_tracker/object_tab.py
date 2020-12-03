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
        self.objectSettingsLayout.addWidget(qtw.QLabel("Intensity Min."), current_row, 0)
        self.minIntensityEntry = qtw.QLineEdit()
        self.minIntensityEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.objectSettingsLayout.addWidget(self.minIntensityEntry, current_row, 1)

        current_row += 1
        self.objectSettingsLayout.addWidget(qtw.QLabel("Diameter"), current_row, 0)
        self.diameterEntry = qtw.QLineEdit()
        self.diameterEntry.setValidator(qtg.QIntValidator(999999,1))
        self.objectSettingsLayout.addWidget(self.diameterEntry, current_row, 1)

        current_row += 1
        self.darkSpotCheckBox = qtw.QCheckBox("Dark particles?")
        self.objectSettingsLayout.addWidget(self.darkSpotCheckBox, current_row, 0)

        current_row += 1
        self.maxSizeCheckBox = qtw.QCheckBox('Set maximum size?')
        self.maxSizeCheckBox.clicked.connect(self.updateMaxSize)
        self.objectSettingsLayout.addWidget(self.maxSizeCheckBox, current_row, 0)
        self.maxSizeEntry = qtw.QLineEdit()
        self.maxSizeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.objectSettingsLayout.addWidget(self.maxSizeEntry, current_row, 1)

        # Setting for the separation
        current_row += 1
        self.separationCheckBox = qtw.QCheckBox('Set separation?')
        self.separationCheckBox.clicked.connect(self.updateSeparation)
        self.objectSettingsLayout.addWidget(self.separationCheckBox, current_row, 0)
        self.separationEntry = qtw.QLineEdit()
        self.separationEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.objectSettingsLayout.addWidget(self.separationEntry, current_row, 1)

        # Setting for the percentile
        current_row += 1
        self.objectSettingsLayout.addWidget(qtw.QLabel("Percentile"), current_row, 0)
        self.percentileEntry = qtw.QLineEdit()
        self.percentileEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.objectSettingsLayout.addWidget(self.percentileEntry, current_row, 1)

        # Empty widget for display formatting
        for i in range(3):
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
        self.maxSizeEntry.setEnabled( self.maxSizeCheckBox.isChecked() )

    # ---------------------------
    # Update the separation entry
    def updateSeparation(self):
        self.separationEntry.setEnabled( self.separationCheckBox.isChecked() )
