"""Purpose: define functions.

Author: Michel Zeller

Date: 05/10/2021.
"""

# Standard library
import os
import subprocess  # use: run command line commands from python
from io import StringIO

# Third-party
import click  # use: specify command line arguments
import matplotlib.pyplot as plt  # use: to create plots
import numpy as np
import pandas as pd
from matplotlib import ticker

# import pdb  # use: python debugger, i.e. pdb.set_trace()


def reformat_inputs(
    start, end, params, station_id, params_dict, stations_dict, print_steps
):

    print("--- reformating inputs")

    # reformat the date inputs
    end = end + "0000"
    start = start + "0000"

    # reformat the parameter inputs
    params = list(params)  # params: tuple --> list

    if print_steps:
        print(f"params before mapping: {params}")

    i = 0
    for item in params:
        if params_dict[item]:
            params[i] = params_dict[item]
        i += 1
    params.insert(
        0, "742"
    )  # we ALWAYS want to retrieve the height-column. therefore it doesnt need to be an optional parameter

    params_tuple = tuple(params)

    if print_steps:
        print(f"params after mapping: {params}")

    # reformat the params input from tuple to string
    params_string = ""
    for item in params:
        params_string = params_string + item + ","
    # params: list --> str
    params = params_string[:-1]  # remove last comma

    # reformat the station_id to its actual name
    station_name = stations_dict[station_id]

    return start, end, params, params_tuple, station_name


def dwh2pandas(params, station_id, start, end, print_steps):
    cmd = (
        "/oprusers/osm/bin/retrieve_cscs --show_records -j lat,lon,elev,name,wmo_ind -w 22 -s profile -p "
        + params
        + " -i int_ind,"
        + station_id
        + " -t "
        + start
        + "-"
        + end
        + " -C 34"
    )  # TODO: not sure what the -C 34 does actually
    print("--- calling: " + cmd)
    # ~~~~~~~~~~~~~~~ the following code was taken from the dwh2pandas.py script by Claire Merker ~~~~~~~~~~~~~~~
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )
    # ~~~~~~~~~~~~~~~ check if cmd can be executed ~~~~~~~~~~~~~~~
    try:
        out, err = proc.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        raise SystemExit("--- ERROR: timeout expired for process " + cmd)
    if proc.returncode != 0:
        raise SystemExit(err)

    # ~~~~~~~~~~~~~~~ load DWH retrieve output into pandas DataFrame ~~~~~~~~~~~~~~~
    header_line = pd.read_csv(
        StringIO(out), skiprows=0, nrows=1, sep="\s+", header=None, engine="c"
    )

    # parse the command linen output
    data = pd.read_csv(
        StringIO(out),
        skiprows=2,
        skipfooter=2,
        sep="|",
        header=None,
        names=header_line.values.astype(str)[0, :],
        engine="python",
        parse_dates=["termin"],
    )

    # clean up the dataframe a bit
    data.replace(1e7, np.nan, inplace=True)

    # check if no data is available for the time period
    if data.empty:
        raise SystemExit("--- WARN: no data available for period " + start + "-" + end)
    else:
        if print_steps:
            with pd.option_context(
                "display.max_rows",
                None,
                "display.max_columns",
                None,
                "display.width",
                1000,
            ):
                print(data.head())
        print("--- data retrieved into dataframe")
        return data


def extract_columns(params_tuple, data, print_steps, alt_bot, alt_top):

    columns = list(params_tuple)
    params_df = pd.DataFrame(data, columns=columns)
    params_df = params_df[params_df["742"] >= alt_bot]
    params_df = params_df[params_df["742"] <= alt_top]
    # print(params_df)
    if print_steps:
        print(params_df.head())
    print("--- relevant columns extracted into a new dataframe")
    return params_df


def extract_clouds(df, relhum_thresh):
    # print(df)
    cloud_df = df[["742", "746"]]  # extract the altitude & relhum columns
    cloud_df = cloud_df[
        cloud_df["746"] >= relhum_thresh
    ]  # remove rows where no clouds are present
    cloud_df = cloud_df[["742"]]  # remove the relhum column
    cloud_list = list(cloud_df.index.values)  # index list of cloud layers
    cloud_array = (
        cloud_df.to_numpy()
    )  # to cloud_list corresponding array of altitudes, where clouds are presen

    if not cloud_list:
        return [], []
    else:
        cloud_start = []  # array containing the cloud layer start-altitudes
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
                tmp1 = row  # temporary start point
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

        # print(f'cloud list: {cloud_list} \n cloud array: {cloud_array} \n cloud start: {cloud_start}  \n cloud_end: {cloud_end}')
        return cloud_start, cloud_end


def map_degrees(avg_winddir_array):
    x_dir, y_dir, i = [], [], 0
    while i < len(avg_winddir_array):
        x_dir.append(np.cos(avg_winddir_array[i] - 90))
        y_dir.append(np.sin(avg_winddir_array[i] - 90))
        i += 1
    # print(f'x_dir = {x_dir} and y_dir = {y_dir}')
    return x_dir, y_dir


