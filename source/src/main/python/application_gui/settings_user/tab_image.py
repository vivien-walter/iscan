import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CLabel, CHorizontalSeparator, CLabelledLineEdit

##-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR USER SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/

class imageSettingsTab:

    def createImageSettings(self):

        # Generate the widget
        self.imageSettingsWidget = qtw.QWidget()
        self.imageSettingsLayout = qtw.QVBoxLayout(self.imageSettingsWidget)

        # Settings for image preparation
        self.imageSettingsLayout.addWidget( CLabel("Image Preparation:") )

        # Crop the image if recommended
        self.cropImageCheckBox = qtw.QCheckBox("Crop the image")
        self.cropImageCheckBox.setChecked( self.parent.config.crop_image )
        self.imageSettingsLayout.addWidget(self.cropImageCheckBox)

        cropSizeEntry_l, self.cropSizeEntry = CLabelledLineEdit("Crop size (px):", bold=False)
        self.cropSizeEntry.setText( str(self.parent.config.crop_size) )
        self.imageSettingsLayout.addWidget(cropSizeEntry_l)

        # Correct signed bits if recommended
        self.correctSignedBitsCheckBox = qtw.QCheckBox("Correct signed bits")
        self.correctSignedBitsCheckBox.setChecked( self.parent.config.correct_signed )
        self.imageSettingsLayout.addWidget(self.correctSignedBitsCheckBox)

        self.imageSettingsLayout.addWidget( CHorizontalSeparator() )

        # Settings for image correction
        self.imageSettingsLayout.addWidget( CLabel("Image Correction:") )

        # Settings for the background settings
        self.imageSettingsLayout.addWidget( qtw.QLabel("Background correction settings") )

        # Get the correction type
        self.correctionTypeComboBox = qtw.QComboBox()
        self.correctionTypeComboBox.addItem('Division')
        self.correctionTypeComboBox.addItem('Subtraction')
        _index_correction = self.correctionTypeComboBox.findText(self.parent.config.correction_type.capitalize(), qtc.Qt.MatchFixedString)
        if _index_correction >= 0:
             self.correctionTypeComboBox.setCurrentIndex(_index_correction)
        self.imageSettingsLayout.addWidget(self.correctionTypeComboBox)

        # Get the background type
        self.backgroundTypeComboBox = qtw.QComboBox()
        self.backgroundTypeComboBox.addItem('Median')
        self.backgroundTypeComboBox.addItem('Mean')
        _index_background = self.backgroundTypeComboBox.findText(self.parent.config.background_type.capitalize(), qtc.Qt.MatchFixedString)
        if _index_background >= 0:
             self.backgroundTypeComboBox.setCurrentIndex(_index_background)
        self.imageSettingsLayout.addWidget(self.backgroundTypeComboBox)

        # Correct intensity fluctuation
        self.correctFluctuationsCheckBox = qtw.QCheckBox("Correct intensity fluctuations")
        self.correctFluctuationsCheckBox.setChecked( self.parent.config.correct_intensity )
        self.imageSettingsLayout.addWidget(self.correctFluctuationsCheckBox)

        # Get the correction type
        self.fluctuationCorrectionTypeComboBox = qtw.QComboBox()
        self.fluctuationCorrectionTypeComboBox.addItem('Median')
        self.fluctuationCorrectionTypeComboBox.addItem('Mean')
        _index_fluctuation = self.fluctuationCorrectionTypeComboBox.findText(self.parent.config.intensity_correction_type.capitalize(), qtc.Qt.MatchFixedString)
        if _index_fluctuation >= 0:
             self.fluctuationCorrectionTypeComboBox.setCurrentIndex(_index_fluctuation)
        self.imageSettingsLayout.addWidget(self.fluctuationCorrectionTypeComboBox)

        # Correct intensity fluctuation
        self.newTabCheckBox = qtw.QCheckBox("Open corrected stack in a new tab")
        self.newTabCheckBox.setChecked( self.parent.config.correct_newtab )
        self.imageSettingsLayout.addWidget(self.newTabCheckBox)

        # Display the widget
        self.imageSettingsWidget.setLayout(self.imageSettingsLayout)
        return self.imageSettingsWidget
        #parentWidget.addWidget(self.serverSettingsWidget)
