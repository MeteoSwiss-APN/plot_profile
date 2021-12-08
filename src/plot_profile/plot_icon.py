"""Purpose: Visualise vertical profiles of variables from ICON simulation.

Author: Stephanie Westerhuis

Date: 25/11/2021.
"""

# Standard library
import datetime as dt

# Third-party
import matplotlib.pyplot as plt
import seaborn as sns

# Local
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
        ymin = df_height.iloc[-1]
    else:
        ymin = alt_bot

    if alt_top is None:
        ymax = df_height.iloc[0]
    else:
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


def plot_single_variable(
    data_dict,
    outpath,
    date,
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
    variable,
    verbose,
    grid,
    zeroline,
):

    print(f"--- creating plot for variable {variable}")

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
    plt.rcParams["figure.figsize"] = (4.5, 6)
    # plt.rcParams["figure.subplot.left"] = 0.15

    # dates
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # create figure
    fig, ax = plt.subplots()

    # add grid to figure
    if grid:
        ax.xaxis.grid(color="black", linestyle="--", linewidth=0.5)
        ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)

    # add zero-line to figure
    if zeroline:
        ax.axvline(linewidth=2, color="k")

    # define color sequence
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
            label=str_valid_time(date, lt),
            color=colors[icolor],
        )
        icolor = icolor + 1

    # adjust appearance
    ax.set(
        xlabel=f"{var.long_name} [{var.unit}]",
        ylabel="Altitude [m asl]",
        ylim=(get_yrange(alt_bot, alt_top, df_height)),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )

    # define min and max values for xaxis
    if xrange_fix:
        ax.set_xlim(var.min_value, var.max_value)
    else:
        try:
            ax.set_xlim(xmin, xmax)
        except NameError:
            if verbose:
                print("No xrange defined.")

    ax.legend(fancybox=True)

    # save figure
    if len(lts) == 1:
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_+{lts[0]}h_{var.short_name}_{loc}'
    else:
        name = (
            f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{loc}'
        )
    if appendix:
        name = name + "_" + appendix
    plt.tight_layout()

    save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return


def plot_two_variables(
    df_height,
    variables_list,
    data_dict,
    outpath,
    date,
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
    grid,
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

    # linestyles for several lead times
    linestyle_dict = {
        0: "solid",
        1: "dotted",
        2: "dashed",
        3: (0, (1, 10)),  # loosely dotted
        4: (0, (5, 10)),  # loosely dashed
        5: (0, (3, 10, 1, 10)),  # loosely dashdotted
    }

    # dates
    init_date = date.strftime("%b %-d, %Y")
    init_hour = date.hour

    # create figure
    fig, ax_bottom = plt.subplots()
    ax_top = ax_bottom.twiny()  # add shared x-axis

    # add grid to figure, if show_grid flag was provided
    if grid:
        visibility = 0.5
        ax_bottom.xaxis.grid(
            color=var_0.color, linestyle="-", linewidth=0.5, alpha=visibility
        )
        ax_bottom.yaxis.grid(
            color="black", linestyle="-", linewidth=0.5, alpha=visibility
        )
        ax_top.xaxis.grid(
            color=var_1.color, linestyle="-", linewidth=0.5, alpha=visibility
        )

    # add zeroline to figure, if zeroline flag was provided
    if zeroline:
        ax_bottom.axvline(linewidth=2, color=var_0.color)
        ax_top.axvline(linewidth=2, color=var_1.color)

    ln0, ln1 = list(), list()
    # loop over leadtimes to create one line for each leadtime corresponding to variable 1
    tmp = 0
    for (lt, values) in df_values_0.iteritems():
        print(f"--- adding leadtime: {lt}")
        ln = ax_bottom.plot(
            values,
            df_height.values,
            label=f"{str_valid_time(date, lt)}: {variables_list[0]}",
            color=var_0.color,
            linestyle=linestyle_dict[tmp],
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
            label=f"{str_valid_time(date, lt)}: {variables_list[1]}",
            color=var_1.color,
            linestyle=linestyle_dict[tmp],
        )
        ln1 += ln
        tmp += 1

    # define min and max values for bottom xaxis
    if not xmin:
        xmin_bottom = var_0.min_value
        xmin_top = var_1.min_value
    if not xmax:
        xmax_bottom = var_0.max_value
        xmax_top = var_1.max_value

    # adjust appearance
    ax_bottom.set(
        xlabel=f"{var_0.long_name} [{var_0.unit}]",
        xlim=(xmin_bottom, xmax_bottom),
        ylabel="Altitude [m asl]",
        ylim=(get_yrange(alt_bot, alt_top, df_height)),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )

    ax_top.set(
        xlabel=f"{var_1.long_name} [{var_1.unit}]",
        xlim=(xmin_top, xmax_top),
        ylabel="Altitude [m asl]",
        ylim=(get_yrange(alt_bot, alt_top, df_height)),
        label=f"{variables_list[1]}",
    )

    lns = ln0 + ln1
    labs = [l.get_label() for l in lns]
    ax_bottom.legend(
        lns,
        labs,
        # loc=0
    )

    # save figure
    if len(lts) == 1:
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_+{lts[0]}h_{var_0.short_name}_{var_1.short_name}_{loc}'
    else:
        name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var_0.short_name}_{var_1.short_name}_{loc}'
    if appendix:
        name = name + "_" + appendix
    plt.tight_layout()

    save_fig(filename=name, datatypes=datatypes, outpath=outpath)
    return


