"""Purpose: Retrieve observational data from DWH.

Author: Stephanie Westerhuis

Date: 27/12/2022.
"""

# Standard library
import datetime as dt
import pprint
import subprocess  # use: run command line commands from python
import sys
from io import StringIO

# Third-party
import numpy as np
import pandas as pd

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.variables import vdf

# import ipdb


def yy2yyyy(yy):
    """Add '20' to timestamp.

    E.g. '21081812' will become '2021081812'

    Args:
        yy (string)

    Returns:
        yyyy (string)

    """
    return f"20{yy}"


def parse_timestamps(timestamps):
    """Parse different formats of timestamps.

    Args:
    timestamps  (str, datetime-obj or list of one of those)

    Returns:
    t1, t2      (YYYYmmddHH)

    """
    # if list
    if isinstance(timestamps, list):

        # only 1 element in list
        if len(timestamps) == 1:
            ts0 = timestamps[0]

            # if string
            if isinstance(ts0, str):
                if len(ts0) == 10:
                    return ts0, ts0
                elif len(ts0) == 8:
                    ts0_20 = yy2yyyy(ts0)
                    return ts0_20, ts0_20

            # if datetime object
            elif isinstance(ts0, dt.datetime):
                ts0_str = ts0.strftime("%Y%m%d%H")
                return ts0_str, ts0_str

        # 2 elements in list
        elif len(timestamps) == 2:
            ts0 = timestamps[0]
            ts1 = timestamps[1]
            # if string
            if isinstance(ts0, str):
                if len(ts0) == 10:
                    return ts0, ts1
                elif len(ts0) == 8:
                    ts0_20 = yy2yyyy(ts0)
                    ts1_20 = yy2yyyy(ts1)
                    return ts0_20, ts1_20

            # if datetime-obj
            elif isinstance(ts0, dt.datetime):
                ts0_str = ts0.strftime("%Y%m%d%H")
                ts1_str = ts1.strftime("%Y%m%d%H")
                return ts0_str, ts1_str

        else:
            print("! too many timestamps")
            sys.exit(1)

    # if only 1 string is given
    elif isinstance(timestamps, str):
        if len(timestamps) == 10:
            return timestamps, timestamps
        elif len(timestamps) == 8:
            ts_20 = yy2yyyy(timestamps)
            return ts_20, ts_20

    # if only 1 datetime object is given
    elif isinstance(timestamps, dt.datetime):
        ts_str = timestamps.strftime("%Y%m%d%H")
        return ts_str, ts_str

    else:
        print("! timestamps input is nonsense!")
        sys.exit(1)


def parse_vars(vars, device):
    """Create comma-separated strings of DWH IDs from tuple with one or more variables.

    Args:
    vars        (tuple)     variables
    device      (str)       measurement device: rs, mwr, 2m, 5cm

    Returns:
    str         E.g. 'temp' or 'temp,dewp_temp'

    """
    # only one string in tuple
    if len(vars) == 1:
        try:
            vars_str = vdf[vars[0]].dwh_id[device]
        except KeyError:
            print(f"! Device {device} not available for {vars[0]}!")
            sys.exit(1)

    # multiple strings
    else:
        try:
            vars_str = vdf[vars[0]].dwh_id[device]
            for var in vars[1:]:
                # add variable separated by comma
                vars_str += f",{vdf[var].dwh_id[device]}"
        except KeyError:
            print(f"! Device not available for {vars}!")

    # add altitude for radiosounding retrieves
    if device == "rs":
        # add altitude separated by comma
        vars_str += f",{vdf['altitude'].dwh_id['rs']}"

    return vars_str


