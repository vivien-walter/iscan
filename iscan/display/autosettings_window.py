import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR AUTOTRACK ADVANCED SETTINGS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class autotrackSettingsPanel(qtw.QMainWindow):
    def __init__(self, parent, initial_settings):
        super(autotrackSettingsPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Extract the default settings
        self.particle_size = initial_settings['particle_size']
        self.min_mass = initial_settings['min_mass']
        self.min_frame = initial_settings['min_frame']
        self.memory = initial_settings['memory']

        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Auto-Tracking Settings")

        # Populate the panel
        self.createSettingsInput(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createSettingsActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['auto_settings'] = None

    # -----------------------------------------------------------
    # Generate the manual input and display of the fit parameters
    def createSettingsInput(self, parentWidget):

        # Generate the widget
        self.autotrackSettingsWidget = qtw.QWidget()
        self.autotrackSettingsLayout = qtw.QFormLayout(self.autotrackSettingsWidget)
        self.autotrackSettingsLayout.setContentsMargins(0, 0, 0, 0)

        # Particle size
        self.particleSizeEntry = qtw.QLineEdit()
        self.particleSizeEntry.returnPressed.connect(self.checkParticleInput)
        self.particleSizeEntry.setText( str(self.particle_size) )
        self.particleSizeEntry.setStatusTip("Expected diameter of the particle to locate.")
        self.autotrackSettingsLayout.addRow(qtw.QLabel("Particle diameter (px)"), self.particleSizeEntry)

        # Minimum Intensity
        self.minMassEntry = qtw.QLineEdit()
        self.minMassEntry.returnPressed.connect(self.checkMassInput)
        self.minMassEntry.setText( str(self.min_mass) )
        self.minMassEntry.setStatusTip("Minimum integrated intensity of the particle to locate.")
        self.autotrackSettingsLayout.addRow(qtw.QLabel("Min. Integrated intensity"), self.minMassEntry)

        # Minimum frame number
        self.minFrameEntry = qtw.QLineEdit()
        self.minFrameEntry.returnPressed.connect(self.checkFrameInput)
        self.minFrameEntry.setText( str(self.min_frame) )
        self.minFrameEntry.setStatusTip("Minimum number of frames in the path to be saved.")
        self.autotrackSettingsLayout.addRow(qtw.QLabel("Min. Frames in path"), self.minFrameEntry)

        # Memory
        self.memoryEntry = qtw.QLineEdit()
        self.memoryEntry.returnPressed.connect(self.checkMemoryInput)
        self.memoryEntry.setText( str(self.memory) )
        self.memoryEntry.setStatusTip("Maximum number of frame skipped in a path to belong to one particle.")
        self.autotrackSettingsLayout.addRow(qtw.QLabel("Max. Frames skipped"), self.memoryEntry)

        # Display the widget
        self.autotrackSettingsWidget.setLayout(self.autotrackSettingsLayout)
        parentWidget.addWidget(self.autotrackSettingsWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createSettingsActions(self, parentWidget):

        # Generate the widget
        self.settingsActionsWidget = qtw.QWidget()
        self.settingsActionsLayout = qtw.QGridLayout(self.settingsActionsWidget)

        # Save and reset settings
        currentRow = 0
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveSettings)
        self.saveButton.setStatusTip("Save the settings.")
        self.settingsActionsLayout.addWidget(self.saveButton, currentRow, 0)

        self.resetButton = qtw.QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetSettings)
        self.resetButton.setStatusTip("Reset to the default settings.")
        self.settingsActionsLayout.addWidget(self.resetButton, currentRow, 1)

        # Close the window
        currentRow += 1
        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.settingsActionsLayout.addWidget(self.closeButton, currentRow, 1)

        # Display the widget
        self.settingsActionsWidget.setLayout(self.settingsActionsLayout)
        parentWidget.addWidget(self.settingsActionsWidget)

    ##-\-\-\-\-\-\
    ## MANAGE INPUT
    ##-/-/-/-/-/-/

    # -------------------------------------
    # Check the entry for the particle size
    def checkParticleInput(self, event=None):

        # Retrieve the text from the entry box
        particleSizeText = self.particleSizeEntry.text()

        # Check if the value is an integer
        particleSizeText = string2Int(particleSizeText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if particleSizeText == False:
            self.particleSizeEntry.setText( str(self.particle_size) )

        else:
            # Turn even numbers into odd ones
            if particleSizeText % 2 == 0:
                particleSizeText += 1
                self.particleSizeEntry.setText( str(particleSizeText) )

            self.particle_size = particleSizeText

    # -------------------------------------
    # Check the entry for the particle size
    def checkMassInput(self, event=None):

        # Retrieve the text from the entry box
        minMassText = self.minMassEntry.text()

        # Check if the value is an integer
        minMassText = string2Int(minMassText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if minMassText == False:
            self.minMassEntry.setText( str(self.min_mass) )

        else:
            self.min_mass = minMassText

    # -------------------------------------
    # Check the entry for the particle size
    def checkFrameInput(self, event=None):

        # Retrieve the text from the entry box
        minFrameText = self.minFrameEntry.text()

        # Check if the value is an integer
        minFrameText = string2Int(minFrameText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if minFrameText == False:
            self.minFrameEntry.setText( str(self.min_frame) )

        else:
            self.min_frame = minFrameText

    # -------------------------------------
    # Check the entry for the particle size
    def checkMemoryInput(self, event=None):

        # Retrieve the text from the entry box
        memoryText = self.memoryEntry.text()

        # Check if the value is an integer
        memoryText = string2Int(memoryText, convert=False)

        # Reinitialize the value if the input text is not an integer
        if memoryText == False:
            self.memoryEntry.setText( str(self.memory) )

        else:
            self.memory = memoryText

    ##-\-\-\-\-\-\-\-\-\-\
    ## MANAGE THE SETTINGS
    ##-/-/-/-/-/-/-/-/-/-/

    # -----------------
    # Save the settings
    def saveSettings(self):

        # Get the number of frame in the stack
        currentTab, _ = self.parent.getCurrentTab()
        currentImage = currentTab.image

        # Save the settings
        self.particle_size = int(self.particleSizeEntry.text())
        currentImage.tracking_settings['particle_size'] = self.particle_size
        self.min_mass = int(self.minMassEntry.text())
        currentImage.tracking_settings['min_mass'] = self.min_mass
        self.min_frame = int(self.minFrameEntry.text())
        currentImage.tracking_settings['min_frame'] =  self.min_frame
        self.memory = int(self.memoryEntry.text())
        currentImage.tracking_settings['memory'] = self.memory

    # ------------------
    # Reset the settings
    def resetSettings(self):

        # Get the number of frame in the stack
        currentTab, _ = self.parent.getCurrentTab()
        defaultSettings = currentTab.image.default_settings

        # Update the entry
        self.particle_size = defaultSettings['particle_size']
        self.particleSizeEntry.setText( str(self.particle_size) )
        self.min_mass = defaultSettings['min_mass']
        self.minMassEntry.setText( str(self.min_mass) )
        self.min_frame = defaultSettings['min_frame']
        self.minFrameEntry.setText( str(self.min_frame) )
        self.memory = defaultSettings['memory']
        self.memoryEntry.setText( str(self.memory) )

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.general_functions import string2Int
