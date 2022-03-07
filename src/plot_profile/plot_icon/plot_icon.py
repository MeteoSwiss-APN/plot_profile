"""Purpose: Visualise vertical profiles of variables from ICON simulation.

Author: Stephanie Westerhuis

Date: 25/11/2021.
"""

# Standard library
import datetime
import datetime as dt
import sys
from pprint import pprint

# Third-party
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# First-party
from plot_profile.plot_rs.plot_rs import plot_clouds
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import calc_qv_from_td
from plot_profile.utils.utils import linestyle_dict
from plot_profile.utils.utils import save_fig
from plot_profile.utils.variables import vdf

converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter

# from ipdb import set_trace


def get_yrange(alt_bot, alt_top, df_height):
    """Define values for lower and upper boundary of plot.

    Args:
        alt_bot (int):
        alt_top (int):
        df_height (pandas Series):

    Returns:
        tuple of float: min height, max height

    """
    if alt_bot is None:
        ymin = int(df_height.values.min())
    else:
        ymin = alt_bot

    ymax = alt_top

    return ymin, ymax


def str_valid_time(ini, lt):
    """Calculate valid time, create nice string.

    Args:
        ini (datetime obj):     init date and time
        lt (int):               leadtime

    Returns:
        str:                    valid time (HH:MM)

    """
    valid = ini + dt.timedelta(hours=lt)

    return valid.strftime("%H:%M")


def add_obs(ax, obs_dict, var, add_clouds, relhum_thresh, verbose=False):
    """Add obs data to ax."""
    try:
        rs_data = obs_dict["rs"]

        # loop over timestamps
        for i, (timestamp, sounding) in enumerate(rs_data.items()):

            values = None

            # for other radiosounding variables
            if var.short_name in ["temp", "dewp_temp", "wind_vel", "wind_dir"]:
                values = sounding[var.short_name]

            # calculate qv from td and pressure
            if var.short_name == "qv":
                values = calc_qv_from_td(sounding["dewp_temp"], sounding["press"])

            # plot radiosounding profiles
            if isinstance(values, pd.Series):
                alt = sounding["altitude"]
                ax.plot(
                    values,
                    alt,
                    label=f"RS: {timestamp.strftime('%b %d, %H')}",
                    color="black",
                    linestyle=linestyle_dict[i],
                )
                ax.legend()

            # add cloud shading
            if add_clouds:
                plot_clouds(
                    df=sounding,
                    relhum_thresh=relhum_thresh,
                    print_steps=verbose,
                    ax=ax,
                    case="single",
                )

    except (TypeError, KeyError) as e:
        if verbose:
            print("No radiosounding obs added.")

    return ax


