import os
import pandas as pd
import xml.etree.ElementTree as ET

from trajectory.track_management import selectTrack, returnFrames, returnTracks

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# --------------------------------------
# Check that the extension is authorized
def _check_extensions(file, extensions=[".csv",".xml"]):

    file_name, file_extension = os.path.splitext(file)

    # Save in the new list on if the extension is authorized
    if file_extension in extensions:
        return file

    # Raise an error if not valid
    else:
        raise Exception("The extension is not valid.")

# --------------------------------------
# Convert the trajectory to a XML format
def _traj2XML(positions, calibration=None):

    # Initialize the attribute dictionary
    data_attributes = {"generationDateTime": "None", "from": "TPHelper"}

    # Extract informations from the trajectory
    particle_list = returnTracks(positions)
    data_attributes["nTracks"] = str(len(particle_list))

    # Get the space and time calibration
    if calibration is None:
        data_attributes["spaceUnits"] = "pixels"
        data_attributes["frameInterval"] = "1.0"
        data_attributes["timeUnits"] = "frames"

    # Prepare the data and its attributes
    data = ET.Element("Tracks")
    for attribute in data_attributes.keys():
        data.set(attribute, data_attributes[attribute])

    # Loop over all the particles in the trajectory
    for particle_id in particle_list:

        # Get the number of frames
        crt_particle = selectTrack(positions, particle_id)
        frame_list = returnFrames(positions, [crt_particle])
        item_attributes = {"nSpots": str(len(frame_list))}

        # Prepare the item and its attributes
        item = ET.SubElement(data, "particle")
        for attribute in item_attributes.keys():
            item.set(attribute, item_attributes[attribute])

        # Fill the tree with all the items
        for frame in frame_list:

            # Generate a temp subitem for the array
            tmp_subitem = ET.SubElement(item, "detection")
            tmp_subitem.set("t", str(frame))

            # Get the value from the trajectory
            crt_frame = crt_particle.loc[crt_particle["frame"] == frame]
            tmp_subitem.set("x", str(float(crt_frame["x"])))
            tmp_subitem.set("y", str(float(crt_frame["y"])))

            tmp_subitem.set("z", "0.0")

    return ET.tostring(data)

# ---------------------------
# Save the data in a XML file
def _saveXML(positions, file_name, calibration=None):

    # Convert position into an .xml file
    dataXML = _traj2XML(positions, calibration=calibration)

    # Save in file
    fileToSave = open(file_name, "w")
    fileToSave.write(dataXML.decode("utf-8"))
    fileToSave.close()

# ---------------------------
# Save the data in a CSV file
def _saveCSV(positions, file_name):

    # Save in a file
    positions.to_csv(file_name)

# ----------------------------------
# Convert a XML file to a trajectory
def _xml2Traj(filename):

    # Extract the tree from the file
    trajXML = ET.parse(filename).getroot()

    # Initialize the lists
    particle_id = []
    frame_nbr = []
    x_position = []
    y_position = []

    # Loop over all particles
    for id, track in enumerate(trajXML):

        # Loop over all positions
        for position in track:
            particle_id.append(int(id))
            frame_nbr.append(int(position.attrib["t"]))
            x_position.append(float(position.attrib["x"]))
            y_position.append(float(position.attrib["y"]))

    # Generate the DataFrame
    trajectory = pd.DataFrame(
        {"y": y_position, "x": x_position, "frame": frame_nbr, "particle": particle_id}
    )

    return trajectory

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------------
# Save the trajectories in file(s)
def saveTrajectory(dataframe, filename, default=".xml", particle_ids=None):

    # Generate the file name
    filename = _check_extensions(filename)

    # Select the tracks to save
    if particle_ids is not None:
        dataframe = dataframe[dataframe["particle"].isin(particle_ids)]

    # Save as a XML file
    if os.path.splitext(filename)[1] == ".xml":
        _saveXML(dataframe, filename)

    # Save as a CSV file
    else:
        _saveCSV(dataframe, filename)

# ---------------------------------------------
# Load a trajectory into a TrackManager session
def loadTrajectory(filename):
    return _xml2Traj(filename)
