"""Purpose: Visualise vertical profiles of variables from ICON simulation.

Author: Stephanie Westerhuis

Date: 25/11/2021.
"""

# Standard library
from pathlib import Path

# Third-party
# import ipdb
import matplotlib.pyplot as plt
import pandas as pd

# Local
from .utils import save_fig
from .variables import vdf


def create_plot(
    var_shortname,
    df_height,
    df_values,
    outpath,
    date,
    alt_bot,
    alt_top,
    loc,
    model,
    appendix,
    xmin,
    xmax,
    datatypes,
):
    """Plot vertical profile of variable.

    Args:
        var_shortname (str):            short name of variable
        df_height (pandas series):      contains the height values
        df_values (pandas dataframe):   values of variable at one or multiple leadtimes
        outpath (str):                  path where figure should be stored
        date (datetime obj):            init date of simulation
        alt_bot (int):                  lower boundary of altitude
        alt_top (int):                  upper boundary of altitude
        loc (str):                      location string
        model (str):                    name of nwp model
        appendix (str):                 add to output filename to e.g. distinguish versions
        xmin (float):                   minimum value of xaxis
        xmax (float):                   maximum value of xaxis
        datatypes (tuple):              tuple containig all desired datatypes for the output files

    """
    # specify variable (pandas dataframe with attributes)
    var = vdf[var_shortname]

    # figure settings
    plt.rcParams["figure.figsize"] = (4.5, 6)
    # plt.rcParams["figure.subplot.left"] = 0.15

    # dates
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # create figure
    fig, ax = plt.subplots()

    # loop over leadtimes to create one line for each leadtime
    for (lt, values) in df_values.iteritems():
        print(f"Plotting leadtime: {lt}")
        ax.plot(values, df_height.values, label=f"+ {lt:02} h")

    # define min and max values for xaxis
    if not xmin:
        xmin = var.min_value
    if not xmax:
        xmax = var.max_value

    # adjust appearance
    ax.set(
        xlabel=f"{var.long_name} [{var.unit}]",
        # xlim=(xmin, xmax),
        ylabel="Altitude [m asl]",
        ylim=(alt_bot, alt_top),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )
    ax.legend(fancybox=True)

    # save figure
    name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{loc}'
    if appendix:
        name = name + "_" + appendix
    plt.tight_layout()

    save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return
