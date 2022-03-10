"""Purpose: generate profiles for obs and models.

Author: Michel Zeller

Date: 09/03/2022.
"""

# Standard library
from pprint import pprint

# Third-party
import matplotlib.pyplot as plt

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import colour_dict
from plot_profile.utils.utils import save_fig
from plot_profile.utils.variables import vdf


def create_plot(
    data_dict,
    lt_dict,
    multi_axes,
    location,
    date,
    xlims,
    ylims,
    colours,
    grid,
    show_marker,
    datatypes,
    outpath,
    appendix,
    verbose=True,
):
    # get location dataframe
    loc = sdf[location]
    devices = data_dict.keys()

    # get ymin, ymax
    ymin = ylims[0]
    ymax = ylims[1]

    # determine ymin_dynamic from data & apply if ymin=None
    ymin_dynamic = None

    # overwrite colour-dict with user-specified colours
    if isinstance(colours, tuple):
        for i, colour in enumerate(colours):
            colour_dict[i] = colour

    # prepare figure
    fig, ax = plt.subplots(1, 1, figsize=(5, 8), tight_layout=True)
    if multi_axes:
        top_ax = ax.twiny()

    if grid:
        ax.grid(which="major", color="#DDDDDD", linewidth=0.8)
        ax.grid(which="minor", color="#EEEEEE", linestyle=":", linewidth=0.5)
        ax.minorticks_on()

    # xlims = (xmin, xmax) & xmin = (xmin1, xmin2) & xmax = (xmax1, xmax2)
    if xlims:
        xmins = xlims[0]
        xmaxs = xlims[1]
        if len(xmins) == len(xmaxs):
            if len(xmins) == 1:
                ax.set_xlim(xmins[0], xmaxs[0])
            if len(xmins) == 2:  # have xmins for two x-axes
                ax.set_xlim(xmins[0], xmaxs[0])
                top_ax.set_xlim(xmins[1], xmaxs[1])
        else:
            print(
                f"Check xmin/xmax values again. Got {len(xmins)} x-min values and {len(xmaxs)} x-max values."
            )
            print(f"Warning: No x-limits have been applied.")

    title = f"{loc.long_name}, {date.strftime('%d. %b, %Y, %H:%M')} UTC"
    if multi_axes:
        ax.set_title(label=title, bbox=dict(facecolor="none"), x=0.5, y=1.07)
    else:
        ax.set_title(label=title, bbox=dict(facecolor="none"), x=0.5, y=1.02)
    ax.set_ylabel(f"Altitude [m asl]")
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
        altitude_min = altitude.min()

        if ymin_dynamic == None:
            ymin_dynamic = altitude_min

        elif (ymin_dynamic is not None) and (altitude_min < ymin_dynamic):
            ymin_dynamic = altitude_min

        # check if there are more than one variable in this dataframe
        if verbose:
            if len(df.columns) > 2:
                print(f"More than one variable in the df for {device}")
            else:
                print(f"Only one variable in the df for {device}")

        # iterate over the columns
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

            if device in lt_dict:
                lt = lt_dict[device]

            if "~" in device:  # this means it must be a model (model~model_id)
                if device.split("~")[1] != "0":
                    label = f"{var_long}: {device.split('~')[0].upper()} {device.split('~')[1].upper()} ({lt}h)"
                else:
                    label = f"{var_long}: {device.split('~')[0].upper()} ({lt}h)"
            else:  # else it is a device
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
                if ("icon" in device) and show_marker:
                    ax.plot(
                        x,
                        altitude,
                        color=colour_dict[colour_index],
                        linestyle="-",
                        marker="d",
                        label=label,
                    )
                else:
                    ax.plot(
                        x,
                        altitude,
                        color=colour_dict[colour_index],
                        linestyle="-",
                        label=label,
                    )

            if unit == second_unit:
                if ("icon" in device) and show_marker:
                    top_ax.plot(
                        x,
                        altitude,
                        color=colour_dict[colour_index],
                        linestyle="-",
                        marker="d",
                        label=label,
                    )
                else:
                    top_ax.plot(
                        x,
                        altitude,
                        color=colour_dict[colour_index],
                        linestyle="-",
                        label=label,
                    )
            colour_index += 1

    # add ylim
    if ymin == None:
        ax.set_ylim(ymin_dynamic, ymax)
    else:
        ax.set_ylim(ymin, ymax)

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
            if column != "height":
                var_dev += f"_{column}"

    filename = f"profiles_{start_str}_{loc.short_name}{var_dev}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    first_unit, second_unit = None, None

    return
