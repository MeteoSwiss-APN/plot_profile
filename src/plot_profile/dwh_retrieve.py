"""Purpose: Retrieve observational data from DWH.

Author: Stephanie Westerhuis

Date: 27/12/2022.
"""

# Standard library
import subprocess  # use: run command line commands from python
import sys
from datetime import time
from io import StringIO
from os import stat

# Third-party
import numpy as np
import pandas as pd

# Local
# remove leading '.' if this script should be used on its own
from .stations import sdf
from .variables import vdf

# import ipdb


def check_vars(vars, device):
    """Create comma-separated strings of DWH IDs from one or more variables."""
    # single string
    if isinstance(vars, str):
        try:
            vars_str = vdf[vars].dwh_id[device]
        except KeyError:
            print(f"! Device {device} not available for {vars}!")
            sys.exit(1)

    # list containing string(s)
    elif isinstance(vars, list):

        # only one string
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
                    vars_str += f",{vdf[var].dwh_id[device]}"
            except KeyError:
                print(f"! Device not available for {vars}!")

    else:
        print("! nonsense variable list !")
        sys.exit(1)

    # add altitude for radiosounding retrieves
    # NEW: also add relative humidity for radiosounding retrieves
    if device == "rs":
        vars_str += f",{vdf['altitude'].dwh_id['rs']}"
        vars_str += f",{vdf['rel_hum'].dwh_id['rs']}"

    return vars_str


def dwh2pandas(cmd, verbose):
    """Run retrieve_cscs command in terminal, create pandas dataframe."""
    if verbose:
        print("--- calling: " + cmd)

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

    # clean up the dataframe: replae "10000000" with NaN
    data.replace(1e7, np.nan, inplace=True)

    # check if no data is available for the time period
    if data.empty:
        raise SystemExit("--- WARN: no data available.")
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
            print("--- data retrieved into dataframe")
    return data


def dwh_surface(station_name, vars_str, start, end, verbose):
    """Retrieve surface-based data from DWH.

    Args:
        station_name    (str):  DWH station name
        vars_str        (str):  comma-separated list of DWH IDs of variables
        start           (str):  YYYYMMDDHHmm
        end             (str):  YYYYMMDDHHmm (same or later as <start>)
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


def dwh_profile(station_id, vars_str, date, verbose):
    """Retrieve profile-based data from DWH.

    Args:
        station_id  (str):  DWH ID of station (number as string!)
        vars_str    (str):  comma-separated list of DWH IDs of variables
        date        (str):  YYYYMMDDHHmm
        verbose     (bool): verbose statements

    Returns:
        pandas dataframe:   DWH profile data

    """
    if verbose:
        print(f"Retrieving profile-based data for:")
        print(f"  {vars_str}")
        print(f"  on {date}")
        print(f"  at {station_id}.")

    cmd = (
        "/oprusers/osm/bin/retrieve_cscs --show_records -j lat,lon,elev,name,wmo_ind"
        + " -w 22 -s profile -p "
        + vars_str
        + " -i int_ind,"
        + station_id
        + " -t "
        + date
        + "-"
        + date
        + " -C 34"
    )

    # run command
    data = dwh2pandas(cmd, verbose)

    return data


def check_timestamps_surface(timestamps):
    """Check timestamps user input for surface-based data.

    Timestamps should either be a single string or a list of strings
    with two entries.

    Input:
        timestamps  (str or list of strings)

    Return:
        string tuple:   t1, t2

    """
    if isinstance(timestamps, list):
        if len(timestamps) == 1:
            return timestamps[0], timestamps[0]
        elif len(timestamps) == 2:
            return timestamps[0], timestamps[1]
        else:
            print("! too many timestamps")
            sys.exit(1)
    elif isinstance(timestamps, str):
        return timestamps, timestamps
    else:
        print("! timestamps input is nonsense!")
        sys.exit(1)


def check_timestamps_profile(timestamps):
    """Check timestamps user input for profile-based data.

    Timestamps should either be a single string or a list of strings
    with only one entry.

    Args:
        timestamps

    Returns:
        timestamp

    """
    if isinstance(timestamps, list):
        if len(timestamps) == 1:
            return timestamps[0]
        else:
            print("! only one timestamp allowed for profile data")
            sys.exit(1)
    elif isinstance(timestamps, str):
        return timestamps
    else:
        print(f"! timestamps input is nonsense: {timestamps}")


def dwh_retrieve(device, station, vars, timestamps, verbose):
    """Retrieve observational data from DWH.

    The retrieve_cscs command works for two different observational types:
        a) surface-based data (2m stations including ceilometers & scintillometers)
        b) profile-based data (radiosoundings - 'rs', radiometers - 'mwr')

    Input:
        device      string              measurement device: 'rs', 'mwr', 'cm', ...
        station     string              station short or longname
        vars        list of strings     variables
        timestamps  list of strings     either 1 or 2 timestamps YYYYMMDDHHMM

    Output:
        pandas dataframe
    """
    if verbose:
        print(f"Calling dwh retrieve command:")
        print(f"  device: {device}")
        print(f"  station: {station}")
        print(f"  variables: {vars}")
        print(f"  timestamps: {timestamps}")

    # prepare string of DWH IDs for variable(s)
    vars_str = check_vars(vars, device)

    # profile-based data
    if device in ["rs", "mwr"]:

        # check timestamps input:
        #  must be either string or one string in a list
        timestamp = check_timestamps_profile(timestamps)

        # call dwh retrieve for profile-based data
        raw_data = dwh_profile(
            station_id=sdf[station].dwh_id,
            vars_str=vars_str,
            date=timestamp,
            verbose=verbose,
        )

        # rename column names to nice short names and
        #  make list of relevant columns
        raw_data.rename(columns={"termin": "timestamp"}, inplace=True)
        relevant_vars = ["timestamp", "altitude", "rel_hum"]
        for var in vars:
            dwh_id = vdf[var].dwh_id[device]
            short_name = vdf[var].short_name
            raw_data.rename(columns={dwh_id: short_name}, inplace=True)
            relevant_vars.append(short_name)
        if device == "rs":
            raw_data.rename(columns={"742": "altitude"}, inplace=True)
            raw_data.rename(columns={"746": "rel_hum"}, inplace=True)
        else:
            raw_data.rename(columns={"level": "altitude"}, inplace=True)

        data = raw_data[relevant_vars]

    # surface-based data
    elif device in ["2m"]:

        # check timestamp input:
        #  must be two strings
        t1, t2 = check_timestamps_surface(timestamps)

        # call dwh retrieve for surface-based data
        raw_data = dwh_surface(
            station_name=sdf[station].dwh_name,
            vars_str=vars_str,
            start=t1,
            end=t2,
            verbose=verbose,
        )

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

    else:
        print("! unknown device!")
        sys.exit(1)

    return data


if __name__ == "__main__":

    test_profile = True
    test_surface = False

    if test_profile:
        data = dwh_retrieve(
            device="rs",
            station="pay",
            vars=["temp", "dewp_temp"],
            timestamps=[
                "202111190000",
            ],
            verbose=False,
        )
        print(f"Radio Sounding dataframe looks like:\n{data}")

    if test_surface:
        data = dwh_retrieve(
            device="2m",
            station="pay",
            vars=[
                "temp",
            ],
            timestamps=["202111190000", "202111190300"],
            verbose=True,
        )
        print(f"\nSurface Station dataframe looks like:\n{data}")
