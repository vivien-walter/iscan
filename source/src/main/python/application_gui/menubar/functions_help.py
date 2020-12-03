import os
from pathlib import Path
import webbrowser

import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow

from application_gui.about_iscan.display import aboutHelpWindow
from application_gui.settings_user.display import userSettingsWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarHelpFunctions(object):

    ##-\-\-\-\-\
    ## HELP MENU
    ##-/-/-/-/-/

    # ------------------------------------------
    # Open the online help of iSCAN in a browser
    def openiSCANBrowser(self):
        webbrowser.open('https://github.com/vivien-walter/iscan/wiki',new=2)

    # ---------------------------------------------------
    # Open the online help of trackpy locate in a browser
    def openTrackpyLocateBrowser(self):
        webbrowser.open('http://soft-matter.github.io/trackpy/dev/generated/trackpy.locate.html',new=2)

    # --------------------------------------------------
    # Open the online help of trackpy batch in a browser
    def openTrackpyBatchBrowser(self):
        webbrowser.open('http://soft-matter.github.io/trackpy/dev/generated/trackpy.batch.html',new=2)

    # -------------------------------------------------
    # Open the online help of trackpy link in a browser
    def openTrackpyLinkBrowser(self):
        webbrowser.open('http://soft-matter.github.io/trackpy/dev/generated/trackpy.link.html',new=2)

    # ---------------------------------------------------------
    # Open the online help of trackpy filter_stubs in a browser
    def openTrackpyFilterBrowser(self):
        webbrowser.open('http://soft-matter.github.io/trackpy/dev/generated/trackpy.filtering.filter_stubs.html',new=2)

    # --------------------------------
    # Display the user settings window
    def callUserSettingsWindow(self):
        openWindow(self.parent, userSettingsWindow, 'user_settings')

    # ------------------------------------------
    # Display the information about iSCAN window
    def callAboutiSCANWindow(self):
        openWindow(self.parent, aboutHelpWindow, 'about')
