"""Purpose: parse inputs and retrieve data into dictionary.

Author: Michel Zeller

Date: 09/03/2022.
"""

# Standard library
import sys
from pprint import pprint

# Third-party
import pandas as pd

# First-party
from plot_profile.plot_arome.get_arome import get_arome_profiles
# from plot_profile.plot_arome.get_arome import get_arome_profiles
from plot_profile.plot_icon.get_icon import get_icon
from plot_profile.plot_timeseries.parse_timeseries_inputs import check_units
from plot_profile.utils.calc_new_vars import calc_new_var_profiles
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf
from plot_profile.utils.utils import calc_qv_from_td
from plot_profile.utils.utils import check_inputs
from plot_profile.utils.utils import slice_top_bottom

# from ipdb import set_trace


def parse_inputs(loc, add_model, add_obs, model_src, verbose):

    # create a dict out of model_src. each model id should be one key.
    model_src_dict = {}
    model_ids = []
    for source in model_src:
        id, dir, init_time = source[0], source[1], source[2]
        model_src_dict[id] = [dir, init_time]
        model_ids.append(id)

    # iterate through list of models and add init & folder to it
    l_model = []
    for model in add_model:
        if model[2] not in model_ids:
            print(
                f"--- No model source information provided for model w/ id: {model[2]}"
            )
            print(
                f"--- (Could just be a typo. Make sure the model ids in the --add_model & --model_src flags match)"
            )
            sys.exit(1)
        model = tuple(list(model) + (model_src_dict[model[2]]))
        l_model.append(model)

    if add_obs:
        l_obs = list(add_obs)
    else:
        l_obs = []

    elements = l_model + l_obs

    devs = [ele[0] for ele in elements]
    vars = [ele[1] for ele in elements]

    # check, wheter all desired variables are available for the provided location and corresponding devices
    for dev, var in zip(devs, vars):
        if verbose:
            print("checking inputs for: ", dev, var)
        if (
            dev == "rs" and var == "qv"
        ):  # qv is a variable, which does not actually exist for radiousoundings, but can be computed
            continue
        else:
            check_inputs(var=var, dev=dev, loc=loc, verbose=verbose)

    # check, that the provided variables at most require 2 units
    multi_axes = check_units(vars)
    return elements, multi_axes


def get_data(
    date,
    loc,
    grid,
    ylims,
    elements,
    verbose,
):

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

    # collect data for various devices
    data_dict = {}

    # collect leadtimes for various models
    lt_dict = {}

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
                        int((date - init).total_seconds() / 3600)
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
                    tmp_df.set_axis(["height"] + var_open_icon, axis=1, inplace=True)
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
                    pprint(pd.concat([data_dict[f"icon~{model_id}"], tmp_df], axis=1))
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                data_dict[f"icon~{model_id}"] = pd.concat(
                    [data_dict[f"icon~{model_id}"], tmp_df], axis=1
                )
                continue

            else:
                lt_dict[f"icon~{model_id}"] = int((date - init).total_seconds() / 3600)

                # retrieve data from ICON forecasts
                tmp_dict = get_icon(
                    folder=folder,
                    date=init,
                    leadtime=[
                        int((date - init).total_seconds() / 3600)
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
                    tmp_df.set_axis(["height"] + var_open_icon, axis=1, inplace=True)
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
                        int((date - init).total_seconds() / 3600)
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
                    tmp_df.set_axis(["height"] + var_open_arome, axis=1, inplace=True)
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
                    pprint(pd.concat([data_dict[f"arome~{model_id}"], tmp_df], axis=1))
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                data_dict[f"arome~{model_id}"] = pd.concat(
                    [data_dict[f"arome~{model_id}"], tmp_df], axis=1
                )
                continue

            else:
                lt_dict[f"arome~{model_id}"] = int((date - init).total_seconds() / 3600)

                # retrieve data from AROME forecasts
                tmp_dict = get_arome_profiles(
                    folder=folder,
                    date=init,
                    leadtime=[
                        int((date - init).total_seconds() / 3600)
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
                    tmp_df.set_axis(["height"] + var_open_arome, axis=1, inplace=True)
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
                    timestamps=date,
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
                    timestamps=date,
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
                    timestamps=date,
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

    return data_dict, lt_dict
