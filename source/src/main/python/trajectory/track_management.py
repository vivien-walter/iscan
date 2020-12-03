import numpy as np

##-\-\-\-\-\-\-\-\
## TRACK FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------
# Select the required track
def selectTrack(dataframe, track_id):
    return dataframe[dataframe["particle"] == track_id]

# ----------------------------------------
# Return all the frames in multiple tracks
def returnFrames(dataframe, all_tracks):

    # Read the frames listed in all tracks
    all_frames = []
    for track in all_tracks:
        all_frames.append(track["frame"].to_numpy())

    # Concatenate the list of all frames
    all_frames = np.concatenate(all_frames)

    return np.unique(all_frames)

# -----------------------------
# Return the list of all tracks
def returnTracks(dataframe):
    return np.unique(dataframe["particle"].to_numpy())

# ----------------------
# Renumber the particles
def renumberList(dataframe):

    # Build the dictionary
    old_nbr = dataframe["particle"].unique()
    new_nbr = np.arange(old_nbr.shape[0])

    # Replace all values
    dataframe["particle"] = dataframe["particle"].replace(old_nbr, new_nbr)

    return dataframe

# ----------------
# Merge two tracks
def mergeTracks(dataframe, track_id1, track_id2):

    # Extract both tracks
    track1 = selectTrack(dataframe, track_id1)
    track2 = selectTrack(dataframe, track_id2)

    # Get the list of all frames
    all_frames = returnFrames(dataframe, [track1, track2])

    # Process all frames
    for frame in all_frames:

        # Remove the doublons
        if (
            len(track1[track1["frame"] == frame]) == 1
            and len(track2[track2["frame"] == frame]) == 1
        ):
            dataframe = dataframe.drop(track2[track2["frame"] == frame].index)

        # Convert the second track into the 1st one
        elif len(track1[track1["frame"] == frame]) == 0:
            dataframe.at[
                track2[track2["frame"] == frame].index[0], "particle"
            ] = track_id1

    return dataframe

# -------------
# Split a track
def splitTrack(dataframe, track_id, split_after):

    # Extract the track
    old_track = selectTrack(dataframe, track_id)

    # Get the list of track numbers
    all_tracks = returnTracks(dataframe)
    new_track_id = np.amax(all_tracks) + 1

    # Get the list of all frames
    all_frames = returnTracks(dataframe, [old_track])

    # Process all frames
    for frame in all_frames:

        # Change the track number
        if frame > split_after:
            object_index = old_track[old_track["frame"] == frame].index[0]
            dataframe.at[object_index, "particle"] = new_track_id

    return dataframe

# -------------------------
# Delete the selected track
def deleteTrack(dataframe, track_id):

    # Extract the track
    old_track = selectTrack(dataframe, track_id)

    # Delete the track
    dataframe = dataframe.drop(old_track.index)

    return dataframe
