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
from plot_profile.plot_arome.variables_tmp import vdf

# from ipdb import set_trace


def create_plot(
    data,
    multi_axes,
    location,
    start,
    end,
    ymin,
    ymax,
    colours,
    grid,
    show_marker,
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
        colours (tuple): User-specified colours
        grid (bool): add grid to plot or not
        show_marker (bool): add marker to model plots or not
        datatypes (tuple): output data types
        outpath (str): output folder path
        appendix (bool): add appendix to output name
        verbose (bool): print details

    """
    # get location dataframe
    loc = sdf[location]
    devices = data.keys()

    # overwrite colour-dict with user-specified colours
    if isinstance(colours, tuple):
        for i, colour in enumerate(colours):
            colour_dict[i] = colour

    # prepare figure
    fig, left_ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)
    if multi_axes:
        right_ax = left_ax.twinx()
        if verbose:
            print("Creating right axis.")
    if grid:
        # align ticks by implementing ideas from:
        # https://stackoverflow.com/questions/20243683/matplotlib-align-twinx-tick-marks
        left_ax.grid(visible=True)
        # if multi_axes:
        #     right_ax.grid(visible=True)

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
    left_unit, right_unit = None, None

    # plotting
    colour_index = 0
    actual_devices = []
    for i, device in enumerate(devices):
        model = False
        # 1) retrieve df
        df = data[device]
        if verbose:
            print(i, device)
            pprint(df)

        # x-axis information: dates/timestamps
        dates = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S")

        # check if there are more than one variable in this dataframe
        if verbose:
            if len(df.columns) > 2:
                print(f"More than one variable in the df for {device}")
            else:
                print(f"Only one variable in the df for {device}")

        # iterate over the c
        for (variable, columnData) in df.iteritems():
            if variable == "timestamp":
                continue

            if verbose:
                print(f"  Variable: {variable}")

            # extract current variable
            if "icon" in device:
                # i.e. 2m_temp could be an icon variable w/o '~'; so make sure the model variable has the correct value!
                model = True
                level = None

            # specify marker
            if model and show_marker:
                marker = "d"
            else:
                marker = None

            # it is only possible for ICON variables to have '~' in them, because a level has to be specified.
            if "~" in variable:
                var, level = (variable.split(sep="~"))[0], (variable.split(sep="~"))[1]
                variable = var
                model = True

            variable = vdf[variable]
            unit = variable.unit
            var_long = variable.long_name
            y = columnData.values

            if model:
                if device.split("~")[1] != "0":
                    if not level:
                        label = f"{var_long}: {device.split('~')[0].upper()} {device.split('~')[1].upper()}"
                    else:
                        label = f"{var_long}: {device.split('~')[0].upper()} {device.split('~')[1].upper()} (Level: {level})"
                else:
                    if not level:
                        label = f"{var_long}: {device.split('~')[0].upper()}"
                    else:
                        label = f"{var_long}: {device.split('~')[0].upper()} (Level: {level})"

            # for observations, the label looks a bit differently
            if not model:  # 'icon' not in device and 'arome' not in device:
                device = device.split("~")[0]
                if "_" in device:
                    label = f"{var_long}: OBS @ {device.split('_')[0].upper()} {device.split('_')[1].upper()}"
                else:
                    label = f"{var_long}: OBS @ {device.upper()}"

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
                    marker=marker,
                    label=label,
                )
            if unit == right_unit:
                right_ax.plot(
                    dates,
                    y,
                    color=colour_dict[colour_index],
                    linestyle="-",
                    marker=marker,
                    label=label,
                )
            colour_index += 1

    # add legends
    if multi_axes:
        h1, l1 = left_ax.get_legend_handles_labels()
        h2, l2 = right_ax.get_legend_handles_labels()
        left_ax.legend(h1 + h2, l1 + l2, fontsize="small")
    else:
        left_ax.legend(fontsize="small")

    # filename
    start_str = start.strftime("%y%m%d_%H")
    end_str = end.strftime("%y%m%d_%H")

    var_dev = ""
    for key, df in data.items():

        # a) keys: "icon~0", "icon~1", "2m", "2m_tower"
        # remove "0" for model-levels
        if "~0" in key:
            key = key.split(sep="~")[0]
        var_dev += f"_{key}"

        # b) columns: "clct", "sw_up", "temp"
        columns = df.columns
        for column in columns:
            if column != "timestamp":
                var_dev += f"_{column}"
        if "icon" in key:
            # a) keys: "icon~ref", "icon~0", "2m~cbh", "2m_tower~temp"
            # remove "0" for model-levels
            if "~0" in key:
                key = key.split(sep="~")[0]
            var_dev += f"_{key}"

            # b) columns: "clct", "sw_up", "temp"
            columns = df.columns
            for column in columns:
                if column != "timestamp":
                    var_dev += f"_{column}"

#        elif "arome" in key:
#            print("changement ici")
#            # same as icon
#            if "~0" in key:
#                key = key.split(sep="~")[0]
#            var_dev += f"_{key}"
#
#            # b) columns: "clct", "sw_up", "temp"
#            columns = df.columns
#            for column in columns:
#                if column != "timestamp":
#                    var_dev += f"_{column}"

        else:  # now its actually a device --> remove variable from key
            var_dev += f"_{key.split('~')[0]}_{key.split('~')[1]}"

        # # b) columns: "clct", "sw_up", "temp"
        # columns = df.columns
        # for column in columns:
        #     if column != "timestamp":
        #         var_dev += f"_{column}"

    filename = f"timeseries_{start_str}-{end_str}_{loc.short_name}{var_dev}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    return
