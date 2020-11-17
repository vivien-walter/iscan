import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\-\-\-\-\-\-\-\
## GENERIC ERROR AND WARNING
##-/-/-/-/-/-/-/-/-/-/-/-/-/

# -----------------------------------------------------------
# Display a warning message box with a user choice to proceed
def warningProceedMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)

    # Add the informations
    msg.setWindowTitle('WARNING')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
    retval = msg.exec_()

    return retval == qtw.QMessageBox.Ok

# -----------------------------
# Display a warning message box
def warningMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Warning)

    # Add the informations
    msg.setWindowTitle('WARNING')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

    return retval == qtw.QMessageBox.Ok

# ------------------------------------------------
# Display an error message with a single OK button
def errorMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)

    # Add the informations
    msg.setWindowTitle('ERROR')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

# -------------------------------------------------
# Display a notification message to inform the user
def notificationMessage(title, text):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)

    # Add the informations
    msg.setWindowTitle('INFO(S)')
    msg.setText(title)
    msg.setInformativeText(text)

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

##-\-\-\-\-\-\-\-\-\-\-\-\
## CUSTOM ERROR AND WARNING
##-/-/-/-/-/-/-/-/-/-/-/-/

# -------------------------------------------------------
# Display an error message when an open image is required
def errorMessageNoImage():

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)

    # Add the informations
    msg.setWindowTitle('ERROR')
    msg.setText('No image open')
    msg.setInformativeText('There are no images open.')

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

# -------------------------------------------------
# Display an error message when a stack is required
def errorMessageNoStack():

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)

    # Add the informations
    msg.setWindowTitle('ERROR')
    msg.setText('No stack open')
    msg.setInformativeText('An open stack is required to proceed.')

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

# ------------------------------------------------------
# Display an error message when a trajectory is required
def errorMessageNoTrajectory():

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Critical)

    # Add the informations
    msg.setWindowTitle('ERROR')
    msg.setText('No trajectory in memory')
    msg.setInformativeText('There are no trajectory on a selected tab.')

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()

# ---------------------------------------------------------
# Display a notification message when a file has been saved
def notificationFileSaved(file_name):

    # Generate the box
    msg = qtw.QMessageBox()
    msg.setIcon(qtw.QMessageBox.Information)

    # Add the informations
    msg.setWindowTitle('INFO(S)')
    msg.setText("File Saved")
    msg.setInformativeText("The file "+file_name+" has been successfully saved.")

    # Complete the box
    msg.setStandardButtons(qtw.QMessageBox.Ok)
    retval = msg.exec_()
