import numpy as  np
import pandas as pd
import trackpy as tp

##-\-\-\-\-\-\-\-\-\
## PARTICLE SELECTION
##-/-/-/-/-/-/-/-/-/

# -------------------------------------------------
# Select the closest particle to the given position
def selectClosestParticle(trajectories, reference):

    # Calculate the distances between the particle and the reference
    distances = np.sqrt(np.sum( (trajectories - reference)**2, axis=1))

    # Return the closest particle to the reference
    closestParticle = trajectories[ np.argmin(distances) ]

    return closestParticle

# ---------------------------------------------
# Select the closest path to the given position
def selectClosestPath(trajectories, reference, frame):

    # Get the list of the particle found
    particle_list = np.unique(trajectories['particle'])

    # Initialize the selection
    selected_particle = 0
    selected_distance = 1e+32
    for particle in particle_list:

        # Extract the particle specific positions
        particle_trajectory = trajectories[ trajectories['particle'] == particle ]

        # Get the position array
        particle_frames = np.array( particle_trajectory['frame'] )
        particle_positions = np.array( [particle_trajectory['x'], particle_trajectory['y']] ).T

        # Calculate the distances
        distances = np.sqrt(np.sum( (particle_positions - reference)**2, axis=1))
        current_frame = abs( particle_frames - frame )
        current_distance = distances[np.argmin(current_frame)]

        # Check if the path is closer
        if current_distance < selected_distance:
            selected_particle = particle
            selected_distance = current_distance

    # Return the values
    particle_trajectory = trajectories[ trajectories['particle'] == selected_particle ]

    return np.array( [particle_trajectory['frame'],  particle_trajectory['x'], particle_trajectory['y']] ).T


##-\-\-\-\-\-\-\-\
## PARTICLE FINDER
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Locate all the particles in the array
def locateParticle(array, invert=False, particle_size = 45, min_mass = 20):

    # Locate the particles
    particleCollection = tp.locate(array, particle_size, invert=invert, minmass=min_mass)

    particlePosition = np.array( [particleCollection['x'], particleCollection['y']] ).T

    return particlePosition

# -------------------------------
# Find all the paths in the array
def locatePath(array, particle_size=45, min_mass = 20, min_frame = 10, memory=3, invert=False):

    # Process all the frames
    particleCollection = tp.batch(array[:], particle_size, minmass=min_mass, invert=invert)

    filteredCollection = tp.link_df(particleCollection, particle_size, memory=memory)
    filteredCollection = tp.filter_stubs(filteredCollection, min_frame)

    return filteredCollection

# ----------------------------------------
# Find a single particle in a reduced area
def findSingleParticle(array, position, crop_size=50, particle_size=45, invert=False):

    # Crop the array to reduce the calculation time
    croppedArray = cropImage(position, array, size=crop_size)
    center = (np.array(croppedArray.shape) / 2).astype(int)

    # Locate all particles in the area
    particlesPosition = locateParticle(croppedArray, particle_size=particle_size, invert=invert)

    # Convert to absolute coordinates
    particlesPosition = np.rint(particlesPosition - center + position).astype(int)

    # Only keep the closest particle to the position
    if particlesPosition.shape[0] == 1:
        return particlesPosition[0]
    else:
        return selectClosestParticle(particlesPosition, position)

##-\-\-\-\-\-\-\-\
## PATH GENERATION
##-/-/-/-/-/-/-/-/

# ----------------------------------------------------
# Complete automatically the missing frame in the path
def completePath(path, number_frames):

    # Take the very first position of the array as reference
    initial_position = np.array([ path.positions[0] ])

    # Complete the first points if missing
    if path.positions[0,0] != 0:

        # Use the first point saved as reference for all the initial missing points
        for i in range( path.positions[0,0] ):
            initial_position[0,0] = i
            path.positions = np.append(path.positions, np.copy(initial_position), axis=0)
        path.positions = np.sort( path.positions.view('i8,i8,i8'), order=['f0'], axis=0 ).view(np.int)

    # Loop over all the points in the path
    for i in range(number_frames):

        # Add the previous position if current position is missing
        if i not in path.positions[:,0]:
            initial_position[0,0] = i
            path.positions = np.append(path.positions, np.copy(initial_position), axis=0)
            path.positions = np.sort( path.positions.view('i8,i8,i8'), order=['f0'], axis=0 ).view(np.int)

        # Move the reference position
        initial_position = np.array([ path.positions[i] ])

