from glob import glob
import numpy as np
import os
import sys

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

import iscan.image_handling as img

##-\-\-\-\-\-\-\-\
## COMMON FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Check if the extension can be opened
def _checkValidExtension(fileName):

    name, nameExtension = os.path.splitext(fileName)
    if nameExtension in [".tif"]:
        return True
    else:
        _badFileMessageBox()
        return False


# -------------------------------------
# Check the extension and/or modify it
def _checkExtension(fileName, extension):

    name, nameExtension = os.path.splitext(fileName)
    if nameExtension != extension:
        fileName += extension

    return fileName


# ---------------------------------------------------
# Return error message if the file is not recognised
def _badFileMessageBox():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("ERROR: Unrecognized input")
    msg.setInformativeText("""The file(s) cannot be opened by the software.""")
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()


##-\-\-\-\-\-\-\-\
## OPEN IMAGE FILES
##-/-/-/-/-/-/-/-/

# ------------------------------
# Open and load an image folder
def loadImageFolder(parent, path):

    # Check if the first file of the folder is recognised by the software
    fileInFolder = glob(path + "*.*")
    if not _checkValidExtension(fileInFolder[0]):
        return 0

    # Load the folder
    imageName, imageExtension = os.path.splitext(fileInFolder[0])
    frames = img.loadStack(path + "*" + imageExtension)

    # Create the tab display if not created yet
    if not parent.isTabDisplayActive:
        parent.createTabDisplay()

    # Append the image in a new tab
    if path[-1] == "/":
        path = path[0:-1]
    displayName = os.path.split(path)[1]
    parent.addImageTab(frames.image.raw, name=displayName)


# -------------------------------------
# Prompt for the user to open a folder
def openFolder(parent):

    # Select the folder to open
    name = qtw.QFileDialog.getExistingDirectory(parent, "Open Folder")
    if name[0] == "":
        return 0

    # Correct the name
    if name[-1] != "/":
        name += "/"

    # Load the folder
    loadImageFolder(parent, name)


# -----------------------------
# Open and load an image stack
def loadImageFile(parent, path):

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("ERROR: Function(s) unavailable")
    msg.setInformativeText(
        """Single image stack file opening have not been implemented yet.
Please check if a more recent version of this software has been released."""
    )
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()


# -----------------------------------
# Prompt for the user to open a file
def openFile(parent):
    loadImageFile(parent, "untitled")


# -----------------------------------------------------
# Check the type of element and process it accordingly
def checkItemType(parent, item):

    # Return an error if there is more than one file
    if len(item) != 1:
        msg = qtw.QMessageBox()
        msg.setIcon(qtw.QMessageBox.Warning)
        msg.setText("ERROR: Too many files")
        msg.setInformativeText(
            """The software can only open one file or folder at the time."""
        )
        msg.setWindowTitle("ERROR")
        msg.setStandardButtons(qtw.QMessageBox.Ok)
        returnValue = msg.exec_()
        return 0
    item = item[0]

    # Proceed if the input is a directory
    if os.path.isdir(item):
        loadImageFolder(parent, item)

    # Proceed if the input is a file
    elif os.path.isfile(item):
        loadImageFile(parent, item)

    # Raise an error if the file does not exist
    else:
        _badFileMessageBox()


##-\-\-\-\-\-\-\-\-\
## SAVE PROFILES DATA
##-/-/-/-/-/-/-/-/-/

# --------------------------------
# Save the table into a .csv file
def saveTable(parent, allData):

    # Get the name of the file to create
    name = qtw.QFileDialog.getSaveFileName(parent, "Save File")
    if name[0] == "":
        return 0
    name = _checkExtension(name[0], ".csv")

    # Generate the array
    dataListOfLists = [data.getData() for data in allData]
    dataArray = np.array(dataListOfLists).astype(str)

    # Prepare the header
    # NOTE: Take this from profiling_control.py, line 396
    columnNames = [
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
    headerText = ""
    for headerName in columnNames:
        headerText += headerName + ","
    headerText = headerText[0:-1]

    # Save the file
    np.savetxt(name, dataArray, fmt="%s", delimiter=",", header=headerText)

    # Notify the user
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)
    msg.setText("The file has been successfully saved")
    msg.setInformativeText("""The table has been saved in the folder.""")
    msg.setWindowTitle("File Saved")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()


