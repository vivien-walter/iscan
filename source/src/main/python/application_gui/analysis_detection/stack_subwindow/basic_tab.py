import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class basicSettingsFunctions:

    def createBasicSettings(self):

        # Generate the widget
        self.basicSettingsWidget = qtw.QWidget()
        self.basicSettingsLayout = qtw.QGridLayout(self.basicSettingsWidget)

        # Setting for the memory
        current_row = 0
        self.basicSettingsLayout.addWidget(qtw.QLabel("Memory"), current_row, 0)
        self.memoryEntry = qtw.QLineEdit()
        self.memoryEntry.setValidator(qtg.QIntValidator(999999,0))
        self.basicSettingsLayout.addWidget(self.memoryEntry, current_row, 1)

        # Setting for the search range
        current_row += 1
        self.basicSettingsLayout.addWidget(qtw.QLabel("Search range"), current_row, 0)
        self.searchRangeEntry = qtw.QLineEdit()
        self.searchRangeEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.basicSettingsLayout.addWidget(self.searchRangeEntry, current_row, 1)

        # Setting for the adaptive step
        current_row += 1
        self.basicSettingsLayout.addWidget(qtw.QLabel("Adaptive step"), current_row, 0)
        self.adaptiveStepEntry = qtw.QLineEdit()
        self.adaptiveStepEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.basicSettingsLayout.addWidget(self.adaptiveStepEntry, current_row, 1)

        # Setting for the filter stub threshold
        current_row += 1
        self.basicSettingsLayout.addWidget(qtw.QLabel("Filter stubs"), current_row, 0)
        self.filterStubsEntry = qtw.QLineEdit()
        self.filterStubsEntry.setValidator(qtg.QIntValidator(999999,0))
        self.basicSettingsLayout.addWidget(self.filterStubsEntry, current_row, 1)

        # Display the widget
        self.basicSettingsWidget.setLayout(self.basicSettingsLayout)
        return self.basicSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
