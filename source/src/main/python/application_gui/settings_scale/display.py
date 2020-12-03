import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CLabelledLineEdit
from application_gui.settings_scale.functions import SetScaleFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class SetScaleWindow(qtw.QMainWindow, SetScaleFunctions):
    def __init__(self, parent, image_class=None):
        super(SetScaleWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        #self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Set Scale")

        # Populate the panel
        self.createScaleSettings(self.mainLayout)
        #self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['set_scale'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Generate the display for the spatial scale
    def createScaleSettings(self, parentWidget):

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
        self.pixelDistanceEntry.setText( str(self.image_class.scale.space_scale) )
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
        self.lengthUnitEntry.setText( self.image_class.scale.space_unit )
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
        self.frameRateEntry.setText( str(self.image_class.scale.frame_rate) )
        self.scaleSettingsLayout.addWidget( self.frameRateEntry, current_row, 1 )

        # Display the widget
        self.scaleSettingsWidget.setLayout(self.scaleSettingsLayout)
        parentWidget.addWidget(self.scaleSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionWidget = qtw.QWidget()
        self.userActionLayout = qtw.QVBoxLayout(self.userActionWidget)

        # Add the global checkbox
        self.globalScaleCheckBox = qtw.QCheckBox("Global")
        self.userActionLayout.addWidget(self.globalScaleCheckBox)

        # Generate the widget
        self.userButtonWidget = qtw.QWidget()
        self.userButtonLayout = qtw.QHBoxLayout(self.userButtonWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Apply")
        self.applyButton.clicked.connect(self.applyScale)
        self.applyButton.setStatusTip("Apply the scale to the stack.")
        self.applyButton.setFixedWidth(125)
        self.userButtonLayout.addWidget(self.applyButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userButtonLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userButtonWidget.setLayout(self.userButtonLayout)
        self.userActionLayout.addWidget(self.userButtonWidget)

        # Display the widget
        self.userActionWidget.setLayout(self.userActionLayout)
        parentWidget.addWidget(self.userActionWidget)