# ---------------------------
# Manual creation of the path
def generateManualPath(path, position, frame, canEdit=False):

    # Array to append if needed
    newArrayPosition = np.array( [[frame, position[0], position[1]]] )

    # Initialize the array if needed
    if path.positions is None:
        path.positions = newArrayPosition

    # Edit the path
    else:
        # Append if the frame hasn't been saved yet
        if frame not in path.positions[:,0]:
            path.positions = np.append(path.positions, newArrayPosition, axis=0)
            path.positions = np.sort( path.positions.view('i8,i8,i8'), order=['f0'], axis=0 ).view(np.int)

        # Edit if permitted
        elif canEdit:
            path.positions[ path.positions[:,0]==frame, 1 ] = position[0]
            path.positions[ path.positions[:,0]==frame, 2 ] = position[1]

# ------------------------------------------------------------------------
# Generate a single path automatically, based on the position of the click
def generateAutomaticSinglePath(array, path, position, frame, tracking_option=None):

    # Use default options or retrieve them from the input parameters
    if tracking_option is None:
        crop_size=200
        particle_size = 45
        invert = False
        min_mass = 20
        min_frame = 10
        memory = 3
    else:
        crop_size = tracking_option['crop_size']
        particle_size = tracking_option['particle_size']
        invert = tracking_option['invert']
        min_mass = tracking_option['min_mass']
        min_frame = tracking_option['min_frame']
        memory = tracking_option['memory']

    # Reduce the size of the stack for fast processing
    croppedStack = cropImage(position, array, size=crop_size)
    center = (np.array(croppedStack.shape) / 2).astype(int)

    # Find all trajectories in the given array
    all_particles = locatePath(croppedStack, particle_size=particle_size, invert=invert, min_mass = min_mass, min_frame = min_frame, memory=memory)

    # Re-center the particles
    all_particles['x'] = np.rint(all_particles['x'] - center[1] + position[0]).astype(int)
    all_particles['y'] = np.rint(all_particles['y'] - center[2] + position[1]).astype(int)

    # Select the appropriate path
    path.positions = selectClosestPath(all_particles, position, frame)

# -----------------------------------
# Find all the paths inside the array
def generateAutomaticPaths(image, array, tracking_option=None):

    # Retrieve options
    particle_size = tracking_option['particle_size']
    invert = tracking_option['invert']
    min_mass = tracking_option['min_mass']
    min_frame = tracking_option['min_frame']
    memory = tracking_option['memory']

    # Find all trajectories in the given array
    all_particles = locatePath(array, particle_size=particle_size, invert=invert, min_mass = min_mass, min_frame = min_frame, memory=memory)

    # Append all the paths found to the list of paths
    for particle in np.unique(all_particles['particle']):

        particle_trajectory = all_particles[ all_particles['particle'] == particle ]
        particle_position = np.array( [particle_trajectory['frame'],  particle_trajectory['x'], particle_trajectory['y']] ).T

        newPath = trajectory()
        newPath.positions = np.copy(particle_position)

        image.path_saved.append(newPath)

##-\-\-\-\-\-\-\-\-\-\
## CALCULATION ON PATHS
##-/-/-/-/-/-/-/-/-/-/

# ---------------------------------------------------------
# Calculate the maximum size possible for the cropped array
def getMaxCropSize(positions, image_size):

    # Get the limits of the path array
    t, x_min, y_min = np.amin(positions, axis=0)
    t, x_max, y_max = np.amax(positions, axis=0)

    # Get the size limits
    all_limits = [x_min, y_min, image_size[0]-x_max, image_size[1]-y_max]

    return np.amin(all_limits)

# ---------------------------------------
# Merge all the MSD in a single dataframe
def mergeMSD(path_dictionnary, ignore_index):

    # Process all paths
    msd_dataframe = []
    for path_index in path_dictionnary.keys():

        if path_dictionnary[path_index]['index'] not in ignore_index:

            # Append the MSD in the list
            tmp_msd = path_dictionnary[path_index]['msd']
            msd_dataframe.append( tmp_msd.copy() )

        else:
            path_dictionnary[path_index]['display'] = False

    # Merge the MSD
    msd_dataframe = pd.concat(msd_dataframe, ignore_index=True)

    return msd_dataframe

