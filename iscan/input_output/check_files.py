import os

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\
## PROMPT FILE AND FOLDERS
##-/-/-/-/-/-/-/-/-/-/-/-/

# ----------------------------------
# Get the name of the file to create
def getFileToCreate(parent, file_name = None, extension='.dat'):

    # Get the name of the file to create
    if file_name is None:
        file_name = qtw.QFileDialog.getSaveFileName(parent, "Save File")
        if file_name[0] == "":
            return False, 'untitled'
        else:
            file_name = file_name[0]

    # Check the extension of the file]
    file_name = checkExtension(file_name, extension)

    return True, file_name

# -------------------------------------
# Get the path to the folder to save in
def getFolderToSaveIn(parent):

    # Prompt the path
    folder_path = qtw.QFileDialog.getExistingDirectory(parent, "Save in Folder")
    if folder_path == "":
        return False, 'untitled'
    else:
        return True, os.path.join(folder_path, "")

# --------------------------------------------------------------------------
# Ask whether to use the default name or a given one - prompt for the folder
def getFileOrFolder(parent):

    # Check if default name should be used
    useDefault = checkUseDefaultName()

    # Prompt for the folder or default name
    if useDefault:
        proceed, path = getFolderToSaveIn(parent)
        if not proceed:
            return False, False, 'untitled'
    else:
        proceed, file_name = getFileToCreate(parent, extension='.csv')
        if not proceed:
            return False, False, 'untitled'
        path, _ = os.path.splitext(file_name)

    return True, useDefault, path

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## CHECK FILE TYPES AND EXTENSION
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

# ------------------------------------
# Check if the extension can be opened
def checkValidExtension(fileList, accepted_formats=[".tif"], skipped_format=[".dat", ".txt"]):

    for fileIndex, fileName in enumerate(fileList):

        # Check that the extension can be opened
        name, nameExtension = os.path.splitext(fileName)
        if nameExtension in accepted_formats:
            return True, fileIndex

        # Ignore data and log files
        elif nameExtension in skipped_format:
            pass

        else:
            errorBadFile()
            return False, 0

    # Return an error if there is no readable file in the folder
    return False, 0

# ------------------------------------
# Check the extension and/or modify it
def checkExtension(fileName, extension):

    name, nameExtension = os.path.splitext(fileName)
    if nameExtension != extension:
        fileName += extension

    return fileName

# ----------------------------------------------------
# Check the type of element and process it accordingly
def checkItemType(parent, item):

    # Return an error if there is more than one file
    if len(item) != 1:
        errorMessage("ERROR: Too many files", """The software can only open one file or folder at the time.""")
        return 0, 0

    item = item[0]

    # Proceed if the input is a directory
    if os.path.isdir(item):
        return "folder", item

    # Proceed if the input is a file
    elif os.path.isfile(item):
        return "file", item

    # Raise an error if the file does not exist
    else:
        errorBadFile()

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.display.error_messages import errorBadFile, errorMessage, checkUseDefaultName
