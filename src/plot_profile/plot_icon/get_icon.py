"""Purpose: Get data from icon simulation.

Author: Stephanie Westerhuis

Date: 11/11/2021
"""

# Standard library
import datetime as dt
import sys
from doctest import DocFileCase
from pathlib import Path
from pprint import pprint

# Third-party
import numpy as np
import pandas as pd
import scipy
import xarray as xr

# First-party
from plot_profile.utils.utils import deaverage
from plot_profile.utils.utils import get_dim_names
from plot_profile.utils.utils import get_icon_name
from plot_profile.utils.utils import slice_top_bottom
from plot_profile.utils.variables import vdf

# from ipdb import set_trace


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


def calc_hfl(hhl):
    """Interpolate from half levels to full levels.

    Args:
        hhl (1d array): values of a variable defined on N half model levels

    Returns:
        1d array        values of this variable interpolated to N-1 full model levels

    """
    if hhl.ndim == 1:
        hfl = hhl[1:] + (hhl[:-1] - hhl[1:]) / 2
    else:
        print("height field has too many dimensions")
        sys.exit(1)

    return hfl


def index_height_from_grid_file(lat, lon, grid, verbose):
    """Retrieve index and height for specific grid point.

    Args:
        lat (float): latitude
        lon (float): longitude
        grid (str): grid file (netcdf)
        verbose (bool): print details

    Returns:
        index (int)
        height (1-dimensional np array)
        size (int): size of grid file

    """
    if verbose:
        print(
            "Assuming that variable's grid corresponds to clat_1 and clon_1 from grid-file"
        )
        print(" with uuid FC046F09-ED97-850E-1E31-8927421B2B60.")

    # load grid file
    if verbose:
        print(f"Load grid from: {grid}")
    if Path(grid).is_file():
        ds_grid = xr.open_dataset(grid).squeeze()
    else:
        print("Grid file does not exist!")
        sys.exit(1)

    # load latitude and longitude grid of constants file
    lats_grid = ds_grid.clat_1.values
    lons_grid = ds_grid.clon_1.values

    # convert from radians to degrees if given in radians
    if lats_grid.max() < 2.0 and lons_grid.max() < 2.0:
        print("Assuming that lats and lons of grid file are given in radians.")
        lats_grid = np.rad2deg(lats_grid)
        lons_grid = np.rad2deg(lons_grid)

    # find index closest to specified lat, lon (in grid file)
    ind = ind_from_latlon(lats_grid, lons_grid, lat, lon, False)
    if verbose:
        print(f"Determined ind: {ind}.")

    # lat and lon from grid file
    if verbose:
        print("Latitude and longitude of selected index in grid file:")
        print(f"{lats_grid[ind]:.4f}, {lons_grid[ind]:.4f}")

    # load HEIGHT from grid file
    try:
        height = ds_grid.isel(cells_1=ind)["HEIGHT"].values
    except KeyError:
        print(f"Variable HEIGHT does not exist in grid file: {grid}")
        sys.exit(1)

    return ind, height, lats_grid.size


