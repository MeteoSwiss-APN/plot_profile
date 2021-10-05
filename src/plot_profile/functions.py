"""Purpose: define functions.

Author: Michel Zeller

Date: 05/10/2021.
"""

# Standard library
# import pdb  # use: python debugger, i.e. pdb.set_trace()
import subprocess  # use: run command line commands from python
from io import StringIO

# Third-party
import click  # use: specify command line arguments
import matplotlib.pyplot as plt  # use: to create plots
import numpy as np
import pandas as pd


def reformat_inputs(start, end, params, print_steps, station_id, station_type):
    # reformat the date inputs
    end = end + "0000"
    start = start + "0000"

    # reformat the params input
    params = list(params)
    params_edited = []

    if print_steps:
        print(f"params before mapping: {params}")

    # TODO: rewrite this mapping function - there ought to be a cleaner solution
    i = 0
    while i < len(params):
        if params[i] == "gph":
            params_edited.append("742")
        if params[i] == "winddir":
            params_edited.append("743")
        if params[i] == "press":
            params_edited.append("744")
        if params[i] == "temp":
            params_edited.append("745")
        if params[i] == "relhum":
            params_edited.append("746")
        if params[i] == "dewp":
            params_edited.append("747")
        if params[i] == "windvel":
            params_edited.append("748")
        if params[i] == "742":
            params_edited.append("742")
        if params[i] == "743":
            params_edited.append("743")
        if params[i] == "744":
            params_edited.append("744")
        if params[i] == "745":
            params_edited.append("745")
        if params[i] == "746":
            params_edited.append("746")
        if params[i] == "747":
            params_edited.append("747")
        if params[i] == "748":
            params_edited.append("748")
        i += 1
    params = params_edited
    params_tuple = tuple(params)

    if print_steps:
        print(f"params after mapping: {params}")

    # reformat the params input from tuple to string
    params_string = ""
    for item in params:
        params_string = params_string + item + ","
    params = params_string[:-1]  # remove last comma

    if print_steps:
        # check default params
        print(f"The station ID is {station_id}")
        print(f"The start date is {start}")
        print(f"The end date is {end}")
        print(f"The chosen params are: {params}")
        print(f"The default DWH station type is: {station_type}")

    return start, end, params, params_tuple


def dwh2pandas(params, station_id, start, end, station_type, print_steps):
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
        return data


def extract_columns(params_tuple, data, print_steps, alt_bot, alt_top):

    columns = list(params_tuple)
    params_df = pd.DataFrame(data, columns=columns)
    params_df = params_df[params_df["742"] >= alt_bot]
    params_df = params_df[params_df["742"] <= alt_top]
    # print(params_df)
    if print_steps:
        print(params_df.head())

    return params_df


def create_plots(params_df, start, station_id, outpath):
    # plot temperatures agains altitude
    plt.figure(0)
    plt.plot(params_df["745"], params_df["742"], label="temperature")  # etc.
    plt.plot(params_df["747"], params_df["742"], label="dew point temperature")
    plt.xlabel("Tempterature [°C]")
    plt.ylabel("Geopotential Height [m]")
    date = start[6:8] + "." + start[4:6] + "." + start[:4]
    plt.title(f"Radiosounding Data from station {station_id} on {date}")
    plt.legend()
    start = start[:8]
    plt.savefig(outpath + "temp_" + station_id + "_" + start + ".png")

    # # plot pressure against altitude
    # plt.figure(1)
    # plt.plot(params_df["744"], params_df["742"], label="pressure")  # etc.
    # plt.xlabel("Pressure [hPa]")
    # plt.ylabel("Geopotential Height [m]")
    # date = start[6:8] + "." + start[4:6] + "." + start[:4]
    # plt.title(f"Radiosounding Data from station {station_id} on {date}")
    # plt.legend()
    # start = start[:8]
    # plt.savefig('plots/' + 'press_' + station_id + '_' + start + '.png')
