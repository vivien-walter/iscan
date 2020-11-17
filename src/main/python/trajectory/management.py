import numpy as np

from trajectory.trajectory_class import startManager

##-\-\-\-\-\-\-\-\-\-\
## TRAJECTORY FUNCTIONS
##-/-/-/-/-/-/-/-/-/-/

# ----------------------------------------------------
# Find the ID of a path/particle based on the location
def generateTrajectory(positions):

    # Format the pandas dataframe
    positions = positions[['y','x']].copy()
    positions['frame'] = [0]*len(positions['x'])
    positions['particle'] = np.arange(len(positions['x']))
    positions.reset_index(drop=True, inplace=True)

    # Initialise the manager
    trajectory = startManager(positions)

    return trajectory

# -------------------------------------------------
# Make a substack selection of the given trajectory
def substackTrajectory(trajectory, selection):

    # Get the current positions
    crt_positions = trajectory.positions

    # Make the selection
    crt_positions = crt_positions[ crt_positions['frame'].isin(selection) ]

    # Remap the frame indices
    old_frames = crt_positions['frame'].unique()
    new_frames = np.arange(old_frames.shape[0])
    convert_dict = dict(zip( old_frames, new_frames ))

    # Convert the values
    new_frame_positions = np.copy( crt_positions['frame'].to_numpy() )
    for key in convert_dict.keys():
        new_frame_positions[new_frame_positions == key] = convert_dict[key]

    # Replace the trajectory
    new_positions = crt_positions.copy()
    new_positions['frame'] = new_frame_positions

    # Generate the new manager
    new_trajectory = startManager(new_positions)

    return new_trajectory