def dwh2pandas(cmd, verbose):
    """Run retrieve_cscs command in terminal, create pandas dataframe."""
    if verbose:
        print("Calling: " + cmd)

    # run command in terminal
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )
    try:
        out, err = proc.communicate(timeout=120)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        raise SystemExit("--- ERROR: timeout expired for process " + cmd)
    if proc.returncode != 0:
        raise SystemExit(err)

    # load DWH retrieve output
    header_line = pd.read_csv(
        StringIO(out), skiprows=0, nrows=1, sep="\s+", header=None, engine="c"
    )

    check = (
        f"{header_line[0].iloc[0]} {header_line[1].iloc[0]} {header_line[2].iloc[0]}"
    )
    if check == "records read: 0":
        print(
            f"--- WARNING: For the given time period, location and/or device, no data could be retrieved. Returning empty dataframe."
        )
        return pd.DataFrame()

    # parse the command line output into pandas dataframe
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

    # check if no data is available for the time period
    if data.empty:
        # TODO: Code should not break but return empty dataframe
        raise SystemExit("--- WARN: no DWH data available.")
    else:
        if verbose:
            with pd.option_context(
                "display.max_rows",
                None,
                "display.max_columns",
                None,
                "display.width",
                1000,
            ):
                print(data.head())
            print("Finished data retrieve from DWH into dataframe.")

    # clean up the dataframe: replae "10000000" with NaN
    data.replace(1e7, np.nan, inplace=True)

    return data


def dwh_surface(station_name, vars_str, start, end, verbose=False):
    """Retrieve surface-based data from DWH.

    Args:
        station_name    (str):  DWH station name
        vars_str        (str):  DWH IDs of variables, separated by comma
        start           (str):  YYYYmmddHH
        end             (str):  YYYYmmddHH (same or later as <start>)
        verbose         (bool): verbose statements

    Returns:
        pandas dataframe:   DWH surface data

    """
    if verbose:
        print(f"Retrieving surface-based data for:")
        print(f"  {vars_str}")
        print(f"  from {start} to {end}")
        print(f"  at {station_name}.")

    # retrieve_cscs command:
    cmd = (
        "/oprusers/osm/bin/retrieve_cscs --show_records -j lat,lon,name,wmo_ind"
        + " -s surface "
        + " -i nat_abr,"
        + station_name
        + " -p "
        + vars_str
        + " -t "
        + start
        + "-"
        + end
        + " --use-limitation 50"
    )

    # run command
    data = dwh2pandas(cmd, verbose)

    return data


def dwh_profile(device, station_id, vars_str, start, end, verbose=False):
    """Retrieve profile-based data from DWH.

    Args:
        station_id  (str):  DWH ID of station (number as string!)
        vars_str    (str):  DWH IDs of variables, separated by comma
        start       (str):  YYYYmmddHH
        end         (str):  YYYYmmddHH (same or later as <start>)
        verbose     (bool): verbose statements

    Returns:
        pandas dataframe:   DWH profile data

    """
    if verbose:
        print(f"Retrieving profile-based data for:")
        print(f"  {vars_str}")
        print(f"  from {start}")
        print(f"  to   {end}")
        print(f"  at {station_id}.")

    cmd = (
        "/oprusers/osm/bin/retrieve_cscs --show_records -j lat,lon,elev,name,wmo_ind"
        + " -s profile -p "
        + vars_str
        + " -i int_ind,"
        + station_id
        + " -t "
        + start
        + "-"
        + end
    )

    if device == "rs":
        cmd = cmd + " -C 34 -w 22"
    elif device == "mwr":
        cmd = cmd + " -C 38 -w 31"
    else:
        print(f"Unknown profile obs device: {device}.")
        sys.exit(1)

    # run command
    data = dwh2pandas(cmd, verbose)

    return data


