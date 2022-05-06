"""Purpose: Retrieve data into dictionary.

Author: Arthur Dandoy

Date: 04/05/2022.
"""

# Standard library
import sys
from datetime import timedelta
from pprint import pprint

# Third-party
import pandas as pd

# First-party
from plot_profile.plot_arome.get_arome import get_arome_profiles
from plot_profile.plot_icon.get_icon import get_icon
from plot_profile.utils.calc_new_vars import calc_new_var_profiles
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import calc_qv_from_td
from plot_profile.utils.utils import check_inputs
from plot_profile.utils.utils import slice_top_bottom

# from ipdb import set_trace


def parse_inputs(variable, model, model_src, add_obs, loc, verbose=False):

    if loc == None:
        print(f"! --- No location specified. Use --loc.")
        sys.exit(1)

    if variable == None:
        print(f"! --- No variable specified. Use --variable.")
        sys.exit(1)

    # if a model is specified
    if model != None:
        if model_src == None:
            print(f"! --- Need --model_src <folder> for model: {model}.")
            sys.exit(1)
        l_devices = [model]

    else:
        # if no obs specified
        if add_obs == None or add_obs == ():
            print(
                f"! --- Neither model nor observation device have been specified. Use --model or --add_obs."
            )
            sys.exit(1)
        l_devices = []

    if add_obs:
        l_obs = list(add_obs)
    else:
        l_obs = []

    l_devices += l_obs

    for dev in l_devices:
        if verbose:
            print("checking inputs for: ", dev, variable)

        check_inputs(var=variable, dev=dev, loc=loc, verbose=verbose)

    return


