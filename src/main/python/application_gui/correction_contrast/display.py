import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from application_gui.common_gui_functions import CHorizontalSeparator
from application_gui.correction_contrast.functions import contrastCorrectionFunctions

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR READING METADATA
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class contrastCorrectionWindow(qtw.QMainWindow, contrastCorrectionFunctions):
    def __init__(self, parent, image_class=None):
        super(contrastCorrectionWindow, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent
        self.image_class = image_class
        self.analyzed_image = image_class.image.source
        self.auto_attempt = 0
        self.setWindowModality(qtc.Qt.ApplicationModal)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.mainLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Brightness & Contrast")

        # Populate the panel
        self.createGraphDisplay(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createBrightnessControls(self.mainLayout)
        self.mainLayout.addWidget( CHorizontalSeparator() )
        self.createBrightnessActions(self.mainLayout)
        self.createUserActions(self.mainLayout)

        # Display the panel
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.show()
        self.setFixedSize(375,600)

        # Update the panel with image content
        self.getDistribution()

    # ---------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event=None):
        event.accept()
        self.parent.subWindows['contrast_correction'] = None

        # Reset the display if needed
        tab_id = self.parent.imageTabDisplay.currentIndex()
        self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.rescaleTest()
        self.parent.imageTabDisplay.displayedTabs[tab_id].displayImage()

    ##-\-\-\-\-\-\-\-\-\-\
    ## GENERATE THE DISPLAY
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------
    # Generate the display for the graph
    def createGraphDisplay(self, parentWidget):

        # Generate the widget
        self.plotGraphWidget = qtw.QWidget()
        self.plotGraphLayout = qtw.QVBoxLayout(self.plotGraphWidget)

        # Make the graph
        self.graphWidget = pg.PlotWidget()
        self.plotGraphLayout.addWidget(self.graphWidget)

        # Add the subwidget for PV values
        self.pixelValuesWidget = qtw.QWidget()
        self.pixelValuesLayout = qtw.QHBoxLayout(self.pixelValuesWidget)

        self.minValueLabel = qtw.QLabel('Min')
        self.pixelValuesLayout.addWidget(self.minValueLabel, alignment=qtc.Qt.AlignLeft)

        self.maxValueLabel = qtw.QLabel('Max')
        self.pixelValuesLayout.addWidget(self.maxValueLabel, alignment=qtc.Qt.AlignRight)

        self.pixelValuesWidget.setLayout(self.pixelValuesLayout)
        self.plotGraphLayout.addWidget(self.pixelValuesWidget)

        # Add the live update checkbox
        self.liveCheckBox = qtw.QCheckBox("Preview?")
        self.liveCheckBox.setChecked(True)
        self.liveCheckBox.toggled.connect(self.refreshFrameDisplay)
        self.plotGraphLayout.addWidget(self.liveCheckBox)

        # Display the widget
        self.plotGraphWidget.setLayout(self.plotGraphLayout)
        parentWidget.addWidget(self.plotGraphWidget)

    # ----------------------------------------------------
    # Generate the control for the brightness and contrast
    def createBrightnessControls(self, parentWidget):

        # Generate the widget
        self.brightnessSettingsWidget = qtw.QWidget()
        self.brightnessSettingsLayout = qtw.QVBoxLayout(self.brightnessSettingsWidget)

        # Generate the min value slider
        self.minPVSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.minPVSlider.valueChanged.connect(self.minChanged)
        self.brightnessSettingsLayout.addWidget(self.minPVSlider)
        self.brightnessSettingsLayout.addWidget(qtw.QLabel("Minimum"), alignment=qtc.Qt.AlignCenter)

        # Generate the max value slider
        self.maxPVSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.maxPVSlider.valueChanged.connect(self.maxChanged)
        self.brightnessSettingsLayout.addWidget(self.maxPVSlider)
        self.brightnessSettingsLayout.addWidget(qtw.QLabel("Maximum"), alignment=qtc.Qt.AlignCenter)

        # Generate the brightness slider
        self.brightnessSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.brightnessSlider.valueChanged.connect(self.brightnessChanged)
        self.brightnessSettingsLayout.addWidget(self.brightnessSlider)
        self.brightnessSettingsLayout.addWidget(qtw.QLabel("Brightness"), alignment=qtc.Qt.AlignCenter)

        # Generate the contrast slider
        self.contrastSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.contrastSlider.valueChanged.connect(self.contrastChanged)
        self.brightnessSettingsLayout.addWidget(self.contrastSlider)
        self.brightnessSettingsLayout.addWidget(qtw.QLabel("Contrast"), alignment=qtc.Qt.AlignCenter)

        # Display the widget
        self.brightnessSettingsWidget.setLayout(self.brightnessSettingsLayout)
        parentWidget.addWidget(self.brightnessSettingsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createBrightnessActions(self, parentWidget):

        # Generate the widget
        self.contrastActionsWidget = qtw.QWidget()
        self.contrastActionsLayout = qtw.QHBoxLayout(self.contrastActionsWidget)

        # Add the button to open a new file
        self.autoButton = qtw.QPushButton("Auto")
        self.autoButton.clicked.connect(self.setAutoValues)
        self.autoButton.setStatusTip("Automatically set the contrast correction.")
        self.autoButton.setFixedWidth(125)
        self.contrastActionsLayout.addWidget(self.autoButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.resetButton = qtw.QPushButton("Reset")
        self.resetButton.clicked.connect(self.resetValues)
        self.resetButton.setStatusTip("Reset the brightness and contrast settings.")
        self.resetButton.setFixedWidth(125)
        self.contrastActionsLayout.addWidget(self.resetButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.contrastActionsWidget.setLayout(self.contrastActionsLayout)
        parentWidget.addWidget(self.contrastActionsWidget)

    # ----------------------------------
    # Generate the controls for the user
    def createUserActions(self, parentWidget):

        # Generate the widget
        self.userActionsWidget = qtw.QWidget()
        self.userActionsLayout = qtw.QHBoxLayout(self.userActionsWidget)

        # Add the button to open a new file
        self.applyButton = qtw.QPushButton("Apply")
        self.applyButton.clicked.connect(self.applySettings)
        self.applyButton.setStatusTip("Apply the background correction.")
        self.applyButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.applyButton, alignment=qtc.Qt.AlignLeft)

        # Add the button to close
        self.closeButton = qtw.QPushButton("Cancel")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the current window.")
        self.closeButton.setFixedWidth(125)
        self.userActionsLayout.addWidget(self.closeButton, alignment=qtc.Qt.AlignRight)

        # Display the widget
        self.userActionsWidget.setLayout(self.userActionsLayout)
        parentWidget.addWidget(self.userActionsWidget)
