"""Retrieve available data into dict for timeseries plots."""
# Standard library
from pprint import pprint

# Third-party
import pandas as pd
import glob

# First-party
from plot_profile.plot_icon.get_icon import get_icon_timeseries
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf

# from ipdb import set_trace

# TODO: implement function to retrieve data from AROME model (.csv, .nc, whatever)
# and parse into pandas dataframe
def get_arome(lat, lon, vars, init, level, start_lt, end_lt, folder, verbose):
    """Retrieve timeseries from AROME output.
    Args:
        lat (float): latitude
        lon (float): longitude
        vars (list of strings or string): icon variables
        init (datetime object): init date of simulation
        level (int): model level ("1" = lowest model level)
        start_lt (int): start leadtime
        end_lt (int): end leadtime
        folder (str): folder containing subfolders with icon runs
        verbose (bool): print details
    """

    print('aaaa')
    return print("should return AROME dataframe at this point")


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

            # check if a key for this icon-instance (for example icon-ref or icon-exp,...) already exists.
            # if yes --> retrieve df as usual, but instead of assigning it to a new key, only append/concatenate
            # the variable column to the already existing dataframe.
            if f"icon~{id}" in timeseries_dict:
                df = get_icon_timeseries(
                    lat=sdf[loc].lat,
                    lon=sdf[loc].lon,
                    vars=var_name,
                    init=init,
                    level=level,
                    start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                    end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                    folder=folder,
                    grid_file=grid_file,
                    verbose=verbose,
                )
                del df["timestamp"]
                timeseries_dict[f"icon~{id}"] = pd.concat(
                    [timeseries_dict[f"icon~{id}"], df], axis=1
                )

                # print(id, timeseries_dict[f"icon~{id}"].columns.tolist(), df.columns.tolist())

            else:
                timeseries_dict[f"icon~{id}"] = get_icon_timeseries(
                    lat=sdf[loc].lat,
                    lon=sdf[loc].lon,
                    vars=var_name,
                    init=init,
                    level=level,
                    start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                    end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                    folder=folder,
                    grid_file=grid_file,
                    verbose=verbose,
                )

            # increase icon index
            continue

        # AROME
        elif element[0] == "arome":
            print("Has to be implemented.")
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