def plot_single_variable(
    data_dict,
    obs_dict,
    variable,
    outpath,
    date,
    add_clouds,
    relhum_thresh,
    alt_bot,
    alt_top,
    loc,
    model,
    appendix,
    xmin,
    xmax,
    xrange_fix,
    datatypes,
    df_height,
    verbose,
    show_grid,
    show_marker,
    zeroline,
):
    print(f"--- creating plot for variable {variable}")

    # check if data dictionary looks reasonable
    # print(f"data_dict =\n{data_dict}")

    # load values from dictionary
    # test whether variable is even available
    try:
        df_values = data_dict[variable]
    except KeyError:
        print(f"No plot is generated for {variable}.")
        return

    # specify variable (pandas dataframe with attributes)
    var = vdf[variable]

    # figure settings
    plt.rcParams["figure.figsize"] = (5, 6)
    # plt.rcParams["figure.subplot.left"] = 0.15

    # dates
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # create figure
    _, ax = plt.subplots()

    # add grid to figure
    if show_grid:
        ax.xaxis.grid(color="black", linestyle="--", linewidth=0.5)
        ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)

    # add zero-line to figure
    if zeroline:
        ax.axvline(linewidth=1.5, color="k")

    # specify marker
    if show_marker:
        marker = "o"
    else:
        marker = None

    # define color sequence
    #  if only 1 leadtime: color from variable dataframe
    #  if multiple leadtimes: seaborn husl color palette
    lts = df_values.columns  # leadtimes
    if len(lts) == 1:
        colors = [
            var.color,
        ]
    else:
        colors = sns.color_palette("husl", n_colors=len(lts))

    # loop over leadtimes to create one line for each leadtime
    icolor = 0
    for (lt, values) in df_values.iteritems():
        if verbose:
            print(f"Adding leadtime: {lt}.")

        ax.plot(
            values,
            df_height.values,
            label=f"{str_valid_time(date, lt)} (+{lt:02}h)",
            color=colors[icolor],
            marker=marker,
        )
        icolor = icolor + 1

    # add observational data: radiosounding variables or cloud shading
    ax = add_obs(ax, obs_dict, var, add_clouds, relhum_thresh, verbose)

    # adjust appearance
    ax.set(
        xlabel=f"{var.long_name} [{var.unit}]",
        ylabel="Altitude [m asl]",
        ylim=(get_yrange(alt_bot, alt_top, df_height)),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )

    # define min and max values for xaxis
    #  if flag --xrange_fix is set: use values from variable dataframe
    #  else check whether user has specified min and max
    #  or just let matplotlib handle the job (default)
    if xrange_fix:
        ax.set_xlim(var.min_value, var.max_value)
    if xmin and xmax:
        try:
            ax.set_xlim(xmin[0], xmax[0])
        except NameError or IndexError:
            if verbose:
                print("No xrange defined.")

    # add nice legend
    ax.legend(fancybox=True)

    # define output filename
    #  if only 1 leadtime: include leadtime in filename
    #  if multuple leadtimes: no leadtimes specified in filename
    #  (user can add customised appendix to distinguish situations)
    if len(lts) == 1:
        name = f'profile_{model}_{date.strftime("%y%m%d_%H")}_+{lts[0]}_{loc}_{var.short_name}'
    else:
        name = f'profile_{model}_{date.strftime("%y%m%d_%H")}_+{lts[0]}_+{lts[-1]}_{loc}_{var.short_name}'
    if appendix:
        name = name + "_" + appendix

    # make plot tight
    plt.tight_layout()

    # save figure
    save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return


