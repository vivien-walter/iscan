import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class positionsDisplayFunctions:

    def createPositionsDisplaySettings(self):

        # Generate the widget
        self.positionsSettingsWidget = qtw.QWidget()
        self.positionsSettingsLayout = qtw.QGridLayout(self.positionsSettingsWidget)

        # Checkbox to display positions
        self.displayPositionsCheckbox = qtw.QCheckBox("Display positions")
        self.displayPositionsCheckbox.setChecked( self.parent.disptrack_conf.show_positions )
        self.positionsSettingsLayout.addWidget( self.displayPositionsCheckbox )

        # Checkbox to display current positions
        self.currentOnlyPositionsCheckbox = qtw.QCheckBox("Show only current position?")
        self.currentOnlyPositionsCheckbox.setChecked( self.parent.disptrack_conf.current_position )
        self.positionsSettingsLayout.addWidget( self.currentOnlyPositionsCheckbox )

        # Checkbox to display current positions
        self.colorCurrentPositionCheckbox = qtw.QCheckBox("Color current position?")
        self.colorCurrentPositionCheckbox.setChecked( self.parent.disptrack_conf.color_position )
        self.positionsSettingsLayout.addWidget( self.colorCurrentPositionCheckbox )

        # Display the widget
        self.positionsSettingsWidget.setLayout(self.positionsSettingsLayout)
        return self.positionsSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
