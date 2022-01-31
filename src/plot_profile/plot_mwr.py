"""Purpose: Plot microwave radiometer.

Author: Stephanie Westerhuis

Date: 05/12/2022.
"""

# Standard library
import datetime

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Local
from .utils import save_fig

# import ipdb


def mwr_heatmap(
    mwr_data, station, var, min_value, max_value, appendix, datatypes, outpath
):
    """Plot heatmap of MWR observational data.

    Args:
        mwr_data (pandas dataframe): data
        station (pandas dataframe): station
        var (pandas dataframe): variable
        min_value (float): minimal value
        max_value (float): maximum value
        appendix (str): append to file outname
        datatypes (str): output filetype
        outpath (str): path to output

    """
    plt.rcParams["figure.figsize"] = (7.5, 4.5)
    _, ax = plt.subplots()

    # copied from plot_icon
    # im = ax.pcolormesh(
    #    lt_dt_series,
    #    np.round(df_values.index.to_list()),
    #    df_values,
    #    shading="auto",
    #    cmap=var.colormap,
    # )
    # cbar = fig.colorbar(im, ax=ax)
    # cbar.ax.set_ylabel(f"{var.long_name} [{var.unit}]")

    # if var_min:
    #    im.set_clim(var_min, var_max)

    ax.set_title(f"MWR {var.long_name} @ {station.long_name}: ")
    ax.set_ylabel(f"Altitude [m asl]")
    plt.tight_layout()

    # save figure
    name = f'heatmap_mwr_{date.strftime("%y%m%d_%H")}_{station.short_name}_{var.short_name}'
    if appendix:
        name = name + "_" + appendix

    save_fig(
        filename=name,
        datatypes=[
            "png",
        ],
        outpath=outpath,
    )
    return