def plot_two_variables(
    df_height,
    variables_list,
    data_dict,
    obs_dict,
    outpath,
    date,
    add_clouds,
    relhum_thresh,
    alt_bot,
    alt_top,
    loc,
    model,
    appendix,
    xmin,
    xmax,
    xrange_fix,
    datatypes,
    verbose,
    show_grid,
    show_marker,
    zeroline,
    single_xaxis,
):
    print(f"--- creating plot for variables ({variables_list[0]}, {variables_list[1]})")

    # specify first variable (bottom x-axis) (pandas dataframe with attributes)
    # test whether variable is even available
    try:
        df_values_0 = data_dict[variables_list[0]]
    except KeyError:
        print(f"{variables_list[0]} is not available.")
        print(f"No plot is generated for {variables_list[0]} and {variables_list[1]}.")
        return

    var_0 = vdf[variables_list[0]]

    # specify second variable (top x-axis) (pandas dataframe with attributes)
    # test whether variable is even available
    try:
        df_values_1 = data_dict[variables_list[1]]
    except KeyError:
        print(f"{variables_list[1]} is not available.")
        print(f"No plot is generated for {variables_list[0]} and {variables_list[1]}.")
        return
    var_1 = vdf[variables_list[1]]

    # check the units
    same_unit = var_0.unit == var_1.unit

    if single_xaxis:
        print(
            f"Single X-Axis Flag has been provided. \
        \nVariable 1 has unit:\t{var_0.unit} \
        \nVariable 2 has unit:\t{var_1.unit}"
        )
        if same_unit:
            print("Create one plot with both variables using the same x-axis.")
        if not same_unit:
            print("Caution: Variables dont share the same unit. Add second x-axis.")
            single_xaxis = False

    # leadtimes
    lts = df_values_0.columns

    # figure settings
    plt.rcParams["figure.figsize"] = (5, 6)
    # plt.rcParams["figure.subplot.left"] = 0.15

    # dates
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # create figure
    _, ax_bottom = plt.subplots()

    if single_xaxis and same_unit:  # plot both variables on same axis
        ax_top = ax_bottom
    if (
        not same_unit or not single_xaxis
    ):  # plot first variable on bottom xaxis & second variable on top xaxis
        ax_top = ax_bottom.twiny()

    # add grid to figure, if show_grid flag was provided
    if show_grid:
        ax_bottom.xaxis.grid(linestyle="-", linewidth=0.5, alpha=0.5)
        ax_bottom.yaxis.grid(linestyle="-", linewidth=0.5, alpha=0.5)
        if verbose:
            print("Grid is only plotted for bottom variable.")

    # add zeroline to figure, if zeroline flag was provided
    if zeroline:
        ax_bottom.axvline(color="black", linewidth=1.5)
        if verbose:
            print("Zeroline is only plotted for bottom variable.")

    # specify marker
    if show_marker:
        marker = "o"
    else:
        marker = None

    ln0, ln1 = list(), list()
    # loop over leadtimes to create one line for each leadtime corresponding to variable 0
    tmp = 0
    for (lt, values) in df_values_0.iteritems():
        print(f"--- adding leadtime: {lt}")
        ln = ax_bottom.plot(
            values,
            df_height.values,
            label=f"{str_valid_time(date, lt)}: {variables_list[0].upper()}",
            color=var_0.color,
            linestyle=linestyle_dict[tmp],
            marker=marker,
        )
        ln0 += ln
        tmp += 1

    # loop over leadtimes to create one line for each leadtime corresponding to variable 1
    tmp = 0
    for (lt, values) in df_values_1.iteritems():
        print(f"--- adding leadtime: {lt}")
        ln = ax_top.plot(
            values,
            df_height.values,
            label=f"{str_valid_time(date, lt)}: {variables_list[1].upper()}",
            color=var_1.color,
            linestyle=linestyle_dict[tmp],
            marker=marker,
        )
        ln1 += ln
        tmp += 1

    add_obs(ax_bottom, obs_dict, var_0, add_clouds, relhum_thresh, verbose)

    # define min and max values for xaxis
    # if flag --xrange_fix is set: use values from variable dataframe
    # else check whether user has specified min and max for BOTH variables
    # or just let matplotlib handle the job (default)
    if xrange_fix:
        ax_bottom.set_xlim(var_0.min_value, var_0.max_value)
        ax_top.set_xlim(var_1.min_value, var_1.max_value)

    if xmin and xmax:
        if not single_xaxis:
            if len(xmin) is not len(variables_list):
                print(
                    f"No xrange defined for both variables. (xmin = {xmin} / xmax = {xmax}, single_xaxis flag: {single_xaxis})"
                )
                ax_bottom.set_xlim(xmin[0], xmax[0])
            elif len(xmin) == len(variables_list):
                print(
                    f"X-range defined for both variables. (xmin = {xmin} / xmax = {xmax}"
                )
                ax_bottom.set_xlim(xmin[0], xmax[0])
                ax_top.set_xlim(xmin[1], xmax[1])

        if single_xaxis:
            ax_bottom.set_xlim(xmin[0], xmax[0])

    # adjust appearance
    if not same_unit:
        ax_bottom.set(
            xlabel=f"{var_0.long_name} [{var_0.unit}]",
            ylabel="Altitude [m asl]",
            ylim=(get_yrange(alt_bot, alt_top, df_height)),
            title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
        )

        ax_top.set(
            xlabel=f"{var_1.long_name} [{var_1.unit}]",
            ylabel="Altitude [m asl]",
            ylim=(get_yrange(alt_bot, alt_top, df_height)),
            label=f"{variables_list[1]}",
        )
    if same_unit:
        ax_bottom.set(
            xlabel=f"{var_0.long_name} & {var_1.long_name} [{var_0.unit}]",
            ylabel="Altitude [m asl]",
            ylim=(get_yrange(alt_bot, alt_top, df_height)),
            title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
        )

    # create legend
    lns = ln0 + ln1
    labs = [l.get_label() for l in lns]
    ax_bottom.legend(
        lns,
        labs,
        # loc=0
    )

    # filename
    if len(lts) == 1:
        name = f'profile_{model}_{date.strftime("%y%m%d_%H")}_+{lts[0]}_{loc}_{var_0.short_name}_{var_1.short_name}'
    else:
        name = f'profile_{model}_{date.strftime("%y%m%d_%H")}_+{lts[0]}_+{lts[-1]}_{loc}_{var_0.short_name}_{var_1.short_name}'
    if appendix:
        name = name + "_" + appendix

    # make plot tight
    plt.tight_layout()

    # save figure
    save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return


