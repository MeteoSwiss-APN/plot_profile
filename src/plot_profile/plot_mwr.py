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


def mwr_heatmap(mwr_data, var, station, datatypes, outpath):
    """Plot heatmap of MWR observational data.

    Args:
        mwr_data (pandas dataframe): data
        var (pandas dataframe): variable
        station (pandas dataframe): station
        datatypes (str): output filetype
        outpath (str): path to output

    """
    plt.rcParams["figure.figsize"] = (7.5, 4.5)
    fig, ax = plt.subplots()

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
    # filename = f'mwr_heatmap_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{station.short_name}'
    filename = f"mwr_heatmap_{var.short_name}_{station.short_name}"
    if appendix:
        filename = name + "_" + appendix

    save_fig(
        filename=filename,
        datatypes=[
            "png",
        ],
        outpath=outpath,
    )
    return
