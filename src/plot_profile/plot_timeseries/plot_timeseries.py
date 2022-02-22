"""Plot variables of various measurement devices over time."""

# Standard library
import datetime
from pprint import pprint

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

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import colour_dict
from plot_profile.utils.utils import save_fig
from plot_profile.utils.variables import vdf


def create_plot(
    data,
    multi_axes,
    location,
    start,
    end,
    ymin,
    ymax,
    grid,
    datatypes,
    outpath,
    appendix,
    verbose,
):
    """Create timeseries plot.

    Args:
        data (dict): dictionary, containing one dataframe for each device
        multi_axes (bool): plot 2 yaxis if True
        devices (list): list of devices
        variables (list): list of variables (w/ same unit) to be added to plot
        location (str): abbreviation of station name
        start (datetime obj): start time
        end (datetime obj): end time
        ymin (tuple): y-min values
        ymax (tuple): y-max values
        grid (bool): add grid to plot or not
        datatypes (tuple): output data types
        outpath (str): output folder path
        appendix (bool): add appendix to output name
        verbose (bool): print details

    """
    # get location dataframe
    loc = sdf[location]
    devices = data.keys()

    # prepare figure
    fig, left_ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)
    if multi_axes:
        right_ax = left_ax.twinx()
    if grid:
        # align ticks by implementing ideas from:
        # https://stackoverflow.com/questions/20243683/matplotlib-align-twinx-tick-marks
        left_ax.grid(visible=True)
        right_ax.grid(visible=True)

    # apply limits to the y-axis/axes if some have been specified
    if ymin and ymax:
        if not multi_axes:
            left_ax.set_ylim(ymin[0], ymax[0])
            if len(ymin) != len(ymax):
                print(
                    f"WARNING: inconsistent number of y-axes limits provided! #min: {len(ymin)}, #max: {len(ymax)}"
                )
                print(f"Applied limits: ymin = {ymin[0]}, ymax = {ymax[0]}")

        else:  # there are two y axes
            if (
                len(ymin) == 1 and len(ymax) == 1
            ):  # user provided one ymin/ymax pair --> apply to the left axis
                left_ax.set_ylim(ymin[0], ymax[0])
            elif (
                len(ymin) == 2 and len(ymax) == 2
            ):  # user provided 2 ymin/xmax pairs --> apply to both axis
                left_ax.set_ylim(ymin[0], ymax[0])
                right_ax.set_ylim(ymin[1], ymax[1])
            else:  # ymin/ymax flags have been used iconsistently --> print warning
                print(
                    f"WARNING: inconsistent number of y-axes limits provided! #min: {len(ymin)}, #max: {len(ymax)}"
                )
                print(f"No y-axes limits have been applied.")

    left_ax.set_xlim(start, end)
    title = f"{loc.long_name}: {start.strftime('%d. %b, %H:%M')} - {end.strftime('%d. %b, %H:%M')}"
    left_ax.set_title(label=title)
    left_unit, right_unit = "", ""

    # plotting
    colour_index = 0
    for i, device in enumerate(devices):
        tmp = False
        # 1) retrieve df
        df = data[device]
        # df = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")
        if verbose:
            print(i, device)
            pprint(df)

        # x-axis information: dates/timestamps
        dates = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")

        # check if there are more than one variable in this dataframe
        if verbose:
            if len(df.columns) > 2:
                print(
                    f"There are more than one variable ({len(df.columns)}) in the df for: {device}"
                )
            else:
                print(
                    f"There is only one variable ({len(df.columns)}) in the df for: {device}"
                )

        # iterate over the c
        for (variable, columnData) in df.iteritems():
            if variable == "timestamp":
                continue

            # extract current variable
            if "~" in variable:
                var, level = (variable.split(sep="~"))[0], (variable.split(sep="~"))[1]
                tmp = True

            if tmp:
                variable = var

            variable = vdf[variable]
            unit = variable.unit
            var_short = variable.short_name
            y = columnData.values
            label = f"{var_short}: {device}"

            if tmp:
                label = f"{var_short}: {device} (level: {level})"

            # define unit for the left axes
            if not left_unit:
                left_unit = unit
                left_ax.set_ylabel(f"{left_unit}")

            # define unit for the right axes
            if (not right_unit) and (unit is not left_unit):
                right_unit = unit
                right_ax.set_ylabel(f"{right_unit}")

            # choose correct axes for the current variable and plot data
            if unit == left_unit:
                left_ax.plot(
                    dates,
                    y,
                    color=colour_dict[colour_index],
                    linestyle="-",
                    label=label,
                )
            if unit == right_unit:
                right_ax.plot(
                    dates,
                    y,
                    color=colour_dict[colour_index],
                    linestyle="-",
                    label=label,
                )

            colour_index += 1

    # add legends
    if multi_axes:
        h1, l1 = left_ax.get_legend_handles_labels()
        h2, l2 = right_ax.get_legend_handles_labels()
        left_ax.legend(h1 + h2, l1 + l2)
    else:
        left_ax.legend()

    # filename
    start_str = start.strftime("%y%m%d_%H")
    end_str = end.strftime("%y%m%d_%H")

    var_dev = ""
    for key in data:
        var_dev += f"_{key}"
        df = data[key]
        columns = df.columns.tolist()
        for column in columns:
            if column != "timestamp":
                var_dev += f"_{column}"

    filename = f"timeseries_{start_str}-{end_str}_{loc.short_name}{var_dev}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    return