def create_plot(
    variables_list,
    data_dict,
    obs_dict,
    outpath,
    date,
    add_clouds,
    relhum_thresh,
    alt_bot,
    alt_top,
    loc,
    model,
    appendix,
    xmin,
    xmax,
    xrange_fix,
    datatypes,
    verbose,
    show_grid,
    show_marker,
    zeroline,
    single_xaxis,
):
    """Plot vertical profile of variable(s).

    Args:
        variables_list (list):          List of all variables of interest
        data_dict (dict):               Dictionary w/ keys for each variable. Each key contains the
                                        dataframe corresponding to this variable.
        obs_dict (dict):                additional obs: radiosoundings
        outpath (str):                  path where figure should be stored
        date (datetime obj):            init date of simulation
        add_clouds (bool):              add cloud shading
        relhum_thresh (float):          threshold for cloud shading [%]
        add_rs (list of int)            add radiosoundings for specified leadtimes
        alt_bot (int):                  lower boundary of altitude
        alt_top (int):                  upper boundary of altitude
        loc (str):                      location string
        model (str):                    name of nwp model
        appendix (str):                 add to output filename to e.g. distinguish versions
        xmin (float):                   minimum value of xaxis
        xmax (float):                   maximum value of xaxis
        xrange_fix(bool):               take fix xrange from variables.py
        datatypes (tuple):              tuple containig all desired datatypes for the output files
        verbose (bool):                 print verbose messages
        show_grid (bool):               add grid to plot
        show_marker (bool):             add marker to vertical lines
        zeroline (bool):                add zeroline to plot
        single_xaxis (bool):            plot variables w/ same unit on one xaxis if this flag has been provided

    """
    df_height = data_dict["height"]
    # CASE: one plot which comprises two variables
    if len(variables_list) == 2:
        plot_two_variables(
            df_height,
            variables_list,
            data_dict,
            obs_dict,
            outpath,
            date,
            add_clouds,
            relhum_thresh,
            alt_bot,
            alt_top,
            loc,
            model,
            appendix,
            xmin,
            xmax,
            xrange_fix,
            datatypes,
            verbose,
            show_grid,
            show_marker,
            zeroline,
            single_xaxis,
        )
    # CASE: one plot for each variable
    else:
        for variable in variables_list:
            plot_single_variable(
                data_dict,
                obs_dict,
                variable,
                outpath,
                date,
                add_clouds,
                relhum_thresh,
                alt_bot,
                alt_top,
                loc,
                model,
                appendix,
                xmin,
                xmax,
                xrange_fix,
                datatypes,
                df_height,
                verbose,
                show_grid,
                show_marker,
                zeroline,
            )

    return


