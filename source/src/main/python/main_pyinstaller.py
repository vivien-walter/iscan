import sys

import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw

from application_gui.window_main import mainGUI

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setWindowIcon(qtg.QIcon('icon.ico'))
    main_window = mainGUI(app, compiler='pyinstaller')
    sys.exit(app.exec_())