def create_plots(
    df, relhum_thresh, grid, clouds, outpath, station_name, start, alt_bot, alt_top
):
    print("--- creating plots")

    cloud_start, cloud_end = extract_clouds(df=df, relhum_thresh=relhum_thresh)

    fig = plt.figure()

    gs = fig.add_gridspec(
        1, 2, wspace=0, width_ratios=[2, 1]
    )  # 2 horizontally aligned subplots wi/ ratio 2:1
    ax = gs.subplots(sharex=False, sharey=True)

    fig.subplots_adjust()
    tkw = dict(size=4, width=1.5)
    handles_left, handles_right = [], []

    # TEMPERATURE & DEW POINT (plottet on the regular x-axis of ax[0])
    (temp,) = ax[0].plot(df["745"], df["742"], "b-", label="Temperature")
    (dewp,) = ax[0].plot(df["747"], df["742"], "b--", label="Dew Point Temperature")
    ax[0].set_xlim(
        df["747"].min() * 1.1, df["745"].max() * 1.1
    )  # limit for bottom x-axis:  temp; dewp
    ax[0].set_ylim(alt_bot, alt_top)  # limit for left y-axis:    altitude
    ax[0].set_xlabel("Temperature [°C]")
    ax[0].set_ylabel("Altitude [m]")
    ax[0].xaxis.label.set_color(temp.get_color())
    ax[0].tick_params(axis="x", colors=temp.get_color(), **tkw)

    handles_left.append(temp)
    handles_left.append(dewp)

    # WIND VELOCITY (plottet on the regular x-axis of ax[1])
    (windvel,) = ax[1].plot(df["748"], df["742"], "c-", label="Wind Velocity")
    ax[1].set_xlim(0, df["748"].max() + 10)
    ax[1].set_xlabel("Wind Velocity [m/s]")
    ax[1].xaxis.label.set_color(windvel.get_color())
    ax[1].xaxis.set_major_locator(ticker.MaxNLocator(6))
    ax[1].tick_params(axis="x", colors=windvel.get_color(), **tkw)
    handles_right.append(windvel)

    # WIND DIRECTION
    # ax_winddir = ax[1].twiny() # additional x-axis for right subplot
    # winddir, = ax_winddir.plot(df['743'][0::100], df['742'][0::100], "y-", label="Wind Direction")
    # winddir, = ax_winddir.plot(df['743'], df['742'], "y-", label="Wind Direction")
    # ax_winddir.set_xlim(0,360)
    # ax_winddir.xaxis.set_major_locator(ticker.MaxNLocator(6))
    # ax_winddir.set_xlabel("Wind Direction [°]")
    # ax_winddir.xaxis.label.set_color(winddir.get_color())
    # ax_winddir.tick_params(axis='x', colors=winddir.get_color(), **tkw)
    # handles_right.append(winddir)

    # WIND DIRECTION USING QUIVER
    winddir_df = df["743"].groupby(pd.qcut(df.index, 10)).mean()
    altitude_df = df["742"].groupby(pd.qcut(df.index, 10)).mean()
    # 2) pd.df --> np.array
    avg_winddir_array = (
        winddir_df.to_numpy().round()
    )  # map these values to an x-y array: [x_dir_1,..,x_dir_10], [y_dir_1,..,y_dir_10]
    x_dir, y_dir = map_degrees(avg_winddir_array=avg_winddir_array)
    avg_altitude_array = altitude_df.to_numpy().round()
    arrow_anchor = [df["748"].max() + 5] * len(avg_altitude_array)
    X, Y = np.meshgrid(arrow_anchor, avg_altitude_array)
    qv_winddir = ax[1].quiver(
        arrow_anchor,
        avg_altitude_array,
        x_dir,
        y_dir,
        pivot="middle",
        scale=5,
        color="m",
    )

    if clouds:
        if not cloud_start:
            print(
                f'No clouds for this altidue range/date. (max relhum: {df["746"].max()} while relhum_thresh: {relhum_thresh})'
            )
        else:
            # plot lines which correspond to clouds
            i = 0
            while i < len(cloud_start):
                ax[0].axhspan(
                    ymin=cloud_start[i],
                    ymax=cloud_end[i],
                    color="grey",
                    linestyle="-",
                    alpha=0.5,
                )
                i += 1

    if grid:
        # display & colour grid for right subplot
        ax[1].xaxis.grid(color=windvel.get_color(), linestyle="--", linewidth=0.5)
        ax[1].yaxis.grid(color="black", linestyle="--", linewidth=0.5)
        ax[0].xaxis.grid(color=temp.get_color(), linestyle="--", linewidth=0.5)
        ax[0].yaxis.grid(color="black", linestyle="--", linewidth=0.5)
    ax[0].legend(handles=handles_left)
    date = start[6:8] + "." + start[4:6] + "." + start[:4]
    fig.suptitle(f"Radiosounding Data from {station_name} on {date}")

    os.makedirs(outpath, exist_ok=True)  # create outpath if it doesn't already exist
    start = start[:8]
    plt.savefig(outpath + station_name + "_" + start + ".png")
    # plt.show() # display plot
