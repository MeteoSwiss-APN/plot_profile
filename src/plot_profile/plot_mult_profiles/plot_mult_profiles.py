"""Purpose: generate profiles for obs and models at multiple leadtimes.

Author: Arthur Dandoy

Date: 04/05/2022.
"""

# Standard library
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
    variable,
    leadtimes,
    date_ref,
    location,
    xlims,
    ylims,
    grid,
    datatypes,
    outpath,
    verbose=False,
):
    # get location dataframe
    loc = sdf[location]

    # get devices
    devices = data_dict.keys()

    # get ymin, ymax
    ymin = ylims[0]
    ymax = ylims[1]

    # determine ymin_dynamic from data & apply if ymin=None
    ymin_dynamic = None

    # prepare figure
    fig, ax = plt.subplots(1, 1, figsize=(5, 8), tight_layout=True)

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
        else:
            print(
                f"Check xmin/xmax values again. Got {len(xmins)} x-min values and {len(xmaxs)} x-max values."
            )
            print(f"Warning: No x-limits have been applied.")

    first_unit = None

    # variable informations
    variable = vdf[variable]
    unit = variable.unit
    var_long = variable.long_name

    color = variable.color

    device_namelist = []
    device_title = None

    # plotting
    for i, device in enumerate(devices):

        if "~" in device:
            device_name = device.split("~")[0]
            device_lt = device.split("~")[1]
        else:
            device_name, device_title = device, device
            device_lt = None

        if device_name not in device_namelist:
            device_namelist.append(device_name)

        # 1) retrieve df
        try:
            df = data_dict[device]
        except KeyError:
            print(f"! no data for: {device_name} at leadtime: {device_lt} :(")
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

        # equivalent to if observations
        if device_name != device:
            lt = device.split("~")[1]
            index = list(leadtimes).index(int(lt))
            label = f"{var_long}: {device_name.upper()} (+{lt}h)"

            # define unit for the bottom axis
            if not first_unit:
                first_unit = unit
                ax.set_xlabel(f"{first_unit}")

            # avoid KeyError if column name is "0"
            columns = df.columns
            x = df[columns[1]]

            # choose correct axes for the current variable and plot data
            ax.plot(
                x,
                altitude,
                color=color,
                linestyle=linestyle_dict[index],
                label=label,
            )

        # if model, a df column for each leadtime
        else:
            for k, lt in enumerate(leadtimes):

                label = f"{var_long}: {device_name.upper()} (+{lt}h)"

                # define unit for the bottom axis
                if not first_unit:
                    first_unit = unit
                    ax.set_xlabel(f"{first_unit}")

                # avoid KeyError if column name is "0"
                columns = df.columns
                x = df[columns[k + 1]]

                # choose correct axes for the current variable and plot data
                ax.plot(
                    x,
                    altitude,
                    color=color,
                    linestyle=linestyle_dict[k],
                    label=label,
                )
    # title
    if device_title == None:
        device_title = "OBS"
    title = f"{device_title.upper()}, {loc.short_name}, ref: {date_ref.strftime('%d. %b, %Y, %H:%M')} UTC"

    ax.set_title(label=title, bbox=dict(facecolor="none"), x=0.5, y=1.02)
    ax.set_ylabel(f"Altitude [m asl]")

    # add ylim
    if ymin == None:
        ax.set_ylim(ymin_dynamic, ymax)
    else:
        ax.set_ylim(ymin, ymax)

    ax.legend(fontsize="small")

    # filename
    start_str = date_ref.strftime("%y%m%d_%H")

    var_dev = f"{variable.short_name}_lt"

    for lt in leadtimes:
        var_dev += f"~{str(lt)}"

    for devname in device_namelist:
        var_dev += f"~{devname}"

    filename = f"profiles_{start_str}_{loc.short_name}_{var_dev}"
    save_fig(filename, datatypes, outpath, fig=fig)
    plt.clf()
    first_unit = None

    return
