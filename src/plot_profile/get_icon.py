"""Purpose: Get data from icon simulation.

Author: Stephanie Westerhuis

Date: 11/11/2021
"""

# Standard library
import datetime as dt
import sys
from pathlib import Path

# Third-party
# import ipdb
import numpy as np
import pandas as pd
import xarray as xr
from click.decorators import option

# Local
from .variables import vdf


def lfff_name(lt):
    """Create mch-filename for icon ctrl run for given leadtime.

    Args:
        lt (int): leadtime

    Returns:
        str: filename of icon output simulation in netcdf, following mch-convention

    """
    hour = int(lt) % 24
    day = (int(lt) - hour) // 24
    remaining_s = round((lt - int(lt)) * 3600)
    sec = int(remaining_s % 60)
    mm = int((remaining_s - sec) / 60)

    return f"lfff{day:02}{hour:02}{mm:02}{sec:02}.nc"


def ind_from_latlon(lats, lons, lat, lon, verbose=False):
    """Find the nearest neighbouring index to given location.

    Args:
        lats (2d array):            Latitude grid
        lons (2d array):            Longitude grid
        lat (float):                Latitude of location
        lon (float):                Longitude of location
        verbose (bool, optional):   Print information. Defaults to False.

    Returns:
        int     Index of nearest grid point.

    """
    dist = [
        np.sqrt((lats[i] - lat) ** 2 + (lons[i] - lon) ** 2) for i in range(len(lats))
    ]
    ind = np.where(dist == np.min(dist))[0][0]

    if verbose:
        print(f"Closest ind: {ind}")
        print(f" Given lat: {lat:.3f} vs found lat: {lats[ind]:.3f}")
        print(f" Given lat: {lon:.3f} vs found lon: {lons[ind]:.3f}")

    return ind


def calc_hhl(hfl):
    """Interpolate from full levels to half levels.

    Args:
        hfl (1d array): values of a variable defined on N full model levels

    Returns:
        1d array        values of this variable interpolated to N-1 half model levels

    """
    if hfl.ndim == 1:
        hhl = hfl[1:] + (hfl[:-1] - hfl[1:]) / 2
    else:
        print("height field has too many dimensions")
        sys.exit(1)

    return hhl


def get_icon(
    folder, date, leadtime, lat, lon, ind, grid, variables_list, alt_bot, alt_top
):
    """Retrieve vertical profile of variable from icon simulation.

    Args:
        folder (str):           here are the icon simulation output files
        date (datetime object): init date of simulation
        leadtime (list of int): simulation leadtime(s)
        lat (float):            latitude of location
        lon (float):            longitude of location
        ind (int):              index of location
        grid (str):             icon grid file containing HEIGHT field
        var_shortname (str):    variable shortname
        alt_bot (int):          lower boundary of plot
        alt_top (int):          upper boundary of plot

    Returns:
        pandas dataframe:       icon simulation values

    """
    print("--- retrieving & filtering data")

    data_dict = {}
    for variable in variables_list:
        # specify variable (pandas dataframe with attributes)
        var = vdf[variable]

        # list icon files
        date_str = date.strftime("%y%m%d%H")
        # print(f"Looking for files in {str(Path(folder, date_str))}")
        files = [Path(folder, date_str, lfff_name(lt)) for lt in leadtime]

        # load as xarray dataset
        ds = xr.open_mfdataset(files).squeeze()

        # extract latitude and longitude
        lats = ds.clat_1.values
        lons = ds.clon_1.values

        # convert from radians to degrees if given in radians
        if lats.max() < 2.0 and lons.max() < 2.0:
            print("assuming that lats and lons are given in radians")
            lats = np.rad2deg(lats)
            lons = np.rad2deg(lons)

        # find index closest to specified lat, lon
        ind = ind_from_latlon(lats, lons, lat, lon, False)

        # load constants file
        if Path(grid).is_file():
            ds_grid = xr.open_dataset(grid).squeeze()
        else:
            print("grid file does not exist!")

        # load latitude and longitude grid of constants file
        lats_grid = ds_grid.clat_1.values
        lons_grid = ds_grid.clon_1.values

        # convert from radians to degrees if given in radians
        if lats_grid.max() < 2.0 and lons_grid.max() < 2.0:
            print("assuming that lats and lons are given in radians")
            lats_grid = np.rad2deg(lats_grid)
            lons_grid = np.rad2deg(lons_grid)

        if ds.cells_1.size != ds_grid.cells_1.size:
            print("Attention: Sizes of output and grid file do not match!")

        # print("Latitude and logitude of selected index in grid file:")
        # print(f"{lats_grid[ind]:.2f}, {lons_grid[ind]:.2f}")

        # subselect values from column
        values = ds.isel(cells_1=ind)[var.icon_name].values * var.mult + var.plus
        height = ds_grid.isel(cells_1=ind)["HEIGHT"].values

        # create pandas objects of height and data values
        df_height = pd.Series(data=calc_hhl(height))

        df_values = pd.DataFrame(
            columns=leadtime,
            data=values.transpose(),
        )

        # criteria: height specifcations

        # crit = (df_height < alt_top) & (df_height > alt_bot)
        # exclude rows above specified altitude (alt_top)
        crit_upper = df_height < alt_top
        # set last False in to True
        last_false = crit_upper[crit_upper == False]
        if len(last_false) > 0:
            crit_upper[last_false.index.max()] = True

        # exclude rows below specified altitude (alt_bot)
        crit_lower = df_height > alt_bot
        last_false = crit_lower[crit_lower == False]
        if len(last_false) > 0:
            crit_lower[last_false.index.max()] = True

        # combine selection criteria
        crit = crit_upper & crit_lower

        data_dict["height"] = df_height[crit]
        data_dict[variable] = df_values[crit]

    return data_dict

    return df_height[crit], df_values[crit], data_dict
