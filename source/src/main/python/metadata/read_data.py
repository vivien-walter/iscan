import xml.etree.ElementTree as xml

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ----------------------------
# Read the experiment metadata
def _read_experiment_metadata(root):

    # Get the general settings
    general_data = {}
    for child in root:
        if child.tag != 'Pictures':
            general_data[child.tag] = child.text

    # Get all the pictures information
    picture_dict = {}
    picture_list = [x for x in root if x.tag == 'Pictures'][0]

    # Loop over all the images
    for picture in picture_list:

        # Get all the data
        crt_data = {}
        for picture_data in picture:
            if picture_data.tag == 'Index':
                picture_id = 'Frame '+picture_data.text
            else:
                crt_data[picture_data.tag] = picture_data.text

        # Save the dictionary
        picture_dict[picture_id] = crt_data

    return {'General':general_data, 'Frames':picture_dict}

# -----------------------------
# Read the fast record metadata
def _read_fast_record_metadata(root):

    # Get the general settings
    general_data = {}
    for child in root:
        if child.tag != 'Pictures':
            general_data[child.tag] = child.text

    # Get all the pictures information
    picture_dict = {}
    picture_list = [x for x in root if x.tag == 'Pictures'][0]

    # Loop over all the images
    for picture in picture_list:

        # Append info the general dict
        if 'Frame' not in picture.tag or picture.tag == 'NbrFrames':
            general_data[picture.tag] = picture.text

        # Populate the picture dict
        else:
            picture_id = picture.tag

            # Get all the data
            crt_data = {}
            for picture_data in picture:
                crt_data[picture_data.tag] = picture_data.text

            picture_dict[picture_id] = crt_data

    return {'General':general_data, 'Frames':picture_dict}

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------
# Read the content of a metadata file
def readMetadataFile(file_path):

    # Load the file
    tree = xml.parse(file_path)
    root = tree.getroot()

    # Detect which type of file is being read
    if 'Name' in [x.tag for x in root]:
        data_type = 'experiment'
        data_content = _read_experiment_metadata(root)
    else:
        data_type = 'fast_record'
        data_content = _read_fast_record_metadata(root)

    return data_type, data_content
