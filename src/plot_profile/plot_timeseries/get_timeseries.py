"""Check user inputs for subpackage plot_timeseries and retrieve available data."""


# Standard library
import sys
from pprint import pprint

# Local
from ..plot_icon.get_icon import get_icon_timeseries
from ..utils.dwh_retrieve import dwh_retrieve
from ..utils.stations import sdf
from ..utils.utils import check_inputs
from ..utils.variables import vdf

# from ipdb import set_trace


def get_timeseries_dict(
    start, end, variable, loc, device, init, level, folder, grid_file, verbose
):
    # check, that the provided variables at most require 2 units
    units = []
    for var in list(set(variable)):
        units += [vdf[var].unit]

    if len(set(units)) > 2:
        print(f"Can only create plots w/ 2 different units.")
        print(f"Provided variables have the following units: {list(set(units))}")
        sys.exit(1)

    if len(set(units)) == 2:
        multi_axes = True

    else:
        multi_axes = False

    # merge devices and variables

    # CASE 1: multiple devices, 1 variable (i.e. len(device)>1 && len(var)==1)
    #  --> plot this one variable for all devices
    if len(variable) == 1 and len(device) > 1:
        variables = [variable[0]] * len(device)
        devices = list(device)

    # CASE 2: single device, multiple vars (i.e. len(device)==1 && len(var)>1)
    #  --> plot all variables for the single device
    elif len(device) == 1 and len(variable) > 1:
        devices = [device[0]] * len(variable)
        variables = list(variable)

    # CASE 3: multiple devices and multiple variables --> require len(device)==len(var)
    #  otherwise the assignment of variables to devices is ambiguous --> throw
    elif len(device) == len(variable):
        devices = list(device)
        variables = list(variable)

    else:
        print(f"Assignement of devices and variables cannot be done explicitly.")
        print(f"Review command. (#variables: {len(variable)}, #devices: {len(device)})")
        sys.exit(1)

    # check, wheter all desired variables are available for the provided location and corresponding devices:
    for dev, var in zip(devices, variables):
        # print('checking inputs for: ', dev, var)
        check_inputs(var=var, dev=dev, loc=loc, verbose=verbose)

    # retrieve for each device one dataframe, containing all corresponding variables
    timeseries_dict = {}
    for dev in list(set(devices)):

        # get indices of variables corresponding to dev
        vars_indices = [
            device for device in range(len(devices)) if devices[device] == dev
        ]
        # create list w/ variables correpsonding to dev
        vars = []
        for index in vars_indices:
            vars += [variables[index]]

        # device = icon
        if dev == "icon":
            timeseries_dict["icon"] = get_icon_timeseries(
                lat=sdf[loc].lat,
                lon=sdf[loc].lon,
                vars=vars,
                init=init,
                level=level,
                start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                folder=folder,
                grid_file=grid_file,
                verbose=verbose,
            )
            # go to next variable
            continue

        # all other devices which are retrievable from DWH
        timeseries_dict[dev] = dwh_retrieve(
            device=dev,
            station=loc,
            vars=vars,
            timestamps=[start, end],
            verbose=False,  # TODO: change False to verbose
        )

    return timeseries_dict, multi_axes
