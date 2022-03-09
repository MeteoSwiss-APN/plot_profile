"""Purpose: generate profiles for obs and models.

Author: Michel Zeller

Date: 09/03/2022.
"""

# Standard library
from pprint import pprint

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import colour_dict
from plot_profile.utils.utils import save_fig
from plot_profile.utils.variables import vdf


def create_plot(
    data_dict,
    multi_axes,
    location,
    date,
    xlims,
    ylims,
    grid,
    datatypes,
    outpath,
    appendix,
    verbose=True,
):
    # get location dataframe
    loc = sdf[location]
    devices = data_dict.keys()

    # prepare figure
    fig, ax = plt.subplots(1, 1, figsize=(5, 8), tight_layout=True)
    if multi_axes:
        top_ax = ax.twiny()
        top_ax.set_ylim(ylims[0], ylims[1])

        if verbose:
            print("Creating top axis.")
    if True:  # grid:
        ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
        ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)
        ax.minorticks_on()

    # apply limits to the y-axis/axes if some have been specified
    ax.set_ylim(ylims[0], ylims[1])

    if xlims[0] and xlims[1]:
        ax.set_xlim(xlims[0], xlims[1])
        # TODO: implement xlims s.t. several xlims can be provided for
        # the top and bottom x-axis (w/ two different units)

    title = f"{loc.long_name}, {date.strftime('%d. %b, %H:%M')}"
    ax.set_title(label=title, bbox=dict(boxstyle="round", facecolor="none"), loc="left")
    ax.set_ylabel(f"Altitude [m] (asl)")
    first_unit, second_unit = None, None

    # plotting
    colour_index = 0
    for i, device in enumerate(devices):
        model = False
        # 1) retrieve df
        df = data_dict[device]
        if verbose:
            print(i, device)
            pprint(df)

        # y-axis information: altitude
        altitude = df["height"]

        # check if there are more than one variable in this dataframe
        if verbose:
            if len(df.columns) > 2:
                print(f"More than one variable in the df for {device}")
            else:
                print(f"Only one variable in the df for {device}")

        # iterate over the c
        for (variable, columnData) in df.iteritems():
            if variable == "height":
                continue

            if verbose:
                print(f"  Variable: {variable}")

            # extract current variable
            variable = vdf[variable]
            unit = variable.unit
            var_long = variable.long_name
            x = columnData.values

            if "~" in device:
                label = f"{var_long}: {device.split('~')[0].upper()} {device.split('~')[1].upper()}"
            else:
                label = f"{var_long}: {device.upper()}"

            # define unit for the bottom axis
            if not first_unit:
                first_unit = unit
                ax.set_xlabel(f"{first_unit}")

            # define unit for the right axes
            if (not second_unit) and (unit is not first_unit):
                second_unit = unit
                top_ax.set_xlabel(f"{second_unit}")

            # choose correct axes for the current variable and plot data
            if unit == first_unit:
                ax.plot(
                    x,
                    altitude,
                    color=colour_dict[colour_index],
                    linestyle="-",
                    label=label,
                )
            if unit == second_unit:
                top_ax.plot(
                    x,
                    altitude,
                    color=colour_dict[colour_index],
                    linestyle="-",
                    label=label,
                )

            colour_index += 1

    # add legends
    if multi_axes:
        h1, l1 = ax.get_legend_handles_labels()
        h2, l2 = top_ax.get_legend_handles_labels()
        ax.legend(h1 + h2, l1 + l2, fontsize="small")
    else:
        ax.legend(fontsize="small")

    # filename
    start_str = date.strftime("%y%m%d_%H")

    var_dev = ""
    for key, df in data_dict.items():

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

    filename = f"timeseries_{start_str}_{loc.short_name}{var_dev}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    first_unit, second_unit = None, None

    return
