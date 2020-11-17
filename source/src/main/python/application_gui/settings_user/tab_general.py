import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class userGeneralSettingsTab:

    def createGeneralSettings(self):

        # Generate the widget
        self.generalSettingsWidget = qtw.QWidget()
        self.generalSettingsLayout = qtw.QVBoxLayout(self.generalSettingsWidget)

        # Settings for image opening
        self.generalSettingsLayout.addWidget( CLabel("Open Image(s):") )

        # Default type of object
        self.imageTypeButtonGroupWidget = qtw.QWidget()
        self.imageTypeButtonGroupLayout = qtw.QVBoxLayout(self.imageTypeButtonGroupWidget)

        self.imageTypeGroupButton = qtw.QButtonGroup(self.imageTypeButtonGroupWidget)

        self.singleFileRadiobutton = qtw.QRadioButton("Single File")
        self.singleFileRadiobutton.setChecked( self.parent.config.single_images )
        self.imageTypeGroupButton.addButton(self.singleFileRadiobutton)
        self.imageTypeButtonGroupLayout.addWidget(self.singleFileRadiobutton)

        self.imageFolderRadiobutton = qtw.QRadioButton("Images Folder")
        self.imageFolderRadiobutton.setChecked( not self.parent.config.single_images )
        self.imageTypeGroupButton.addButton(self.imageFolderRadiobutton)
        self.imageTypeButtonGroupLayout.addWidget(self.imageFolderRadiobutton)

        self.imageTypeButtonGroupWidget.setLayout(self.imageTypeButtonGroupLayout)
        self.imageTypeButtonGroupWidget.setContentsMargins(0, 0, 0, 0)
        self.generalSettingsLayout.addWidget(self.imageTypeButtonGroupWidget)

        # Load automatically with the recommandation
        self.autoOpenImageCheckBox = qtw.QCheckBox("Auto-load with suggestions?")
        self.autoOpenImageCheckBox.setChecked( self.parent.config.autoload_images )
        self.generalSettingsLayout.addWidget(self.autoOpenImageCheckBox)

        # Load automatically with the recommandation
        self.autoBackgroundCorrectionCheckBox = qtw.QCheckBox("Correct background automatically?")
        self.autoBackgroundCorrectionCheckBox.setChecked( self.parent.config.auto_background )
        self.generalSettingsLayout.addWidget(self.autoBackgroundCorrectionCheckBox)

        self.generalSettingsLayout.addWidget( CHorizontalSeparator() )

        # Add dark theme checkbox
        #self.darkThemeCheckBox = qtw.QCheckBox("Use dark theme?")
        #self.darkThemeCheckBox.setChecked( self.parent.config.dark_theme )
        #self.generalSettingsLayout.addWidget(self.darkThemeCheckBox)

        # Add empty widget
        for i in range(8):
            self.generalSettingsLayout.addWidget(qtw.QWidget())

        # Display the widget
        self.generalSettingsWidget.setLayout(self.generalSettingsLayout)
        return self.generalSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
