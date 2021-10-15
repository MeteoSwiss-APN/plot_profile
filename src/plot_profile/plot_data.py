"""Purpose: define functions.

Author: Michel Zeller

Date: 05/10/2021.
"""

# Standard library
import os
from mmap import ACCESS_DEFAULT

# Third-party
import matplotlib.pyplot as plt  # use: to create plots
import numpy as np
import pandas as pd
from matplotlib import ticker

# from .get_data import *

# import pdb  # use: python debugger, i.e. pdb.set_trace()


def extract_clouds(df, relhum_thresh, print_steps):
    cloud_df = df[["altitude", "relhum"]]  # extract the altitude & relhum columns
    cloud_df = cloud_df[
        cloud_df["relhum"] >= relhum_thresh
    ]  # remove rows where no clouds are present
    cloud_df = cloud_df[["altitude"]]  # remove the relhum column
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
    x_dir, y_dir, i = [], [], 0
    while i < len(avg_winddir_array):
        x_dir.append(np.cos(avg_winddir_array[i] - 90))
        y_dir.append(np.sin(avg_winddir_array[i] - 90))
        i += 1
    # print(f'x_dir = {x_dir} and y_dir = {y_dir}')
    return x_dir, y_dir


def adjustFigAspect(fig, aspect=1):
    """**summary line** this function was taken from stackoverflow, to create plots with different aspect ratios.

    **description starts after blank line above***
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


def plot_clouds(df, relhum_thresh, print_steps, ax, params, plot_properties):
    cloud_start, cloud_end = extract_clouds(
        df=df, relhum_thresh=relhum_thresh, print_steps=print_steps
    )
    if not cloud_start:
        print(
            f'No clouds for this altidue range/date. (max relhum: {df["relhum"].max()} while relhum_thresh: {relhum_thresh})'
        )
    else:
        # plot lines which correspond to clouds
        i = 0
        while i < len(cloud_start):
            if params in plot_properties:
                ax.axhspan(
                    ymin=cloud_start[i],
                    ymax=cloud_end[i],
                    color="grey",
                    linestyle="-",
                    alpha=0.5,
                )
            else:
                ax[0].axhspan(
                    ymin=cloud_start[i],
                    ymax=cloud_end[i],
                    color="grey",
                    linestyle="-",
                    alpha=0.5,
                )
            i += 1

    return


def plot_grid(ax, plot_properties, params):
    if params in plot_properties:  # single plot case:
        ax.xaxis.grid(
            color=plot_properties[params]["xlabel_color"], linestyle="--", linewidth=0.5
        )
        ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)
        ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)
    else:  # mutli plot case
        ax[1].xaxis.grid(
            color=plot_properties[("742", "746", "748")]["xlabel_color"],
            linestyle="--",
            linewidth=0.5,
        )
        ax[1].yaxis.grid(color="black", linestyle="--", linewidth=0.5)
        ax[0].xaxis.grid(
            color=plot_properties[("742", "745", "746")]["xlabel_color"],
            linestyle="--",
            linewidth=0.5,
        )
        ax[0].yaxis.grid(color="black", linestyle="--", linewidth=0.5)

    return


def check_settings(
    standard_settings,
    params,
    personal_settings,
    windvel_min,
    windvel_max,
    temp_min,
    temp_max,
    plot_properties,
):
    if params in plot_properties:  # single plot case
        x_min, x_max = 0, 0
        if standard_settings:  # here, the standard settings are being defined
            if "748" in params:  # if the x-axis displays the windvelocity
                x_min = 0  # [m/s]
                x_max = 30  # [m/s]
            else:  # if the x-axis displays the (dew point) temperature
                x_min = -100  # [°C]
                x_max = 30  # [°C]

        if personal_settings:
            if "748" in params:  # if the x-axis displays the windvelocity
                x_min = windvel_min  # [m/s]
                x_max = windvel_max  # [m/s]
            else:  # if the x-axis displays the (dew point) temperature
                x_min = temp_min  # [°C]
                x_max = temp_max  # [°C]
        return x_min, x_max
    else:
        x_min_wind, x_max_wind, x_min_temp, x_max_temp = 0, 0, 0, 0
        if standard_settings:  # here, the standard settings are being defined
            x_min_wind = 0  # [m/s]
            x_max_wind = 30  # [m/s]
            x_min_temp = -100  # [°C]
            x_max_temp = 30  # [°C]
        if personal_settings:
            x_min_wind = windvel_min  # [m/s]
            x_max_wind = windvel_max  # [m/s]
            x_min_temp = temp_min  # [°C]
            x_max_temp = temp_max  # [°C]
        return x_min_wind, x_max_wind, x_min_temp, x_max_temp


def create_plot(
    df,
    relhum_thresh,
    grid,
    clouds,
    outpath,
    station_name,
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
):
    fig = plt.figure()

    blue = "b"
    cyan = "c"
    magenta = "m"

    date_ugly = date[:8]
    date_nice = (
        date[6:8] + "." + date[4:6] + "." + date[:4]
    )  # nicely formated date for figure title, i.e. DD.MM.YYYY

    outpath = outpath + date_ugly + "/"

    gs_multi = fig.add_gridspec(
        1, 2, wspace=0, width_ratios=[2, 1]
    )  # 2 horizontally aligned subplots
    gs_single = fig.add_gridspec(1, 1, wspace=0)

    os.makedirs(
        outpath, exist_ok=True
    )  # create plot folder if it doesn't already exist

    # properties dict for single plot cases
    plot_properties = {
        # winddir only
        ("742", "743", "746"): {
            "name": "winddir",
            "which_plot": "--- creating winddir plot",
            "label": "Wind Direction",
            "xlabel": "Wind Direction [°]",
            "xlabel_color": "m",
            "line_color": "m",
        },
        # windvel only
        ("742", "746", "748"): {
            "name": "windvel",
            "which_plot": "--- creating windvel plot",
            "label": "Wind Velocity",
            "xlabel": "Wind Velocity [m/s]",
            "xlabel_color": "c",
            "line_color": "c-",
            "x_axis": df["windvel"],
            "x_min": df["windvel"].min() * 1.1,
            "x_max": df["windvel"].max() * 1.1,
        },
        # temp only
        ("742", "745", "746"): {
            "name": "temp",
            "which_plot": "--- creating temp plot",
            "label": "Temperature",
            "xlabel": "Temperature [°C]",
            "xlabel_color": "b",
            "line_color": "b-",
            "x_axis": df["temp"],
            "x_min": df["temp"].min() * 1.1,
            "x_max": df["temp"].max() * 1.1,
        },
        # dewp only
        ("742", "746", "747"): {
            "name": "dewp",
            "which_plot": "--- creating dewp plot",
            "label": "Dew Point Temperature ",
            "xlabel": "Temperature [°C]",
            "xlabel_color": "b",
            "line_color": "b--",
            "x_axis": df["dewp"],
            "x_min": df["dewp"].min() * 1.1,
            "x_max": df["dewp"].max() * 1.1,
        },
        # temp + dewp
        ("742", "745", "746", "747"): {
            "name": "temperature",
            "which_plot": "--- creating temp+dewp plot",
            "label": "Temperature",
            "label_dewp": "Dew Point Temperature",
            "xlabel": "Temperature [°C]",
            "xlabel_color": "b",
            "line_color": "b-",
            "line_color_dewp": "b--",
            "x_axis": df["temp"],
            "x_axis_2": df["dewp"],
            "x_min": df["dewp"].min() * 1.1,
            "x_max": df["temp"].max() * 1.1,
        },
    }

    if params in plot_properties:  # single plot cases
        gs = gs_single
        ax = gs.subplots(sharex=False, sharey=True)
        fig.subplots_adjust()
        tkw = dict(size=4, width=1.5)
        handles = []

        print(
            plot_properties[params]["which_plot"]
        )  # print, which plot is being created

        ax.set_xlabel(plot_properties[params]["xlabel"])
        ax.xaxis.label.set_color(plot_properties[params]["xlabel_color"])
        ax.set_ylabel("Altitude [m]")

        if params == (
            "742",
            "743",
            "746",
        ):  # winddir is a 'special case' because it's plottet using the quiver function.
            adjustFigAspect(fig, aspect=0.5)
            winddir_df = df["winddir"].groupby(pd.qcut(df.index, 10)).mean()
            altitude_df = df["altitude"].groupby(pd.qcut(df.index, 10)).mean()
            # 2) pd.df --> np.array
            avg_winddir_array = winddir_df.to_numpy().round()
            # map these values to an x-y array: [x_dir_1,..,x_dir_10], [y_dir_1,..,y_dir_10]
            x_dir, y_dir = map_degrees(avg_winddir_array=avg_winddir_array)
            avg_altitude_array = altitude_df.to_numpy().round()
            arrow_anchor = [1] * len(avg_altitude_array)
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
                color="m",
            )
            if clouds:
                plot_clouds(
                    df=df,
                    relhum_thresh=relhum_thresh,
                    print_steps=print_steps,
                    ax=ax,
                    params=params,
                    plot_properties=plot_properties,
                )

            if grid:
                ax.yaxis.grid(color="black", linestyle="--", linewidth=0.5)

            if True:
                fig.suptitle(f"Radiosounding Data from {station_name} on {date_nice}")
                path_to_figure = (
                    outpath
                    + station_name
                    + "_"
                    + date_ugly
                    + "_"
                    + plot_properties[params]["name"]
                    + "_plot.png"
                )
                print("Saved plot: ", os.getcwd() + "/" + path_to_figure)
                plt.savefig(path_to_figure)
                return

        (plot,) = ax.plot(
            plot_properties[params]["x_axis"],
            df["altitude"],
            plot_properties[params]["line_color"],
            label=plot_properties[params]["label"],
        )

        if params == ("742", "745", "746", "747"):
            (plot2,) = ax.plot(
                plot_properties[params]["x_axis_2"],
                df["altitude"],
                plot_properties[params]["line_color_dewp"],
                label=plot_properties[params]["label_dewp"],
            )
            handles.append(plot2)

        x_min, x_max = check_settings(
            standard_settings=standard_settings,
            params=params,
            personal_settings=personal_settings,
            windvel_min=windvel_min,
            windvel_max=windvel_max,
            temp_min=temp_min,
            temp_max=temp_max,
            plot_properties=plot_properties,
        )

        if (not standard_settings) and (
            not personal_settings
        ):  # scale the x-axis according to the measurements (+- 10% on either side)
            x_min = plot_properties[params]["x_min"]
            x_max = plot_properties[params]["x_max"]

        ax.set_xlim(x_min, x_max)
        ax.tick_params(axis="x", colors=plot_properties[params]["xlabel_color"], **tkw)
        handles.append(plot)

        if clouds:  # add clouds
            plot_clouds(
                df=df,
                relhum_thresh=relhum_thresh,
                print_steps=print_steps,
                ax=ax,
                params=params,
                plot_properties=plot_properties,
            )

        if grid:  # add grid
            plot_grid(ax=ax, plot_properties=plot_properties, params=params)

        if True:  # save figure
            ax.legend(handles=handles)
            fig.suptitle(f"Radiosounding Data from {station_name} on {date_nice}")
            path_to_figure = (
                outpath
                + station_name
                + "_"
                + date_ugly
                + "_"
                + plot_properties[params]["name"]
                + "_plot.png"
            )
            print("Saved plot: ", os.getcwd() + "/" + path_to_figure)
            plt.savefig(path_to_figure)
            return

    else:  # multi plot cases
        gs = gs_multi
        ax = gs.subplots(sharex=False, sharey=True)
        fig.subplots_adjust()
        tkw = dict(size=4, width=1.5)
        handles_left, handles_right = [], []

        if ("743" in params or "748" in params) and (
            "745" in params or "747" in params
        ):  # wind-/temp-parameters together
            print("--- creating all-in-one plot")

            if "745" in params:  # add temp to subplot
                (temp,) = ax[0].plot(
                    plot_properties[("742", "745", "746")]["x_axis"],
                    df["altitude"],
                    plot_properties[("742", "745", "746")]["line_color"],
                    label=plot_properties[("742", "745", "746")]["xlabel"],
                )

                _, _, x_min_temp, x_max_temp = check_settings(
                    standard_settings=standard_settings,
                    params=params,
                    personal_settings=personal_settings,
                    windvel_min=windvel_min,
                    windvel_max=windvel_max,
                    temp_min=temp_min,
                    temp_max=temp_max,
                    plot_properties=plot_properties,
                )

                if (not standard_settings) and (
                    not personal_settings
                ):  # scale the x-axis according to the measurements (+- 10% on either side)
                    x_min_temp = df["temp"].min() * 1.1
                    x_max_temp = df["temp"].max() * 1.1

                handles_left.append(temp)

            if "747" in params:  # add dewp to subplot
                (dewp,) = ax[0].plot(
                    plot_properties[("742", "746", "747")]["x_axis"],
                    df["altitude"],
                    plot_properties[("742", "746", "747")]["line_color"],
                    label=plot_properties[("742", "746", "747")]["label"],
                )

                if (not standard_settings) and (not personal_settings):
                    x_min_temp = (
                        df["dewp"].min() * 1.1
                    )  # if dewp is in params, this is the lower x-axis boundary
                    if (
                        "745" not in params
                    ):  # if temp is in params as well, this is the upper x-axis boundary
                        x_max_temp = df["dewp"].max() * 1.1
                handles_left.append(dewp)

                ax[0].set_xlim(x_min_temp, x_max_temp)
                ax[0].set_ylim(alt_bot, alt_top)  # limit for left y-axis:    altitude
                ax[0].set_xlabel("Temperature [°C]")
                ax[0].set_ylabel("Altitude [m]")
                ax[0].xaxis.label.set_color(blue)
                ax[0].tick_params(axis="x", colors=blue, **tkw)

            if "748" in params:  # add windvelocity to subplot
                (windvel,) = ax[1].plot(
                    plot_properties[("742", "746", "748")]["x_axis"],
                    df["altitude"],
                    plot_properties[("742", "746", "748")]["line_color"],
                    label=plot_properties[("742", "746", "748")]["label"],
                )

                x_min_wind, x_max_wind, _, _ = check_settings(
                    standard_settings=standard_settings,
                    params=params,
                    personal_settings=personal_settings,
                    windvel_min=windvel_min,
                    windvel_max=windvel_max,
                    temp_min=temp_min,
                    temp_max=temp_max,
                    plot_properties=plot_properties,
                )

                if (not standard_settings) and (
                    not personal_settings
                ):  # scale the x-axis according to the measurements (+- 10% on either side)
                    x_min_wind = plot_properties[("742", "746", "748")]["x_min"]
                    x_max_wind = plot_properties[("742", "746", "748")]["x_max"]

                ax[1].set_xlim(x_min_wind, x_max_wind)
                ax[1].set_xlabel("Wind Velocity [m/s]")
                ax[1].xaxis.label.set_color(cyan)
                ax[1].tick_params(axis="x", colors=cyan, **tkw)
                handles_right.append(windvel)

            if "743" in params:  # add winddirection to subplot
                winddir_df = df["winddir"].groupby(pd.qcut(df.index, 10)).mean()
                altitude_df = df["altitude"].groupby(pd.qcut(df.index, 10)).mean()
                # 2) pd.df --> np.array
                avg_winddir_array = (
                    winddir_df.to_numpy().round()
                )  # map these values to an x-y array: [x_dir_1,..,x_dir_10], [y_dir_1,..,y_dir_10]
                x_dir, y_dir = map_degrees(avg_winddir_array=avg_winddir_array)
                avg_altitude_array = altitude_df.to_numpy().round()

                if "748" in params:
                    if standard_settings or personal_settings:
                        arrow_anchor = [x_max_wind - 10] * len(avg_altitude_array)
                    else:
                        arrow_anchor = [df["windvel"].max() * 0.9] * len(
                            avg_altitude_array
                        )
                else:  # if only the wind direction is plottet alongside the temp. curves remove the x-axis for ax[1]
                    arrow_anchor = [1] * len(avg_altitude_array)
                    ax[1].set_xticklabels("")
                    ax[1].set_xticks([])
                np.meshgrid(arrow_anchor, avg_altitude_array)
                ax[1].quiver(
                    arrow_anchor,
                    avg_altitude_array,
                    x_dir,
                    y_dir,
                    pivot="middle",
                    scale=5,
                    color="m",
                )
                if "748" not in params:
                    ax[1].set_xlabel("Wind Direction [°]")
                    ax[1].xaxis.label.set_color(magenta)
                    ax[1].tick_params(axis="x", colors=magenta, **tkw)

            if clouds:  # add clouds
                plot_clouds(
                    df=df,
                    relhum_thresh=relhum_thresh,
                    print_steps=print_steps,
                    ax=ax,
                    params=params,
                    plot_properties=plot_properties,
                )

            if grid:  # add grid
                plot_grid(ax=ax, plot_properties=plot_properties, params=params)

            if True:  # save figure
                ax[0].legend(handles=handles_left)
                fig.suptitle(f"Radiosounding Data from {station_name} on {date_nice}")
                path_to_figure = (
                    outpath + station_name + "_" + date_ugly + "_complete_plot.png"
                )
                print("Saved plot: ", os.getcwd() + "/" + path_to_figure)
                plt.savefig(path_to_figure)
                return

        if "743" in params and "748" in params:  # plot windvel & winddir
            print("--- creating complete wind plot")

            if True:  # windvel properties (left subplot)
                (windvel,) = ax[0].plot(
                    plot_properties[("742", "746", "748")]["x_axis"],
                    df["altitude"],
                    plot_properties[("742", "746", "748")]["line_color"],
                    label=plot_properties[("742", "746", "748")]["label"],
                )

                x_min_wind, x_max_wind, _, _ = check_settings(
                    standard_settings=standard_settings,
                    params=params,
                    personal_settings=personal_settings,
                    windvel_min=windvel_min,
                    windvel_max=windvel_max,
                    temp_min=temp_min,
                    temp_max=temp_max,
                    plot_properties=plot_properties,
                )

                if (not standard_settings) and (
                    not personal_settings
                ):  # scale the x-axis according to the measurements (+- 10% on either side)
                    x_min_wind = plot_properties[("742", "746", "748")]["x_min"]
                    x_max_wind = plot_properties[("742", "746", "748")]["x_max"]

                ax[0].set_xlim(x_min_wind, x_max_wind)
                ax[0].set_xlabel("Wind Velocity [m/s]")
                ax[0].xaxis.label.set_color(cyan)
                ax[0].tick_params(axis="x", colors=cyan, **tkw)
                handles_left.append(windvel)

            if True:  # winddir properties (right subplot)
                winddir_df = df["winddir"].groupby(pd.qcut(df.index, 10)).mean()
                altitude_df = df["altitude"].groupby(pd.qcut(df.index, 10)).mean()
                # 2) pd.df --> np.array
                avg_winddir_array = (
                    winddir_df.to_numpy().round()
                )  # map these values to an x-y array: [x_dir_1,..,x_dir_10], [y_dir_1,..,y_dir_10]
                x_dir, y_dir = map_degrees(avg_winddir_array=avg_winddir_array)
                avg_altitude_array = altitude_df.to_numpy().round()
                arrow_anchor = [1] * len(avg_altitude_array)
                ax[1].set_xticklabels("")
                ax[1].set_xticks([])
                ax[1].set_xlabel("Wind Direction [°]")
                ax[1].xaxis.label.set_color(magenta)
                ax[1].tick_params(axis="x", colors=magenta, **tkw)
                np.meshgrid(arrow_anchor, avg_altitude_array)
                ax[1].quiver(
                    arrow_anchor,
                    avg_altitude_array,
                    x_dir,
                    y_dir,
                    pivot="middle",
                    scale=5,
                    color="m",
                )

            if clouds:  # add clouds
                plot_clouds(
                    df=df,
                    relhum_thresh=relhum_thresh,
                    print_steps=print_steps,
                    ax=ax,
                    params=params,
                    plot_properties=plot_properties,
                )

            if grid:  # add grid
                plot_grid(ax=ax, plot_properties=plot_properties, params=params)

            if True:  # save figure
                ax[0].legend(handles=handles_left)
                fig.suptitle(f"Radiosounding Data from {station_name} on {date_nice}")
                path_to_figure = (
                    outpath + station_name + "_" + date_ugly + "_wind_plot.png"
                )
                print("Saved plot: ", os.getcwd() + "/" + path_to_figure)
                plt.savefig(path_to_figure)
                return