def dwh_retrieve(device, station, vars, timestamps, verbose=False):
    """Retrieve observational data from DWH.

    The retrieve_cscs command works for two different observational types:
        a) surface-based data (2m stations including ceilometers & scintillometers)
        b) profile-based data (radiosoundings - 'rs', radiometers - 'mwr')

    Input:
        device      string              measurement device: 'rs', 'mwr', 'cm', ...
        station     string              station short name
        vars        list of strings     variables
        timestamps  list of strings     either 1 or 2 timestamps YYYYmmddHH

    Output:
        pandas dataframe
    """
    # parse timestamp input to 2 string of format YYYYmmddHH
    t1, t2 = parse_timestamps(timestamps)

    # create tuple of variables if only 1 variable is given
    if isinstance(vars, str):
        vars = (vars,)

    # prepare string of DWH IDs for variable(s)
    vars_str = parse_vars(vars, device)

    if verbose:
        print(f"Calling dwh retrieve command:")
        print(f"  device: {device}")
        print(f"  station: {station}")
        print(f"  variables: {vars}")
        print(f"  timestamps: {t1}, {t2}")

    # profile-based data
    if device in ["rs", "mwr"]:

        # call dwh retrieve for profile-based data
        raw_data = dwh_profile(
            device=device,
            station_id=sdf[station].dwh_id,
            vars_str=vars_str,
            start=t1,
            end=t2,
            verbose=verbose,
        )

        if raw_data.empty:
            return raw_data

        # rename column names to nice short names and
        #  make list of relevant columns
        raw_data.rename(columns={"termin": "timestamp"}, inplace=True)
        relevant_vars = [
            "timestamp",
            "altitude",
        ]

        # renaming columns of variable(s)
        for var in vars:
            dwh_id = vdf[var].dwh_id[device]
            short_name = vdf[var].short_name
            raw_data.rename(columns={dwh_id: short_name}, inplace=True)
            relevant_vars.append(short_name)

        # rename altitude-column
        if device == "rs":
            raw_data.rename(columns={"742": "altitude"}, inplace=True)
        else:
            raw_data.rename(columns={"level": "altitude"}, inplace=True)

        data = raw_data[relevant_vars]

        # case A) only 1 timestamp specified for profile data
        if t1 == t2:
            return data

        # case B) 2 timestamps specified for profile data -> rearrange dataframe
        else:
            if len(vars) > 1:
                print(
                    f"! Profile retrieve not yet supported for multiple times AND multiple variables!"
                )
                sys.exit(1)
            else:

                # print warning
                print(
                    "! Assuming that retrieved profiles all have same altitude levels !"
                )

                # extract unique timestamps
                unique_ts = data.timestamp.unique()

                # create new dataframe with timestamps as columns
                new_df = pd.DataFrame(columns=unique_ts)

                # loop over timestamps to fill new dataframe
                for ts in unique_ts:
                    # print(ts)
                    new_df[ts] = data[data.timestamp == ts][var].values

                # use altitude as index
                new_df.index = data[data.timestamp == ts]["altitude"]

                return new_df

    # surface-based data
    elif device in ["5cm", "2m", "2m_tower", "10m_tower", "30m_tower"]:

        # call dwh retrieve for surface-based data
        raw_data = dwh_surface(
            station_name=sdf[station].dwh_name,
            vars_str=vars_str,
            start=t1,
            end=t2,
            verbose=verbose,
        )

        if raw_data.empty:
            return raw_data

        # rename column names to nice short names and
        #  make list of relevant columns
        raw_data.rename(columns={"termin": "timestamp"}, inplace=True)
        relevant_vars = [
            "timestamp",
        ]
        for var in vars:
            dwh_id = vdf[var].dwh_id[device]
            short_name = vdf[var].short_name
            raw_data.rename(columns={dwh_id: short_name}, inplace=True)
            relevant_vars.append(short_name)

        data = raw_data[relevant_vars]

        return data

    else:
        print("! unknown device!")
        sys.exit(1)


if __name__ == "__main__":

    test_profile = False
    test_surface = False
    test_timeseries = True

    if test_timeseries:
        data = dwh_retrieve(
            device="2m_tower",
            station="gla",
            vars="temp",
            timestamps=[
                "2021111900",
                "2021111902",
            ],
            verbose=False,
        )
        print(f"5cm dataframe looks like:\n{data}")

    if test_profile:
        data = dwh_retrieve(
            device="mwr",
            station="pay",
            vars="temp",
            timestamps=[
                "2021111900",
                "2021111902",
            ],
            verbose=False,
        )
        print(f"Sounding dataframe looks like:\n{data}")

    if test_surface:
        data = dwh_retrieve(
            device="5cm",
            station="gla",
            vars=("temp",),
            timestamps=["202201190000", "202201191400"],
            verbose=True,
        )
        print(f"\nSurface Station dataframe looks like:\n{data}")
