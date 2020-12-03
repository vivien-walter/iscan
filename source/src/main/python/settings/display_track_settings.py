import configparser
import os

from input_output.folder_management import createFolder
from settings.manage_settings import config2dict
from settings.settings_files import getConfigPath

##-\-\-\-\-\-\-\-\-\
## USER CONFIG CLASS
##-/-/-/-/-/-/-/-/-/

class TrackDisplayConfig :
    def __init__(self, config):

        # Convert the config into a dictionary
        config_dict = config2dict(config)
        config_dict = config_dict['DISPLAY']

        ## - Get the booleans
        # Positions
        self.show_positions = config_dict['show_positions'] == 'True'
        self.current_position = config_dict['current_position'] == 'True'
        self.color_position = config_dict['color_position'] == 'True'
        # Paths
        self.show_paths = config_dict['show_paths'] == 'True'
        self.current_path = config_dict['current_path'] == 'True'
        self.color_path = config_dict['color_path'] == 'True'

    # ---------------------------
    # Save the config in the file
    def save(self, file_name='display_track_config.ini'):

        # Get the content
        config = _open_config_file(file_name=file_name)

        # Replace the settings in the file
        _replace_settings(self, config, file_name=file_name)

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['DISPLAY'] = {
    # Positions
    'show_positions':True,
    'current_position':False,
    'color_position':True,
    # Paths
    'show_paths':True,
    'current_path':False,
    'color_path':True,
    }

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# -------------------------
# Open the user config file
def _open_config_file(file_name='display_track_config.ini'):

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Initialise the config file if it does not exist
    if not os.path.exists(file_path):
        _init_default_config(file_path=file_path)

    # Load the content of the file
    config = configparser.RawConfigParser()
    config.read(file_path)

    return config

# -------------------------------------
# Replace the user settings in the file
def _replace_settings(settings, config, file_name='display_track_config.ini'):

    # Replace the dictionary
    config['DISPLAY'] = {
    # Positions
    'show_positions':settings.show_positions,
    'current_position':settings.current_position,
    'color_position':settings.color_position,
    # Paths
    'show_paths':settings.show_paths,
    'current_path':settings.current_path,
    'color_path':settings.color_path,
    }

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -----------------------------------------
# Load the track display configuration file
def loadDisplayTrackConfig(file_name='display_track_config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Load in the class
    conf_class = TrackDisplayConfig(config)

    return conf_class

# --------------------------------------------------
# Edit the track display settings in the config file
def editDisplayTrackConfig(settings, file_name='display_track_config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Replace the settings in the file
    _replace_settings(settings, config, file_name=file_name)
