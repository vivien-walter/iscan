import configparser
import os

from input_output.folder_management import createFolder
from settings.manage_settings import config2list
from settings.settings_files import getConfigPath

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['Recent'] = {
    }

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# -------------------------
# Open the user config file
def _open_config_file(file_name='recent_files.ini'):

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    if not os.path.exists(file_path):
        _init_default_config(file_path=file_path)

    # Load the content of the file
    config = configparser.RawConfigParser()
    config.read(file_path)

    return config

# -----------------------------------------
# Replace the recent files list in the file
def _append_settings(new_file, config, file_name='recent_files.ini'):

    # Get the list
    config_list = config2list(config)

    # Update the list
    new_list = [new_file]
    for item in config_list:
        if item not in new_list:
            new_list.append(item)

    # Reinitialise the dictionary
    config['Recent'] = {}

    # Fill the dictionary
    for i, item in enumerate(new_list):
        if i < 10:
            config['Recent'][str(i)] = str(item)

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# --------------------------------------
# Delete the selecter file from the file
def _delete_settings(file_to_remove, config, file_name='recent_files.ini'):

    # Get the list
    config_list = config2list(config)

    # Update the list
    new_list = []
    for item in config_list:
        if item != file_to_remove:
            new_list.append(item)

    # Reinitialise the dictionary
    config['Recent'] = {}

    # Fill the dictionary
    for i, item in enumerate(new_list):
        if i < 10:
            config['Recent'][str(i)] = str(item)

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ----------------------------------
# List all the files recently opened
def listRecentFiles(file_name='recent_files.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Convert the config into a dictionary
    config_list = config2list(config)

    return config_list

# ---------------------------------------------
# Append a new file to the list of recent files
def appendRecentFiles(new_file, file_name='recent_files.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Replace the settings in the file
    _append_settings(new_file, config, file_name=file_name)

# ---------------------------
# Remove a file from the list
def deleteRecentFiles(file_to_remove, file_name='recent_files.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Replace the settings in the file
    _delete_settings(file_to_remove, config, file_name=file_name)
