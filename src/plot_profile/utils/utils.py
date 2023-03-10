"""Utils for various functions."""
# Standard library
import datetime as dt
import getpass
import logging
import sys
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.variables import vdf

# from ipdb import set_trace


def count_to_log_level(count: int) -> int:
    """Map occurrence of the command line option verbose to the log level."""
    if count == 0:
        return logging.ERROR
    elif count == 1:
        return logging.WARNING
    elif count == 2:
        return logging.INFO
    else:
        return logging.DEBUG


def save_fig(filename, datatypes, outpath, fig=None):
    """Save current figure at outpath.

    Create outpath if it doesn't exist or
    default to /scratch/<user>/tmp/.

    Args:
        filename:       str     Name of File.
        datatypes:      tuple   Tuple containig the desired output file types
        outpath:        str     Path to output directory
        fig:            Figure  Figure which should be saved. If None, get current figure.

    """
    fig = fig or plt.gcf()

    if not outpath:
        for datatype in datatypes:
            username = getpass.getuser()
            filepath = Path(f"/scratch/{username}/tmp/{filename}.{datatype}")
            Path(filepath).parents[0].mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=200)
            print(f"--- file saved @ {filepath}")
        return
    else:
        for datatype in datatypes:
            filepath = Path(f"{outpath}/{filename}.{datatype}")
            Path(filepath).parents[0].mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=200)
            print(f"--- file saved @ {filepath}")
        return


def slice_top_bottom(df_height, alt_top, alt_bot, verbose=False):
    """Criteria to cut away top and bottom of dataframe.

    Args:
        df_height (pandas series):      height variable
        alt_top (int):                  top
        alt_bot (int):                  bottom

    Returns:
        list of booleans; rows containing True are to be kept in the original dataframe

    """
    # create pandas series of len(df_height) full of NaN values
    crit = pd.Series(
        len(df_height) * [False]
    )  # change False to NaN if so desired (other changes necessary as well!)

    # get index values to slice the dataframe
    tmp = True
    upper_cut_off_index = len(df_height)  # default

    for i, height in enumerate(df_height):
        if alt_bot:  # if a bottom altitude has been specified
            if height > alt_bot:
                if tmp:
                    lower_cut_off_index = (
                        i - 1
                    )  # include first value below bottom altitude as well
                    tmp = False
        else:
            # if verbose:
            #    print("No bottom specified, use minimal height.")
            lower_cut_off_index = 0

        if height > alt_top:
            upper_cut_off_index = i + 1  # include first value above top altitude
            break

    # assign True to the relevant rows of crit
    crit.iloc[lower_cut_off_index:upper_cut_off_index] = True

    return crit


def validtime_from_leadtime(date, leadtime, verbose=False):
    """Calculate validtime from leadtime.

    Args:
        date (str or datetime obj): start of simulation (YYmmddHH or YYYYmmddHH)
        leadtime (int):             leadtime in hours
        verbose (bool):             print details

    Returns:
        datetime object

    """
    if isinstance(date, dt.datetime):
        ini = date
    else:
        try:
            ini = dt.datetime.strptime(date, "%y%m%d%H")
        except ValueError:
            try:
                ini = dt.datetime.strptime(date, "%Y%m%d%H")
            except ValueError:
                print(f"! problem in validtime_from_leadtime in utils.py!")
                print(f"  -> {date} does not match any known format")
                sys.exit()

    validtime = ini + dt.timedelta(hours=leadtime)

    if verbose:
        print(f"{date} + {leadtime}h = {validtime.strftime('%y%m%d%H')}")

    return validtime


def check_inputs(var, loc, dev, verbose):
    """Check if the variables/stations are in the dataframes.

    Args:
        var (str): variable(s)
        loc (str): station id (i.e. gla for Glarus)
        dev (str): device (i.e. 2m, 5cm,...)
        verbose (bool): add print statements to output or not

    """
    print(dev)
    # 1) check if location is available
    try:
        station = sdf[loc]
    except KeyError:
        print(f"! {loc} is not listed as an available station.")
        sys.exit(1)

    # 2) check if variables are defined for given devices

    # for icon
    if dev == "icon":
        if isinstance(vdf[var].icon_name, str):
            return
        else:
            print(f"--- selected variable: {vdf[var].long_name} not available for icon")
            sys.exit(1)

    # for arome
    if dev == "arome":
        if isinstance(vdf[var].arome_name, str):
            return
        else:
            print(
                f"--- selected variable: {vdf[var].long_name} not available for arome"
            )
            sys.exit(1)

    # only for DWH variables
    try:
        var_for_device = vdf[var].dwh_id[dev]
        if verbose:
            print(f"--- selected variable: {vdf[var].long_name} for device: {dev}")
        return

    except KeyError:
        print(f"! {var} is not available as variable for device: {dev}")
        sys.exit(1)


# linestyles, i.e. for several lead times
linestyle_dict = {
    0: "solid",
    1: "dashed",
    2: "dotted",
    3: "dashdot",
    4: (0, (1, 10)),  # loosely dotted
    5: (0, (5, 10)),  # loosely dashed
    6: (0, (3, 10, 1, 10)),  # loosely dashdotted
}

# colours, i.e .for different devices
colour_dict = {
    0: "black",
    1: "blue",
    2: "red",
    3: "green",
    4: "cyan",
    5: "magenta",
    6: "yellow",
    7: "grey",
    8: "chartreuse",
    9: "peru",
}


