import numpy as np

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------------------------
# Find the ID of a path/particle based on the location
def findPathID(event_position, trajectory_dataframe):

    # Extract informations from the dataframe
    path_positions = trajectory_dataframe[['x','y']].to_numpy()
    path_ids = trajectory_dataframe['particle'].to_numpy()

    # Find the closest particle to the event position
    distances = np.sqrt( np.sum((event_position - path_positions)**2, axis=1) )
    selected_id = path_ids[ np.argmin(distances) ]

    return selected_id

# ------------------------
# Delete the selected path
def deletePath(path_id, trajectory_session):

    # Delete the session
    trajectory_session.remove(path_id)

    # Refresh the list
    trajectory_session.resetID()

# -------------------------
# Delete the selected point
def deletePoint(path_id, trajectory_session, current_frame):

    # Make the selection
    true_id = trajectory_session.positions['particle'] != path_id
    true_frame = trajectory_session.positions['frame'] != current_frame

    true_keep = true_id | true_frame

    # Remove the points
    trajectory_session.positions = trajectory_session.positions[ true_keep ]
