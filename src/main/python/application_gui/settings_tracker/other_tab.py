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
        self.otherSettingsLayout.addWidget(self.engineComboBox, current_row, 0, 1, 2)

        # Empty widget for display formatting
        for i in range(6):
            current_row += 1
            self.otherSettingsLayout.addWidget(qtw.QWidget(), current_row, 0)

        # Display the widget
        self.otherSettingsWidget.setLayout(self.otherSettingsLayout)
        return self.otherSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
