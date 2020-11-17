from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel

from application_gui.window_main import mainGUI

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()
    main_window = mainGUI(appctxt)
    sys.exit(appctxt.app.exec_())
