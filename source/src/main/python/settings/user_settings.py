import configparser
import os

from input_output.folder_management import createFolder
from settings.manage_settings import config2dict
from settings.settings_files import getConfigPath

##-\-\-\-\-\-\-\-\-\
## USER CONFIG CLASS
##-/-/-/-/-/-/-/-/-/

class UserConfig :
    def __init__(self, config):

        # Convert the config into a dictionary
        config_dict = config2dict(config)
        config_dict = config_dict['USER']

        ## - Get the booleans
        # General
        self.single_images = config_dict['single_images'] == 'True'
        self.autoload_images = config_dict['autoload_images'] == 'True'
        self.auto_background = config_dict['auto_background'] == 'True'
        self.dark_theme = config_dict['dark_theme'] == 'True'
        # Image
        self.crop_image = config_dict['crop_image'] == 'True'
        self.crop_size = int(config_dict['crop_size'])
        self.correct_signed = config_dict['correct_signed'] == 'True'
        self.correction_type = config_dict['correction_type']
        self.background_type = config_dict['background_type']
        self.correct_intensity = config_dict['correct_intensity'] == 'True'
        self.correct_newtab = config_dict['correct_newtab'] == 'True'
        # Scale
        self.space_scale = float( config_dict['space_scale'] )
        self.space_unit = config_dict['space_unit']
        self.frame_rate = float( config_dict['frame_rate'] )
        # Other(s)
        self.tracker = config_dict['tracker']

    # ---------------------------
    # Save the config in the file
    def save(self, file_name='config.ini'):

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
    config['USER'] = {
    # General
    'single_images':False,
    'autoload_images':False,
    'auto_background':False,
    'dark_theme':True,
    # Image
    'crop_image':True,
    'crop_size':512,
    'correct_signed':True,
    'correction_type':'Division',
    'background_type':'Median',
    'correct_intensity':True,
    'correct_newtab':False,
    # Scale
    'space_scale':44.9,
    'space_unit':'micron',
    'frame_rate':150,
    # Other(s)
    'tracker':'Default'
    }

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# -------------------------
# Open the user config file
def _open_config_file(file_name='config.ini'):

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
def _replace_settings(settings, config, file_name='config.ini'):

    # Replace the dictionary
    config['USER'] = {
    # General
    'single_images':settings.single_images,
    'autoload_images':settings.autoload_images,
    'auto_background':settings.auto_background,
    'dark_theme':settings.dark_theme,
    # Image
    'crop_image':settings.crop_image,
    'crop_size':settings.crop_size,
    'correct_signed':settings.correct_signed,
    'correction_type':settings.correction_type,
    'background_type':settings.background_type,
    'correct_intensity':settings.correct_intensity,
    'correct_newtab':settings.correct_newtab,
    # Scale
    'space_scale':settings.space_scale,
    'space_unit':settings.space_unit,
    'frame_rate':settings.frame_rate,
    # Other(s)
    'tracker':settings.tracker,
    }

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------
# Load the configuration file
def loadUserConfig(file_name='config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Load in the class
    conf_class = UserConfig(config)

    return conf_class

# -----------------------------------------
# Edit the user settings in the config file
def editUserConfig(settings, file_name='config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Replace the settings in the file
    _replace_settings(settings, config, file_name=file_name)
