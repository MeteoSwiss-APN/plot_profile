"""Check user inputs for subpackage plot_timeseries."""

# Standard library
import sys

# First-party
from plot_profile.utils.utils import check_inputs
from plot_profile.utils.variables import vdf


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


def parse_inputs(loc, var, device, add_model, add_obs, verbose):
    # create timeseries_plots using the '--add_obs' & '--add_model' flags
    if add_model or add_obs:
        add = list(add_obs) + list(
            add_model
        )  # this list also stores all elements that should be plotted incl. levels for icon variables
        elements = [
            list(item) for item in add
        ]  # convert list of tuples to list of lists
        devs = list([list[0] for list in add])
        vars = list([list[1] for list in add])

    # create timeseries plots using the '--var' & '--device' flags
    if device and var:
        device, variable = list(device), list(var)

        # CASE 1: multiple devices, 1 variable --> plot this one variable for all devices
        if len(variable) == 1 and len(device) > 1:
            vars = [variable[0]] * len(device)
            devs = list(device)

        # CASE 2: 1 device, multiple variables --> plot all variables for the single device
        elif len(device) == 1 and len(variable) > 1:
            devs = [device[0]] * len(variable)
            vars = list(variable)

        # CASE 3: multiple devices and multiple variables --> require len(device)==len(var)
        #  otherwise the assignment of variables to devices is ambiguous --> throw warning and exit
        elif len(device) == len(variable):
            devs = list(device)
            vars = list(variable)

        else:
            print(f"Assignement of devices and variables cannot be done explicitly.")
            print(
                f"Review command. (#variables: {len(variable)}, #devices: {len(device)})"
            )
            sys.exit(1)

        elements = []
        for dev, var in zip(devs, vars):
            elements.append([dev, var])

    # check, wheter all desired variables are available for the provided location and corresponding devices
    for dev, var in zip(devs, vars):
        # print('checking inputs for: ', dev, var)
        check_inputs(var=var, dev=dev, loc=loc, verbose=verbose)

    # check, that the provided variables at most require 2 units
    multi_axes = check_units(vars)

    return elements, devs, multi_axes
