##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------------------------
# Convert a config content into a dictionary
def config2dict(configs):

    # Process all sections
    conf_dict = {}
    for section in configs.sections():

        # Initialise the section dictionary
        conf_dict[section] = {}

        # Process all subsections
        for subsection in configs[section]:
            conf_dict[section][subsection] = configs[section][subsection]

    return conf_dict

# ------------------------------------
# Convert a config content into a list
def config2list(configs):

    # Process all sections
    conf_dict = {}
    for section in configs.sections():

        # Process all subsections
        for subsection in configs[section]:
             conf_dict[int(subsection)] = configs[section][subsection]

    # Get and sort the keys
    conf_indices = list(conf_dict.keys())
    conf_indices.sort()

    # Make the list
    conf_list = []
    for key in conf_indices:
        conf_list.append( conf_dict[key] )

    return conf_list
