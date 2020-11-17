import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class trajectorySettingsFunctions:

    def createTrajectorySettings(self):

        # Generate the widget
        self.trajectorySettingsWidget = qtw.QWidget()
        self.trajectorySettingsLayout = qtw.QGridLayout(self.trajectorySettingsWidget)

        # Setting for the maximum size
        current_row = 0
        self.trajectorySettingsLayout.addWidget(qtw.QLabel("Memory"), current_row, 0)
        self.memoryEntry = qtw.QLineEdit()
        self.memoryEntry.setValidator(qtg.QIntValidator(999999,0))
        self.trajectorySettingsLayout.addWidget(self.memoryEntry, current_row, 1)

        # Setting for the search range
        current_row += 1
        self.trajectorySettingsLayout.addWidget(qtw.QLabel("Search range"), current_row, 0)
        self.searchRangeEntry = qtw.QLineEdit()
        self.searchRangeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.trajectorySettingsLayout.addWidget(self.searchRangeEntry, current_row, 1)

        # Setting for the adaptive step
        current_row += 1
        self.trajectorySettingsLayout.addWidget(qtw.QLabel("Adaptive step"), current_row, 0)
        self.adaptiveStepEntry = qtw.QLineEdit()
        self.adaptiveStepEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.trajectorySettingsLayout.addWidget(self.adaptiveStepEntry, current_row, 1)

        # Setting for the filter stub threshold
        current_row += 1
        self.trajectorySettingsLayout.addWidget(qtw.QLabel("Filter stubs"), current_row, 0)
        self.filterStubsEntry = qtw.QLineEdit()
        self.filterStubsEntry.setValidator(qtg.QIntValidator(999999,0))
        self.trajectorySettingsLayout.addWidget(self.filterStubsEntry, current_row, 1)

        # Setting for the adaptive stop
        current_row += 1
        self.adaptiveStopCheckBox = qtw.QCheckBox('Set adaptive stop?')
        self.adaptiveStopCheckBox.clicked.connect(self.updateAdaptiveStop)
        self.trajectorySettingsLayout.addWidget(self.adaptiveStopCheckBox, current_row, 0)
        self.adaptiveStopEntry = qtw.QLineEdit()
        self.adaptiveStopEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.trajectorySettingsLayout.addWidget(self.adaptiveStopEntry, current_row, 1)

        # Setting for the neighbor strategy
        current_row += 1
        self.trajectorySettingsLayout.addWidget(qtw.QLabel("Neighbor strategy:"), current_row, 0)
        current_row += 1
        self.neighborStrategyComboBox = qtw.QComboBox()
        self.neighborStrategyComboBox.addItem('None')
        self.neighborStrategyComboBox.addItem('KDTree')
        self.neighborStrategyComboBox.addItem('BTree')
        self.trajectorySettingsLayout.addWidget(self.neighborStrategyComboBox, current_row, 0, 1, 2)

        # Setting for the link strategy
        current_row += 1
        self.trajectorySettingsLayout.addWidget(qtw.QLabel("Link strategy:"), current_row, 0)
        current_row += 1
        self.linkStrategyComboBox = qtw.QComboBox()
        self.linkStrategyComboBox.addItem('None')
        self.linkStrategyComboBox.addItem('Recursive')
        self.linkStrategyComboBox.addItem('Nonrecursive')
        self.linkStrategyComboBox.addItem('Numba')
        self.linkStrategyComboBox.addItem('Hybrid')
        self.linkStrategyComboBox.addItem('Drop')
        self.linkStrategyComboBox.addItem('Auto')
        self.trajectorySettingsLayout.addWidget(self.linkStrategyComboBox, current_row, 0, 1, 2)

        # Empty widget for display formatting
        for i in range(0):
            current_row += 1
            self.trajectorySettingsLayout.addWidget(qtw.QWidget(), current_row, 0)

        # Display the widget
        self.trajectorySettingsWidget.setLayout(self.trajectorySettingsLayout)
        return self.trajectorySettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)

    ##-\-\-\-\-\-\-\
    ## UPDATE DISPLAY
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Update the adaptive stop entry
    def updateAdaptiveStop(self):
        self.adaptiveStopEntry.setEnabled( self.adaptiveStopCheckBox.isChecked() )
