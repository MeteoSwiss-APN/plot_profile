"""Purpose: Retrieve data into dictionary.

Author: Arthur Dandoy

Date: 04/05/2022.
"""

# Standard library
import pprint
import sys
from datetime import timedelta

# Third-party
import pandas as pd

# First-party
from plot_profile.plot_arome.get_arome import get_arome_profiles
from plot_profile.plot_icon.get_icon import get_icon
from plot_profile.utils.calc_new_vars import calc_new_var_profiles
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import calc_qv_from_td
from plot_profile.utils.utils import slice_top_bottom


def get_mult_data(
    date_ref,
    leadtimes,
    loc,
    grid,
    ylims,
    elements,
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

    # collect data for various devices and leadtimes
    mult_dict = {}

    # if leadtimes is string transform it to a 1 element list
    if isinstance(leadtimes, str):
        leadtimes = [
            leadtimes,
        ]

    for lt in leadtimes:

        # will contain model/obs info for this leadtime
        data_dict = {}

        date_lt = date_ref + timedelta(hours=lt)

        if verbose:
            print(f"* Get data at {date_lt} (ref + {lt}H).")

        # loop over elements
        for element in elements:

            # retrieve variable name
            var_name = element[1]

            # define 'device'
            device = element[0]

            # A.1) retrieve data from ICON forecasts
            ########################################
            if device == "icon":
                model_id = element[2]
                folder = element[3]
                init = element[4]

                if var_name == "wind_vel" or var_name == "wind_dir":
                    var_open_icon = ["u", "v"]

                elif var_name == "rel_hum":
                    var_open_icon = ["temp", "qv"]

                else:
                    var_open_icon = var_name

                # check if a key for this icon-instance (for example icon-ref or icon-exp,...) already exists.
                # if yes --> retrieve df as usual, but instead of assigning it to a new key, only append/concatenate
                # the variable column to the already existing dataframe.
                if f"icon~{model_id}" in data_dict:
                    # retrieve data from ICON forecasts
                    tmp_dict = get_icon(
                        folder=folder,
                        date=init,
                        leadtime=[
                            int((date_lt - init).total_seconds() / 3600)
                        ],  # full hours!; has to be a list,
                        lat=lat,
                        lon=lon,
                        ind=None,
                        grid=grid,
                        variables_list=var_open_icon,
                        alt_bot=ylims[0],
                        alt_top=ylims[1],
                        verbose=verbose,
                    )

                    if var_open_icon != var_name:
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.set_axis(
                            ["height"] + var_open_icon, axis=1, inplace=True
                        )
                        tmp_df = calc_new_var_profiles(tmp_df, var_name, verbose)

                    else:
                        # re-format output from get_icon slightly
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.rename(columns={0: "height", 1: var_name}, inplace=True)

                    tmp_df = tmp_df.reset_index(drop=True)
                    tmp_df = tmp_df.dropna()
                    del tmp_df["height"]

                    if verbose:
                        print("Should add this df to the existing df: ")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        pprint(tmp_df)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        pprint(data_dict[f"icon~{model_id}"])
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        pprint(
                            pd.concat([data_dict[f"icon~{model_id}"], tmp_df], axis=1)
                        )
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                    data_dict[f"icon~{model_id}"] = pd.concat(
                        [data_dict[f"icon~{model_id}"], tmp_df], axis=1
                    )
                    continue

                else:
                    # lt_dict[f"icon~{model_id}"] = int((date - init).total_seconds() / 3600)

                    # retrieve data from ICON forecasts
                    tmp_dict = get_icon(
                        folder=folder,
                        date=init,
                        leadtime=[
                            int((date_lt - init).total_seconds() / 3600)
                        ],  # full hours!; has to be a list,
                        lat=lat,
                        lon=lon,
                        ind=None,
                        grid=grid,
                        variables_list=var_open_icon,
                        alt_bot=ylims[0],
                        alt_top=ylims[1],
                        verbose=verbose,
                    )

                    if var_open_icon != var_name:
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.set_axis(
                            ["height"] + var_open_icon, axis=1, inplace=True
                        )
                        tmp_df = calc_new_var_profiles(tmp_df, var_name, verbose)

                    else:
                        # re-format output from get_icon slightly
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.rename(columns={0: "height", 1: var_name}, inplace=True)

                    tmp_df = tmp_df.reset_index(drop=True)
                    tmp_df = tmp_df.dropna()

                    # add df w/ height & variable columns to data_dict
                    data_dict[f"icon~{model_id}"] = tmp_df

                continue

            # A.2) retrieve data from AROME forecasts
            #########################################
            if device == "arome":
                model_id = element[2]
                folder = element[3]
                init = element[4]

                # some parameters are not in arome and therefore need to be calculated from other parameters

                if var_name == "qv":
                    var_open_arome = ["press", "dewp_temp"]

                elif var_name == "wind_vel" or var_name == "wind_dir":
                    var_open_arome = ["u", "v"]

                else:
                    var_open_arome = var_name

                # check if a key for this arome-instance (for example arome-ref or arome-exp,...) already exists.
                # if yes --> retrieve df as usual, but instead of assigning it to a new key, only append/concatenate
                # the variable column to the already existing dataframe.
                if f"arome~{model_id}" in data_dict:
                    # retrieve data from AROME forecasts
                    tmp_dict = get_arome_profiles(
                        folder=folder,
                        date=init,
                        leadtime=[
                            int((date_lt - init).total_seconds() / 3600)
                        ],  # full hours!; has to be a list,
                        lat=lat,
                        lon=lon,
                        variables_list=var_open_arome,  # list of str or str
                        alt_bot=ylims[0],
                        alt_top=ylims[1],
                        verbose=verbose,
                    )

                    # calculate new variables
                    if (
                        var_name != var_open_arome
                    ):  # equivalent to "if var needs to be calculated"
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.set_axis(
                            ["height"] + var_open_arome, axis=1, inplace=True
                        )
                        tmp_df = calc_new_var_profiles(tmp_df, var_name, verbose)

                    else:
                        # re-format output from get_arome_profiles slightly
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.rename(columns={0: "height", 1: var_name}, inplace=True)

                    tmp_df = tmp_df.reset_index(drop=True)
                    tmp_df = tmp_df.dropna()
                    del tmp_df["height"]

                    if verbose:
                        print("Should add this df to the existing df: ")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        pprint(tmp_df)
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        pprint(data_dict[f"arome~{model_id}"])
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        pprint(
                            pd.concat([data_dict[f"arome~{model_id}"], tmp_df], axis=1)
                        )
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                    data_dict[f"arome~{model_id}"] = pd.concat(
                        [data_dict[f"arome~{model_id}"], tmp_df], axis=1
                    )
                    continue

                else:
                    # lt_dict[f"arome~{model_id}"] = int((date - init).total_seconds() / 3600)

                    # retrieve data from AROME forecasts
                    tmp_dict = get_arome_profiles(
                        folder=folder,
                        date=init,
                        leadtime=[
                            int((date_lt - init).total_seconds() / 3600)
                        ],  # full hours!; has to be a list,
                        lat=lat,
                        lon=lon,
                        variables_list=var_open_arome,
                        alt_bot=ylims[0],
                        alt_top=ylims[1],
                        verbose=verbose,
                    )

                    if (
                        var_name != var_open_arome
                    ):  # equivalent to "if var needs to be calculated"

                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.set_axis(
                            ["height"] + var_open_arome, axis=1, inplace=True
                        )
                        tmp_df = calc_new_var_profiles(tmp_df, var_name, verbose)

                    else:

                        # re-format output from get_icon slightly
                        tmp_df = pd.concat(tmp_dict, axis=1, ignore_index=True)
                        tmp_df.rename(columns={0: "height", 1: var_name}, inplace=True)

                    tmp_df = tmp_df.reset_index(drop=True)
                    tmp_df = tmp_df.dropna()

                    # add df w/ height & variable columns to data_dict
                    data_dict[f"arome~{model_id}"] = tmp_df

                continue

            # B) retrieve observational data
            ################################
            else:
                if device == "rs" and var_name == "qv":
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
                        data_dict[device] = sliced_df

                    continue

                if device not in data_dict:
                    unsliced_df = dwh_retrieve(
                        device=device,  # i.e. rs
                        station=loc,  # i.e. pay
                        vars=var_name,
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
                        data_dict[device] = sliced_df
                    continue

                else:
                    unsliced_df = dwh_retrieve(
                        device=device,  # i.e. rs
                        station=loc,  # i.e. pay
                        vars=var_name,
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
                        del sliced_df["altitude"]
                        data_dict[device] = pd.concat(
                            [data_dict[device], sliced_df], axis=1
                        )

                    continue
        mult_dict[f"{lt}"] = data_dict

    return mult_dict
