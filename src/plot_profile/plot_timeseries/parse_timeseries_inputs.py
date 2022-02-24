"""Check user inputs for subpackage plot_timeseries."""

# Standard library
import sys

# First-party
from plot_profile.utils.utils import check_inputs
from plot_profile.utils.variables import vdf

# from ipdb import set_trace


def check_units(vars):
    units = []
    for var in list(set(vars)):
        units += [vdf[var].unit]

    if len(set(units)) > 2:
        print(f"Can only create plots w/ 2 different units.")
        print(f"Provided variables have the following units: {list(set(units))}")
        sys.exit(1)

    if len(set(units)) == 2:
        multi_axes = True

    else:
        multi_axes = False

    return multi_axes


def parse_inputs(loc, var, device, add_model, add_obs, folder, init, verbose):

    n_model = len(add_model)
    n_obs = len(add_obs)

    # add folder and init information to add_model
    # create list "folders_inits" for each "add_model"
    if n_model > 0:

        # if only 1 folder and 1 init has been specified:
        #  -> same for all add_model-inputs
        # if multiple folders OR inits have been specified
        #  -> connect tuples

        n_folder = len(folder)
        n_init = len(init)

        if n_folder == 1 and n_init == 1:
            folder_init = (folder[0], init[0])
            folders_inits = [
                folder_init,
            ] * n_model
        elif n_folder == n_init == n_model:
            folders_inits = list(zip(folder, init))
        elif n_folder == 1 and n_init == n_model:
            folders_inits = list(zip((folder[0],) * n_init, init))
        elif n_folder == n_model and n_init == 1:
            folders_inits = list(zip(folder, (init[0],) * n_folder))
        else:
            print(f"--- ! Specified folders and inits cannot be combined!")
            print(f"---   {n_model} model instances specified")
            print(f"---   {n_init} inits specified")
            print(f"---   {n_folder} folder specified")
            sys.exit(1)

    # list containing model information as 6-item tuples
    #   model-name, variable, level, 'identification',input-folder, init-time
    l_model = []
    for t in range(n_model):
        l_model.append(add_model[t] + folders_inits[t])

    # list for observations (just to be consistent)
    if n_obs > 0:
        l_obs = list(add_obs)
    else:
        l_obs = []

    elements = l_model + l_obs

    devs = [ele[0] for ele in elements]
    vars = [ele[1] for ele in elements]

    # check, wheter all desired variables are available for the provided location and corresponding devices
    for dev, var in zip(devs, vars):
        # print('checking inputs for: ', dev, var)
        check_inputs(var=var, dev=dev, loc=loc, verbose=verbose)

    # check, that the provided variables at most require 2 units
    multi_axes = check_units(vars)

    # create timeseries plots using the '--var' & '--device' flags
    # if device and var:
    #    device, variable = list(device), list(var)

    #    # CASE 1: multiple devices, 1 variable --> plot this one variable for all devices
    #    if len(variable) == 1 and len(device) > 1:
    #        vars = [variable[0]] * len(device)
    #        devs = list(device)

    #    # CASE 2: 1 device, multiple variables --> plot all variables for the single device
    #    elif len(device) == 1 and len(variable) > 1:
    #        devs = [device[0]] * len(variable)
    #        vars = list(variable)

    #    # CASE 3: multiple devices and multiple variables --> require len(device)==len(var)
    #    #  otherwise the assignment of variables to devices is ambiguous --> throw warning and exit
    #    elif len(device) == len(variable):
    #        devs = list(device)
    #        vars = list(variable)

    #    else:
    #        print(f"Assignement of devices and variables cannot be done explicitly.")
    #        print(
    #            f"Review command. (#variables: {len(variable)}, #devices: {len(device)})"
    #        )
    #        sys.exit(1)

    #    elements = []
    #    for dev, var in zip(devs, vars):
    #        elements.append([dev, var])
    return elements, multi_axes
