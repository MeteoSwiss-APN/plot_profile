"""Utils for various functions."""
# Standard library
import getpass
import logging
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt


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
        df_height (pandas dataframe):   height variable
        alt_top (int):                  top
        alt_bot (int):                  bottom

    Returns:
        list of booleans

    """
    # exclude rows above specified altitude (alt_top)
    crit_upper = df_height < alt_top
    # set last False to True
    last_false = crit_upper[crit_upper == False]
    if len(last_false) > 0:
        crit_upper[last_false.index.max()] = True

    # exclude rows below specified altitude (alt_bot)
    if alt_bot is None:
        crit = crit_upper
        if verbose:
            print("No bottom specified, use minimal height.")
    else:
        crit_lower = df_height > alt_bot
        last_false = crit_lower[crit_lower == False]
        # include first False
        if len(last_false) > 0:
            crit_lower[last_false.index.max()] = True

        # combine selection criteria
        crit = crit_upper & crit_lower

    return crit
