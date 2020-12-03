import os
from pathlib import Path

import PyQt5.QtWidgets as qtw

from application_gui.common_gui_functions import openWindow

from application_gui.correction_background.display import backgroundCorrectionWindow
from application_gui.correction_contrast.display import contrastCorrectionWindow
from application_gui.correction_fluctuations.display import fluctuationCorrectionWindow
from application_gui.correction_dark2bright.display import darkToBrightCorrectionWindow
from application_gui.correction_averaging.display import frameAveragingWindow
from application_gui.correction_crop.display import imageCropWindow
from application_gui.messageboxes.display import errorMessageNoImage, errorMessageNoStack
from application_gui.progressbar.correction_background import ImageCorrectionProgressBarWindow

##-\-\-\-\-\-\-\-\-\-\-\
## INTERFACE INTERACTION
##-/-/-/-/-/-/-/-/-/-/-/

class menuBarProcessFunctions(object):

    ##-\-\-\-\-\-\
    ## PROCESS MENU
    ##-/-/-/-/-/-/

    # ----------------------------------------
    # Display the background correction window
    def callBackgroundCorrection(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class
            n_frames = crt_class.n_frames

            # Check if there is more than one image in the stack
            if n_frames > 1:
                openWindow(self.parent, backgroundCorrectionWindow, 'background_correction', image_array=crt_class.image.source)

            else:
                errorMessageNoStack()

        else:
            errorMessageNoImage()

    # ---------------------------------------------------
    # Display the intensity fluctuation correction window
    def callBrightnessCorrection(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Open the window
            openWindow(self.parent, contrastCorrectionWindow, 'contrast_correction', image_class=crt_class)

        else:
            errorMessageNoImage()

    # ---------------------------------------------------
    # Display the intensity fluctuation correction window
    def callIntensityFluctuations(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class
            n_frames = crt_class.n_frames

            # Check if there is more than one image in the stack
            if n_frames > 1:
                openWindow(self.parent, fluctuationCorrectionWindow, 'fluctuations_correction', image_array=crt_class.image.source)

            else:
                errorMessageNoStack()

        else:
            errorMessageNoImage()

    # ---------------------------------------------
    # Display the frame averaging processing window
    def callFrameAveraging(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class
            n_frames = crt_class.n_frames

            # Check if there is more than one image in the stack
            if n_frames > 1:
                openWindow(self.parent, frameAveragingWindow, 'frame_average', image_array=crt_class.image.source)

            else:
                errorMessageNoStack()

        else:
            errorMessageNoImage()

    # --------------------------------------------
    # Display the dark to bright conversion window
    def callDarkToBright(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:
            openWindow(self.parent, darkToBrightCorrectionWindow, 'dark_to_bright')

        else:
            errorMessageNoImage()

    # --------------------------------------
    # Make a substack from the current stack
    def callMakeSubstack(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class
            n_frames = crt_class.n_frames

            # Check if there is more than one image in the stack
            if n_frames > 1:
                # Duplicate the current tab
                self.parent.imageTabDisplay.substackTab(tab_id)

            else:
                errorMessageNoStack()

        else:
            errorMessageNoImage()

    # ---------------------------------
    # Crop the image on the current tab
    def callCropCurrentImage(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()
            crt_class = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class

            # Open the window
            openWindow(self.parent, imageCropWindow, 'crop_image', image_class=crt_class)

        else:
            errorMessageNoImage()

    # -------------------------
    # Duplicate the current tab
    def callDuplicateCurrentTab(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Duplicate the current tab
            self.parent.imageTabDisplay.copyTab(tab_id)

        else:
            errorMessageNoImage()

    # ----------------------
    # Rename the current tab
    def callRenameCurrentTab(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Rename the current tab
            self.parent.imageTabDisplay.renameTab(tab_id)

        else:
            errorMessageNoImage()

    # ---------------------------------
    # Zoom in or out in the current tab
    def callZoomInOutCurrentTab(self, dezoom=False):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Modify the zoom
            self.parent.imageTabDisplay.changeZoom(dezoom=dezoom, tab_id=tab_id)

        else:
            errorMessageNoImage()

    # ------------------------------
    # Zoom back to the original size
    def callZoomBack(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Reset the zoom
            self.parent.imageTabDisplay.changeZoom(new_zoom=1, tab_id=tab_id)

        else:
            errorMessageNoImage()

    # ---------------------
    # Zoom to fit the frame
    def callZoomToFit(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Reset the zoom
            self.parent.imageTabDisplay.zoomToFitFrame(tab_id=tab_id)

        else:
            errorMessageNoImage()

    # ---------------------------------
    # Zoom the image to the given value
    def callZoomToValue(self):

        # Check if a tab is open
        if len( self.parent.imageTabDisplay.displayedTabs ) > 0:

            # Get the current tab
            tab_id = self.parent.imageTabDisplay.currentIndex()

            # Get the current zoom value
            old_zoom = self.parent.imageTabDisplay.displayedTabs[tab_id].image_class.zoom

            # Get the user input
            new_zoom, is_ok = qtw.QInputDialog.getDouble( self.parent, 'Set Zoom', 'Set the zoom to (%):', value=old_zoom*100, min=0, decimals=2 )

            # Edit the zoom
            if is_ok:
                self.parent.imageTabDisplay.changeZoom(new_zoom=new_zoom/100, tab_id=tab_id)

        else:
            errorMessageNoImage()