# -------------------------------
# Calculate the MSD using trackpy
def calculateMSD(path_dictionnary, max_tau, micron_per_pixel = 1, fps=1):

    # Process all the paths in the dictionnary
    for path_index in path_dictionnary.keys():

        # Get the current trajectory
        tmp_trajectory = path_dictionnary[path_index]['trajectory']

        # Compute the msd
        tmp_msd = tp.motion.msd(tmp_trajectory, micron_per_pixel, fps, max_tau)
        tmp_msd = tmp_msd[['lagt','msd']]

        # Append the index of the path
        tmp_msd['path_index'] = np.array( [path_index]*len(tmp_msd['lagt']) )

        # Append the dataframe to the structures
        path_dictionnary[path_index]['msd'] = tmp_msd

# ----------------------------------------
# Calculate the diffusitivity of all paths
def calculateDiffusion(path_dictionnary, ignore_index, do_all=False):

    # Store all the value
    all_tau = []
    all_msd = []

    # Process all the paths in the dictionnary
    for i in path_dictionnary.keys():

        # Get the MSD from the dictionnary
        tmp_msd = path_dictionnary[i]['msd']

        if do_all:
            # Calculate the diffusitivity
            fitParam, fitError = fitMSD(np.array(tmp_msd['lagt']), np.array(tmp_msd['msd']))

            # Save the results
            path_dictionnary[i]['power_law'] = fitParam
            path_dictionnary[i]['power_law_error'] = fitError
            path_dictionnary[i]['D'] = fitParam[0] / 4
            path_dictionnary[i]['D_error'] = fitError[0] / 4

        if path_dictionnary[i]['index'] not in ignore_index:
            # Append to the lists
            all_tau = np.copy(np.array( tmp_msd['lagt'] ))
            all_msd.append( np.copy(np.array( tmp_msd['msd'] )) )

    # Merge all MSD
    if len(all_msd) == 1:
        all_msd = all_msd[0]
        all_msd_error = None
    else:
        all_msd = np.array(all_msd).T
        all_msd_error = np.std(all_msd, axis=1, ddof=1)
        all_msd = np.mean(all_msd, axis=1)

    # Fit the general MSD
    fitParam, fitError = fitMSD(all_tau, all_msd, all_msd_error)

    diff = [ fitParam[0]/4,fitError[0]/4 ]
    powerlaw = [ fitParam, fitError ]

    return diff, powerlaw

##-\-\-\-\-\-\-\-\-\
## SAVE TRAJECTORIES
##-/-/-/-/-/-/-/-/-/

# --------------------------------------
# Save the selected trajectory in a file
def saveTrajectoryInFile(parent, path, file_type = "csv"):

    # Generate the data array
    valuesArray = np.copy( path.positions )

    # Apply the calibration if any

    # Save the file in the appropriate format
    if file_type == 'csv':

        # Generate the header
        columnNames = ['frame','x (px)','y (px)']

        # Save the file
        saveDataFile(parent, valuesArray, name_array=columnNames)

    elif file_type == 'xml':

        # Prepare the properties/informations for the XML generator
        element_names = ['Tracks','particle','detection']
        column_names = ['t','x','y','z']
        track = {
        'nTracks': "1",
        'spaceUnits': 'pixels',
        'frameInterval': "1.0",
        'timeUnits': 'frames',
        'generationDateTime': "None",
        'from':"iSCAN " + parent.version
        }
        particle = { 'nSpots': str(valuesArray.shape[0]) }

        # Convert the array into an XML object
        valuesXML, stringXML = array2XML(valuesArray, element_names, column_names, data_attributes=track, item_attributes=particle)

        # Save the XML file
        saveTextFile(parent, stringXML.decode("utf-8") , extension='.xml')

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## CLASS TO HANDLE TRAJECTORIES
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/

class trajectory:
    def __init__ (self):

        # Elements of the path
        self.positions = None
        self.time_option = 'all'
        self.colour = 'black'

##-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
## IMPORT ISCAN MODULES TO AVOID CYCLIC CONFLICTS
##-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/

from iscan.input_output.data_files import saveDataFile, array2XML, saveTextFile
from iscan.operations.general_functions import fitMSD
from iscan.operations.image_calculation import cropImage
