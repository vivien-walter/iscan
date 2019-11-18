import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns

sns.set(style="darkgrid")
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 1.0})

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from PIL import Image, ImageQt

import iscan.image_handling as img
from iscan.input_output import saveTable
import iscan.math_functions as mfunc
from iscan.saved_data import iScatSignal

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## SIDE BAR FOR PARTICLE TRACKING
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/


class profilingControlPanel(qtw.QDockWidget):
    def __init__(self, name, parent):
        super(profilingControlPanel, self).__init__(name, parent)

        # Generate the display
        self.parent = parent
        self.mainWidget = qtw.QWidget()
        self.mainWidget.setMinimumWidth(550)
        self.widgetLayout = qtw.QHBoxLayout(self.mainWidget)
        self.widgetLayout.setContentsMargins(0, 0, 0, 0)

        # ------------------------
        # Populate the left panel
        self.leftPanelWidget = qtw.QWidget()
        self.leftPanelLayout = qtw.QVBoxLayout(self.leftPanelWidget)
        # self.leftPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.createSelectionSnapshot(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createProfileDisplay(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createLineSettings(self.leftPanelLayout)
        self.leftPanelLayout.addWidget(self.parent.Hseparator())
        self.createFitFunctions(self.leftPanelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget = qtw.QWidget()
        emptyWidget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.leftPanelLayout.addWidget(emptyWidget)

        self.leftPanelWidget.setLayout(self.leftPanelLayout)
        self.widgetLayout.addWidget(self.leftPanelWidget)

        self.widgetLayout.addWidget(self.parent.Vseparator())

        # -------------------------
        # Populate the right panel
        self.rightPanelWidget = qtw.QWidget()
        self.rightPanelLayout = qtw.QVBoxLayout(self.rightPanelWidget)
        # self.rightPanelLayout.setContentsMargins(0, 0, 0, 0)

        self.createParametersInput(self.rightPanelLayout)
        self.rightPanelLayout.addWidget(self.parent.Hseparator())
        self.createFitResults(self.rightPanelLayout)
        self.rightPanelLayout.addWidget(self.parent.Hseparator())
        self.createResultsTable(self.rightPanelLayout)

        # Fill the bottom of the panel with blank
        emptyWidget2 = qtw.QWidget()
        emptyWidget2.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        self.rightPanelLayout.addWidget(emptyWidget2)

        self.rightPanelWidget.setLayout(self.rightPanelLayout)
        self.widgetLayout.addWidget(self.rightPanelWidget)

        # Display the panel
        self.mainWidget.setLayout(self.widgetLayout)
        self.setWidget(self.mainWidget)
        self.setFloating(False)

    # ----------------------------------------------
    # Generate the display of the current selection
    def createSelectionSnapshot(self, parentWidget):

        # Generate the widget
        self.selectionSnapshotWidget = qtw.QWidget()
        self.selectionSnapshotLayout = qtw.QVBoxLayout(self.selectionSnapshotWidget)
        self.selectionSnapshotLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Current Selection")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.selectionSnapshotLayout.addWidget(widgetName)

        # Create the display
        self.captionCanvas = qtw.QLabel(self.selectionSnapshotWidget)
        self.captionCanvas.setAlignment(qtc.Qt.AlignCenter)
        self.selectionSnapshotLayout.addWidget(self.captionCanvas)

        # Create the position display
        self.currentPositionDisplay = qtw.QLineEdit()
        self.currentPositionDisplay.setEnabled(False)
        self.currentPositionDisplay.setStatusTip(
            "Current position used for the center of the profile."
        )
        self.selectionSnapshotLayout.addWidget(self.currentPositionDisplay)

        # Display the widget
        self.selectionSnapshotWidget.setLayout(self.selectionSnapshotLayout)
        parentWidget.addWidget(self.selectionSnapshotWidget)

    # ------------------------------------
    # Generate the display of the profile
    def createProfileDisplay(self, parentWidget):

        # Generate the widget
        self.profileDisplayWidget = qtw.QWidget()
        self.profileDisplayLayout = qtw.QVBoxLayout(self.profileDisplayWidget)
        self.profileDisplayLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Intensity Profile")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.profileDisplayLayout.addWidget(widgetName)

        # Histogram in a matplotlib figure
        self.profileFigure = plt.Figure(figsize=(3, 2), dpi=50)
        self.profileCanvas = FigureCanvas(self.profileFigure)

        # Set up the figure and axis
        self.profileAxis = self.profileFigure.add_subplot(111)
        self.profileAxis.clear()
        self.profileFigure.subplots_adjust(0, 0, 1, 1)
        self.profileAxis.tick_params(
            axis="x", which="both", bottom=False, top=False, labelbottom=False
        )
        self.profileAxis.tick_params(
            axis="y", which="both", left=False, right=False, labelleft=False
        )

        self.profileCanvas.setStatusTip(
            "Intensity profile at the given location, angle and length."
        )
        self.profileDisplayLayout.addWidget(self.profileCanvas)

        # Checkbox for the pre-fit display
        self.prefitDisplayCheckBox = qtw.QCheckBox("Show pre-fit")
        self.prefitDisplayCheckBox.setChecked(True)
        self.prefitDisplayCheckBox.toggled.connect(self.plotProfile)
        self.prefitDisplayCheckBox.setStatusTip(
            "Display the pre-fitted function based on the given initial fit parameters."
        )
        self.profileDisplayLayout.addWidget(self.prefitDisplayCheckBox)

        # Display the widget
        self.profileDisplayWidget.setLayout(self.profileDisplayLayout)
        parentWidget.addWidget(self.profileDisplayWidget)

    # ------------------------------------------
    # Generate the controls of the profile line
    def createLineSettings(self, parentWidget):

        # Generate the widget
        self.lineSettingsWidget = qtw.QWidget()
        self.lineSettingsLayout = qtw.QVBoxLayout(self.lineSettingsWidget)
        self.lineSettingsLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Line Settings")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.lineSettingsLayout.addWidget(widgetName)

        # Sliders
        self.angleSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.angleSlider.setMinimum(-89.9)  # Set to -89.9 and 89.9 to avoid crashes
        self.angleSlider.setMaximum(89.9)
        self.angleSlider.setValue(0)
        self.angleSlider.valueChanged.connect(self.generateProfileLine)
        self.angleSlider.setStatusTip(
            "Modify the angle of the profile line on the image."
        )
        self.lineSettingsLayout.addWidget(qtw.QLabel("Angle"))
        self.lineSettingsLayout.addWidget(self.angleSlider)

        self.lengthSlider = qtw.QSlider(qtc.Qt.Horizontal)
        self.lengthSlider.setMinimum(60)  # All the following values are arbitrary
        self.lengthSlider.setMaximum(1200)
        self.lengthSlider.setValue(200)
        self.lengthSlider.valueChanged.connect(self.generateProfileLine)
        self.lengthSlider.setStatusTip(
            "Modify the length of the profile line on the image."
        )
        self.lineSettingsLayout.addWidget(qtw.QLabel("Length"))
        self.lineSettingsLayout.addWidget(self.lengthSlider)

        # Display the widget
        self.lineSettingsWidget.setLayout(self.lineSettingsLayout)
        parentWidget.addWidget(self.lineSettingsWidget)

    # -------------------------------------------
    # Generate the selection of the fit function
    def createFitFunctions(self, parentWidget):

        # Generate the widget
        self.fitFunctionWidget = qtw.QWidget()
        self.fitFunctionLayout = qtw.QGridLayout(self.fitFunctionWidget)
        self.fitFunctionLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        currentRow = 0
        widgetName = qtw.QLabel("Fit Process")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.fitFunctionLayout.addWidget(widgetName, currentRow, 0, 1, -1)

        # Fit function selection
        currentRow += 1
        self.functionGroupButton = qtw.QButtonGroup(self.fitFunctionWidget)

        self.sincFunctionRadiobutton = qtw.QRadioButton("Sinc")
        self.sincFunctionRadiobutton.setChecked(True)
        self.sincFunctionRadiobutton.toggled.connect(self.fitProfile)
        self.sincFunctionRadiobutton.setStatusTip(
            "Select the sine cardinal function for profile fitting."
        )
        self.gaussFunctionRadiobutton = qtw.QRadioButton("Gauss")
        self.gaussFunctionRadiobutton.toggled.connect(self.fitProfile)
        self.gaussFunctionRadiobutton.setStatusTip(
            "Select the gaussian function for profile fitting."
        )
        self.functionGroupButton.addButton(self.sincFunctionRadiobutton)
        self.fitFunctionLayout.addWidget(self.sincFunctionRadiobutton, currentRow, 0)
        self.functionGroupButton.addButton(self.gaussFunctionRadiobutton)
        self.fitFunctionLayout.addWidget(self.gaussFunctionRadiobutton, currentRow, 1)

        # Button to start the fit
        currentRow += 1

        self.makeFitButton = qtw.QPushButton("FIT")
        self.makeFitButton.clicked.connect(self.fitProfile)
        self.makeFitButton.setStatusTip("Fit the profile with the current settings.")
        self.fitFunctionLayout.addWidget(self.makeFitButton, currentRow, 0, 1, -1)

        # Button to store the results of the fit
        currentRow += 1

        self.storeFitButton = qtw.QPushButton("Store results")
        self.storeFitButton.clicked.connect(self.storeProfile)
        self.storeFitButton.setStatusTip(
            "Store the result of the fit in the table to save it later."
        )
        self.fitFunctionLayout.addWidget(self.storeFitButton, currentRow, 0, 1, -1)

        # Display the widget
        self.fitFunctionWidget.setLayout(self.fitFunctionLayout)
        parentWidget.addWidget(self.fitFunctionWidget)

    # ------------------------------------------------------------
    # Generate the manual input and display of the fit parameters
    def createParametersInput(self, parentWidget):

        # Generate the widget
        self.fitParametersWidget = qtw.QWidget()
        self.fitParametersLayout = qtw.QFormLayout(self.fitParametersWidget)
        self.fitParametersLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Fit Parameters")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.fitParametersLayout.addRow(widgetName, qtw.QWidget())

        self.amplitudeEntry = qtw.QLineEdit()
        self.amplitudeEntry.returnPressed.connect(self.plotProfile)
        self.amplitudeEntry.setStatusTip("Input for the amplitude of the profile.")
        self.amplitudeOutput = qtw.QLineEdit()
        self.amplitudeOutput.setEnabled(False)
        self.amplitudeOutput.setStatusTip("Output for the amplitude of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Amplitude"), self.amplitudeEntry)
        self.fitParametersLayout.addRow("", self.amplitudeOutput)

        self.centerEntry = qtw.QLineEdit()
        self.centerEntry.returnPressed.connect(self.plotProfile)
        self.centerEntry.setStatusTip("Input for the center of the profile.")
        self.centerOutput = qtw.QLineEdit()
        self.centerOutput.setEnabled(False)
        self.centerOutput.setStatusTip("Output for the center of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Center"), self.centerEntry)
        self.fitParametersLayout.addRow("", self.centerOutput)

        self.widthEntry = qtw.QLineEdit()
        self.widthEntry.returnPressed.connect(self.plotProfile)
        self.widthEntry.setStatusTip("Input for the width of the profile.")
        self.widthOutput = qtw.QLineEdit()
        self.widthOutput.setEnabled(False)
        self.widthOutput.setStatusTip("Output for the width of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Width"), self.widthEntry)
        self.fitParametersLayout.addRow("", self.widthOutput)

        self.offsetEntry = qtw.QLineEdit()
        self.offsetEntry.returnPressed.connect(self.plotProfile)
        self.offsetEntry.setStatusTip("Input for the offset of the profile.")
        self.offsetOutput = qtw.QLineEdit()
        self.offsetOutput.setEnabled(False)
        self.offsetOutput.setStatusTip("Output for the offset of the profile.")
        self.fitParametersLayout.addRow(qtw.QLabel("Offset"), self.offsetEntry)
        self.fitParametersLayout.addRow("", self.offsetOutput)

        # Display the widget
        self.fitParametersWidget.setLayout(self.fitParametersLayout)
        parentWidget.addWidget(self.fitParametersWidget)

    # ----------------------------------------------
    # Generate the display of the result of the fit
    def createFitResults(self, parentWidget):

        # Generate the widget
        self.imageValuesWidget = qtw.QWidget()
        self.imageValuesLayout = qtw.QFormLayout(self.imageValuesWidget)
        self.imageValuesLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Image Values")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.imageValuesLayout.addRow(widgetName, qtw.QWidget())

        self.contrastOutput = qtw.QLineEdit()
        self.contrastOutput.setEnabled(False)
        self.contrastOutput.setStatusTip("Contrast of the profile.")
        self.imageValuesLayout.addRow(qtw.QLabel("Contrast (%)"), self.contrastOutput)

        self.noiseOutput = qtw.QLineEdit()
        self.noiseOutput.setEnabled(False)
        self.noiseOutput.setStatusTip("Noise of the profile.")
        self.imageValuesLayout.addRow(qtw.QLabel("Noise (%)"), self.noiseOutput)

        self.snrOutput = qtw.QLineEdit()
        self.snrOutput.setEnabled(False)
        self.snrOutput.setStatusTip("Signal-to-Noise Ratio of the profile.")
        self.imageValuesLayout.addRow(qtw.QLabel("SNR"), self.snrOutput)

        # Display the widget
        self.imageValuesWidget.setLayout(self.imageValuesLayout)
        parentWidget.addWidget(self.imageValuesWidget)

    # ----------------------------------------------
    # Generate the display of the result of the fit
    def createResultsTable(self, parentWidget):

        # Generate the widget
        self.resultsDisplayWidget = qtw.QWidget()
        self.resultsDisplayLayout = qtw.QVBoxLayout(self.resultsDisplayWidget)
        self.resultsDisplayLayout.setContentsMargins(0, 0, 0, 0)

        # Name of the panel
        widgetName = qtw.QLabel("Analysis Results")
        widgetNameFont = qtg.QFont()
        widgetNameFont.setBold(True)
        widgetName.setFont(widgetNameFont)
        self.resultsDisplayLayout.addWidget(widgetName)

        # Table for the results
        self.resultsTable = qtw.QTableWidget(0, 21)
        self.resultsTable.setHorizontalHeaderLabels(
            [
                "Name",
                "Contrast",
                "ContrastErr",
                "Noise",
                "NoiseErr",
                "SNR",
                "SNRErr",
                "Frame",
                "X",
                "Y",
                "Angle",
                "Length",
                "Fit",
                "Amplitude",
                "AErr",
                "Center",
                "CErr",
                "Width",
                "WErr",
                "Offset",
                "OErr",
            ]
        )
        self.resultsTable.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.resultsTable.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)
        self.resultsTable.cellDoubleClicked.connect(self.tableIsDoubleClicked)
        self.resultsDisplayLayout.addWidget(self.resultsTable)

        # Save button
        self.saveButton = qtw.QPushButton("Save Results")
        self.saveButton.clicked.connect(self.saveTableInFile)
        self.saveButton.setStatusTip("Save the table of results in a .csv file.")
        self.resultsDisplayLayout.addWidget(self.saveButton)

        # Display the widget
        self.resultsDisplayWidget.setLayout(self.resultsDisplayLayout)
        parentWidget.addWidget(self.resultsDisplayWidget)

    ##-\-\-\-\-\-\-\-\-\
    ## UPDATE THE PROFILE
    ##-/-/-/-/-/-/-/-/-/

    # ---------------------------------------------
    # Update the profile when the image is clicked
    def updateOnClick(self, position, imageArray):

        # Update the general informations of the profile
        positionText = "(" + str(position[0]) + ";" + str(position[1]) + ")"
        self.currentPositionDisplay.setText(positionText)

        # Update the caption display
        captionArray = img.cropArray(position, imageArray)

        self.captionToDisplay = Image.fromarray(captionArray.astype(np.uint8))
        self.pixmapToDisplay = qtg.QPixmap.fromImage(
            qtg.QImage(ImageQt.ImageQt(self.captionToDisplay))
        )
        self.captionCanvas.setPixmap(self.pixmapToDisplay)

        # Save the profile sources in the class
        self.currentPosition = position
        self.currentArray = imageArray

        self.generateProfileLine(makeFit=True)

    # ------------------------
    # Update the profile line
    def generateProfileLine(self, event=None, makeFit=False):

        # Extract the values
        self.currentAngle = self.angleSlider.value()
        self.currentLength = self.lengthSlider.value()

        # Update the line on the image
        tabIndex = self.parent.centralWidget.currentIndex()
        p1, p2 = self.parent.imageTabsImage[tabIndex].drawNewProfile(
            self.currentPosition, self.currentAngle, self.currentLength
        )

        # Compute the profile and display it
        self.distance, self.profile = self.parent.imageTabsImage[
            tabIndex
        ].extractProfile(p1, p2, self.currentPosition)

        # Fit profiles if required
        if makeFit or self.parent.controlPanel.liveFitCheckBox.isChecked():
            self.initialParameters = mfunc.initialiseParameters(
                self.distance, self.profile, brightSpot=self.parent.controlPanel.brightSpotCheckBox.isChecked()
            )
            self.updateInitialParameters(self.initialParameters)
            self.fitProfile()

        else:
            self.plotProfile()

    # ----------------
    # Fit the profile
    def fitProfile(self):

        # Retrieve the initial parameters to use from the UI
        initialParameters = self.getInitialParameters()

        # Fit the profile using the given fit parameters
        self.fitType = self.returnFitType()
        self.fitParameters, self.fitErrors = mfunc.fitProfile(
            self.distance, self.profile, initialParameters, fitType=self.fitType
        )

        # Update the display
        self.updateFittedParameters(self.fitParameters, self.fitErrors)
        self.calculateContrastNoise()
        self.plotProfile()

        # Enable the store profile button
        if not self.storeFitButton.isEnabled():
            self.generateProfileLine()
            self.storeFitButton.setEnabled(True)

    # -----------------------------------------------------------------------------
    # Plot the intensity profile with the current position, angle and length given
    def plotProfile(self):

        # Reset the display
        self.profileAxis.clear()

        # Calculate the fitted range
        xMin = self.distance[0]
        xMax = self.distance[-1]
        xStep = (xMax - xMin) / 1000
        self.fittedDistance = np.arange(xMin, xMax + xStep, xStep)

        # Plot the profile
        self.profileAxis.plot(self.distance, self.profile, "k-", linewidth=3)

        # Plot the pre-fit plot
        if self.prefitDisplayCheckBox.isChecked():
            self.profileAxis.plot(
                self.fittedDistance,
                mfunc.fittedProfile(
                    self.fittedDistance,
                    self.getInitialParameters(),
                    fitType=self.returnFitType(),
                ),
                "r--",
                linewidth=2,
            )

        # Plot the plot
        self.fittedShortProfile = mfunc.fittedProfile(
            self.distance, self.fitParameters, fitType=self.returnFitType()
        )
        self.fittedProfile = mfunc.fittedProfile(
            self.fittedDistance, self.fitParameters, fitType=self.returnFitType()
        )
        self.profileAxis.plot(
            self.fittedDistance, self.fittedProfile, "b-", linewidth=4
        )

        # Refresh the canvas
        self.profileCanvas.draw()

    ##-\-\-\-\-\-\-\
    ## DATA HANDLING
    ##-/-/-/-/-/-/-/

    # ------------------------------
    # Return the type of fit to use
    def returnFitType(self):

        # Lists
        modes = np.array(["sinc", "gauss"])
        buttonState = np.array(
            [
                self.sincFunctionRadiobutton.isChecked(),
                self.gaussFunctionRadiobutton.isChecked(),
            ]
        )

        # Get the enabled mode
        modeIndex = np.where(buttonState == True)[0]

        return modes[modeIndex[0]]

    # ---------------------------------------------
    # Update the display of the initial parameters
    def updateInitialParameters(self, parameters):

        # Extract the parameters
        amplitude, width, center, offset = parameters

        # Update the display
        self.amplitudeEntry.setText(str(round(amplitude, 3)))
        self.centerEntry.setText(str(round(center, 3)))
        self.widthEntry.setText(str(round(width, 3)))
        self.offsetEntry.setText(str(round(offset, 3)))

    # ---------------------------------------------
    # Update the display of the fitted parameters
    def updateFittedParameters(self, fitParameters, fitErrors):

        # Extract the parameters
        amplitude, width, center, offset = fitParameters
        aErr, wErr, cErr, oErr = fitErrors

        # Update the display
        amplitudeText = str(round(amplitude, 3)) + " ± " + str(round(aErr, 3))
        self.amplitudeOutput.setText(amplitudeText)

        centerText = str(round(center, 3)) + " ± " + str(round(cErr, 3))
        self.centerOutput.setText(centerText)

        widthText = str(round(width, 3)) + " ± " + str(round(oErr, 3))
        self.widthOutput.setText(widthText)

        offsetText = str(round(offset, 3)) + " ± " + str(round(oErr, 3))
        self.offsetOutput.setText(offsetText)

    # -----------------------------------------------
    # Get the initial parameters currently displayed
    def getInitialParameters(self):

        # Update the display
        amplitude = float(self.amplitudeEntry.text())
        center = float(self.centerEntry.text())
        width = float(self.widthEntry.text())
        offset = float(self.offsetEntry.text())

        return [amplitude, width, center, offset]

    # -----------------------------------------------------------------
    # Calculate and display the contrast, noise and SNR of the profile
    def calculateContrastNoise(self):

        # Calculate the values
        signal = self.distance, self.profile
        fittedSignal = (
            self.distance,
            mfunc.fittedProfile(
                self.distance, self.fitParameters, fitType=self.returnFitType()
            ),
        )
        imageValues, imageValuesErr = mfunc.computeSNR(
            signal, fittedSignal, self.fitParameters, self.fitErrors, brightSpot=self.parent.controlPanel.brightSpotCheckBox.isChecked()
        )
        self.currentContrast, self.currentNoise, self.currentSNR = imageValues
        (
            self.currentContrastErr,
            self.currentNoiseErr,
            self.currentSNRErr,
        ) = imageValuesErr

        # Update the display
        contrastText = (
            str(round(self.currentContrast, 3))
            + " ± "
            + str(round(self.currentContrastErr, 3))
        )
        self.contrastOutput.setText(contrastText)
        noiseText = (
            str(round(self.currentNoise, 3))
            + " ± "
            + str(round(self.currentNoiseErr, 3))
        )
        self.noiseOutput.setText(noiseText)
        snrText = (
            str(round(self.currentSNR, 3)) + " ± " + str(round(self.currentSNRErr, 3))
        )
        self.snrOutput.setText(snrText)

    # ----------------------------------------
    # Store the current profile in the memory
    def storeProfile(self):

        # Prepare all the values
        allData = []
        tabIndex = self.parent.centralWidget.currentIndex()
        currentImage = self.parent.imageTabsImage[tabIndex]

        numberStoredData = len(currentImage.savedData)
        dataName = (
            self.parent.imageTabsImage[tabIndex].name + "_" + str(numberStoredData + 1)
        )

        imageValues = [
            round(self.currentContrast, 3),
            round(self.currentContrastErr, 3),
            round(self.currentNoise, 3),
            round(self.currentNoiseErr, 3),
            round(self.currentSNR, 3),
            round(self.currentSNRErr, 3),
        ]

        frameNumber = currentImage.currentFrame

        positionAndSetup = [
            int(self.currentPosition[0]),
            int(self.currentPosition[1]),
            int(self.currentAngle),
            int(self.currentLength),
        ]

        fitType = self.fitType

        fitParams = self.fitParameters
        fitErrors = self.fitErrors

        # Append values to the memory
        signal = self.distance, self.profile
        fittedSignal = self.distance, self.fittedShortProfile
        currentImage.savedData.append(
            iScatSignal(
                dataName,
                imageValues,
                frameNumber,
                positionAndSetup,
                fitType,
                fitParams,
                fitErrors,
                signal,
                fittedSignal,
            )
        )

        # Update table display
        self.populateTable()

        # Update profile display
        currentImage.savedProfiles.append(currentImage.activeProfile)
        currentImage.activeProfile = None
        currentImage.updateArrays()

        # Disable the store profile button
        self.storeFitButton.setEnabled(False)

    ##-\-\-\-\-\-\-\-\
    ## TABLE GENERATION
    ##-/-/-/-/-/-/-/-/

    # ------------------------
    # Populate the data table
    def populateTable(self):

        # Delete the values
        rowCount = self.resultsTable.rowCount()
        if rowCount > 0:
            for i in range(rowCount):
                self.resultsTable.removeRow(0)

        # Retrieve the data associated with the current image
        tabIndex = self.parent.centralWidget.currentIndex()
        currentData = self.parent.imageTabsImage[tabIndex].savedData

        # Fill the table
        if len(currentData) > 0:
            for i, savedData in enumerate(currentData):

                # Fill the rows
                self.resultsTable.insertRow(i)
                valueList = savedData.getData()

                # Fill the columns
                for j, data in enumerate(valueList):
                    item = qtw.QTableWidgetItem(str(data))
                    self.resultsTable.setItem(i, j, item)

    # ---------------------------------------
    # React if table has been double clicked
    def tableIsDoubleClicked(self, row, column):

        # Display the message box
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Question)
        msg.setText("Delete Profile")
        msg.setInformativeText(
            """Do you want to delete this profile from the current memory?"""
        )
        msg.setWindowTitle("")
        msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        returnValue = msg.exec_()

        # Remove the line from the memory
        if returnValue == qtw.QMessageBox.Ok:

            # Remove from table
            self.resultsTable.removeRow(row)

            # Remove line and data
            tabIndex = self.parent.centralWidget.currentIndex()
            currentImage = self.parent.imageTabsImage[tabIndex]
            currentImage.savedData.pop(row)
            currentImage.savedProfiles.pop(row)
            currentImage.updateArrays()

    # -------------------------------------------
    # Save the content of the table in a file(s)
    def saveTableInFile(self):

        # Check if profiles are stored in the memory
        tabIndex = self.parent.centralWidget.currentIndex()
        profileNumbers = len(self.parent.imageTabsImage[tabIndex].savedData)

        # Display an error message if the table is empty
        if profileNumbers < 1:

            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Warning)
            msg.setText("ERROR: Not enough data")
            msg.setInformativeText("""At least one profile is required.""")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            returnValue = msg.exec_()

        # Save the results in a file
        else:
            saveTable(self.parent, self.parent.imageTabsImage[tabIndex].savedData)
