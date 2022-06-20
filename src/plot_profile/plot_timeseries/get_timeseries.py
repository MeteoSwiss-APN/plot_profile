"""Retrieve available data into dict for timeseries plots."""
# Standard library
from pprint import pprint
import numpy as np

# Third-party
import pandas as pd

# First-party
from plot_profile.plot_arome.get_arome import get_arome_hm
from plot_profile.plot_arome.get_arome import get_arome_timeseries
from plot_profile.plot_icon.get_icon import get_icon_hm
from plot_profile.plot_icon.get_icon import get_icon_timeseries
from plot_profile.utils.calc_new_vars import calc_new_var_timeseries
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf

from ipdb import set_trace


def get_arome():
    # TODO: implement function to retrieve data from AROME model (.csv, .nc, whatever)
    # and parse into pandas dataframe
    return print("should return AROME dataframe at this point")


def get_timeseries_dict(start, end, elements, loc, grid_file, verbose):
    timeseries_dict = {}

    # loop over elements
    for element in elements:

        # retrieve variable name
        var_name = element[1]

        # ICON
        if element[0] == "icon":

            levels = element[2]
            id = element[3]
            folder = element[4]
            init = element[5]

            do_interpolation = False  # False by default, can be set to True later
            # if True, we need to call a different function in order to interpolate vertically model outputs

            # some parameters are not in icon and therefore need to be calculated from other parameters
            # so we first need to open theses other parameters
            if var_name == "wind_dir" or var_name == "wind_vel":
                var_open_icon = ["u", "v"]

            elif var_name == "rel_hum":
                var_open_icon = ["temp", "qv"]

            elif var_name == "grad_temp":
                var_open_icon = "temp"
                levels = [486, 506]
                do_interpolation = True

            else:
                var_open_icon = var_name

            # check if a key for this icon-instance (for example icon-ref or icon-exp,...) already exists.
            # if yes --> retrieve df as usual, but instead of assigning it to a new key, only append/concatenate
            # the variable column to the already existing dataframe.
            if f"icon~{id}" in timeseries_dict:

                if do_interpolation == True:
                    df = get_icon_hm(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        var=var_open_icon,
                        init=init,
                        height_list=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        grid_file=grid_file,
                        verbose=verbose,
                    )
                    do_interpolation = False  # reset

                else:
                    df = get_icon_timeseries(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        vars=var_open_icon,
                        init=init,
                        level=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        grid_file=grid_file,
                        verbose=verbose,
                    )

                # calculate new variables
                if (
                    var_name != var_open_icon
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, levels, sdf[loc].lat, sdf[loc].lon, verbose)

                del df["timestamp"]
                timeseries_dict[f"icon~{id}"] = pd.concat(
                    [timeseries_dict[f"icon~{id}"], df], axis=1
                )

                # print(id, timeseries_dict[f"icon~{id}"].columns.tolist(), df.columns.tolist())

            else:

                if do_interpolation == True:
                    df = get_icon_hm(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        var=var_open_icon,
                        init=init,
                        height_list=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        grid_file=grid_file,
                        verbose=verbose,
                    )
                    do_interpolation = False  # reset

                else:
                    df = timeseries_dict[f"icon~{id}"] = get_icon_timeseries(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        vars=var_open_icon,
                        init=init,
                        level=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        grid_file=grid_file,
                        verbose=verbose,
                    )

                # calculate new variables
                if (
                    var_name != var_open_icon
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, levels, sdf[loc].lat, sdf[loc].lon, verbose)

                timeseries_dict[f"icon~{id}"] = df

            # increase icon index
            continue

        # AROME
        elif element[0] == "arome":

            levels = element[2]
            id = element[3]
            folder = element[4]
            init = element[5]

            do_interpolation = False  # False by default, can be set to True later
            # if True, we need to call a different function in order to interpolate vertically model outputs

            # some parameters are not in arome and therefore need to be calculated from other parameters
            if var_name == "qv":
                var_open_arome = ["press", "dewp_temp"]

            elif var_name == "2m_qv":
                var_open_arome = ["press", "2m_dewp_temp"]

            elif var_name == "wind_dir" or var_name == "wind_vel":
                var_open_arome = ["u", "v"]

            elif var_name == "grad_temp":
                var_open_arome = "temp"
                levels = [486, 506]
                do_interpolation = True

            elif var_name == "tqc":
                var_open_arome = ["press", "temp", "qc", "rel_hum"]
                levels = np.arange(1,21)

            else:
                var_open_arome = var_name

            if f"arome~{id}" in timeseries_dict:

                # to calculate some kind of variables we need the levels in meters
                # and the values needs to be extrapolated for comparison
                if do_interpolation == True:
                    df = get_arome_hm(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        var=var_open_arome,
                        init=init,
                        height_list=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        verbose=verbose,
                    )
                    do_interpolation = False  # reset

                else:
                    df = get_arome_timeseries(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        vars=var_open_arome,
                        init=init,
                        levels=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        verbose=verbose,
                    )

                # calculate new variables
                if (
                    var_name != var_open_arome
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, levels, sdf[loc].lat, sdf[loc].lon, verbose)

                del df["timestamp"]
                timeseries_dict[f"arome~{id}"] = pd.concat(
                    [timeseries_dict[f"arome~{id}"], df], axis=1
                )

                # print(id, timeseries_dict[f"icon~{id}"].columns.tolist(), df.columns.tolist())

            else:
                if do_interpolation == True:
                    df = get_arome_hm(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        var=var_open_arome,
                        init=init,
                        height_list=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        verbose=verbose,
                    )
                    do_interpolation = False  # reset

                else:
                    df = get_arome_timeseries(
                        lat=sdf[loc].lat,
                        lon=sdf[loc].lon,
                        vars=var_open_arome,
                        init=init,
                        levels=levels,
                        start_lt=int(
                            (start - init).total_seconds() / 3600
                        ),  # full hours!
                        end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                        folder=folder,
                        verbose=verbose,
                    )

                # calculate new variables
                if (
                    var_name != var_open_arome
                ):  # equivalent to "if var needs to be calculated"
                    df = calc_new_var_timeseries(df, var_name, levels, sdf[loc].lat, sdf[loc].lon, verbose)

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

    return timeseries_dict
