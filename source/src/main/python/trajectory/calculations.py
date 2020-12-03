import numpy as np
from scipy.optimize import curve_fit
import trackpy as tp

##-\-\-\-\-\-\-\-\
## MATHS FUNCTIONS
##-/-/-/-/-/-/-/-/

# ------------------------
# Define a linear function
def _linear(x, a, b):
    return a*x + b

# ---------------------------
# Define a power law function
def _powerlaw(x, a, b):
    return a * (x ** b)

##-\-\-\-\-\-\-\-\-\
## PRIVATE FUNCTIONS
##-/-/-/-/-/-/-/-/-/

# -----------------------------------------
# Calculate the combined MSD of the objects
def _combined_MSD(trajectory, mpp, fps):

    # Get the MSD
    data_msd = tp.motion.emsd(trajectory, mpp, fps)

    # Split the data
    lagtime, msd = data_msd.index.to_numpy(), data_msd.to_numpy()

    return lagtime, msd

# ------------------------------
# Get the MSD of a group of path
def _group_MSD(trajectory, mpp, fps, path_id):

    # Get the selection from the path
    trj_mask = trajectory['particle'] == path_id[0]
    for id in path_id[1:]:
        trj_mask = trj_mask | (trajectory['particle'] == id)

    # Refine the trajectory
    refined_trajectory = trajectory[trj_mask]

    # Get the MSD
    data_msd = tp.motion.imsd(refined_trajectory, mpp, fps)

    # Split the data
    lagtime, msd = data_msd.index.to_numpy(), data_msd.to_numpy()

    return lagtime, msd

# ----------------------------
# Get the MSD of a single path
def _single_MSD(trajectory, mpp, fps, path_id):

    # Refine the trajectory
    trj_mask = trajectory['particle'] == path_id
    refined_trajectory = trajectory[trj_mask]

    # Get the MSD
    data_msd = tp.motion.msd(refined_trajectory, mpp, fps)

    # Split the data
    lagtime, msd = data_msd.index.to_numpy(), data_msd.to_numpy()

    return lagtime, msd

# ------------------------------------
# Fit the current MSD with a power law
def _fit_MSD(lagtime, msd):

    # Convert to log values
    log_lagtime, log_msd = np.log10(lagtime), np.log10(msd)

    # Remove NANs
    log_lagtime = log_lagtime[np.isfinite(log_msd)]
    log_msd = log_msd[np.isfinite(log_msd)]

    # Initialise the fit
    a_init = (log_msd[-1] - log_msd[0])/(log_lagtime[-1] - log_lagtime[0])
    b_init = log_msd[0] - a_init * log_lagtime[0]

    # Do the fit
    params, pcov = curve_fit(_linear, log_lagtime, log_msd, p0=[a_init, b_init])

    # Convert the parameters
    power = params[0]
    factor = np.exp( params[1] )
    params = np.array( [factor, power] )

    # Convert the errors
    perr = np.sqrt(np.diag( pcov ))
    err_power = perr[0]
    err_factor = factor * perr[1]
    perr = np.array( [err_factor, err_power] )

    return params, perr

##-\-\-\-\-\-\-\-\
## PUBLIC FUNCTIONS
##-/-/-/-/-/-/-/-/

# -------------------------------------
# Compute the Mean Squared Displacement
def getMSD(trajectory, mpp, fps, path_id = None):

    # Process all the paths
    if path_id is None:
        lagtime, msd = _combined_MSD(trajectory, mpp, fps)

    elif isinstance(path_id, list):
        lagtime, msd = _group_MSD(trajectory, mpp, fps, path_id)

    else:
        lagtime, msd = _single_MSD(trajectory, mpp, fps, path_id)

    return lagtime, msd

# ---------------------------------------
# Fit the MSD and compute the diffusivity
def getDiffusivity(lagtime, msd, dimension=2):

    # Initialise the values
    all_fits = []
    all_d = []
    all_d_err = []

    # Process all the elements
    for i in range(len(lagtime)):

        # Fit the values
        params, perr = _fit_MSD( lagtime[i], msd[i] )

        # Plot the fit
        lag_fit = np.linspace(lagtime[i][0], lagtime[i][-1], 10000)
        msd_fit = _powerlaw(lag_fit, *params)

        # Save the results
        all_fits.append( [lag_fit, msd_fit] )
        all_d.append( params[0]/(dimension * 2) )
        all_d_err.append( perr[0]/(dimension * 2) )

    return all_fits, all_d, all_d_err
