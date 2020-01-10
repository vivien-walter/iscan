import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\
## GENERIC MESSAGES
##-/-/-/-/-/-/-/-/

# ---------------------------------------------------
# Generic error message - for errors only called once
def errorMessage(title, text):

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText(title)
    msg.setInformativeText(text)
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()

# ----------------------------------------------------
# Ask the user to confirm the action if data are saved
def checkMessage(title, text):

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText(title)
    msg.setInformativeText(text)
    msg.setWindowTitle("WARNING")
    msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
    returnValue = msg.exec_()

    if returnValue == qtw.QMessageBox.Cancel:
        return False
    else:
        return True

##-\-\-\-\-\-\-\-\-\-\
## COMMON DIALOG BOXES
##-/-/-/-/-/-/-/-/-/-/

# ------------------------------------------------------------------
# Display a message to say that the file has been successfully saved
def messageFileSaved():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)
    msg.setText("File saved")
    msg.setInformativeText("""The file has been successfully saved.""")
    msg.setWindowTitle("File Saved")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()

# ---------------------------------------------------------
# Display an error messsage when the file couldn't be saved
def errorFileSaved():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("ERROR: File was not saved")
    msg.setInformativeText("""The file couldn't be saved.""")
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()

# -------------------------------------------------
# Display an error messsage when no images are open
def errorNoImage():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("ERROR: No opened image")
    msg.setInformativeText("""Open an image first.""")
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()

# --------------------------------------------------------
# Display an error message when the file is not recognized
def errorBadFile():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("ERROR: Unrecognized input")
    msg.setInformativeText("""The file(s) cannot be opened by the software.""")
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()

# ---------------------------------------------------------
# Display an error message if the window was already opened
def errorAlreadyOpen():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("ERROR: Already open")
    msg.setInformativeText("""The window is already open.""")
    msg.setWindowTitle("ERROR")
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    returnValue = msg.exec_()

##-\-\-\-\-\-\-\-\-\-\-\
## USER INTERACTION BOXES
##-/-/-/-/-/-/-/-/-/-/-/

# -------------------------------------------
# Ask the user to use the default name or not
def checkUseDefaultName():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("Use default name(s)?")
    msg.setInformativeText("""Do you want to use the default name(s) or provide one?""")
    msg.setWindowTitle("DEFAULT NAME")
    msg.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No)
    returnValue = msg.exec_()

    if returnValue == qtw.QMessageBox.No:
        return False
    else:
        return True

# ----------------------------------------------------
# Ask the user to confirm the action if data are saved
def checkSavedData():

    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)
    msg.setText("WARNING: Data in the memory")
    msg.setInformativeText("""Data have been saved on this tab. Doing this operation will erase all data or part of them.
Are you sure want to proceed?""")
    msg.setWindowTitle("WARNING")
    msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
    returnValue = msg.exec_()

    if returnValue == qtw.QMessageBox.Cancel:
        return False
    else:
        return True
