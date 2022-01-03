"""Utils for various functions."""
# Standard library
import datetime as dt
import getpass
import logging
import sys
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt
import pandas as pd

# from numpy import NaN


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
            plt.savefig(filepath)
            print(f"--- file saved @ {filepath}")
        return
    else:
        for datatype in datatypes:
            filepath = Path(f"{outpath}/{filename}.{datatype}")
            Path(filepath).parents[0].mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath, dpi=200)
            print(f"--- file saved @ {filepath}")
        return


def slice_top_bottom(df_height, alt_top, alt_bot, verbose):
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
    for i, height in enumerate(df_height):
        if alt_bot:  # if a bottom altitude has been specified
            if height > alt_bot:
                if tmp:
                    lower_cut_off_index = (
                        i - 1
                    )  # include first value below bottom altitude as well
                    tmp = False
        else:
            if verbose:
                print("No bottom specified, use minimal height.")
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


# linestyles for several lead times
linestyle_dict = {
    0: "solid",
    1: "dashed",
    2: "dotted",
    3: "dashdot",
    4: (0, (1, 10)),  # loosely dotted
    5: (0, (5, 10)),  # loosely dashed
    6: (0, (3, 10, 1, 10)),  # loosely dashdotted
}
