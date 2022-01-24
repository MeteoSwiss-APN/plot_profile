"""Plot variables of various measurement devices over time."""

# Standard library
import datetime
from datetime import datetime as dt

# Third-party
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pandas as pd

converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter

# Local
from .stations import sdf
from .utils import save_fig
from .variables import vdf


def create_plot(
    data,
    var,
    start,
    end,
    datatypes,
    outpath,
    grid,
    devices,
    loc,
    appendix,
    verbose,
):
    """Create timeseries plot.

    Args:
        data (dict): dictionary, containing one dataframe for each device
        var (tuple): list of variables (w/ same unit) to be added to plot
        start (datetime obj): start time
        end (datetime obj): end time
        datatypes (tuple): list of output data types
        outpath (str): output folder path
        grid (bool): add grid to plot or not
        devices (list): list of devices
        loc (str): abbreviation of station name (location)
        appendix (bool): add appendix to output name
        verbose (bool): print 'extra' statements during computation

    """
    variable = vdf[var]
    var_short = variable.short_name
    station = sdf[loc]
    ylabel = f"{variable.long_name} [{variable.unit}]"
    lims = (start, end)
    dates = pd.to_datetime(data[devices[0]]["timestamp"], format="%Y-%m-%d %H:%M:%S")
    fig, ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)

    line_style_dict = {
        0: "-",
        1: "-",
        2: "-",
        3: "-",
        4: (0, (1, 10)),
    }

    colour_dict = {
        0: "black",
        1: "blue",
        2: "red",
        3: "magenta",
        4: "cyan",
    }

    for i, device in enumerate(devices):
        label = f"{var_short}: {device}"
        y = data[device][var_short].values
        dates = pd.to_datetime(data[device]["timestamp"], format="%Y-%m-%d %H:%M:%S")
        print(i, device, len(y), len(dates))
        ax.plot(dates, y, color=colour_dict[i], linestyle="-", label=label)

    ax.set_xlim(lims)
    title = f"Station: {station.long_name} | Period: {dt.strftime(start, '%d %b %H:%M')} - {dt.strftime(end, '%d %b %H:%M')}"
    ax.set_title(label=title)
    ax.set_ylabel(ylabel)
    ax.legend()

    if grid:
        ax.grid(visible=True)

    filename = f"ts_{start.day}{start.hour}_{end.day}{end.hour}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    return
