import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class scaleSettingsTab:

    def createScaleSettings(self):

        # Generate the widget
        self.scaleSettingsWidget = qtw.QWidget()
        self.scaleSettingsLayout = qtw.QGridLayout(self.scaleSettingsWidget)

        # Label for space scale
        current_row = 0
        self.scaleSettingsLayout.addWidget( CLabel("Space Scale:"), current_row, 0, 1, 2 )

        # Entry for the distance in pixel
        current_row += 1
        self.scaleSettingsLayout.addWidget( qtw.QLabel("Distance in pixels"), current_row, 0 )
        self.pixelDistanceEntry = qtw.QLineEdit()
        self.pixelDistanceEntry.setText( str(self.parent.config.space_scale) )
        self.scaleSettingsLayout.addWidget( self.pixelDistanceEntry, current_row, 1 )

        # Entry for the real distance
        current_row += 1
        self.scaleSettingsLayout.addWidget( qtw.QLabel("Known distance"), current_row, 0 )
        self.knownDistanceEntry = qtw.QLineEdit()
        self.knownDistanceEntry.setText( "1" )
        self.scaleSettingsLayout.addWidget( self.knownDistanceEntry, current_row, 1 )

        # Entry for the length unit
        current_row += 1
        self.scaleSettingsLayout.addWidget( qtw.QLabel("Unit of length"), current_row, 0 )
        self.lengthUnitEntry = qtw.QLineEdit()
        self.lengthUnitEntry.setText( str(self.parent.config.space_unit) )
        self.scaleSettingsLayout.addWidget( self.lengthUnitEntry, current_row, 1 )

        current_row += 1
        self.scaleSettingsLayout.addWidget( CHorizontalSeparator(), current_row, 0, 1, 2 )

        # Label for time scale
        current_row += 1
        self.scaleSettingsLayout.addWidget( CLabel("Time Scale:"), current_row, 0, 1, 2 )

        # Entry for the length unit
        current_row += 1
        self.scaleSettingsLayout.addWidget( qtw.QLabel("Frame rate"), current_row, 0 )
        self.frameRateEntry = qtw.QLineEdit()
        self.frameRateEntry.setText( str(self.parent.config.frame_rate) )
        self.scaleSettingsLayout.addWidget( self.frameRateEntry, current_row, 1 )

        # Add empty widget
        for i in range(6):
            current_row += 1
            self.scaleSettingsLayout.addWidget(qtw.QWidget(), current_row, 0, 1, 2 )

        # Display the widget
        self.scaleSettingsWidget.setLayout(self.scaleSettingsLayout)
        return self.scaleSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
