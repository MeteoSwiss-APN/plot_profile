"""Purpose: Plot microwave radiometer.

Author: Stephanie Westerhuis

Date: 05/12/2022.
"""

# Standard library
import datetime
from pprint import pprint

# Third-party
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np

converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter

# Local
from ..utils.utils import save_fig


def mwr_heatmap(
    start,
    end,
    mwr_data,
    station,
    var,
    min_value,
    max_value,
    appendix,
    datatypes,
    outpath,
):
    """Plot heatmap of MWR observational data.

    Args:
        start (datetime): left limit of x-axis
        end (datetime): right limit of x-axis
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
    fig, ax = plt.subplots()

    im = ax.pcolormesh(
        mwr_data.columns.tolist(),
        np.round(mwr_data.index.to_list()),
        mwr_data,
        shading="auto",
        cmap=var.colormap,
    )
    # ax.axis("off")  # remove x-axis of heatmap
    ax.get_xaxis().set_visible(False)
    ax.set_xlim(left=start, right=end)
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(f"{var.long_name} [{var.unit}]")

    if min_value:
        im.set_clim(min_value, max_value)

    # IF no surface_data is added to heatmap, initialise new axes-instace which can be
    # formatted using the concise date formater
    if True:  # surface_data is None:
        ax_date = ax.twiny()
        ax_date.xaxis.set_ticks_position("bottom")
        ax_date.plot([start, end], [np.NaN, np.NaN])
        ax_date.set_xlim(start, end)

    ax.set_title(f"MWR {var.long_name} @ {station.long_name}: ")
    ax.set_ylabel(f"Altitude [m asl]")
    plt.tight_layout()

    # save figure
    filename = f'heatmap_mwr_{start.strftime("%y%m%d_%H")}-{end.strftime("%y%m%d_%H")}_{station.short_name}_{var.short_name}'
    if appendix:
        filename = filename + "_" + appendix

    datatypes = [
        "png",
    ]
    save_fig(
        filename=filename,
        datatypes=datatypes,
        outpath=outpath,
    )
    return
