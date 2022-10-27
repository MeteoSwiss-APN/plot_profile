"""Purpose: Plot radiosounding.

Author: Michel Zeller

Date: 05/10/2021.
"""

# Standard library
import datetime
from mmap import ACCESS_DEFAULT

# Third-party
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Local
from ..utils.utils import save_fig

# import ipdb


def extract_clouds(df, relhum_thresh, print_steps):
    """Extract the cloud layers based on the relative humidity threshold.

    Args:
        df:                 df          dataframe containing relevant rows/columns
        relhum_thresh:      float       relative humitdity threshold needed to be classified as cloud
        print_steps:        bool        optional parameter to print intermediate steps in terminal

    Returns:
        cloud_start:        array       array containing cloud layer start altitudes
        cloud_end:          array       array containing cloud layer end altitudes

    """
    cloud_df = df[["altitude", "rel_hum"]]  # extract the altitude & rel_hum columns
    cloud_df = cloud_df[
        cloud_df["rel_hum"] >= relhum_thresh
    ]  # remove rows where no clouds are present
    cloud_df = cloud_df[["altitude"]]  # remove the rel_hum column
    cloud_list = list(cloud_df.index.values)  # index list of cloud layers
    cloud_array = (
        cloud_df.to_numpy()
    )  # to cloud_list corresponding array of altitudes, where clouds are presen

    if not cloud_list:
        return [], []
    else:
        cloud_start = []  # array containing the cloud layer date2-altitudes
        cloud_end = []  # array containtg the cloud layer end-altitudes
        index = 0
        tmp1 = cloud_list[0]
        cloud_start.append(cloud_array[0][0])
        cloud_thresh = 5  # threshold to merge otherwise narrow cloud layers

        # row = cloud_list[index]
        for row in cloud_list:
            if row > tmp1:
                # print(f'cloud_list[index] / cloud_array[index][0]: {cloud_array[index][0]} / {cloud_list[index]}')
                tmp_end = cloud_array[index][0]  # temporary end point
                tmp1 = row  # temporary date2 point
                if (
                    index < len(cloud_list) - 1
                ):  # as long as we're not at the end of the list
                    if cloud_list[index + 1] > tmp1 + cloud_thresh:
                        cloud_end.append(tmp_end)
                        cloud_start.append(cloud_array[index + 1][0])
                if index == len(cloud_list) - 1:
                    cloud_end.append(tmp_end)
            # print(f'row ({index}) = {row}, cloud_start = {cloud_start}, cloud_end = {cloud_end}')
            index += 1
        if print_steps:
            print(
                f"cloud list: {cloud_list} \n cloud array: {cloud_array} \n cloud start: {cloud_start}  \n cloud_end: {cloud_end}"
            )
        return cloud_start, cloud_end


def map_degrees(avg_winddir_array):
    """Map the wind directions (°) from to x-y values.

    Args:
        avg_winddir_array:  array       direction of wind in degrees

    Returns:
        x_dir:              array        x-coordinate of wind_dir array
        y_dir:              array        y-coordinate of wind_dir array

    """
    x_dir, y_dir, i = [], [], 0
    while i < len(avg_winddir_array):
        x_dir.append(np.cos(avg_winddir_array[i] - 90))
        y_dir.append(np.sin(avg_winddir_array[i] - 90))
        i += 1
    return x_dir, y_dir


def adjustFigAspect(fig, aspect=1):
    """Create plots with different aspect ratios (taken from stackoverflow).

    Adjust the subplot parameters so that the figure has the correct aspect ratio.

    """
    # no blank lines allowed here according to the docstring rules.
    xsize, ysize = fig.get_size_inches()
    minsize = min(xsize, ysize)
    xlim = 0.4 * minsize / xsize
    ylim = 0.4 * minsize / ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(
        left=0.5 - xlim, right=0.5 + xlim, bottom=0.5 - ylim, top=0.5 + ylim
    )