def get_cubehelix_colors(number_of_colors, start=0.1, stop=0.7):
    """Get colors list from cubehelix colormap.

    Args:
        number_of_colors (int):   number of colors to be in the list
        start (float, optional): color or the first color. Defaults to 0.1.
        stop (float, optional):  color of the last color. Defaults to 0.7.

    Returns:
        list : list of colors

    """
    cm_subsection = np.linspace(start, stop, number_of_colors)

    colors = [cm.cubehelix(x) for x in cm_subsection]

    return colors


def get_icon_name(ds, var, verbose):
    """Determine icon name for this variable from list of possible names.

    Args:
        ds (xr.dataset): dataset
        icon_names (list): list of possible names

    Returns:
        icon_name (str)

    """
    
    for name in var.icon_names:

        # test name
        if name in list(ds.keys()):
            
            # return this
            if verbose:
                print(f"  found {name} in dataset.")
            
            return name
        else:
            if verbose:
                print(f"  {name} does not match.")

    print(f"!  icon_names listed of variable {var.short_name} do not appear in current input dataset")
    sys.exit(1)


def get_dim_names(ds_var, verbose):
    """Retrieve dimension names for specific variable in xarray dataframe.

    Names for time/level/index - dimensions are listed in
    possible_xxx_names. For a given dataset containing only
    1 variable the function deduces the dimension names.

    Args:
        ds_var (xarray df): dataframe for 1 variable
        verbose (bool): print details

    Returns:
        dim_time (str)
        dim_index (str)
        dim_level (str)

    """
    possible_time_names = [
        "time",
    ]
    possible_index_names = ["ncells", "cells_1", "cells"]
    possible_level_names = [
        "height",
        "height_1",
        "height_2",
        "height_3",
        "height_4",
        "level",
        "level_1",
        "z_1",
        "z_2",
        "z_3",
    ]

    dim_time = None
    dim_index = None
    dim_level = None

    # loop over dims given in dataset
    for dim_name in ds_var.dims:

        # check for time names
        for time_name in possible_time_names:
            if time_name == dim_name:
                dim_time = time_name

                if verbose:
                    print(f"Found dim_time: {dim_time}.")
                break

        # check for index names
        for index_name in possible_index_names:
            if index_name == dim_name:
                dim_index = index_name

                if verbose:
                    print(f"Found dim_index: {dim_index}.")
                break

        # check for level names
        for level_name in possible_level_names:
            if level_name == dim_name:
                dim_level = level_name

                if verbose:
                    print(f"Found dim_level: {dim_level}.")
                break

    return dim_time, dim_index, dim_level


def get_grid_names(ds_grid, verbose=False):

    possible_lats_names = ["clat", "clat_1"]
    possible_lons_names = ["clon", "clon_1"]
    possible_height_names = [
        "HHL",
        "hhl",
        "HEIGHT",
    ]
    possible_index_names = ["cells_1", "ncells", "cells"]

    for coo in ds_grid.coords:

        # clat
        for name in possible_lats_names:
            if name == coo:
                lats_name = name
                if verbose:
                    print(f"Found lats_name: {lats_name}.")
                break

        # clon
        for name in possible_lons_names:
            if name == coo:
                lons_name = name
                if verbose:
                    print(f"Found lons_name: {lons_name}.")
                break

    for var in ds_grid.variables:

        # half level height
        for name in possible_height_names:
            if name == var:
                height_name = name
                if verbose:
                    print(f"Found height_name: {height_name}.")
                break

    for dim in ds_grid[height_name].dims:

        # cell index name for height variable
        for name in possible_index_names:
            if name == dim:
                height_index_name = name
                if verbose:
                    print(f"Found height index name: {height_index_name}.")
                break

    return lats_name, lons_name, height_name, height_index_name


def deaverage(arr):
    """De-average values in array.

    Values of some variables have been averaged
    since beginning of the model simulation.

    Args:
        arr (1d array): ICON output variable

    Returns:
        1d array: de-averaged output

    """
    # length of input
    n = len(arr)

    # fill with nan (first value will stay nan)
    de_arr = np.empty(n)
    de_arr[:] = np.nan

    # calculate de-averaged values
    for i in range(1, len(arr)):
        de_arr[i] = arr[i] * (i) - arr[i - 1] * (i - 1)

    return de_arr


def decumulate(arr):
    """De-cumulate values in array.

    Values of some variables have been cumulated
    since beginning of the model simulation.

    Args:
        arr (1d array): arome output variable

    Returns:
        1d numpy nd array: de-averaged output

    """
    arr = arr.to_numpy()
    arr = arr[1:] - arr[:-1]
    arr = np.insert(arr, 0, np.nan)

    return arr


def calc_qv_from_td(td, p):
    """Calculate qv from dewpoint temperature.

    Args:

        td (array): dewpoint temp in °C
        p (array):  pressure in hPa

    Returns:
        array (qv in g/kg)

    """
    e = 6.112 * np.exp((17.67 * td) / (td + 243.5))
    qv = (0.622 * e) / (p - (0.378 * e)) * 1000  # to get g/kg
    # equivalent formula would be:
    # from calculating spec. hum. from dew point temperatures github-discussion
    # after eq. 4.24 in Practical Meteorology from Stull
    # td=td+273.15
    # qv = (622*6.113*np.exp(5423*(td-273.15)/(td*273.15)))/p
    return qv


def parse_grid_file(height_file, model_src):

    if not height_file:
        grid = Path(model_src, "lfff00000000c.nc")
    else:
        grid = Path(model_src, height_file)

    print(grid)
    return grid
