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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Local
from .plot_rs import plot_clouds
from .stations import sdf
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
    plt.rcParams["figure.figsize"] = (5, 6)
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
    var_min,
    var_max,
    surface_data=None,
):
    if surface_data is not None:
        # shift the values of the cbh & ver_vis columns by the elevation of the station (loc)
        surface_data.loc[surface_data["cbh"] != np.NaN, ["cbh"]] += sdf[loc].elevation
        surface_data.loc[surface_data["ver_vis"] > 0, ["ver_vis"]] = sdf[loc].elevation
        surface_timestamp = surface_data.timestamp.values
        surface_cbh = surface_data.cbh.values
        surface_ver_vis = surface_data.ver_vis.values

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

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ NEW ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    same_start = (
        surface_timestamp[0] == lt_dt_2[0]
    )  # --> if True: the model & the measurements start at the same time
    same_end = (
        surface_timestamp[-1] == lt_dt_2[-1]
    )  # --> if True: the model & the measurements end at the same time

    if not (same_start and same_end):
        if verbose:
            print(
                f"The time-axis for the surface station needs to be aligned to the time-axis of the model data."
            )

        # create a list using linspace, which starts at the same time as lt_dt_2 and ends at the same time as lt_dt_2
        # the step size (dt) is chosen as 10 minutes, as this is the smalles possible interval between consecutive measurements
        # at the surface station
        start = dt.datetime.strptime(lt_dt_2[0], "%Y-%m-%d %H:%M")
        end = dt.datetime.strptime(lt_dt_2[-1], "%Y-%m-%d %H:%M")
        n = (
            int(((end - start).total_seconds() / 3600) * 6) + 1
        )  # *6, because there are six 10 minute intervals per hour;
        top_x_axis_values = pd.date_range(
            start, end, periods=n
        ).tolist()  # these values represent the hidden tick marks of the top x axis
        top_x_axis_cbh, top_x_axis_ver_vis = [], []  # these lists need to be filled.
        j = 0

        for timestamp in top_x_axis_values:
            if str(timestamp) not in surface_timestamp:
                if verbose:
                    print(
                        f"No measurement found for time: {timestamp}. Appending {np.NaN}"
                    )
                top_x_axis_cbh.append(np.NaN)
                top_x_axis_ver_vis.append(np.NaN)
            if str(timestamp) in surface_timestamp:
                if verbose:
                    print(
                        f"Measurement found for time: {timestamp}. Appending corresponding values ({surface_cbh[j]}/{surface_ver_vis[j]})"
                    )
                top_x_axis_cbh.append(surface_cbh[j])
                top_x_axis_ver_vis.append(surface_ver_vis[j])
                j += 1

        # assign new lists to old variable names & create masked lists, s.t. NaN values are not ignored
        surface_timestamp = top_x_axis_values
        surface_cbh = np.ma.masked_where(top_x_axis_cbh == np.NaN, top_x_axis_cbh)
        surface_ver_vis = np.ma.masked_where(
            top_x_axis_ver_vis == np.NaN, top_x_axis_ver_vis
        )

    elif verbose:
        print(f"The timestamp axes are aligned already.")
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~ NEW ~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
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

        plt.rcParams["figure.figsize"] = (7.5, 4.5)
        fig, ax = plt.subplots()

        # REMARK: it is important, that the heatmap gets plotted before the scatter plot - don't change this order!
        # plot heatmap
        im = ax.pcolormesh(
            lt_dt_series,
            np.round(df_values.index.to_list()),
            df_values,
            shading="auto",
            cmap=var.colormap,
        )
        cbar = fig.colorbar(im, ax=ax)
        cbar.ax.set_ylabel(f"{var.long_name} [{var.unit}]")

        if var_min:
            im.set_clim(var_min, var_max)

        # scatter plot cloud base height & vertical visibility
        if surface_data is not None:
            ax_scatter = ax.twiny()  # add axis for surface data
            ax_scatter.axis("off")  # & hide it
            ax_scatter.plot(
                surface_timestamp,
                surface_cbh,
                linestyle="None",
                marker="^",
                markerfacecolor="none",
                markeredgecolor="lightcoral",
            )
            ax_scatter.plot(
                surface_timestamp,
                surface_ver_vis,
                linestyle="None",
                marker="^",
                markerfacecolor="None",
                markeredgecolor="indianred",
            )

            # make sure, the top and bottom x-axis both start at the very left/right of the plot
            # these two lines mustn't be removed, as they are necessary to plot the masked arrays correctly
            ax.set_xlim(left=lt_dt_series.iloc[0], right=lt_dt_series.iloc[-1])
            ax_scatter.set_xlim(surface_timestamp[0], surface_timestamp[-1])

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
            ax_scatter.legend(handles=legend_elements)

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
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")  # rotated x-axis ticks
        ax.set_title(f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC")
        ax.set_ylabel(f"Altitude [m asl]")
        # save figure
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{loc}_heatmap'
        if appendix:
            name = name + "_" + appendix
        plt.tight_layout()

        save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return
