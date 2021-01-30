import numpy as np

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------------------------------
# Get the maximal size that can be cropped around the tracks
def getCropSize(positions, array, window_size=50):

        # Extract the informations
        y_positions, x_positions = positions[:,1], positions[:,2]
        array_height, array_width = array.shape[1], array.shape[2]

        # Get the limiting positions
        y_min, y_max = np.amin(y_positions), np.amax(y_positions)
        x_min, x_max = np.amin(x_positions), np.amax(x_positions)

        # Check the limits of the image
        y_max = array_height - y_max
        x_max = array_width - x_max

        # Get the crop size
        crop_size = np.amin([y_min, y_max, x_min, x_max, window_size])

        return int(crop_size)

# --------------------
# Crop the image array
def cropImage(image_array, dimensions, origin=None):

    # New dimensions
    x_new, y_new = dimensions

    # Set the origin
    if origin is None:

        # Full image dimensions
        x_init = image_array.shape[-1]
        y_init = image_array.shape[-2]

        # Calculate the origin
        x0 = int( (x_init - x_new)/2 )
        y0 = int( (y_init - y_new)/2 )

    else:
        x0, y0 = origin

    # Get the other limit
    x1, y1 = x0 + x_new, y0 + y_new

    # Crop the array
    new_array = image_array[:,y0:y1,x0:x1]

    return new_array

# ------------------------------------------
# Crop a miniature around the given position
def cropMiniature(position, array, window_size=12):

    # Get the position
    y, x = position
    y, x = int(y), int(x)

    # Get the limits
    ymin, xmin = y - window_size, x - window_size
    if ymin < 0:
        ymin = 0
    if xmin < 0:
        xmin = 0

    ymax, xmax = y + window_size + 1, x + window_size + 1
    if ymax >= array.shape[0]:
        ymax = array.shape[0]
    if xmax >= array.shape[1]:
        xmax = array.shape[1]

    # Crop the array
    cropped_array = array[ymin:ymax, xmin:xmax]

    return cropped_array, (y - ymin, x - xmin)

# ---------------------------------
# Make the selection from the input
def getSubstackSelection(selection_text):

    # Split the commas
    all_elements = selection_text.split(',')

    # Process all the selections
    selection_list = []
    for selection in all_elements:

        # Split all the hyphens
        crt_items = selection.split('-')

        # Process the different situations
        if len(crt_items) == 1:
            selection_list.append([ int(crt_items[0]) ])

        elif len(crt_items) == 2:
            selection_list.append( list( range( int(crt_items[0]),int(crt_items[1])+1 ) ) )

        else:
            selection_list.append( list( range( int(crt_items[0]),int(crt_items[1])+1,int(crt_items[2]) ) ) )

    # Merge all the selections
    final_selection = []
    for selection in selection_list:
        for item in selection:
            if item not in final_selection:
                final_selection.append(item)

    # Sort the list
    final_selection.sort()

    return final_selection

# -----------------------------------------
# Make a substack using the given selection
def makeSubstack(image_array, selection):

    # Make the selection
    new_array = image_array[selection]

    return new_array
