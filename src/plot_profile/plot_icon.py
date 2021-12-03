"""Purpose: Visualise vertical profiles of variables from ICON simulation.

Author: Stephanie Westerhuis

Date: 25/11/2021.
"""

# Standard library
import random
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Local
from .utils import save_fig
from .variables import vdf


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
    datatypes,
    df_height,
    variable,
):

    print(f"--- creating plot for variable {variable}")
    df_values = data_dict[variable]

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

    # loop over leadtimes to create one line for each leadtime
    first_leadtime = True
    for (lt, values) in df_values.iteritems():
        print(f"--- adding leadtime: {lt}")
        if first_leadtime:
            color = var.color
        else:
            color = (np.random.random(), np.random.random(), np.random.random())
            # color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]

        ax.plot(values, df_height.values, label=f"+ {lt:02} h", color=color)
        first_leadtime = False

    # define min and max values for xaxis
    if not xmin:
        xmin = var.min_value
    if not xmax:
        xmax = var.max_value

    # adjust appearance
    ax.set(
        xlabel=f"{var.long_name} [{var.unit}]",
        # xlim=(xmin, xmax),
        ylabel="Altitude [m asl]",
        ylim=(alt_bot, alt_top),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )
    ax.legend(fancybox=True)

    # save figure
    name = f'{model}_{date.strftime("%y%m%d")}_{date.hour:02}_{var.short_name}_{loc}'
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
    datatypes,
):
    print(f"--- creating plot for variables ({variables_list[0]}, {variables_list[1]})")
    # specify first variable (bottom x-axis) (pandas dataframe with attributes)
    var_0 = vdf[variables_list[0]]
    df_values_0 = data_dict[variables_list[0]]

    # specify second variable (top x-axis) (pandas dataframe with attributes)
    var_1 = vdf[variables_list[1]]
    df_values_1 = data_dict[variables_list[1]]

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
    ln0, ln1 = list(), list()
    # loop over leadtimes to create one line for each leadtime corresponding to variable 1
    tmp = 0
    for (lt, values) in df_values_0.iteritems():
        print(f"--- adding leadtime: {lt}")
        ln = ax_bottom.plot(
            values,
            df_height.values,
            label=f"+ {lt:02} h ({variables_list[0]})",
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
            label=f"+ {lt:02} h ({variables_list[1]})",
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
        # xlim=(xmin_bottom, xmax_bottom),
        ylabel="Altitude [m asl]",
        ylim=(alt_bot, alt_top),
        title=f"{model.upper()} @ {loc.upper()}: {init_date}, {init_hour} UTC",
    )

    ax_top.set(
        xlabel=f"{var_1.long_name} [{var_1.unit}]",
        # xlim=(xmin_top, xmax_top),
        ylabel="Altitude [m asl]",
        ylim=(alt_bot, alt_top),
        label=f"{variables_list[1]}",
    )

    lns = ln0 + ln1
    labs = [l.get_label() for l in lns]
    ax_bottom.legend(
        lns,
        labs,
        # loc=0
    )

    # ax_bottom.legend(fancybox=True)
    # ax_top.legend(fancybox=True)

    # save figure
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
    datatypes,
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
            datatypes=datatypes,
            df_height=df_height,
            variable=variable,
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
    datatypes,
    leadtime,
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
        datatypes (tuple):              tuple containig all desired datatypes for the output files
        leadtime (list):                List of all lead times of interest

    """
    assert (
        len(leadtime) <= 5
    ), "It is not possible, to have more than 5 lead-times in one plot."

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
            datatypes=datatypes,
            df_height=df_height,
            variable=variables_list[0],
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
            datatypes,
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
            datatypes,
        )
    return