def create_heatmap(
    variables_list,
    data_dict,
    outpath,
    date,
    loc,
    model,
    appendix,
    datatypes,
    leadtime,
    verbose,
    var_min,
    var_max,
    surface_data=None,
):
    # the height dataframe is the same for all variables, thus outside of the
    # for-loop below. it needs some reformatting and type alignement for later use
    df_height = data_dict["height"].to_frame()
    df_height.rename(columns={0: "height"}, inplace=True)

    # create date list for all colums of heatmap
    lt_dt = []
    for lt in leadtime:
        lt_dt.append((date + dt.timedelta(hours=lt)).strftime("%Y-%m-%d %H:%M"))

    # dates used in the filename / title of heat plots
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # this loop creates the heatmap. for each variable, one separate heatmap is generated
    for variable in variables_list:
        var = vdf[variable]
        print(f"--- creating heatmap for {var.long_name}")

        try:
            df_values = data_dict[variable]
            df_values.set_index(df_height["height"], inplace=True)
        except KeyError:
            print(f"No plot is generated for {variable}.")
            break  # just continue with the next variable - should not break the whole loop

        plt.rcParams["figure.figsize"] = (7.5, 4.5)
        fig, ax_colormesh = plt.subplots()

        # plot heatmap
        im = ax_colormesh.pcolormesh(
            lt_dt,
            np.round(df_values.index.to_list()),
            df_values,
            shading="auto",
            cmap=var.colormap,
        )
        # ax_colormesh.axis("off")  # remove x-axis of heatmap
        ax_colormesh.get_xaxis().set_visible(False)
        ax_colormesh.set_xlim(left=lt_dt[0], right=lt_dt[-1])
        cbar = fig.colorbar(im, ax=ax_colormesh)
        cbar.ax.set_ylabel(f"{var.long_name} [{var.unit}]")

        if var_min:
            im.set_clim(var_min, var_max)

        # IF no surface_data is added to heatmap, initialise new axes-instace which can be
        # formatted using the concise date formater
        start = date
        end = date + dt.timedelta(hours=leadtime[-1])
        if surface_data is None:
            ax_date = ax_colormesh.twiny()
            ax_date.xaxis.set_ticks_position("bottom")
            ax_date.plot([start, end], [np.NaN, np.NaN])
            ax_date.set_xlim(start, end)

        # plot cloud base height & vertical visibility
        if surface_data is not None:
            # shift the values of the cbh & ver_vis columns by the elevation of the station (loc)
            surface_data.loc[surface_data["cbh"] != np.NaN, ["cbh"]] += sdf[
                loc
            ].elevation
            surface_data.loc[surface_data["ver_vis"] > 0, ["ver_vis"]] = sdf[
                loc
            ].elevation
            surface_cbh = surface_data.cbh.values
            surface_ver_vis = surface_data.ver_vis.values

            dates = pd.to_datetime(
                surface_data["timestamp"], format="%Y-%m-%d %H:%M:%S"
            )
            ax_cbh = ax_colormesh.twiny()  # add axis for surface data
            ax_cbh.xaxis.set_ticks_position("bottom")  # the rest is the same
            ax_cbh.plot(
                dates,
                surface_cbh,
                linestyle="None",
                marker="^",
                markerfacecolor="none",
                markeredgecolor="lightcoral",
            )
            ax_cbh.plot(
                dates,
                surface_ver_vis,
                linestyle="None",
                marker="^",
                markerfacecolor="None",
                markeredgecolor="indianred",
            )

            # to ensure that all axes are aligned, set_xlim
            ax_cbh.set_xlim(start, end)

            # add customised legend
            legend_elements = [
                Patch(color="white", label=f"{var.long_name} (FCST)"),
                Line2D(
                    [0],
                    [0],
                    marker="^",
                    markerfacecolor="None",
                    markeredgecolor="indianred",
                    markersize=10,
                    linestyle="None",
                    label="Cloud base (OBS)",
                ),
            ]
            ax_cbh.legend(handles=legend_elements)

        # if combining automatic and manual legend elemnts
        ### where some data has already been plotted to ax
        ###handles, labels = ax.get_legend_handles_labels()

        ### manually define a new patch
        ###patch = mpatches.Patch(color='grey', label='Manual Label')

        ### handles is a list, so append manual patch
        ###handles.append(patch)

        ### cbar.ax.set_title("placeholder") # title for the colorbar if necessary

        # adjust appearance
        plt.tick_params(axis="both", labelsize=8)
        plt.setp(
            ax_colormesh.get_xticklabels(), rotation=45, ha="right"
        )  # rotated x-axis ticks
        ax_colormesh.set_title(
            f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC"
        )
        ax_colormesh.set_ylabel(f"Altitude [m asl]")

        # save figure
        name = f'heatmap_{model}_{date.strftime("%y%m%d_%H")}_+{leadtime[0]}_+{leadtime[-1]}_{loc}_{var.short_name}'

        if appendix:
            name = name + "_" + appendix

        save_fig(filename=name, datatypes=datatypes, outpath=outpath)

    return