def get_icon(
    folder,
    date,
    leadtime,
    lat,
    lon,
    ind,
    grid,
    variables_list,
    alt_bot,
    alt_top,
    full_levels=False,
    verbose=False,
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
        full_levels(int):       set to True if variables are defined on full levels

    Returns:
        pandas dataframe:       icon simulation values

    """
    if verbose:
        print("--- retrieving & filtering icon data")

    # create dictionary to collect data of height and variables
    data_dict = {}

    ### A) Grid file: latitude, longitude and altitude
    ##################################################

    # index and height only have to be retrieved once
    if not ind:
        ind, height, size = index_height_from_grid_file(lat, lon, grid, verbose)

        # create pandas objects of height values
        if full_levels == True:
            df_height = pd.Series(data=height)
            if verbose:
                print("Variables are on full levels.")
        else:
            df_height = pd.Series(data=calc_hhl(height))

        # reverse order of df_height s.t. it is from bottom to top
        df_height = df_height.iloc[::-1].reset_index(drop=True)

        # get criteria to cut away top and bottom
        crit = slice_top_bottom(
            df_height=df_height, alt_top=alt_top, alt_bot=alt_bot, verbose=verbose
        )

        # fill HEIGHT as sliced pandas series into dictionary
        data_dict["height"] = df_height[crit]

    ### B) ICON forecast files
    ##########################

    date_str = date.strftime("%y%m%d%H")

    # TODO the following should be a separate function which can be reused for
    #      the timeseries
    # list icon files
    if verbose:
        print(f"Looking for files in {str(Path(folder, date_str))}")

    files = [Path(folder, date_str, lfff_name(lt)) for lt in leadtime]

    if verbose:
        print("files:")
        for f in files:
            print(f"  {f}")

    # load as xarray dataset
    if verbose:
        print("Loading files into xarray dataset.")
    ds = xr.open_mfdataset(files).squeeze()
    if verbose:
        print("Finished loading files into xarray dataset.")

    # if var is string transform it to a 1 element list
    if isinstance(variables_list, str):
        variables_list = [
            variables_list,
        ]

    for variable in variables_list:

        # specify variable (pandas dataframe with attributes)
        var = vdf[variable]
        # subselect values from column
        try:
            values = ds.isel(cells_1=ind)[var.icon_name].values * var.mult + var.plus
        except ValueError:
            try:
                values = ds.isel(ncells=ind)[var.icon_name].values * var.mult + var.plus
            except ValueError:
                try:
                    values = (
                        ds.isel(cells=ind)[var.icon_name].values * var.mult + var.plus
                    )
                except ValueError:
                    print(
                        f'! no dimensions called "cells_1", "ncells" or "cells" for {var.icon_name}'
                    )
                    continue
        except KeyError:
            print(f"{var.icon_name} cannot be found in forecast file")
            continue

        # fill into dataframe
        df_values = pd.DataFrame(
            columns=leadtime,
            data=values.transpose(),
        )

        # reverse order of df_values as well. --> now it should be corresonding to the reversed height column
        df_values = df_values.iloc[::-1].reset_index(drop=True)

        # only extract the relevant altitude levels (encoded in the crit series; True --> relevant)
        df_values = df_values[crit]

        # add to dictionary
        data_dict[variable] = df_values

    return data_dict


def get_icon_timeseries(
    lat, lon, vars, init, level, start_lt, end_lt, folder, grid_file, verbose
):
    """Retrieve timeseries from ICON output.

    Args:
        lat (float): latitude
        lon (float): longitude
        vars (list of strings or string): icon variables
        init (datetime object): init date of simulation
        level (int): model level ("1" = lowest model level)
        start_lt (int): start leadtime
        end_lt (int): end leadtime
        folder (str): folder containing subfolders with icon runs
        grid_file (str): icon-1 grid file
        verbose (bool): print details

    """
    # determine index of loc from grid file
    ind, height, size = index_height_from_grid_file(lat, lon, grid_file, verbose)

    hhl = calc_hhl(height)

    # directory with forecast files
    init_str = init.strftime("%y%m%d%H")
    icon_dir = Path(folder, init_str)

    if not icon_dir.is_dir():
        print(f"--- ! {icon_dir} does not exist!")
        sys.exit(1)

    if verbose:
        print(f"Looking for files in {str(icon_dir)}")

    # retrieve lfff-files
    leadtimes = np.arange(start_lt, end_lt + 1)
    files = [Path(icon_dir, lfff_name(lt)) for lt in leadtimes]

    if verbose:
        print("files:")
        for f in files:
            print(f"  {f}")

    # load forecast files as xarray dataset
    if verbose:
        print("Loading files into xarray dataset.")
    ds = xr.open_mfdataset(files).squeeze()
    if verbose:
        print("Finished loading files into xarray dataset.")

    # create df which collects icon variables
    #   pd.Dataframe with columns 'timestamp', 'var1~level1', 'var2', ...
    df = pd.DataFrame()

    # timestamps
    timestamps = []
    for lt in leadtimes:
        timestamps.append(init + dt.timedelta(hours=int(lt)))

    df["timestamp"] = timestamps

    # loop over icon variable(s) and add them to the dataframe

    # "vars" can be string or list of strings
    if isinstance(vars, str):
        vars = [
            vars,
        ]

    for i, variable in enumerate(vars):

        # for variables without level, e.g. 2m_temperature
        if level == 0:
            column_label = variable
        # add level to name
        else:
            column_label = f"{variable}~{level}"

        var = vdf[variable]

        # find correct icon name from list of possible names
        var.icon_name = get_icon_name(ds, var.icon_names, verbose)

        # dataset with only one specific variable
        ds_var = ds[var.icon_name]
        #        except KeyError:
        #            print(f"{var.icon_name} cannot be found in forecast file")
        #            continue

        # assume that variable is of structure:
        # a) time, height, N cells
        # b) time, N cells
        dim_time, dim_index, dim_level = get_dim_names(ds_var, verbose)

        # a)
        if (
            isinstance(dim_time, str)
            and isinstance(dim_index, str)
            and isinstance(dim_level, str)
        ):
            values = ds_var.isel(**{dim_index: ind, dim_level: np.negative(level)})

        # b)
        elif (
            isinstance(dim_time, str)
            and isinstance(dim_index, str)
            and dim_level is None
        ):
            values = ds_var.isel(**{dim_index: ind})
        else:
            print(
                f"--- ! Dims do not make sense: {dim_time}, {dim_index}, {dim_level}!"
            )
            continue

        # de-average
        if var.avg:
            values = deaverage(values)

        df[column_label] = values * var.mult + var.plus
    return df


def get_icon_hm(
    lat, lon, var, init, height_list, start_lt, end_lt, folder, grid_file, verbose
):
    """Retrieve timeseries of an interpolated var for Arome outputs.

    Args:
        lat (float):                   latitude in degrees
        lon (float):                   longitude in degrees
        var (str):                     variable name
        init (datetime object):        init date of simulation
        height_list (list of floats):  list of heights on where to do the interpolation
        start_lt (int):                start leadtime
        end_lt (int):                  end leadtime
        folder (str):                  folder containing subfolders with icon runs
        grid_file (str):               icon-1 grid file
        verbose (bool):                print details

    Returns:
        pandas dataframe:              icon simulation values

    """
    # create df which collects icon variables
    df = pd.DataFrame()

    ind, height, size = index_height_from_grid_file(lat, lon, grid_file, verbose)

    hfl = calc_hfl(height)

    # directory with forecast files
    init_str = init.strftime("%y%m%d%H")
    icon_dir = Path(folder, init_str)

    if not icon_dir.is_dir():
        print(f"--- ! {icon_dir} does not exist!")
        sys.exit(1)

    if verbose:
        print(f"Looking for files in {str(icon_dir)}")

    # retrieve lfff-files
    leadtimes = np.arange(start_lt, end_lt + 1)
    files = [Path(icon_dir, lfff_name(lt)) for lt in leadtimes]

    if verbose:
        print("files:")
        for f in files:
            print(f"  {f}")

    # load forecast files as xarray dataset
    if verbose:
        print("Loading files into xarray dataset.")
    ds = xr.open_mfdataset(files).squeeze()
    if verbose:
        print("Finished loading files into xarray dataset.")

    # select variable
    ds_var = ds[vdf.loc["icon_name"][var]]

    dim_time, dim_index, dim_level = get_dim_names(ds_var, verbose)

    # checking that variable is 3D
    if (
        isinstance(dim_time, str)
        and isinstance(dim_index, str)
        and isinstance(dim_level, str)
    ):
        values = ds_var.isel(**{dim_index: ind})  # , dim_level: np.negative(level)})

    elif isinstance(dim_time, str) and isinstance(dim_index, str) and dim_level is None:
        print(f"--- ! {var} is 2D. Need a 3D variable.")
        sys.exit(1)

    else:
        print(f"--- ! Dims do not make sense: {dim_time}, {dim_index}, {dim_level}!")
        sys.exit(1)

    # creating f_interpolate_ico function thanks to scipy
    if verbose:
        print(f"Interpolating icon {var} and heights on: {height_list}...")

    f_interpolate_ico = scipy.interpolate.interp1d(
        hfl, values, axis=1, fill_value="extrapolate"
    )

    # interoplating icon over requested height levels
    values = f_interpolate_ico(height_list)

    if verbose:
        print(f"Finished interpolating.")

    ## timestamps column
    timestamps = []
    for lt in leadtimes:
        timestamps.append(init + dt.timedelta(hours=int(lt)))

    df["timestamp"] = timestamps

    ## variables columns

    # add factor or values
    mult, plus = vdf.loc["mult"][var], vdf.loc["plus"][var]

    for k in range(len(height_list)):
        col_name = f"{var}~{str(height_list[k])}"
        df[col_name] = values[:, k] * mult + plus

    return df
