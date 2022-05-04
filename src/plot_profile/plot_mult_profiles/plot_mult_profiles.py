"""Purpose: generate profiles for obs and models at multiple leadtimes.

Author: Arthur Dandoy

Date: 04/05/2022.
"""

# Standard library
import sys
from pprint import pprint

# Third-party
import matplotlib.pyplot as plt
import pandas as pd

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import linestyle_dict
from plot_profile.utils.utils import save_fig
from plot_profile.utils.variables import vdf

# from ipdb import set_trace


def create_mult_plot(
    data_dict,
    date_ref,
    multi_axes,
    location,
    xlims,
    ylims,
    grid,
    show_marker,
    datatypes,
    outpath,
    appendix,
    verbose=False,
):
    # get location dataframe
    loc = sdf[location]

    # if leadtimes is string transform it to a 1 element list
    # if isinstance(leadtimes, str):
    #    leadtimes = [
    #        leadtimes,
    #    ]

    # get leadtimes
    leadtimes = list(data_dict.keys())

    # get devices
    devices = data_dict[str(leadtimes[0])].keys()

    # get ymin, ymax
    ymin = ylims[0]
    ymax = ylims[1]

    # determine ymin_dynamic from data & apply if ymin=None
    ymin_dynamic = None

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

    title = f"{loc.long_name}, Ref: {date_ref.strftime('%d. %b, %Y, %H:%M')} UTC"
    if multi_axes:
        ax.set_title(label=title, bbox=dict(facecolor="none"), x=0.5, y=1.07)
    else:
        ax.set_title(label=title, bbox=dict(facecolor="none"), x=0.5, y=1.02)
    ax.set_ylabel(f"Altitude [m asl]")
    first_unit, second_unit = None, None

    # plotting
    for k, lt in enumerate(leadtimes):
        for i, device in enumerate(devices):
            # model = False
            # 1) retrieve df
            try:
                df = data_dict[str(lt)][device]
            except KeyError:
                print(f"! no data for: {device} at leadtime: {lt} :(")
                # sys.exit(1)
                df = pd.DataFrame()
                continue

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
                color = variable.color

                # if device in lt_dict:
                #    lt = lt_dict[device]

                if "~" in device:  # this means it must be a model (model~model_id)
                    if device.split("~")[1] != "0":
                        label = f"{var_long}: {device.split('~')[0].upper()} {device.split('~')[1].upper()} (+{lt}h)"
                    else:
                        label = f"{var_long}: {device.split('~')[0].upper()} (+{lt}h)"
                else:  # else it is a device
                    label = f"{var_long}: {device.upper()} (+{lt}h)"

                # define unit for the bottom axis
                if not first_unit:
                    first_unit = unit
                    ax.set_xlabel(f"{first_unit}")

                # define unit for the right axes
                if (not second_unit) and (unit is not first_unit):
                    second_unit = unit
                    top_ax.set_xlabel(f"{second_unit}")

                # specify marker
                if (("icon" or "arome") in device) and show_marker:
                    marker = "d"
                else:
                    marker = None

                # choose correct axes for the current variable and plot data
                if unit == first_unit:
                    ax.plot(
                        x,
                        altitude,
                        color=color,
                        linestyle=linestyle_dict[k],
                        marker=marker,
                        label=label,
                    )

                if unit == second_unit:
                    top_ax.plot(
                        x,
                        altitude,
                        color=color,
                        linestyle=linestyle_dict[k],
                        marker=marker,
                        label=label,
                    )

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
    start_str = date_ref.strftime("%y%m%d_%H")

    var_dev = "_lt"

    for lt in leadtimes:
        var_dev += f"~{str(lt)}"

    for device in devices:
        df = data_dict[str(leadtimes[0])][device]
        if "~" in device:
            device = device.split(sep="~")[0]
        columns = df.columns
        for column in columns:
            if column != "height":
                var_dev += f"_{device}~{column}"

    filename = f"profiles_{start_str}_{loc.short_name}{var_dev}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    first_unit, second_unit = None, None

    return
