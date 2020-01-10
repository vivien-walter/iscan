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

    # Check if the file has the correct extension
    fileCanBeOpened, _ = checkValidExtension([path], accepted_formats=[".tif", ".tiff", ".gif"])
    if not fileCanBeOpened:
        return 0

    # Load a gif
    if os.path.splitext(path)[1] == '.gif':
        imageArray = loadGifStack(path)

    # Otherwise, load the image stack
    else:
        imageArray = loadStack(path)

    # Check the number of dimensions
    if len(imageArray.shape) == 4:
        imageArray = imageArray[0]

    # Create a new tab with the image inside
    displayName = os.path.splitext( os.path.split(path)[1] )[0]
    parent.addImageTab(imageArray, name=displayName)

# ----------------------------------
# Prompt for the user to open a file
def openFile(parent):

    # Select the folder to open
    name = qtw.QFileDialog.getOpenFileName(parent, "Open Folder", os.getcwd(), 'Image stacks (*.tif *.tiff *.gif)')
    if name[0] == "":
        return 0

    # Load the folder
    loadImageFile(parent, name[0])

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.input_output.check_files import checkValidExtension
from iscan.operations.image_class import loadStack, loadGifStack