def get_axis_limits(df, params, user_inputs_dict):
    """Check, which axis limits should be used (standard/personal settings).

    Args:
        df                      dataframe   dataframe containing all data
        params                  tuple       relevant parameters which are plotted
        users_inputs_dict       dict        dict containing specified settings, personal axes limits...

    Returns:
        windvel_min:            float       lower bound for wind velocity
        windvel_max:            float       upper bound for wind velocity
        temp_min:               float       lower bound for temperature
        temp_max:               float       upper bound for temperature
        pot_temp_min:               float       lower bound for potential temperature
        pot_temp_max:               float       upper bound for potential temperature

    """
    windvel_min, windvel_max, temp_min, temp_max, pot_temp_min, pot_temp_max = None, None, None, None, None, None

    # case 1: use personal settings for the axis limits that have been defined
    if user_inputs_dict["personal_settings"]:
        if user_inputs_dict["windvel_min"]:
            windvel_min = user_inputs_dict["windvel_min"]
        if user_inputs_dict["windvel_max"]:
            windvel_max = user_inputs_dict["windvel_max"]
        if user_inputs_dict["temp_min"]:
            temp_min = user_inputs_dict["temp_min"]
        if user_inputs_dict["temp_max"]:
            temp_max = user_inputs_dict["temp_max"]
        if user_inputs_dict["pot_temp_min"]:
            pot_temp_min = user_inputs_dict["pot_temp_min"]
        if user_inputs_dict["pot_temp_max"]:
            pot_temp_max = user_inputs_dict["pot_temp_max"]
        return windvel_min, windvel_max, temp_min, temp_max, pot_temp_min, pot_temp_max

    # case 2: use standard axis limits
    # > temperature range:   -100 - 30 [°C]
    # > windvelocity range:     0 - 30 [m/s]
    # > potential temperature range:    275 - 325 [K]
    if user_inputs_dict["standard_settings"]:
        windvel_min, windvel_max = 0, 30
        temp_min, temp_max = -100, 30
        pot_temp_min, pot_temp_max = 275,325
        return windvel_min, windvel_max, temp_min, temp_max, pot_temp_max, pot_temp_min

    # case 3: get axis limits dynamically
    else:
        if "temp" in params:
            temp_min = df["temp"].min() - 0.5
            temp_max = df["temp"].max() + 0.5
        if "dewp_temp" in params:
            temp_min = df["dewp_temp"].min() - 0.5
            if "temp" not in params:  # otherwise 'temp' should define the maximum value
                temp_max = df["dewp_temp"].max() + 0.5
        if "wind_vel" in params:
            windvel_min = df["wind_vel"].min() - 0.10 * df["wind_vel"].max()
            windvel_max = df["wind_vel"].max() + 0.10 * df["wind_vel"].max()
        if "pot_temp" in params:
            pot_temp_min = df["pot_temp"].min() - 0.5
            pot_temp_max = df["pot_temp"].max() + 0.5

        return windvel_min, windvel_max, temp_min, temp_max, pot_temp_min, pot_temp_max


def plot_clouds(df, relhum_thresh, print_steps, ax, case=None):
    """Add clouds to plot.

    Args:
        df:                 df          dataframe containing relevant rows/columns
        relhum_thresh:      float       relative humitdity threshold needed to be classified as cloud
        print_steps:        bool        optional parameter to print intermediate steps in terminal
        ax:                 axes        current axes to add clouds to
        case:               str         differ between single and multi plot case

    """
    cloud_start, cloud_end = extract_clouds(
        df=df, relhum_thresh=relhum_thresh, print_steps=print_steps
    )
    if not cloud_start:
        print(
            f'No clouds for this altidue range/date. (max rel_hum: {df["rel_hum"].max()} while relhum_thresh: {relhum_thresh})'
        )
    else:
        # plot lines which correspond to clouds
        i = 0
        while i < len(cloud_start):
            if case == "single":
                ax.axhspan(
                    ymin=cloud_start[i],
                    ymax=cloud_end[i],
                    color="grey",
                    linestyle="-",
                    alpha=0.3,
                )
            else:
                ax[0].axhspan(
                    ymin=cloud_start[i],
                    ymax=cloud_end[i],
                    color="grey",
                    linestyle="-",
                    alpha=0.3,
                )
            i += 1

    return


