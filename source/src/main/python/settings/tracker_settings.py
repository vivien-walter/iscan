import configparser
import os

from input_output.folder_management import createFolder
from settings.manage_settings import config2dict
from settings.settings_files import getConfigPath
from trajectory.tracker_class import startSession

##-\-\-\-\-\-\-\-\-\-\
## TRACKER CONFIG CLASS
##-/-/-/-/-/-/-/-/-/-/

class TrackerConfig :
    def __init__(self, config, name=None):

        # Convert the config into a dictionary
        config_dict = config2dict(config)
        config_dict = config_dict[name]

        # Initialise the session
        self.name = name
        self.modified = False
        self.session = startSession()

        # Set the parameters
        # Object
        self.session.diameter = int( config_dict['diameter'] )
        self.session.minmass = float( config_dict['minmass'] )
        self.session.maxsize = _get_float_or_none( config_dict['maxsize'] )
        self.session.separation =  _get_float_or_none( config_dict['separation'] )
        self.session.percentile = float( config_dict['percentile'] )
        self.session.invert = config_dict['invert'] == 'True'
        # Filter
        self.session.noise_size = float( config_dict['noise_size'] )
        self.session.smoothing_size = _get_float_or_none( config_dict['smoothing_size'] )
        self.session.threshold = _get_float_or_none( config_dict['threshold'] )
        self.session.preprocess = config_dict['preprocess'] == 'True'
        self.session.topn = _get_int_or_none( config_dict['topn'] )
        # Other
        self.session.characterize = config_dict['characterize'] == 'True'
        self.session.engine = config_dict['engine']
        # Trajectory
        self.session.search_range = _get_float_or_none( config_dict['search_range'] )
        self.session.memory = _get_int_or_none( config_dict['memory'] )
        self.session.adaptive_stop = _get_float_or_none( config_dict['adaptive_stop'] )
        self.session.adaptive_step = float( config_dict['adaptive_step'] )
        self.session.neighbor_strategy = _get_str_or_none( config_dict['neighbor_strategy'] )
        self.session.link_strategy = _get_str_or_none( config_dict['link_strategy'] )
        self.session.filter_stubs = _get_int_or_none( config_dict['filter_stubs'] )

    # ---------------------------
    # Save the config in the file
    def save(self, file_name='trackers_config.ini'):

        # Get the content
        config = _open_config_file(file_name=file_name)

        # Replace the settings in the file
        _replace_settings(self, config, file_name=file_name)

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# ------------------------------------------
# Read the string and return None or a float
def _get_float_or_none(value):
    if value == 'None':
        return None
    else:
        return float(value)

# ---------------------------------------------
# Read the string and return None or an integer
def _get_int_or_none(value):
    if value == 'None':
        return None
    else:
        return int(value)

# --------------------------------------------
# Read the string and return None or the value
def _get_str_or_none(value):
    if value == 'None':
        return None
    else:
        return value

# -----------------------------------------------
# Initialise the config file if it does not exist
def _init_default_config(file_path):

    # Initialise the init parser
    config = configparser.RawConfigParser()

    # Get the first information in the init file
    config['Default'] = {
    # Object
    'diameter':21,
    'minmass':1,
    'maxsize':None,
    'separation':None,
    'percentile':64,
    'invert':True,
    # Filter
    'noise_size':1,
    'smoothing_size':None,
    'threshold':None,
    'preprocess':True,
    'topn':None,
    # Other
    'characterize':True,
    'engine':'auto',
    # Trajectory
    'search_range':20,
    'memory':5,
    'adaptive_stop':None,
    'adaptive_step':0.95,
    'neighbor_strategy':None,
    'link_strategy':None,
    'filter_stubs':40,
    }

    # Check if the folders exist
    if not os.path.exists(os.path.dirname(file_path)):
        createFolder(file_path)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

# -------------------------
# Open the user config file
def _open_config_file(file_name='trackers_config.ini'):

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
def _replace_settings(settings, config, file_name='trackers_config.ini'):

    # Extract data
    tracker_name = settings.name
    settings = settings.session

    # Replace the dictionary
    config[tracker_name] = {
    # Object
    'diameter':settings.diameter,
    'minmass':settings.minmass,
    'maxsize':settings.maxsize,
    'separation':settings.separation,
    'percentile':settings.percentile,
    'invert':settings.invert,
    # Filter
    'noise_size':settings.noise_size,
    'smoothing_size':settings.smoothing_size,
    'threshold':settings.threshold,
    'preprocess':settings.preprocess,
    'topn':settings.topn,
    # Other
    'characterize':settings.characterize,
    'engine':settings.engine,
    # Trajectory
    'search_range':settings.search_range,
    'memory':settings.memory,
    'adaptive_stop':settings.adaptive_stop,
    'adaptive_step':settings.adaptive_step,
    'neighbor_strategy':settings.neighbor_strategy,
    'link_strategy':settings.link_strategy,
    'filter_stubs':settings.filter_stubs,
    }

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ---------------------------------------
# Initialise the tracker if none is found
def initTrackerConfig(file_name='trackers_config.ini'):
    config = _open_config_file(file_name=file_name)

# ----------------------------------------------
# List all the trackers saved in the config file
def listTrackerConfigs(file_name='trackers_config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Convert the config into a dictionary
    config_dict = config2dict(config)

    return list( config_dict.keys() )

# ------------------------------------------
# Load the configuration file of the tracker
def loadTrackerConfig(tracker_name, file_name='trackers_config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Load in the class
    conf_class = TrackerConfig(config, name=tracker_name)

    return conf_class

# --------------------------------------------
# Edit the tracker settings in the config file
def editTrackerConfig(settings, file_name='trackers_config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Replace the settings in the file
    _replace_settings(settings, config, file_name=file_name)

# ---------------------------------------
# Delete the tracker from the config file
def deleteTracker(tracker_name, file_name='trackers_config.ini'):

    # Get the content
    config = _open_config_file(file_name=file_name)

    # Delete the selected tracker
    config.remove_section(tracker_name)

    # Get the path to the config file
    file_path = getConfigPath(file_name=file_name)

    # Save the file
    with open(file_path, 'w') as configfile:
        config.write(configfile)
