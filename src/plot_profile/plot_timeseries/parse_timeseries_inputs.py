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


def parse_inputs(loc, var, device, add_model, add_obs, model_src, verbose):

    # create a dict out of model_src. each model id should be one key.
    model_src_dict = {}
    model_ids = []
    for source in model_src:
        id, dir, init_time = source[0], source[1], source[2]
        model_src_dict[id] = [dir, init_time]
        model_ids.append(id)

    # iterate through list of models and add init & folder to it
    l_model = []
    for model in add_model:
        if model[3] not in model_ids:
            print(
                f"--- No model source information provided for model w/ id: {model[3]}"
            )
            print(
                f"--- (Could just be a typo. Make sure the model ids in the --add_model & --model_src flags match)"
            )
            sys.exit(1)
        model = tuple(list(model) + (model_src_dict[model[3]]))
        l_model.append(model)

    if add_obs:
        l_obs = list(add_obs)
    else:
        l_obs = []

    elements = l_model + l_obs

    devs = [ele[0] for ele in elements]
    vars = [ele[1] for ele in elements]

    # check, wheter all desired variables are available for the provided location and corresponding devices
    for dev, var in zip(devs, vars):

        if verbose:
            print("checking inputs for: ", dev, var)
        check_inputs(var=var, dev=dev, loc=loc, verbose=verbose)

    # check, that the provided variables at most require 2 units
    multi_axes = check_units(vars)

    #################################################################################################################
    #################################################################################################################
    # legacy code
    ## CREATE TIMESERIES PLOTS USING THE --VAR & --DEVICE FLAGS
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
