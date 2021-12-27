"""Purpose: Retrieve observational data from DWH.

Author: Stephanie Westerhuis

Date: 27/12/2022.
"""

# Standard library
import subprocess  # use: run command line commands from python
from io import StringIO

# Third-party
import numpy as np
import pandas as pd

# import ipdb

# from .variables import vdf
# from .stations import sdf


def dwh_surface(vars, start, end, station_name, verbose):
    """Retrieve surface-based data from DWH."""
    if verbose:
        print(f"Retrieving surface-based data for:")
        print(f"  {vars}")
        print(f"  from {start} to {end}")
        print(f"  at {station_name}.")

    # retrieve_cscs command:
    cmd = (
        "/oprusers/osm/bin/retrieve_cscs --show_records -j lat,lon,name,wmo_ind"
        + " -s surface "
        + " -i nat_abr,"
        + station_name
        + " -p "
        + vars
        + " -t "
        + start
        + "-"
        + end
        + " --use-limitation 50"
    )
    print("--- calling: " + cmd)
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

    # load DWH retrieve output into pandas DataFrame
    header_line = pd.read_csv(
        StringIO(out), skiprows=0, nrows=1, sep="\s+", header=None, engine="c"
    )

    # parse the command line output
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
        if verbose:
            print("--- data retrieved into dataframe")
    return data


def dwh_profile(vars, date, station_id, verbose):
    """Retrieve profile-based data from DWH."""
    print(f"Retrieve profile-based data from DWH")
    return


def dwh_retrieve(vars, station, timestamps, verbose):
    """Retrieve observational data from DWH.

    Input:
        vars        list of strings     variables
        station     string              station short or longname
        timestamps  list of strings     either 1 or 2 timestamps YYYYMMDDHHMM

    Output:
        pandas dataframe
    """
    # Either call profile or surface retrieve command
    if verbose:
        print(f"Calling dwh retrieve command ...")


if __name__ == "__main__":
    dwh_surface("1541,1547,6199", "2021111900", "202111191200", "PAY", True)
