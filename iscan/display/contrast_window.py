import bottleneck as bn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 1.0})

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR CONTRAST CORRECTION
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class contrastSettingsPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(contrastSettingsPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Extract the array and its properties
        currentTab, _ = self.parent.getCurrentTab()
        self.array = currentTab.image.stack.frame.raw

        # Get the distribution
        (
            self.pixelValues,
            self.histogramData,
            self.initialLimits,
        ) = getPixelValueDistribution(self.array)
        self.initialPositions = (
            currentTab.image.stack.min_pv,
            currentTab.image.stack.max_pv,
        )
        self.autoContrastAttempt = 0

        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Contrast Correction")

        # Populate the panel
        self.createHistogramDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createLimitControl(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createContrastActions(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.initialiseHistogram()
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event):
        event.accept()
        self.parent.subWindows['contrast'] = None

    # --------------------------------------------------------------
    # Generate the pixel value histogram for the contrast adjustment
    def createHistogramDisplay(self, parentWidget):

        # Generate the widget
        self.histogramDisplayWidget = qtw.QWidget()
        self.histogramDisplayLayout = qtw.QVBoxLayout(self.histogramDisplayWidget)

        # Name of the panel
        widgetName = qtw.QLabel("Pixel Values")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.histogramDisplayLayout.addWidget(widgetName)

        # Histogram in a matplotlib figure
        self.histogramFigure = plt.Figure(figsize=(3, 2), dpi=50)
        self.histogramCanvas = FigureCanvas(self.histogramFigure)
        self.histogramCanvas.setStatusTip(
            "Distribution of the pixel values of the image."
        )
        self.histogramDisplayLayout.addWidget(self.histogramCanvas)

        # Display the widget
        self.histogramDisplayWidget.setLayout(self.histogramDisplayLayout)
        parentWidget.addWidget(self.histogramDisplayWidget)

    # ---------------------------------------------
    # Generate the control for the intensity limits
    def createLimitControl(self, parentWidget):

        # Generate the widget
        self.limitControlWidget = qtw.QWidget()
        self.limitControlLayout = qtw.QVBoxLayout(self.limitControlWidget)

        # Name of the panel
        widgetName = qtw.QLabel("Intensity Limits")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.limitControlLayout.addWidget(widgetName)

        # Sliders
        self.minIntensitySlider = QLogSlider(
            qtc.Qt.Horizontal,
            position=self.initialPositions[0],
            min=self.initialLimits[0],
            max=self.initialLimits[1],
        )
        self.minIntensitySlider.valueChanged.connect(self.changeMinimum)
        self.minIntensitySlider.setStatusTip(
            "Modify the minimal pixel value displayed to rescale the image contrast."
        )
        self.limitControlLayout.addWidget(self.minIntensitySlider)

        self.maxIntensitySlider = QLogSlider(
            qtc.Qt.Horizontal,
            position=self.initialPositions[1],
            min=self.initialLimits[0],
            max=self.initialLimits[1],
        )
        self.maxIntensitySlider.valueChanged.connect(self.changeMaximum)
        self.maxIntensitySlider.setStatusTip(
            "Modify the maximal pixel value displayed to rescale the image contrast."
        )
        self.limitControlLayout.addWidget(self.maxIntensitySlider)

        # Display the widget
        self.limitControlWidget.setLayout(self.limitControlLayout)
        parentWidget.addWidget(self.limitControlWidget)

    # --------------------------------------
    # Generate the control of the image zoom
    def createContrastActions(self, parentWidget):

        # Generate the widget
        self.contrastActionsWidget = qtw.QWidget()
        self.contrastActionsLayout = qtw.QGridLayout(self.contrastActionsWidget)

        # Auto contrast and histogram crop
        currentRow = 0
        self.autoContrastButton = qtw.QPushButton("Auto")
        self.autoContrastButton.clicked.connect(self.autoContrast)
        self.autoContrastButton.setStatusTip(
            "Estimate automatically the optimal contrast. Press multiple times to test different auto contrast settings."
        )
        self.cropHistogramButton = qtw.QPushButton("Crop")
        self.cropHistogramButton.clicked.connect(self.cropHistogram)
        self.cropHistogramButton.setStatusTip(
            "Crop the histogram display based on the actual intensity limits."
        )
        self.contrastActionsLayout.addWidget(self.autoContrastButton, currentRow, 0)
        self.contrastActionsLayout.addWidget(self.cropHistogramButton, currentRow, 1)

        # Auto contrast and histogram crop
        currentRow += 1
        self.resetHistogramButton = qtw.QPushButton("Reset")
        self.resetHistogramButton.clicked.connect(self.resetHistogram)
        self.resetHistogramButton.setStatusTip(
            "Reset the contrast and histogram display to their initial values."
        )
        self.closeWindowButton = qtw.QPushButton("Close")
        self.closeWindowButton.clicked.connect(self.close)
        self.closeWindowButton.setStatusTip("Close the current sub-window.")
        self.contrastActionsLayout.addWidget(self.resetHistogramButton, currentRow, 0)
        self.contrastActionsLayout.addWidget(self.closeWindowButton, currentRow, 1)

        # Display the widget
        self.contrastActionsWidget.setLayout(self.contrastActionsLayout)
        parentWidget.addWidget(self.contrastActionsWidget)

    ##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    ## GRAPHIC DISPLAY AND CONTROL
    ##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

    # ------------------------------------------
    # Generate the graph when the window is open
    def initialiseHistogram(self):

        # Create the figure axis
        self.histogramAxis = self.histogramFigure.add_subplot(111)
        self.histogramAxis.clear()

        # Set up the figure and axis
        self.histogramFigure.subplots_adjust(0, 0, 1, 1)

        self.histogramAxis.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        self.histogramAxis.tick_params(
            axis="y", which="both", left=False, right=False, labelleft=False
        )

        # Save default values
        self.currentLimits = self.initialLimits
        self.initialHistogramData = np.copy(self.histogramData)

        # Plot the histogram
        self.plotHistogram()

    # --------------------
    # Update the histogram
    def plotHistogram(self, limits=None):

        # Get the limits of the histogram
        if limits is None:
            limits = self.initialPositions

        # Plot the distribution
        self.histogramAxis.clear()

        self.histogramAxis.fill_between(
            self.histogramData[1], 0, self.histogramData[0], color="b"
        )
        self.histogramAxis.axvline(x=limits[0], color="r")
        self.histogramAxis.axvline(x=limits[1], color="r")
        self.histogramAxis.set_xlim(self.currentLimits)
        self.histogramAxis.set_yscale("log")
        self.histogramAxis.set_xscale("log")

        # Refresh the canvas
        self.histogramCanvas.draw()

        # Update the image
        currentTab, _ = self.parent.getCurrentTab()
        currentTab.image.stack.min_pv = limits[0]
        currentTab.image.stack.max_pv = limits[1]
        currentTab.image.updateArrays()

    ##-\-\-\-\-\-\-\-\-\-\-\-\
    ## CONTROLS CONFIGURATIONS
    ##-/-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------
    # Update the limits of the intensity for display
    def changeLimits(self):

        # Retrieve the values
        minValue = self.minIntensitySlider.realValue()
        maxValue = self.maxIntensitySlider.realValue()

        self.plotHistogram(limits=[minValue, maxValue])

    def changeMinimum(self):

        # Prevent overlap
        minValue = self.minIntensitySlider.value()
        maxValue = self.maxIntensitySlider.value()
        if minValue >= maxValue:
            self.minIntensitySlider.setValue(maxValue - 1)

        # Change the limits
        self.changeLimits()

    def changeMaximum(self):

        # Prevent overlap
        minValue = self.minIntensitySlider.value()
        maxValue = self.maxIntensitySlider.value()
        if maxValue <= minValue:
            self.maxIntensitySlider.setValue(minValue + 1)

        # Change the limits
        self.changeLimits()

    # --------------------------------
    # Guess the contrast automatically
    def autoContrast(self):

        # Calculate the pixel mean value and standard deviation
        logPValues = np.log10(np.copy(self.pixelValues))
        mean = bn.nanmean(logPValues)
        stdev = bn.nanstd(logPValues)

        # Determine the limits based on the mean and standard deviation
        currentAttempt = self.autoContrastAttempt + 1
        if currentAttempt < 5:

            # Calculate the factor for the standard deviation
            factorList = [0, 3, 2, 1, 0.5]
            factor = factorList[currentAttempt]

            # Calculate the limits
            limits = [10 ** (mean - factor * stdev), 10 ** (mean + factor * stdev)]

        # Cover the whole histogram
        elif currentAttempt == 5:
            limits = self.initialLimits

        # Reset to the initial values
        else:
            limits = self.initialPositions
            currentAttempt = 0
        self.autoContrastAttempt = currentAttempt

        # Update the graph and image
        self.plotHistogram(limits=limits)

    # --------------------------
    # Crop the histogram display
    def cropHistogram(self):

        # Crop to the size fixed by the sliders
        self.currentLimits = [
            self.minIntensitySlider.realValue(),
            self.maxIntensitySlider.realValue(),
        ]
        self.plotHistogram()

    # ---------------
    # Reset histogram
    def resetHistogram(self):

        # Crop back to the original size
        self.currentLimits = self.initialLimits

        # Update the graph and image to the initial values
        self.plotHistogram(limits=self.initialPositions)

##-\-\-\-\-\-\-\-\-\
## LOG SCALE SLIDERS
##-/-/-/-/-/-/-/-/-/


class QLogSlider(qtw.QSlider):
    def __init__(self, form, position=1, min=1, max=100, factor=1000):
        super(QLogSlider, self).__init__(form)

        # Set the limits
        self.logPosition = np.log10(position)
        self.logMin = np.log10(min)
        self.logMax = np.log10(max)

        # Optimise the factor for 1000 values
        isScaled = False
        while isScaled == False:
            self.scaledLogMin, self.scaledLogMax = (
                self.logMin * factor,
                self.logMax * factor,
            )
            steps = self.scaledLogMax - self.scaledLogMin
            if steps > 5000:
                factor /= 10
            elif steps < 500:
                factor *= 10
            else:
                isScaled = True
                self.factor = factor
        self.scaledLogPosition = self.logPosition * factor

        # Set the limits of the scale
        self.initialLimits = (self.scaledLogMin, self.scaledLogMax)
        self.initialPosition = self.scaledLogPosition
        self.setMinimum(self.scaledLogMin)
        self.setMaximum(self.scaledLogMax)
        self.setValue(self.scaledLogPosition)

    # ------------------
    # Return the values
    def logValue(self):
        return self.value() / self.factor

    def realValue(self):
        return 10 ** (self.value() / self.factor)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.operations.image_calculation import getPixelValueDistribution
