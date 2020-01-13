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

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## WINDOW FOR STATISTICS ON PROFILES
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class profilesAnalysisPanel(qtw.QMainWindow):
    def __init__(self, parent):
        super(profilesAnalysisPanel, self).__init__(parent)

        # Initialise the subwindow
        self.parent = parent

        # Retrieve the current tab being displayed
        currentTab, _ = self.parent.getCurrentTab()
        saved_profiles = currentTab.image.profile_saved

        # Extract the data
        self.extractData(saved_profiles)

        # Generate the window
        self.mainWidget = qtw.QWidget()
        self.widgetLayout = qtw.QVBoxLayout(self.mainWidget)
        self.setWindowTitle("Profile Statistics")

        # Populate the panel
        self.createStatsDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createSelectionDisplay(self.widgetLayout)
        self.widgetLayout.addWidget(self.parent.Hseparator())
        self.createActionButtons(self.widgetLayout)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setCentralWidget(self.mainWidget)
        self.plotAnalysis()
        self.show()
        self.setFixedSize(self.size())

    # --------------------------------------------------
    # Reinitialise the display when the window is closed
    def closeEvent(self, event = None):
        event.accept()
        self.parent.subWindows['statistics'] = None

    # --------------------------------------------
    # Generate the statistics histogram and values
    def createStatsDisplay(self, parentWidget):

        # Generate the widget
        self.statsDisplayWidget = qtw.QWidget()
        self.statsDisplayLayout = qtw.QGridLayout(self.statsDisplayWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Statistics")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.statsDisplayLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Histogram in a matplotlib figure
        currentRow += 1
        self.statsFigure = plt.Figure(figsize=(3, 2), dpi=50)
        self.statsCanvas = FigureCanvas(self.statsFigure)
        self.statsCanvas.setStatusTip("Distribution of the given parameter.")

        # Initialise the graph
        self.statsAxis = self.statsFigure.add_subplot(111)
        self.statsAxis.clear()
        self.statsFigure.subplots_adjust(0, 0, 1, 1)
        self.statsAxis.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        self.statsAxis.tick_params(
            axis="y", which="both", left=False, right=False, labelleft=False
        )

        self.statsDisplayLayout.addWidget(self.statsCanvas, currentRow, 0, 1, -1)

        # Statistics - Mean value
        currentRow += 1
        self.statsDisplayLayout.addWidget(qtw.QLabel("Mean"), currentRow, 0)
        self.meanOutput = qtw.QLineEdit()
        self.meanOutput.setEnabled(False)
        self.meanOutput.setStatusTip("Mean value of the selected parameter.")
        self.statsDisplayLayout.addWidget(self.meanOutput, currentRow, 1)

        # Statistics - St. Dev.
        currentRow += 1
        self.statsDisplayLayout.addWidget(qtw.QLabel("St. Dev."), currentRow, 0)
        self.stdOutput = qtw.QLineEdit()
        self.stdOutput.setEnabled(False)
        self.stdOutput.setStatusTip("Standard deviation of the selected parameter.")
        self.statsDisplayLayout.addWidget(self.stdOutput, currentRow, 1)

        # Statistics - Spearman's Rho
        currentRow += 1
        self.statsDisplayLayout.addWidget(qtw.QLabel("Spearman's rho"), currentRow, 0)
        self.spearmanROutput = qtw.QLineEdit()
        self.spearmanROutput.setEnabled(False)
        self.spearmanROutput.setStatusTip("Linear correlation estimator.")
        self.statsDisplayLayout.addWidget(self.spearmanROutput, currentRow, 1)

        # Display the widget
        self.statsDisplayWidget.setLayout(self.statsDisplayLayout)
        parentWidget.addWidget(self.statsDisplayWidget)

    # -----------------------------------------------
    # Generate selection of the parameters to analyse
    def createSelectionDisplay(self, parentWidget):

        # Generate the widget
        self.parameterSelectionWidget = qtw.QWidget()
        self.parameterSelectionLayout = qtw.QGridLayout(self.parameterSelectionWidget)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Parameter(s) Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.parameterSelectionLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Parameter selection
        currentRow += 1
        self.contrastSelection = qtw.QCheckBox("Contrast")
        self.contrastSelection.setChecked(True)
        self.contrastSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.contrastSelection)
        )
        self.contrastSelection.setStatusTip("Analyse the contrasts.")
        self.amplitudeSelection = qtw.QCheckBox("Amplitude")
        self.amplitudeSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.amplitudeSelection)
        )
        self.amplitudeSelection.setStatusTip("Analyse the fit amplitudes.")
        self.parameterSelectionLayout.addWidget(self.contrastSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.amplitudeSelection, currentRow, 1)

        currentRow += 1
        self.noiseSelection = qtw.QCheckBox("Noise")
        self.noiseSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.noiseSelection)
        )
        self.noiseSelection.setStatusTip("Analyse the noises.")
        self.centerSelection = qtw.QCheckBox("Center")
        self.centerSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.centerSelection)
        )
        self.centerSelection.setStatusTip("Analyse the centers.")
        self.parameterSelectionLayout.addWidget(self.noiseSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.centerSelection, currentRow, 1)

        currentRow += 1
        self.snrSelection = qtw.QCheckBox("SNR")
        self.snrSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.snrSelection)
        )
        self.snrSelection.setStatusTip("Analyse the signal-to-noise ratios.")
        self.widthSelection = qtw.QCheckBox("Width")
        self.widthSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.widthSelection)
        )
        self.widthSelection.setStatusTip("Analyse the widths.")
        self.parameterSelectionLayout.addWidget(self.snrSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.widthSelection, currentRow, 1)

        currentRow += 1
        self.frameSelection = qtw.QCheckBox("Frame")
        self.frameSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.frameSelection)
        )
        self.frameSelection.setStatusTip("Analyse the frame numbers.")
        self.offsetSelection = qtw.QCheckBox("Offset")
        self.offsetSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.offsetSelection)
        )
        self.offsetSelection.setStatusTip("Analyse the offsets.")
        self.parameterSelectionLayout.addWidget(self.frameSelection, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.offsetSelection, currentRow, 1)

        currentRow += 1
        self.positionSelection = qtw.QCheckBox("Distance from a reference point (X,Y)")
        self.positionSelection.toggled.connect(
            lambda: self.updateCheckBoxes(self.positionSelection)
        )
        self.positionSelection.setStatusTip(
            "Analyse the distance to a reference point."
        )
        self.parameterSelectionLayout.addWidget(
            self.positionSelection, currentRow, 0, 1, -1
        )

        # Center input
        currentRow += 1

        # Get the image size
        currentTab, _ = self.parent.getCurrentTab()
        imageSize = currentTab.image.stack.size

        tabIndex = self.parent.centralWidget.currentIndex()
        self.xCenterInput = qtw.QLineEdit()
        self.xCenterInput.setText(
            str(imageSize[0] / 2)
        )
        self.xCenterInput.setStatusTip("X coordinates of the reference point.")
        self.yCenterInput = qtw.QLineEdit()
        self.yCenterInput.setText(
            str(imageSize[1] / 2)
        )
        self.yCenterInput.setStatusTip("Y coordinates of the reference point.")
        self.parameterSelectionLayout.addWidget(self.xCenterInput, currentRow, 0)
        self.parameterSelectionLayout.addWidget(self.yCenterInput, currentRow, 1)

        currentRow += 1
        self.errorSelection = qtw.QCheckBox("Compare the errors on the parameters")
        self.errorSelection.toggled.connect(self.plotAnalysis)
        self.errorSelection.setStatusTip(
            "Use the errors instead of the values when available."
        )
        self.parameterSelectionLayout.addWidget(
            self.errorSelection, currentRow, 0, 1, -1
        )

        # Display the widget
        self.parameterSelectionWidget.setLayout(self.parameterSelectionLayout)
        parentWidget.addWidget(self.parameterSelectionWidget)

    # ------------------------------------------------
    # Generate selection of the parameters to analyse
    def createActionButtons(self, parentWidget):

        # Generate the widget
        self.buttonWidget = qtw.QWidget()
        self.buttonLayout = qtw.QGridLayout(self.buttonWidget)

        # Buttons
        currentRow = 0
        self.saveButton = qtw.QPushButton("Save")
        self.saveButton.clicked.connect(self.saveData)
        self.saveButton.setStatusTip("Save the result(s) of the analysis.")
        self.buttonLayout.addWidget(self.saveButton, currentRow, 0)

        self.closeButton = qtw.QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setStatusTip("Close the window.")
        self.buttonLayout.addWidget(self.closeButton, currentRow, 1)

        # Save all options
        currentRow += 1
        self.saveAllSelection = qtw.QCheckBox("Save all statistics")
        self.saveAllSelection.setStatusTip("Save all possible statistics.")
        self.buttonLayout.addWidget(self.saveAllSelection, currentRow, 0, 1, -1)

        # Display the widget
        self.buttonWidget.setLayout(self.buttonLayout)
        parentWidget.addWidget(self.buttonWidget)

    ##-\-\-\-\-\-\-\-\
    ## PLOT THE RESULTS
    ##-/-/-/-/-/-/-/-/

    # --------------------------------------
    # Plot the selected statistical analysis
    def plotDistribution(self, valueName):

        # Get the data
        if valueName != "distance":
            currentValue = self.data_dict[valueName]
        else:
            currentValue = self.getDistance()

        # Update the graph
        self.statsAxis.clear()
        sns.distplot(currentValue, ax=self.statsAxis)
        self.statsCanvas.draw()

        # Edit the entries
        self.meanOutput.setText(str(round(bn.nanmean(currentValue), 3)))
        self.stdOutput.setText(str(round(bn.nanstd(currentValue, ddof=1), 3)))
        self.spearmanROutput.setText("---")

    def plotCorrelation(self, valueNames):

        # Get the data
        if valueNames[0] != "distance":
            currentY = self.data_dict[valueNames[0]]
        else:
            currentY = self.getDistance()

        if valueNames[1] != "distance":
            currentX = self.data_dict[valueNames[1]]
        else:
            currentX = self.getDistance()

        # Update the graph
        self.statsAxis.clear()
        sns.regplot(x=currentX, y=currentY, ax=self.statsAxis)
        self.statsCanvas.draw()

        # Edit the entries
        self.meanOutput.setText("---")
        self.stdOutput.setText("---")
        self.spearmanROutput.setText(
            str(round(np.corrcoef(currentX, currentY, ddof=1)[0, 1], 3))
        )

    def plotAnalysis(self):

        # Check the selected checkbox
        rawSelection = self.getBoxChecked()

        # Check if errors exist for the given values
        currentSelection = []
        if self.errorSelection.isChecked():
            for element in rawSelection:
                if element + "Err" in list(self.data_dict.keys()):
                    currentSelection.append(element + "Err")
                else:
                    currentSelection.append(element)
        else:
            currentSelection = rawSelection

        # Update the displayed informations
        if len(currentSelection) == 1:
            self.plotDistribution(currentSelection[0])
        else:
            self.plotCorrelation(currentSelection)

    ##-\-\-\-\-\-\-\-\-\-\
    ## CHECKBOX MANAGEMENT
    ##-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------------------------------
    # Update the checkbox selection depending on the current selection
    def updateCheckBoxes(self, checkbox):

        # Check the number of box currently checked
        numberSelection = len(self.getBoxChecked())
        if numberSelection > 2:
            checkbox.setChecked(False)
        elif numberSelection < 1:
            checkbox.setChecked(True)

        # Refresh the plot if everything is alright
        else:
            self.plotAnalysis()

    # --------------------------------------------
    # Return the list of the box currently checked
    def getBoxChecked(self):

        nameList = np.array(self.keys)
        checkBoxState = np.array(
            [
                self.contrastSelection.isChecked(),
                self.noiseSelection.isChecked(),
                self.snrSelection.isChecked(),
                self.amplitudeSelection.isChecked(),
                self.centerSelection.isChecked(),
                self.widthSelection.isChecked(),
                self.offsetSelection.isChecked(),
                self.frameSelection.isChecked(),
                self.positionSelection.isChecked(),
            ]
        )
        currentSelection = nameList[checkBoxState == True]

        return currentSelection

    ##-\-\-\-\-\-\-\
    ## DATA HANDLING
    ##-/-/-/-/-/-/-/

    # ---------------------------------------------------
    # Extract the data and convert them into a dictionary
    def extractData(self, allData):

        # Store the data
        self.profiles = allData
        self.data_array = np.array([data.getTableValues() for data in allData])

        self.keys = [
            "contrast",
            "noise",
            "snr",
            "amplitude",
            "center",
            "width",
            "offset",
            "frame",
            "distance",
        ]

        # Extract the data from each profiles
        self.data_dict = {
            "frame": np.array([data.frame for data in allData]).astype(float),
            "contrast": np.array([data.contrast['value'] for data in allData]).astype(float),
            "contrastErr": np.array([data.contrast['error'] for data in allData]).astype(float),
            "noise": np.array([data.noise['value'] for data in allData]).astype(float),
            "noiseErr": np.array([data.noise['error'] for data in allData]).astype(float),
            "snr": np.array([data.snr['value'] for data in allData]).astype(float),
            "snrErr": np.array([data.snr['error'] for data in allData]).astype(float),
            "x": np.array([data.position[0] for data in allData]).astype(float),
            "y": np.array([data.position[1] for data in allData]).astype(float),
            "amplitude": np.array([data.amplitude['value'] for data in allData]).astype(float),
            "amplitudeErr": np.array([data.amplitude['error'] for data in allData]).astype(float),
            "center": np.array([data.center['value'] for data in allData]).astype(float),
            "centerErr": np.array([data.center['error'] for data in allData]).astype(float),
            "width": np.array([data.width['value'] for data in allData]).astype(float),
            "widthErr": np.array([data.width['error'] for data in allData]).astype(float),
            "offset": np.array([data.offset['value'] for data in allData]).astype(float),
            "offsetErr": np.array([data.offset['error'] for data in allData]).astype(float)
        }

    # ---------------------
    # Compute the distance
    def getDistance(self):

        # Extract the position of the reference point
        xRef = float(self.xCenterInput.text())
        yRef = float(self.yCenterInput.text())

        # Calculate the distance
        xValues = self.data_dict["x"]
        yValues = self.data_dict["y"]
        distances = np.sqrt((xValues - xRef) ** 2 + (yValues - yRef) ** 2)

        return distances

    # ----------------------------------------
    # Save the current distribution in a file
    def saveCurrentDistribution(self, valueName):

        # Get the data
        if valueName != "distance":
            currentValue = self.data_dict[valueName]
        else:
            currentValue = self.getDistance()

        saveStats(self.parent, currentValue, valueName, 1)

    # ----------------------------------------------
    # Save the current linear correlation in a file
    def saveCurrentCorrelation(self, valueNames):

        # Get the data
        if valueNames[0] != "distance":
            currentY = self.data_dict[valueNames[0]]
        else:
            currentY = self.getDistance()

        if valueNames[1] != "distance":
            currentX = self.data_dict[valueNames[1]]
        else:
            currentX = self.getDistance()
        parameterNames = valueNames[1] + "," + valueNames[0]
        currentValue = np.array([currentX, currentY])

        saveStats(self.parent, currentValue, parameterNames, 2)

    # --------------------------------------------
    # Save all the possible stats on the profiles
    def saveAllStats(self):

        # Prepare the distance
        dictToSave = self.data_dict
        dictToSave["distance"] = self.getDistance()

        # Remove the unwanted parameters
        del dictToSave["x"]
        del dictToSave["y"]

        # Save the file
        allStats(self.parent, dictToSave)

    # -----------------------
    # Select the type of save
    def saveData(self):

        # Save all the data possible
        if self.saveAllSelection.isChecked():
            self.saveAllStats()

        # Save the displayed distribution or linear correlation
        else:

            # Check the selected checkbox
            rawSelection = self.getBoxChecked()

            # Check if errors exist for the given values
            currentSelection = []
            if self.errorSelection.isChecked():
                for element in rawSelection:
                    if element + "Err" in list(self.data_dict.keys()):
                        currentSelection.append(element + "Err")
                    else:
                        currentSelection.append(element)
            else:
                currentSelection = rawSelection

            # Update the displayed informations
            if len(currentSelection) == 1:
                self.saveCurrentDistribution(currentSelection[0])
            else:
                self.saveCurrentCorrelation(currentSelection)

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import errorMessage
from iscan.operations.intensity_profiling import saveStats, allStats