def plot_grid(ax, params, case=None):
    """Add grid to current axes.

    Args:
        ax:                 axes        current axes to add clouds to
        params:             tuple       parameters, that should be included in the plot ('743', '745', '748', '747')
        case:               str         differ between 'single' plot and multi plot

    """
    if case == "single":
        if "temp" or "dewp_temp" in params:
            color = "blue"
        if "wind_dir" in params:
            color = "magenta"
        if "wind_vel" in params:
            color = "cyan"
        if "pot_temp" in params:
            color ="red"

        ax.xaxis.grid(color=color, linestyle="--", linewidth=0.5)
        ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)
        ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)
        return

    else:
        # left subplot
        ax[0].xaxis.grid(
            color="k",
            linestyle="--",
            linewidth=0.5,
        )
        ax[0].yaxis.grid(color="black", linestyle="--", linewidth=0.5)

        # right subplot
        ax[1].xaxis.grid(
            color="k",
            linestyle="--",
            linewidth=0.5,
        )
        ax[1].yaxis.grid(color="black", linestyle="--", linewidth=0.5)
        return


def plot_winddir(df, fig, ax, hide_x_ticks, case=None):
    # TODO: add docstring
    if case == "single":
        adjustFigAspect(fig, aspect=0.5)
    winddir_df = df["wind_dir"].groupby(pd.qcut(df.index, 10)).mean()
    altitude_df = df["altitude"].groupby(pd.qcut(df.index, 10)).mean()
    # 2) pd.df --> np.array
    avg_winddir_array = winddir_df.to_numpy().round()
    # map these values to an x-y array: [x_dir_1,..,x_dir_10], [y_dir_1,..,y_dir_10]
    x_dir, y_dir = map_degrees(avg_winddir_array=avg_winddir_array)
    avg_altitude_array = altitude_df.to_numpy().round()
    arrow_anchor = [1] * len(avg_altitude_array)
    if hide_x_ticks:
        ax.set_xticklabels("")
        ax.set_xticks([])
    np.meshgrid(arrow_anchor, avg_altitude_array)
    ax.quiver(
        arrow_anchor,
        avg_altitude_array,
        x_dir,
        y_dir,
        pivot="middle",
        scale=5,
        color="k",
    )
    return


def add_plot(xaxis, yaxis, plot_properties, ax, handles, linestyle):
    # TODO: add docstring
    (plot,) = ax.plot(
        xaxis,
        yaxis,
        linestyle,
        label=plot_properties["label"],
    )
    handles.append(plot)
    return ax, handles


