"""Purpose: Visualise vertical profiles of variables from ICON simulation.

Author: Stephanie Westerhuis

Date: 25/11/2021.
"""

# Standard library
from pathlib import Path

# Third-party
# Standard packages
# import ipdb
import matplotlib.pyplot as plt
import pandas as pd

# Local
# Local packages
from .variables import vdf


def create_plot(
    var_shortname, df_height, df_values, outpath, date, alt_bot, alt_top, loc, model
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

    # adjust appearance
    ax.set(
        xlabel=f"{var.long_name} [{var.unit}]",
        xlim=(var.min_value, var.max_value),
        ylabel="Altitude [m asl]",
        ylim=(alt_bot, alt_top),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )
    ax.legend(fancybox=True)

    # save figure
    name = f'{model}_{loc}_{date.strftime("%y%m%d%H")}_{var.short_name}'
    plt.tight_layout()
    plt.savefig("/scratch/swester/tmp/dummy.png")
