import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class otherSettingsFunctions:

    def createOtherSettings(self):

        # Generate the widget
        self.otherSettingsWidget = qtw.QWidget()
        self.otherSettingsLayout = qtw.QGridLayout(self.otherSettingsWidget)

        # Setting for the maximum size
        current_row = 0
        self.characterizeCheckBox = qtw.QCheckBox('Characterize?')
        self.characterizeCheckBox.clicked.connect(self.editCharacterize)
        self.otherSettingsLayout.addWidget(self.characterizeCheckBox, current_row, 0)

        # Setting for the separation
        current_row += 1
        self.otherSettingsLayout.addWidget(qtw.QLabel("Engine:"), current_row, 0)

        # Setting for the percentile
        current_row += 1
        self.engineComboBox = qtw.QComboBox()
        self.engineComboBox.addItem('Auto')
        self.engineComboBox.addItem('Python')
        self.engineComboBox.addItem('Numba')
        self.engineComboBox.activated.connect(self.editEngine)
        self.otherSettingsLayout.addWidget(self.engineComboBox, current_row, 0, 1, 2)

        # Empty widget for display formatting
        current_row += 1
        self.otherSettingsLayout.addWidget(qtw.QWidget(), current_row, 0)
        current_row += 1
        self.otherSettingsLayout.addWidget(qtw.QWidget(), current_row, 0)

        # Display the widget
        self.otherSettingsWidget.setLayout(self.otherSettingsLayout)
        return self.otherSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)

    ##-\-\-\-\-\-\-\
    ## UPDATE SESSION
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Edit the characterize settings
    def editCharacterize(self):
        self.detection_session.characterize = self.characterizeCheckBox.isChecked()

        # Refresh display if needed
        self.emitSignalLiveUpdate()

    # ------------------------
    # Edit the engine settings
    def editEngine(self):
        self.detection_session.engine = self.engineComboBox.currentText().lower()

        # Refresh display if needed
        self.emitSignalLiveUpdate()
