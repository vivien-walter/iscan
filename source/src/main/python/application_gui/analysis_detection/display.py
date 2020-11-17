import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import CHorizontalSeparator, CLabel
from application_gui.analysis_detection.functions import particleDetectionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class particleDetectionWindow(qtw.QMainWindow, particleDetectionFunctions):
    def __init__(self, parent, image_class=None):
        super(particleDetectionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        #self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Particle Detection")

        # Populate the panel
        self.createDetectionControls(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createPreviewActions(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

        # Update the panel with image content
        self.initializeDetection()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):

        # Close the subwindow if opened
        if 'particle_advanced' in self.parent.subWindows.keys():
            if self.parent.subWindows['particle_advanced'] is not None:
                self.parent.subWindows['particle_advanced'].close()

        event.accept()
        self.parent.subWindows['particle_analysis'] = None

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the controls for the user
    def createDetectionControls(self, parentWidget):

        # Make the grid for values
        self.settingsGridWidget = qtw.QWidget()
        self.settingsGridLayout = qtw.QGridLayout(self.settingsGridWidget)

        # Minimum intensity input
        current_row = 0
        self.settingsGridLayout.addWidget(CLabel("Intensity Min."), current_row, 0)
        self.minIntensityEntry = qtw.QLineEdit()
        #self.minIntensityEntry.setValidator(qtg.QDoubleValidator(999999,0,3))
        self.minIntensityEntry.editingFinished.connect(self.doLiveUpdate)
        self.settingsGridLayout.addWidget(self.minIntensityEntry, current_row, 1)

        current_row += 1
        self.settingsGridLayout.addWidget(CLabel("Diameter"), current_row, 0)
        self.diameterEntry = qtw.QLineEdit()
        #self.diameterEntry.setValidator(qtg.QIntValidator(999999,1))
        self.diameterEntry.editingFinished.connect(self.doLiveUpdate)
        self.settingsGridLayout.addWidget(self.diameterEntry, current_row, 1)

        current_row += 1
        self.darkSpotCheckBox = qtw.QCheckBox("Dark particles?")
        self.darkSpotCheckBox.clicked.connect(self.doLiveUpdate)
        self.settingsGridLayout.addWidget(self.darkSpotCheckBox, current_row, 0)

        current_row += 1
        self.manageTrackerButton = qtw.QPushButton("Tracker...")
        self.manageTrackerButton.clicked.connect(self.openTrackerMenu)
        self.manageTrackerButton.setFixedWidth(125)
        self.settingsGridLayout.addWidget(self.manageTrackerButton, current_row, 0)

        self.advancedSettingsButton = qtw.QPushButton("Advanced")
        self.advancedSettingsButton.clicked.connect(self.openAdvancedSettings)
        self.advancedSettingsButton.setFixedWidth(125)
        self.settingsGridLayout.addWidget(self.advancedSettingsButton, current_row, 1)

        # Display the widget
        self.settingsGridWidget.setLayout(self.settingsGridLayout)
        parentWidget.addWidget(self.settingsGridWidget)

    # -------------------------------
    # Generate the command to preview
    def createPreviewActions(self, parentWidget):

        # Generate the widget
        self.detectionSettingsWidget = qtw.QWidget()
        self.detectionSettingsLayout = qtw.QVBoxLayout(self.detectionSettingsWidget)

        # Add the button to open a new file
        self.previewButton = qtw.QPushButton("Preview")
        self.previewButton.clicked.connect(self.previewDetection)
        self.previewButton.setStatusTip("Detect particles on the current frame.")
        self.previewButton.setFixedWidth(250)
        self.detectionSettingsLayout.addWidget(self.previewButton, alignment=qtc.Qt.AlignCenter)

        self.livePreviewCheckBox = qtw.QCheckBox("Live preview?")
        self.livePreviewCheckBox.clicked.connect(self.doLiveUpdate)
        self.detectionSettingsLayout.addWidget(self.livePreviewCheckBox)

        # Display the widget
        self.detectionSettingsWidget.setLayout(self.detectionSettingsLayout)
        parentWidget.addWidget(self.detectionSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.processButton = qtw.QPushButton("Process")
        self.processButton.clicked.connect(self.processParticleDetection)
        self.processButton.setStatusTip("Process the whole stack with the given settings.")
        self.processButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.processButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
