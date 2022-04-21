"""Retrieve available data into dict for timeseries plots."""
# Standard library
from pprint import pprint

# Third-party
import pandas as pd

# First-party
from plot_profile.plot_arome.get_arome import get_arome_timeseries
from plot_profile.plot_icon.get_icon import get_icon_timeseries
from plot_profile.plot_timeseries.calc_new_vars import calc_new_var_timeseries
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf

# from ipdb import set_trace


def get_timeseries_dict(start, end, elements, loc, grid_file, verbose):
    timeseries_dict = {}

    # loop over elements
    for element in elements:

        # retrieve variable name

        var_name = element[1]

        # ICON
        if element[0] == "icon":

            level = element[2]
            id = element[3]
            folder = element[4]
            init = element[5]

            # some parameters aren't in icon and therefore needs to be calculated from other parameters

            if var_name == "wind_dir" or "wind_vel":
                var_open_icon = ["u", "v"]

            else:
                var_open_icon = var_name

            # check if a key for this icon-instance (for example icon-ref or icon-exp,...) already exists.
            # if yes --> retrieve df as usual, but instead of assigning it to a new key, only append/concatenate
            # the variable column to the already existing dataframe.
            if f"icon~{id}" in timeseries_dict:
                df = get_icon_timeseries(
                    lat=sdf[loc].lat,
                    lon=sdf[loc].lon,
                    vars=var_open_icon,
                    init=init,
                    level=level,
                    start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                    end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                    folder=folder,
                    grid_file=grid_file,
                    verbose=verbose,
                )

                # calculate new variables
                if (
                    var_name != var_open_icon
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, [level], verbose)

                del df["timestamp"]
                timeseries_dict[f"icon~{id}"] = pd.concat(
                    [timeseries_dict[f"icon~{id}"], df], axis=1
                )

                # print(id, timeseries_dict[f"icon~{id}"].columns.tolist(), df.columns.tolist())

            else:
                df = timeseries_dict[f"icon~{id}"] = get_icon_timeseries(
                    lat=sdf[loc].lat,
                    lon=sdf[loc].lon,
                    vars=var_open_icon,
                    init=init,
                    level=level,
                    start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                    end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                    folder=folder,
                    grid_file=grid_file,
                    verbose=verbose,
                )

                # calculate new variables
                if (
                    var_name != var_open_icon
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, [level], verbose)

                timeseries_dict[f"icon~{id}"] = df
            # increase icon index
            continue

        # AROME
        elif element[0] == "arome":

            levels = [element[2]]
            id = element[3]
            folder = element[4]
            init = element[5]

            # some parameters aren't in arome and therefore needs to be calculated from other parameters
            if var_name == "qv":
                var_open_arome = ["press", "dewp_temp"]

            elif var_name == "wind_dir" or "wind_vel":
                var_open_arome = ["u", "v"]

            else:
                var_open_arome = var_name

            if f"arome~{id}" in timeseries_dict:
                df = get_arome_timeseries(
                    lat=sdf[loc].lat,
                    lon=sdf[loc].lon,
                    vars=var_open_arome,
                    init=init,
                    levels=levels,
                    start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                    end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                    folder=folder,
                    verbose=verbose,
                )

                # calculate new variables
                if (
                    var_name != var_open_arome
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, levels, verbose)

                del df["timestamp"]
                timeseries_dict[f"arome~{id}"] = pd.concat(
                    [timeseries_dict[f"arome~{id}"], df], axis=1
                )

                # print(id, timeseries_dict[f"icon~{id}"].columns.tolist(), df.columns.tolist())

            else:
                df = get_arome_timeseries(
                    lat=sdf[loc].lat,
                    lon=sdf[loc].lon,
                    vars=var_open_arome,
                    init=init,
                    levels=levels,
                    start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                    end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                    folder=folder,
                    verbose=verbose,
                )

                # calculate new variables
                if (
                    var_name != var_open_arome
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, levels, verbose)

                timeseries_dict[f"arome~{id}"] = df

            continue

        # OBS from DWH
        else:
            device = element[0]
            data = dwh_retrieve(
                device=device,
                station=loc,
                vars=var_name,
                timestamps=[start, end],
                verbose=verbose,
            )

            if not data.empty:
                timeseries_dict[f"{device}~{var_name}"] = data

    if verbose:
        pprint(timeseries_dict)

    return timeseries_dict
