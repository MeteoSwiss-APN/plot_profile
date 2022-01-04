"""Purpose: Visualise vertical profiles of variables from ICON simulation.

Author: Stephanie Westerhuis

Date: 25/11/2021.
"""

# Standard library
import datetime as dt

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Local
from .plot_rs import plot_clouds
from .utils import linestyle_dict
from .utils import save_fig
from .variables import vdf

# import ipdb


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

            if var.short_name in ["temp", "dewp_temp", "wind_vel", "wind_dir"]:
                values = sounding[var.short_name]
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
    fig, ax = plt.subplots()

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
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_+{lts[0]}h_{var.short_name}_{loc}'
    else:
        name = (
            f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{loc}'
        )
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

    # leadtimes
    lts = df_values_0.columns

    # figure settings
    plt.rcParams["figure.figsize"] = (4.5, 6)
    # plt.rcParams["figure.subplot.left"] = 0.15

    # dates
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # create figure
    fig, ax_bottom = plt.subplots()
    ax_top = ax_bottom.twiny()  # add shared x-axis

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
        assert len(xmin) == len(
            variables_list
        ), f"No xrange defined for both variables. (xmin = {xmin} / xmax = {xmax})"
        ax_bottom.set_xlim(xmin[0], xmax[0])
        ax_top.set_xlim(xmin[1], xmax[1])

    # adjust appearance
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
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_+{lts[0]}h_{var_0.short_name}_{var_1.short_name}_{loc}'
    else:
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var_0.short_name}_{var_1.short_name}_{loc}'
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
):
    # the height dataframe is the same for all variables, thus outside of the
    # for-loop below. it needs some reformatting and type alignement for later use
    df_height = data_dict[
        "height"
    ].to_frame()  # convert pandas series to pandas dataframe

    df_height.rename(
        columns={0: "height"}, inplace=True
    )  # rename the first column from '0' to 'height'

    # generate new column names for the dataframes
    # the col-dict links the abbreviated leadtimes (i.e. 00, 02, 04,...) to their
    # respective datetime equivalents (i.e. start_date + leadtime)

    # lt-dt contains all leadtimes and the first leadtimes on new dates have a different
    # formatting from the rest

    # lt_dt_2 contains all leadtimes with a uniform format %Y-%m-%d %H:%M (but is not used later)
    lt_dt, col_dict, lt_dt_2 = [], {}, []
    tmp = 0
    start_date = date.date()
    for lt in leadtime:
        lt_dt_2.append((date + dt.timedelta(hours=lt)).strftime("%Y-%m-%d %H:%M"))

        if (date + dt.timedelta(hours=lt)).date() != start_date:
            start_date = (date + dt.timedelta(hours=lt)).date()
            tmp = 0
        # the first leadtime on the startdate is formatted like: %b %-d, %H:%M
        # if the simulation covers several days, the first leadtimes on other days
        # also have this formatting (specified by the tmp variable)
        if tmp == 0:
            col_dict[lt] = (date + dt.timedelta(hours=lt)).strftime("%b %-d, %H:%M")
            lt_dt.append((date + dt.timedelta(hours=lt)).strftime("%b %-d, %H:%M"))
            # col_dict[lt] = (date + dt.timedelta(hours=lt)).strftime("%Y-%m-%d %H:%M")
            # lt_dt.append((date + dt.timedelta(hours=lt)).strftime("%Y-%m-%d %H:%M"))
            tmp = 1
        # else the formatting is only HH:MM. These timesteps ultimately are displayed
        # on the x-axis. It is not desireable to have the date for each x-tick-label.
        else:
            col_dict[lt] = (date + dt.timedelta(hours=lt)).strftime("%H:%M")
            lt_dt.append((date + dt.timedelta(hours=lt)).strftime("%H:%M"))
    lt_dt_series = pd.Series(lt_dt)

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

        # rename the column names from leadtimes as int to leadtimes as datetime objects
        # because the column names are the x-axis ticklabels of the heatmap
        df_values.rename(columns=col_dict, inplace=True)

        fig, ax = plt.subplots()
        im = ax.pcolormesh(
            lt_dt_series,
            np.round(df_values.index.to_list()),
            df_values,
            shading="auto",
            cmap=var.colormap,
        )
        cbar = fig.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(f"{var.long_name} [{var.unit}]")
        # cbar.ax.set_title("placeholder") # title for the colorbar if necessary

        # adjust appearance
        plt.tick_params(axis="both", labelsize=8)
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")  # rotated x-axis ticks
        ax.set_title(f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC")
        ax.set_ylabel(f"Altitude [m asl]")
        # save figure
        name = (
            f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{loc}'
        )
        if appendix:
            name = name + "_" + appendix
        plt.tight_layout()

        save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return
