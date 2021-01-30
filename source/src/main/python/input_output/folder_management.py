from glob import glob
import os
import shutil

from input_output.image_management import getImagesInfos, _open_image, saveStack

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -------------------------------
# Convert the folder into a stack
def _convert_folder(folder):

    # Open the folder
    image_array = _open_image(folder)

    # Build the path
    directory, name = os.path.split(folder)
    name += '.tif'

    # Save the array
    saveStack(image_array, os.path.join(directory, name), bit_depth=16, rescale=False)

# ----------------------------------------
# Retrieve the metadata file in the folder
def _get_metadata_file(folder):

    # List the possible format
    data_files = ['*.xml', '*.dat']

    # Check all formats
    metadata_file = ""
    for file_type in data_files:
        crt_file = glob( os.path.join(folder, file_type) )

        if len(crt_file) != 0:
            metadata_file = crt_file[0]

    return metadata_file

# ------------------------------------------------
# Delete the folder after saving the metadata file
def _delete_folder(folder):

    # Check if a metadata file can be found
    metadata_file = _get_metadata_file(folder)

    # Process the metadata file
    if metadata_file != "":

        # Rename and move
        file_dir, file_name = os.path.split(folder)
        _, ext = os.path.splitext(metadata_file)
        os.rename( os.path.join(folder, metadata_file), os.path.join(file_dir, file_name + ext) )

    # Delete the existing folder
    shutil.rmtree(folder)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# --------------------------
# Create the selected folder
def createFolder(file_path):

    # Create all the directories if needed
    try:
        os.makedirs(os.path.dirname(file_path))

    # Guard against race condition
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

# -------------------------
# Read directory of folders
def getImageFolderList(directory_path):

    # Get the list of all folders in the directory
    init_folder_list = glob( os.path.join(directory_path, '*', '') )

    # Get the list of folders that are compatible
    final_folder_list = []
    image_infos = []
    for crt_folder in init_folder_list:

        # Read the content of the folder
        image_list = glob( os.path.join(crt_folder, '*.tif*') )

        # Proceed if the list of images is not empty
        if len(image_list) != 0:

            # Append the folder to the list
            final_folder_list.append( os.path.split(os.path.split(crt_folder)[0])[1] )

            # Get the image infos
            image_infos.append( getImagesInfos(crt_folder) )

    return final_folder_list, image_infos

# -----------------------------------
# Convert the given folder to a stack
def convertFolders2Stacks(folder_list, delete_folders=True):

    # Process all the folders
    for folder_id, crt_folder in enumerate(folder_list):
        print('folder ' + str(folder_id+1) + ' / ' + str(len(folder_list)))

        # Convert the image
        _convert_folder(crt_folder)

        # Delete the folder if needed
        if delete_folders:
            _delete_folder(crt_folder)
