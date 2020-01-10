from glob import glob
import os

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\
## OPEN IMAGE FILES
##-/-/-/-/-/-/-/-/

# -----------------------------
# Open and load an image folder
def loadImageFolder(parent, path):

    # Check if the first file of the folder is recognised by the software
    fileInFolder = glob(path + "*.*")
    fileCanBeOpened, fileIndex = checkValidExtension(fileInFolder)
    if not fileCanBeOpened:
        return 0

    # Load the folder
    imageName, imageExtension = os.path.splitext(fileInFolder[fileIndex])
    imageArray = loadStack(path + "*" + imageExtension)

    # Create a new tab with the image inside
    path = os.path.normpath(path)
    displayName = os.path.split(path)[1]
    parent.addImageTab(imageArray, name=displayName)


# ------------------------------------
# Prompt for the user to open a folder
def openFolder(parent):

    # Select the folder to open
    name = qtw.QFileDialog.getExistingDirectory(parent, "Open Folder")
    if name[0] == "":
        return 0

    # Correct the name
    name = os.path.join(name, "")

    # Load the folder
    loadImageFolder(parent, name)


# ----------------------------
# Open and load an image stack
def loadImageFile(parent, path):

    # NOTE: Implement this function ASAP!

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


# ----------------------------------
# Prompt for the user to open a file
def openFile(parent):
    loadImageFile(parent, "untitled")

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.input_output.check_files import checkValidExtension
from iscan.operations.image_class import loadStack