def get_mult_data(
    init,
    variable,
    model,
    model_src,
    add_obs,
    leadtimes,
    loc,
    grid,
    ylims,
    verbose,
):
    """Retrieve models and observation data for multiple profiles plots.

    Args:
        date_ref (datetime):     reference date (from where to calc leadtimes) (%y%m%d%H)
        leadtime (list of int):  leadtimes.
        loc (str):               location dwh name
        grid (str):              icon grid file path
        ylims (list of ints):    top and bottom altitude
        elements (tuple):        variables informations
        verbose (bool):          print details.Default: False

    Returns:
        dict: returns models and obs data

    """
    # 0) Parse loc / lat / lon input
    ################################
    try:
        station = sdf[loc]
        lat = station.lat
        lon = station.lon
        if verbose:
            print(f"Selected location: {station.long_name}")
            print(f"  lat: {lat}")
            print(f"  lon: {lon}")
    except KeyError:
        if not lat and not lon:
            print("! lat and lon missing!")
            sys.exit(1)
        if not lat:
            print("! lat missing!")
            sys.exit(1)
        if not lon:
            print("! lon missing!")
            sys.exit(1)
        if not loc:
            print("! Location name is missing!")
            sys.exit(1)
        if verbose:
            print(f"Specified lat: {lat}")
            print(f"Specified lon: {lon}")
            print(f"Specified name for location: {loc}")

    # A) retrieve data from model output
    ####################################

    if variable == "wind_vel" or variable == "wind_dir":
        var_open = ["u", "v"]

    elif variable == "rel_hum" and model == "icon":
        var_open = ["temp", "qv"]

    elif variable == "qv" and model == "arome":
        var_open = ["press", "dewp_temp"]

    else:
        var_open = variable

    data_dict = {}

    # A.1) ICON
    if model == "icon":

        for lt in leadtimes:
            # leadtime at date format
            date_lt = init + timedelta(hours=lt)

            # add height profile to dict
            if "icon" not in data_dict:
                # retrieve data from ICON forecasts
                tmp_dict = get_icon(
                    folder=model_src,
                    date=init,
                    leadtime=[
                        int((date_lt - init).total_seconds() / 3600)
                    ],  # full hours!; has to be a list,
                    lat=lat,
                    lon=lon,
                    ind=None,
                    grid=grid,
                    variables_list=var_open,
                    alt_bot=ylims[0],
                    alt_top=ylims[1],
                    verbose=verbose,
                )

                # if variable needs to be calculated
                if var_open != variable:
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                    tmp_df.set_axis(["height"] + var_open, axis=1, inplace=True)
                    tmp_df = calc_new_var_profiles(tmp_df, variable, verbose)

                else:
                    # re-format output from get_icon slightly
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)

                columns = tmp_df.columns
                tmp_df.rename(
                    columns={columns[0]: "height", columns[1]: str(lt)}, inplace=True
                )
                tmp_df = tmp_df.reset_index(drop=True)
                tmp_df = tmp_df.dropna()

                # add df w/ height & variable columns to data_dict
                data_dict[f"icon"] = tmp_df

            # add new leadtime profile to existing dictionnary
            else:

                # retrieve data from ICON forecasts
                tmp_dict = get_icon(
                    folder=model_src,
                    date=init,
                    leadtime=[
                        int((date_lt - init).total_seconds() / 3600)
                    ],  # full hours!; has to be a list,
                    lat=lat,
                    lon=lon,
                    ind=None,
                    grid=grid,
                    variables_list=var_open,
                    alt_bot=ylims[0],
                    alt_top=ylims[1],
                    verbose=verbose,
                )

                # if variable needs to be calculated
                if var_open != variable:
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                    tmp_df.set_axis(["height"] + var_open, axis=1, inplace=True)
                    tmp_df = calc_new_var_profiles(tmp_df, variable, verbose)

                else:
                    # re-format output from get_icon slightly
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                    tmp_df.rename(columns={0: "height", 1: variable}, inplace=True)

                if verbose:
                    print("Should add this df to the existing dict:")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    pprint(tmp_df)
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    pprint(data_dict[f"icon"])
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                data_dict[f"icon"][lt] = tmp_df[variable]

                if verbose:
                    pprint(data_dict[f"icon"])
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # A.2) AROME
    elif model == "arome":
        for lt in leadtimes:
            # leadtime at date format
            date_lt = init + timedelta(hours=lt)

            # add height profile to dict
            if "arome" not in data_dict:
                # retrieve data from AROME forecasts
                tmp_dict = get_arome_profiles(
                    folder=model_src,
                    date=init,
                    leadtime=[
                        int((date_lt - init).total_seconds() / 3600)
                    ],  # full hours!; has to be a list,
                    lat=lat,
                    lon=lon,
                    variables_list=var_open,
                    alt_bot=ylims[0],
                    alt_top=ylims[1],
                    verbose=verbose,
                )

                # if variable needs to be calculated
                if var_open != variable:
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                    tmp_df.set_axis(["height"] + var_open, axis=1, inplace=True)
                    tmp_df = calc_new_var_profiles(tmp_df, variable, verbose)

                else:
                    # re-format output from get_arome_profiles slightly
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)

                columns = tmp_df.columns
                tmp_df.rename(
                    columns={columns[0]: "height", columns[1]: str(lt)}, inplace=True
                )
                tmp_df = tmp_df.reset_index(drop=True)
                tmp_df = tmp_df.dropna()

                # add df w/ height & variable columns to data_dict
                data_dict[f"arome"] = tmp_df

            # add new leadtime profile to existing dictionnary
            else:

                # retrieve data from arome forecasts
                tmp_dict = get_arome_profiles(
                    folder=model_src,
                    date=init,
                    leadtime=[
                        int((date_lt - init).total_seconds() / 3600)
                    ],  # full hours!; has to be a list,
                    lat=lat,
                    lon=lon,
                    variables_list=var_open,
                    alt_bot=ylims[0],
                    alt_top=ylims[1],
                    verbose=verbose,
                )

                # if variable needs to be calculated
                if var_open != variable:
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                    tmp_df.set_axis(["height"] + var_open, axis=1, inplace=True)
                    tmp_df = calc_new_var_profiles(tmp_df, variable, verbose)

                else:
                    # re-format output from get_arome_profiles slightly
                    tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                    tmp_df.rename(columns={0: "height", 1: variable}, inplace=True)

                if verbose:
                    print("Should add this df to the existing dict:")
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    pprint(tmp_df)
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    pprint(data_dict[f"arome"])
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                data_dict[f"arome"][lt] = tmp_df[variable]

                if verbose:
                    pprint(data_dict[f"arome"])
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    elif model == None:
        if verbose:
            print("No model input. Retrieve observations only.")

    else:
        print(f"--- ! Model {model} output plot not implemented in plot_mult_profiles.")
        sys.exit(1)

    # B) retrieve observational data
    ################################

    # On the contrary to models we
    # have to create for each leadtimes and each devices a dict key.
    # indeed measurments takes place at different altitudes for rs
    # or can be altered sometimes by clouds for lidars...

    for device in add_obs:
        for lt in leadtimes:
            # leadtimes to date format
            date_lt = init + timedelta(hours=lt)

            if device == None:
                if verbose:
                    print("No observations input. Retreive models outputs only.")

            elif device == "rs" and variable == "qv":
                vars = "dewp_temp", "press"

                unsliced_df = dwh_retrieve(
                    device=device,  # i.e. rs
                    station=loc,  # i.e. pay
                    vars=vars,
                    timestamps=date_lt,
                    verbose=verbose,
                )
                # if returned df is not empty add to obs_dict
                if not unsliced_df.empty:
                    del unsliced_df["timestamp"]
                    crit = slice_top_bottom(
                        df_height=unsliced_df["altitude"],
                        alt_bot=ylims[0],
                        alt_top=ylims[1],
                        verbose=verbose,
                    )
                    sliced_df = unsliced_df[crit]
                    sliced_df = sliced_df.reset_index(drop=True)
                    sliced_df.rename(columns={"altitude": "height"}, inplace=True)
                    sliced_df = sliced_df.dropna()

                    # calculate qv from td and pressure
                    sliced_df["qv"] = calc_qv_from_td(
                        sliced_df["dewp_temp"], sliced_df["press"]
                    )
                    del sliced_df["dewp_temp"]
                    del sliced_df["press"]
                    data_dict[f"{device}~{lt}"] = sliced_df

                continue

            else:
                unsliced_df = dwh_retrieve(
                    device=device,  # i.e. rs
                    station=loc,  # i.e. pay
                    vars=variable,
                    timestamps=date_lt,
                    verbose=verbose,
                )

                # if returned df is not empty add to obs_dict
                if not unsliced_df.empty:
                    del unsliced_df["timestamp"]
                    crit = slice_top_bottom(
                        df_height=unsliced_df["altitude"],
                        alt_bot=ylims[0],
                        alt_top=ylims[1],
                        verbose=verbose,
                    )
                    sliced_df = unsliced_df[crit]
                    sliced_df = sliced_df.reset_index(drop=True)
                    sliced_df.rename(
                        columns={"altitude": "height", variable: str(lt)}, inplace=True
                    )
                    sliced_df = sliced_df.dropna()
                    data_dict[f"{device}~{lt}"] = sliced_df

                continue

    return data_dict
