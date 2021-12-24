"""Purpose: Parse Data.

Author: Michel Zeller

Date: 15/10/2021.
"""

# Standard library
import subprocess  # use: run command line commands from python
from io import StringIO

# Third-party
import numpy as np
import pandas as pd

# Local
from .utils import slice_top_bottom


def reformat_params(params, params_dict):
    """Reformat the input parameters.

    Args:
        params:             tuple       parameters, that should be included in the plot
                                        '743', '745', '748', '747'
        params_dict:        dict        dictionary containing the mapping between the
                                        parameter ids and the corresponding physical quantities

    Returns:
        all_params:         tuple       all params that are possible
        relevant_params:    tuple       actually chosen params + the standard params in a list

    """
    params = list(params)  # tuple --> str-array

    i = 0
    for item in params:
        if params_dict[item]:
            params[i] = params_dict[item]
        i += 1

    params_int_array = [int(i) for i in params]
    params_sorted_int_array = np.sort(params_int_array)
    params_sorted_str_array = [str(i) for i in params_sorted_int_array]
    # input_params = tuple(params_sorted_str_array) # sort the input parameters

    params_sorted_int_array = np.append(
        params_sorted_int_array, [742, 746]
    )  # add altitude and relhum to params for data retrieval
    params_sorted_int_array = np.sort(params_sorted_int_array)
    params_str_array = [str(i) for i in params_sorted_int_array]  # int --> str
    relevant_params = tuple(params_str_array)  # str-array --> tuple

    all_params = (
        "742",
        "743",
        "745",
        "746",
        "747",
        "748",
    )  # hard-coded, 'cause why not
    return all_params, relevant_params


def reformat_inputs(date, params, params_dict, print_steps):
    """Reformat all command line inputs. Helper function.

    Args:
        date:               str         YYYYMMDDHH
        params:             tuple       parameters, that should be included in the plot
                                        '743', '745', '748', '747'
        station:            df          station attributes
        params_dict:        dict        dictionary containing the mapping between the
                                        parameter ids and physical quantities
        stations_dict:      type        dictionary containint the mapping between the
                                        station ids and station names
        print_steps:        bool        optional parameter to print intermediate steps in terminal

    Returns:
        date:               str         YYYYMMDDHH+MMSS
        all_params:         tuple       list of all parameters
        relevant_params:    tuple       list of relevant parameters which are plottet
        station_name:       str         Name of station

    """
    if print_steps:
        print("--- reformating inputs")

    date = date + "0000"  # add minutes and seconds to date
    all_params, relevant_params = reformat_params(
        params=params, params_dict=params_dict
    )  # unsorted, incomplete input params to two sorted tuples

    if print_steps:
        print(f"all_params = {all_params} and relevant_params = {relevant_params}")

    return date, all_params, relevant_params


def dwh2pandas(station_id, date, print_steps):
    """Retrieve dwh file and load into pandas dataframe.

    Args:
        station_id:         str         ID of station (i.e. Payerne has ID: 06610)
        date:               str         YYYYMMDDHHMMSS
        print_steps:        bool        optional parameter to print intermediate steps in terminal

    Returns:
        data:               df          unfiltered dataframe from dataretrieval

    """
    cmd = (
        "/oprusers/osm/bin/retrieve_cscs --show_records -j lat,lon,elev,name,wmo_ind -w 22 -s profile -p "
        + "742,743,745,746,747,748"  # extract all columns containing relevant paramenters (i.e. all except the pressure column.)
        + " -i int_ind,"
        + station_id
        + " -t "
        + date
        + "-"
        + date
        + " -C 34"
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

    # clean up the dataframe a bit
    data.replace(1e7, np.nan, inplace=True)

    # check if no data is available for the time period
    if data.empty:
        raise SystemExit("--- WARN: no data available for " + date + ".")
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
        if print_steps:
            print("--- data retrieved into dataframe")
        return data


def extract_rows(df, print_steps, alt_bot, alt_top, all_params):
    """Extract the rows from the complete dataframe, that are within the specified altitude limits.

    Args:
        df:                 df          dataframe w/ columns for all params
        print_steps:        bool        optional parameter to print intermediate steps in terminal
        alt_bot:            int         lower altitude limit
        alt_top:            int         upper altitude limit
        all_params:         tuple       all params that are possible

    Returns:
        params_df:          df          dataframe containing only the relevant rows/columns

    """
    if print_steps:
        print("--- extracting relevant rows from dataframe")

    # subselect relevant columns from df
    columns = list(all_params)
    params_df = pd.DataFrame(df, columns=columns)

    # rename columns
    # params_name = ['altitude', 'winddir', 'temp', 'relhum', 'dewp', 'windvel']
    params_df["altitude"] = params_df.pop("742")
    params_df["winddir"] = params_df.pop("743")
    params_df["temp"] = params_df.pop("745")
    params_df["relhum"] = params_df.pop("746")
    params_df["dewp"] = params_df.pop("747")
    params_df["windvel"] = params_df.pop("748")

    if print_steps:
        print("params_df looks like:")
        print(params_df.head())

    # select rows: cut away top and bottom
    crit = slice_top_bottom(params_df["altitude"], alt_top, alt_bot, print_steps)

    # return sliced dataframe and drop lines with nan-values
    return params_df[crit].dropna()


def get_rs(date, params, station, print_steps, alt_bot, alt_top):
    """Retrieve and parse the relevant data from the server and return a complete dataframe containing the data.

    Args:
        date:               str         YYYYMMDDHH
        params:             tuple       parameters, that should be included in the plot
                                        '743', '745', '748', '747'
        station:            df          station and attributes
        print_steps:        bool        optional parameter to print intermediate steps in terminal
        alt_bot:            int         lower altitude limit
        alt_top:            int         upper altitude limit

    Returns:
        df:                 df          dataframe w/ columns for all params
        relevant_params:    tuple       params + standard params. i.e.
                                        '742', '743', '745', '746', '747', '748'

    """
    # station_id and parameter_id dicts
    params_dict = {
        "742": "742",
        "altitude": "742",
        "743": "743",
        "winddir": "743",
        "744": "744",
        "press": "744",
        "745": "745",
        "temp": "745",
        "746": "746",
        "relhum": "746",
        "747": "747",
        "dewp": "747",
        "748": "748",
        "windvel": "748",
    }

    date, all_params, relevant_params = reformat_inputs(
        date=date,
        params=params,
        params_dict=params_dict,
        print_steps=print_steps,
    )

    # retrieve data for specified date into a dataframe
    df = dwh2pandas(
        date=date,
        station_id=station.dwh_id,
        print_steps=print_steps,
    )

    # extract altitude range from dataframe & re-assign keys

    df = extract_rows(
        df=df,
        print_steps=print_steps,
        alt_bot=alt_bot,
        alt_top=alt_top,
        all_params=all_params,
    )

    return df, relevant_params
