from copy import deepcopy
import numpy as np
import os
import pandas as pd

from input_output.trajectory_management import saveTrajectory, loadTrajectory
from trajectory.track_management import renumberList, mergeTracks, splitTrack, deleteTrack

##-\-\-\-\-\-\
## MAIN CLASSES
##-/-/-/-/-/-/

class TrackManager:
    def __init__(self, input):

        # Extract the informations from the input
        positions = _check_input(input)

        # Initialize the object
        self.positions = positions
        self.signals = None

        # Set the scales
        self.space_scale = None
        self.time_scale = None

    ##-\-\-\-\-\-\-\
    ## PATH SELECTION
    ##-/-/-/-/-/-/-/

    # ---------------------------------
    # List all the tracks in the object
    def listTracks(self):
        return np.copy(self.positions["particle"].unique())

    # -------------------
    # Re-index the tracks
    def resetID(self):
        self.positions = renumberList(self.positions)

    # --------------------------------------
    # Return a copy of the current dataframe
    def duplicate(self):
        return deepcopy(self)

    ##-\-\-\-\-\-\-\-\-\
    ## PATH MODIFICATION
    ##-/-/-/-/-/-/-/-/-/

    # -------------------------
    # Merge two tracks into one
    def merge(self, track_id1, track_id2):
        self.positions = mergeTracks(self.positions, track_id1, track_id2)

    # ----------------------
    # Split a track into two
    def split(self, track_id, split_after):
        self.positions = splitTrack(self.positions, track_id, split_after)

    # -------------------------
    # Remove the selected track
    def remove(self, track_id):
        self.positions = deleteTrack(self.positions, track_id)

    ##-\-\-\-\-\-\
    ## OUTPUT DATA
    ##-/-/-/-/-/-/

    # ----------------------------------------------------------
    # Return a specific selection of track(s) in a new dataframe
    def extract(self, track_ids=[0], as_dataframe=True):

        # Return a new dataframe
        if as_dataframe:
            return deepcopy(self.positions[self.positions["particle"].isin(track_ids)])

        # Return a list of array
        else:

            # Extract all tracks as arrays
            all_arrays = []
            for id in track_ids:
                current_track = self.positions[self.positions["particle"] == id]
                current_array = current_track[["frame", "y", "x"]].to_numpy()
                all_arrays.append(np.copy(current_array))

            return all_arrays

    # --------------------------------------
    # Save the selected trajectory into file
    def save(self, file_name=None, track_ids=None, default=".csv"):
        saveTrajectory(
            self.positions, filename=file_name, default=default, particle_ids=track_ids
        )

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ---------------------------------------------
# Check the input for the TrackManager instance
def _check_input(input):

    # Case if the input is a pandas Dataframe
    if isinstance(input, pd.DataFrame):
        dataframe = input

    # Case if the input is an XML file
    elif os.path.isfile(str(input)):
        dataframe = loadTrajectory(input)

    return dataframe

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------
# Start a track manager session
def startManager(input):
    return TrackManager(input)
