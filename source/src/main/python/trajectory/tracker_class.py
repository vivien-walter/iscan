from copy import deepcopy
import numpy as np
import trackpy as tp

from image_processing.corrections import backgroundCorrection
from input_output.tracker_management import saveSettings, loadSettings

##-\-\-\-\-\-\
## MAIN CLASSES
##-/-/-/-/-/-/

class TrackingSession:
    def __init__(
        self,
        diameter=41,
        dark_spots=False,
        search_range=None,
        load_file=None,
        input=None,
    ):

        # Keep the array in memory
        self.input = input
        self.spots = None
        self.tracks = None

        # Initialize the default parameters for tp.locate and tp.batch
        self.diameter = _nbr2odd(diameter)
        self.minmass = None
        self.maxsize = None
        self.separation = None
        self.noise_size = 1
        self.smoothing_size = None
        self.threshold = None
        self.invert = dark_spots
        self.percentile = 64
        self.topn = None
        self.preprocess = True
        self.max_iterations = 10
        self.filter_before = None
        self.filter_after = None
        self.characterize = True
        self.engine = "auto"

        # Initialize the default parameters for tp.link and trajectory filtering
        if search_range is None:
            search_range = diameter
        self.search_range = search_range
        self.memory = 0
        self.adaptive_stop = None
        self.adaptive_step = 0.95
        self.neighbor_strategy = None
        self.link_strategy = None
        self.filter_stubs = None

        if load_file is not None:
            self.load(load_file)

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## CALL TRACKPY FUNCTIONS
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ----------------------------------------
    # Preview the parameters on a single frame
    def locate(self, input=None, store=True, frame=0):

        # Retrieve the array
        if input is None:
            input = self.input
        array = _get_array(input, frame=frame)

        # Check odd numbers
        self.diameter = _nbr2odd(self.diameter)

        # Run TrackPy
        dataframe = tp.locate(
            array,
            self.diameter,
            minmass=self.minmass,
            maxsize=self.maxsize,
            separation=self.separation,
            noise_size=self.noise_size,
            smoothing_size=self.smoothing_size,
            threshold=self.threshold,
            invert=self.invert,
            percentile=self.percentile,
            topn=self.topn,
            preprocess=self.preprocess,
            max_iterations=self.max_iterations,
            characterize=self.characterize,
            engine=self.engine,
        )

        # Store in the instance
        if store:
            self.spots = deepcopy(dataframe)
            self.tracks = deepcopy(dataframe)

        return dataframe

    # -------------------------------------
    # Batch process all frames of the stack
    def batch(self, array, filter=True, store=True):

        # Check odd numbers
        self.diameter = _nbr2odd(self.diameter)

        # Run TrackPy
        dataframe = tp.batch(
            array,
            self.diameter,
            minmass=self.minmass,
            maxsize=self.maxsize,
            separation=self.separation,
            noise_size=self.noise_size,
            smoothing_size=self.smoothing_size,
            threshold=self.threshold,
            invert=self.invert,
            percentile=self.percentile,
            topn=self.topn,
            preprocess=self.preprocess,
            max_iterations=self.max_iterations,
            characterize=self.characterize,
            engine=self.engine,
        )

        # Store in the instance
        if store:
            self.spots = deepcopy(dataframe)
            self.tracks = deepcopy(dataframe)

        # Filter the trajectory
        if filter:
            dataframe = self.filter(dataframe, store=store)

        return dataframe

    # -----------------------------------------------------------
    # Filter the collected collection of points into a trajectory
    def filter(self, dataframe=None, store=True):

        # Retrieve the dataframe
        if dataframe is None:
            dataframe = self.spots

        # Connect positions together
        dataframe = tp.link(
            dataframe,
            self.search_range,
            memory=self.memory,
            adaptive_stop=self.adaptive_stop,
            adaptive_step=self.adaptive_step,
            neighbor_strategy=self.neighbor_strategy,
            link_strategy=self.link_strategy,
        )

        # Remove spurious trajectory
        if self.filter_stubs is not None:
            dataframe = tp.filtering.filter_stubs(
                dataframe, threshold=self.filter_stubs
            )

        # Regenerate the index
        dataframe = dataframe.reset_index(drop=True)

        # Store in the instance
        if store:
            self.tracks = deepcopy(dataframe)

        return dataframe

    ##-\-\-\-\-\-\-\-\-\-\-\
    ## LOAD AND SAVE SETTINGS
    ##-/-/-/-/-/-/-/-/-/-/-/

    # ---------------------------
    # Save the settings in a file
    def save(self, file_name=None):
        saveSettings(self, file_name)

    # -----------------------------
    # Load the settings from a file
    def load(self, file_name):

        # Load the file into a dictonary
        setting_dict = loadSettings(file_name)

        # Assign all the values
        for setting in setting_dict.keys():
            setattr(self, setting, setting_dict[setting])

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -------------------------
# Round numbers to odd ones
def _nbr2odd(number):

    # Add 1 to even numbers
    if number % 2 == 0:
        number += 1

    return number

# -------------------------------
# Get the array from the instance
def _get_array(input, frame=0):

    # Input is an array
    if type(input) is np.ndarray:
        array = input

    # Select a frame if required
    if len(array.shape) == 3:
        array = array[frame]

    return array

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------
# Start the tracking session
def startSession(
    diameter=41, dark_spots=False, search_range=None, load_file=None, input=None
):
    return TrackingSession(
        diameter=diameter,
        dark_spots=dark_spots,
        search_range=search_range,
        load_file=load_file,
        input=input,
    )
