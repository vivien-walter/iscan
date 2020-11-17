import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class pathDisplayFunctions:

    def createPathsDisplaySettings(self):

        # Generate the widget
        self.pathsSettingsWidget = qtw.QWidget()
        self.pathsSettingsLayout = qtw.QGridLayout(self.pathsSettingsWidget)

        # Checkbox to display positions
        self.displayPathsCheckbox = qtw.QCheckBox("Display path")
        self.displayPathsCheckbox.setChecked( self.parent.disptrack_conf.show_paths )
        self.pathsSettingsLayout.addWidget( self.displayPathsCheckbox )

        # Checkbox to display current paths
        self.currentOnlyPathCheckbox = qtw.QCheckBox("Show only current path?")
        self.currentOnlyPathCheckbox.setChecked( self.parent.disptrack_conf.current_path )
        self.pathsSettingsLayout.addWidget( self.currentOnlyPathCheckbox )

        # Checkbox to display current positions
        self.colorCurrentPathCheckbox = qtw.QCheckBox("Color current path?")
        self.colorCurrentPathCheckbox.setChecked( self.parent.disptrack_conf.color_path )
        self.pathsSettingsLayout.addWidget( self.colorCurrentPathCheckbox )

        # Display the widget
        self.pathsSettingsWidget.setLayout(self.pathsSettingsLayout)
        return self.pathsSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
