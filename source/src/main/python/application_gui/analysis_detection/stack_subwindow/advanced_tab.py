import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class advancedSettingsFunctions:

    def createAdvancedSettings(self):

        # Generate the widget
        self.advancedSettingsWidget = qtw.QWidget()
        self.advancedSettingsLayout = qtw.QGridLayout(self.advancedSettingsWidget)

        # Setting for the adaptive stop
        current_row = 0
        self.adaptiveStopCheckBox = qtw.QCheckBox('Set adaptive stop?')
        self.adaptiveStopCheckBox.clicked.connect(self.updateAdaptiveStop)
        self.advancedSettingsLayout.addWidget(self.adaptiveStopCheckBox, current_row, 0)
        self.adaptiveStopEntry = qtw.QLineEdit()
        self.adaptiveStopEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.advancedSettingsLayout.addWidget(self.adaptiveStopEntry, current_row, 1)

        # Setting for the neighbor strategy
        current_row += 1
        self.advancedSettingsLayout.addWidget(qtw.QLabel("Neighbor strategy:"), current_row, 0)
        current_row += 1
        self.neighborStrategyComboBox = qtw.QComboBox()
        self.neighborStrategyComboBox.addItem('None')
        self.neighborStrategyComboBox.addItem('KDTree')
        self.neighborStrategyComboBox.addItem('BTree')
        self.advancedSettingsLayout.addWidget(self.neighborStrategyComboBox, current_row, 0, 1, 2)

        # Setting for the link strategy
        current_row += 1
        self.advancedSettingsLayout.addWidget(qtw.QLabel("Link strategy:"), current_row, 0)
        current_row += 1
        self.linkStrategyComboBox = qtw.QComboBox()
        self.linkStrategyComboBox.addItem('None')
        self.linkStrategyComboBox.addItem('Recursive')
        self.linkStrategyComboBox.addItem('Nonrecursive')
        self.linkStrategyComboBox.addItem('Numba')
        self.linkStrategyComboBox.addItem('Hybrid')
        self.linkStrategyComboBox.addItem('Drop')
        self.linkStrategyComboBox.addItem('Auto')
        self.advancedSettingsLayout.addWidget(self.linkStrategyComboBox, current_row, 0, 1, 2)

        # Display the widget
        self.advancedSettingsWidget.setLayout(self.advancedSettingsLayout)
        return self.advancedSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Update the adaptive stop entry
    def updateAdaptiveStop(self):
        self.adaptiveStopEntry.setEnabled( self.adaptiveStopCheckBox.isChecked() )
