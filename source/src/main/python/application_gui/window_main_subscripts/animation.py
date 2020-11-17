import time

import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

##-\-\-\-\-\-\
## TIMER CLASS
##-/-/-/-/-/-/

class mainGUIAnimation(qtc.QThread):

    # Set the signals
    next_frame = qtc.pyqtSignal()

    # Initialise
    def __init__(self, parent):
        super(mainGUIAnimation, self).__init__(parent)

        self.parent_connection = parent

        # Start the event
        self.start()

    # ----------------------
    # Run the periodic event
    def run(self):

        # Set the periodic check variable to True
        self.current_state = True

        # Run the event
        while self.current_state:

            # Set the time to wait to the next iteration
            _wait_time = 0.04
            time.sleep(_wait_time)

            # Do the refresh
            self.next_frame.emit()

    # -----------------------
    # Stop the periodic event
    def stop(self):

        # Set the periodic check variable to False
        self.current_state = False

        # Stop the event
        self.quit()