def plot_all_variables_individually(
    df_height,
    variables_list,
    data_dict,
    outpath,
    date,
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
):
    for variable in variables_list:
        plot_single_variable(
            data_dict=data_dict,
            outpath=outpath,
            date=date,
            alt_bot=alt_bot,
            alt_top=alt_top,
            loc=loc,
            model=model,
            appendix=appendix,
            xmin=xmin,
            xmax=xmax,
            xrange_fix=xrange_fix,
            datatypes=datatypes,
            df_height=df_height,
            variable=variable,
            verbose=verbose,
        )
    return


def create_plot(
    variables_list,
    data_dict,
    outpath,
    date,
    alt_bot,
    alt_top,
    loc,
    model,
    appendix,
    xmin,
    xmax,
    xrange_fix,
    datatypes,
    leadtime,
    verbose,
    grid,
    zeroline,
):
    """Plot vertical profile of variable.

    Args:
        variables_list (list):          List of all variables of interest
        data_dict (dict):               Dictionary w/ keys for each variable. Each key contains the
                                        dataframe corresponding to this variable.
        outpath (str):                  path where figure should be stored
        date (datetime obj):            init date of simulation
        alt_bot (int):                  lower boundary of altitude
        alt_top (int):                  upper boundary of altitude
        loc (str):                      location string
        model (str):                    name of nwp model
        appendix (str):                 add to output filename to e.g. distinguish versions
        xmin (float):                   minimum value of xaxis
        xmax (float):                   maximum value of xaxis
        xrange_fix(bool):               take fix xrange from variables.py
        datatypes (tuple):              tuple containig all desired datatypes for the output files
        leadtime (list):                list of all lead times of interest
        verbose (bool):                 print verbose messages
        zeroline (bool):                add zeroline to plot
        grid (bool):                    add grid to plot

    """
    # assert (
    #    len(leadtime) <= 5
    # ), "It is not possible, to have more than 5 lead-times in one plot."

    df_height = data_dict["height"]

    # CASE: one plot, one variable
    if len(variables_list) == 1:
        plot_single_variable(
            data_dict=data_dict,
            outpath=outpath,
            date=date,
            alt_bot=alt_bot,
            alt_top=alt_top,
            loc=loc,
            model=model,
            appendix=appendix,
            xmin=xmin,
            xmax=xmax,
            xrange_fix=xrange_fix,
            datatypes=datatypes,
            df_height=df_height,
            variable=variables_list[0],
            verbose=verbose,
            grid=grid,
            zeroline=zeroline,
        )

    # CASE: one plot, two variables
    if len(variables_list) == 2:
        plot_two_variables(
            df_height,
            variables_list,
            data_dict,
            outpath,
            date,
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
            grid,
            zeroline=zeroline,
        )

    if len(variables_list) > 2:
        plot_all_variables_individually(
            df_height,
            variables_list,
            data_dict,
            outpath,
            date,
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
        )
    return