# ----------------------------------------------
# Save all the profiles in separated .csv files
def saveProfiles(parent, allData):

    # Get the name of the file to create
    name = qtw.QFileDialog.getSaveFileName(parent, "Save File")
    if name[0] == "":
        return 0
    name, _ = os.path.splitext(name[0])

    # Process all the profiles
    for data in allData:

        # Generate the name of the file
        fileName = name + "_" + data.name + ".csv"

        # Construct the array
        distance, profile, profileFit = data.distance, data.profile, data.profileFit
        dataArray = np.array([distance, profile, profileFit]).T

        # Save the file
        headerText = "Distance,Profile,Fitted Profile"
        np.savetxt(fileName, dataArray, delimiter=",", header=headerText)

    # Notify the user
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)
    msg.setText("All files have been successfully saved")
    msg.setInformativeText(
        """All the profiles and their fit have been saved in the files."""
    )
    msg.setWindowTitle("Files Saved")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()


##-\-\-\-\-\-\-\-\
## SAVE STATISTICS
##-/-/-/-/-/-/-/-/

# -----------------------------------------------
# Save all the possible stats on the given array
def saveAllStats(parent, dataDict):

    # Get the name of the file to create
    name = qtw.QFileDialog.getSaveFileName(parent, "Save File")
    if name[0] == "":
        return 0
    name = _checkExtension(name[0], ".csv")

    # Generate the data array
    parameters = list(dataDict.keys())
    dataArray = []
    for param in parameters:
        currentArray = [
            param,
            str(np.mean(dataDict[param])),
            str(np.std(dataDict[param], ddof=1)),
        ]
        for param2 in parameters:
            currentArray.append(
                str(np.corrcoef(dataDict[param], dataDict[param2], ddof=1)[0, 1])
            )
        dataArray.append(np.copy(np.array(currentArray)))

    # Create the file
    headerText = "Parameter,Mean,StDev"
    for param in parameters:
        headerText += "," + param
    np.savetxt(name, dataArray, fmt="%s", delimiter=",", header=headerText)

    # Notify the user
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)
    msg.setText("The file has been successfully saved")
    msg.setInformativeText("""The statistics file has been saved.""")
    msg.setWindowTitle("Files Saved")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()


# --------------------------------------------------------
# Save the stats on the given distribution or correlation
def saveStats(parent, dataArray, parameterNames, numberColumns):

    # Get the name of the file to create
    name = qtw.QFileDialog.getSaveFileName(parent, "Save File")
    if name[0] == "":
        return 0
    name = _checkExtension(name[0], ".csv")

    # Prepare the data to save
    if numberColumns == 2:
        dataArray = np.copy(dataArray).T

        # Initialise the header
        valueNames = parameterNames.split(",")
        headerText = (
            "Mean " + valueNames[0] + ":" + str(np.mean(dataArray[:, 0])) + "\n"
        )
        headerText += (
            "StDev " + valueNames[0] + ":" + str(np.std(dataArray[:, 0], ddof=1)) + "\n"
        )
        headerText += (
            "Mean " + valueNames[1] + ":" + str(np.mean(dataArray[:, 1])) + "\n"
        )
        headerText += (
            "StDev " + valueNames[1] + ":" + str(np.std(dataArray[:, 1], ddof=1)) + "\n"
        )

        # Get the linear correlation estimator
        headerText += (
            "Spearman's Rho:"
            + str(np.corrcoef(dataArray[:, 0], dataArray[:, 1], ddof=1))
            + "\n"
        )

    # Initialise the header for a single distribution
    else:
        headerText = "Mean:" + str(np.mean(dataArray)) + "\n"
        headerText += "StDev:" + str(np.std(dataArray, ddof=1)) + "\n"

    # Save the file
    headerText += parameterNames
    np.savetxt(name, dataArray, delimiter=",", header=headerText)

    # Notify the user
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)
    msg.setText("The file has been successfully saved")
    msg.setInformativeText("""The statistics file has been saved.""")
    msg.setWindowTitle("Files Saved")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()