def create_plot(
    df,
    relhum_thresh,
    grid,
    clouds,
    outpath,
    station,
    date,
    alt_bot,
    alt_top,
    params,
    print_steps,
    standard_settings,
    personal_settings,
    temp_min,
    temp_max,
    windvel_min,
    windvel_max,
    pot_temp_min,
    pot_temp_max
):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ prepare user inputs & get axis limits ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # date parts for the filename (YYMMDD)
    yymmdd, hour = date[2:8], date[8:]

    # date for figure title (DD.MM.YYYY HH:MM:SS UTC)
    date_nice = f"{date[6:8]}.{date[4:6]}.{date[:4]} {date[8:]}:00:00 UTC"

    # date_nice string --> datetime object of a different formatting (for title)
    date_dt = datetime.datetime.strptime(date_nice, "%d.%m.%Y %H:%M:%S %Z").strftime(
        "%b %d, %Y, %H:%M"
    )

    # this dict, just collects the settings information that is relevant for getting the axes limits
    user_inputs_dict = {
        "standard_settings": standard_settings,
        "personal_settings": personal_settings,
        "temp_min": temp_min,
        "temp_max": temp_max,
        "windvel_min": windvel_min,
        "windvel_max": windvel_max,
        "pot_temp_min": pot_temp_min,
        "pot_temp_max": pot_temp_max,
    }

    # remove unnecessary columns from dataframe
    # TODO: this should be implemented in get_rs.py & the relevant params list is no longer necessary
    if clouds:
        relevant_df_columns = [
            "altitude",
            "rel_hum",
        ]  # keep altitude for yaxis & rel_hum for cloud layers
    else:
        relevant_df_columns = [
            "altitude",
        ]  # keep altitude for yaxis
    parameter_string = str()
    for param in params:
        relevant_df_columns.append(param)
        parameter_string += param + "_"

    # plot title and output filename
    filename = f"rs_{yymmdd}_{hour}_{parameter_string}{station.short_name}"
    title = f"Radiosounding @ {station.long_name}: {date_dt} UTC"

    df = df[relevant_df_columns]
    windvel_min, windvel_max, temp_min, temp_max, pot_temp_min, pot_temp_max = get_axis_limits(
        df, params, user_inputs_dict
    )

    plot_properties = {
        "temp": {
            "label": "Temperature",
            "xlabel": "Temperature [°C]",
            "x_min": temp_min,
            "x_max": temp_max,
        },
        "dewp_temp": {
            "label": "Dew point temperature ",
            "xlabel": "Temperature [°C]",
            "x_min": temp_min,
            "x_max": temp_max,
        },
        "wind_dir": {
            "label": "Wind direction",
            "xlabel": "Wind direction [°]",
        },
        "wind_vel": {
            "label": "Wind velocity",
            "xlabel": "Wind velocity [m/s]",
            "x_min": windvel_min,
            "x_max": windvel_max,
        },
        "pot_temp": {
            "label": "potential Temperature",
            "xlabel": "potential Temperature [K]",
            "x_min": pot_temp_min,
            "x_max": pot_temp_max,
        },
    }
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ start plotting pipeline ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    fig = plt.figure()
    fig.suptitle(title)
    fig.subplots_adjust()
    tkw = dict(size=4, width=1.5)
    yaxis = df["altitude"]

    # case 1: one centred plot on figure --> temp / dewp_temp / temp+dewp_temp / wind_dir / wind_vel
    only_one_param = len(params) == 1
    only_temp_params = params == ("temp", "dewp_temp",) or params == (
        "dewp_temp",
        "temp",
    )
    single_plot_case = only_one_param or only_temp_params
    if single_plot_case:
        print(f"--- creating plot for: {params}")

        # various
        gs = fig.add_gridspec(1, 1, wspace=0)
        ax = gs.subplots(sharex=False, sharey=True)
        handles = []

        # set label properties
        ax.set_ylabel("Altitude [m asl]")
        ax.set_ylim(alt_bot, alt_top)
        ax.set_xlabel(plot_properties[params[0]]["xlabel"])

        # case 1.1: only plot wind direction
        if "wind_dir" in params:
            plot_winddir(df, fig, ax, case="single")

        # case 1.2: only plot a temperature, dew point temperature or wind velocity
        if len(params) == 1 and ("wind_dir" not in params):
            ax, handles = add_plot(
                xaxis=df[params[0]],
                yaxis=yaxis,
                plot_properties=plot_properties[params[0]],
                ax=ax,
                handles=handles,
                linestyle="k-",
            )

        # case 1.3: plot temp & dewp_temp together in one plot
        if len(params) == 2:
            ax, handles = add_plot(
                xaxis=df["temp"],
                yaxis=yaxis,
                plot_properties=plot_properties["temp"],
                ax=ax,
                handles=handles,
                linestyle="b-",
            )
            ax, handles = add_plot(
                xaxis=df["dewp_temp"],
                yaxis=yaxis,
                plot_properties=plot_properties["dewp_temp"],
                ax=ax,
                handles=handles,
                linestyle="c-",
            )

        if clouds:
            plot_clouds(
                df=df,
                relhum_thresh=relhum_thresh,
                print_steps=print_steps,
                ax=ax,
                case="single",
            )

        if grid:
            plot_grid(ax=ax, params=params, case="single")

        # fix x-limits or legend (not necessary for wind_dir plot)
        if "wind_dir" not in params:
            ax.set_xlim(
                plot_properties[params[0]]["x_min"], plot_properties[params[0]]["x_max"]
            )
            ax.legend(handles=handles)

        save_fig(
            filename=filename,
            datatypes=[
                "png",
            ],
            outpath=outpath,
        )

        return

    # case 2: two horizontally aligned subplots on figure --> all possible parameter combinations apart from temp+dewp_temp
    else:
        print(f"--- creating plot for: {params}")

        # various
        gs = fig.add_gridspec(1, 2, wspace=0, width_ratios=[2, 1])
        ax = gs.subplots(sharex=False, sharey=True)
        handles_left, handles_right = [], []

        # set label properties
        ax[0].set_ylim(alt_bot, alt_top)
        ax[0].set_ylabel("Altitude [m asl]")

        # case 2.1: multi-plot case w/o temp/dewp_temp
        if ("temp" not in params) and ("dewp_temp" not in params):
            # axis limits and labels
            ax[0].set_xlim(windvel_min, windvel_max)
            ax[0].set_xlabel("Wind Velocity [m/s]")
            ax[1].set_xlabel("Wind Direction [°]")

            # plot wind velocity on the left plot
            _, _ = add_plot(
                xaxis=df["wind_vel"],
                yaxis=yaxis,
                plot_properties=plot_properties["wind_vel"],
                ax=ax[0],
                handles=handles_left,
                linestyle="k-",
            )

            # plot wind direction on the right subplot
            plot_winddir(df=df, fig=fig, ax=ax[1])

        # case 2.2: multi-plot case w/ temperature and/or dew point temperature
        else:
            ax[0].set_xlim(temp_min, temp_max)
            ax[0].set_xlabel("Temperature [°C]")
            if "wind_vel" in params:
                ax[1].set_xlim(windvel_min, windvel_max)
                ax[1].set_xlabel("Wind Velocity [m/s]")
            else:
                ax[1].set_xlabel("Wind Direction [°]")

            if "temp" in params:
                ax[0], handles_left = add_plot(
                    xaxis=df["temp"],
                    yaxis=yaxis,
                    plot_properties=plot_properties["temp"],
                    ax=ax[0],
                    handles=handles_left,
                    linestyle="b-",
                )

            if "dewp_temp" in params:
                ax[0], handles_left = add_plot(
                    xaxis=df["dewp_temp"],
                    yaxis=yaxis,
                    plot_properties=plot_properties["dewp_temp"],
                    ax=ax[0],
                    handles=handles_left,
                    linestyle="c-",
                )

            if "wind_vel" in params:
                ax[1], handles_right = add_plot(
                    xaxis=df["wind_vel"],
                    yaxis=yaxis,
                    plot_properties=plot_properties["wind_vel"],
                    ax=ax[1],
                    handles=handles_right,
                    linestyle="m-",
                )
                ax[1].legend(handles=handles_right)

            if "wind_dir" in params:
                hide_x_ticks = True
                hide_x_ticks = (
                    "wind_vel" not in params
                )  # if windvel is also in params --> False --> x_ticks are not hidden
                plot_winddir(df=df, fig=fig, ax=ax[1], hide_x_ticks=hide_x_ticks)

        if clouds:
            plot_clouds(
                df=df,
                relhum_thresh=relhum_thresh,
                print_steps=print_steps,
                ax=ax,
            )

        if grid:
            plot_grid(ax=ax, params=params)

        # add legends
        ax[0].legend(handles=handles_left)

        save_fig(
            filename=filename,
            datatypes=[
                "png",
            ],
            outpath=outpath,
        )
        return
