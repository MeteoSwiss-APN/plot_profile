"""Get data from arome simulation.

Author: Arthur Dandoy
"""

# Standard library
import glob
import sys
from datetime import datetime
from datetime import timedelta
from pathlib import Path

# Third-party
import netCDF4 as nc
import pandas as pd
import scipy
import xarray as xr

# First-party
from plot_profile.utils.utils import decumulate
from plot_profile.utils.variables import vdf

# from ipdb import set_trace


def coord_2_arome_pts(lat, lon, verbose=False):
    """Convert lat/lon to dy/dx in arome domain.

    Args:
        lat (float): latitude
        lon (float): longitude
        verbose (bool): print details
    Returns: x,y (int)

    """
    A, B = 121 / 3, 201 / 5

    if (5 <= lon <= 10) and (46 <= lat <= 49):
        dy, dx = int(round((49 - lat) * A)), int(round((lon - 5) * B))
        if verbose:
            print(
                f"Determined (dx,dy) corresponding to (lon,lat): ({lon},{lat}) -> ({dx},{dy})"
            )
        return (dy, dx)

    else:
        print(
            "Coordonnées lat/lon en dehors du domaine, par défaut Payerne: 46.81291/6.94418"
        )
        return (int(round((49 - 46.81291) * A)), int(round((6.94418 - 5) * B)))


def slice_top_bottom_V2(df_height, alt_top=None, alt_bot=None, verbose=False):
    """Criteria to cut away top and bottom of dataframe.

    Args:
        df_height (pandas series):      height variable
        alt_top (int):                  top
        alt_bot (int):                  bottom

    Returns:
        list of booleans; rows containing True are to be kept in the original dataframe

    """
    # create pandas series of len(df_height) full of NaN values
    crit = pd.Series(
        len(df_height) * [False]
    )  # change False to NaN if so desired (other changes necessary as well!)

    if not type(alt_bot) == float:
        if verbose:
            print("No bottom specified, use minimal height.")
        alt_bot = -1

    if not type(alt_top) == float:
        if verbose:
            print("No bottom specified, use maximal height.")
        alt_top = 1e6

    for i, height in enumerate(df_height):

        if alt_bot < height < alt_top:
            crit[i - 1 : i + 2] = True

    return crit


def calc_arome_height(dx, dy, verbose=False):
    """Calculate height levels above sea level in arome.

    Args:
        dx (int):        x-coordinate in arome domain
        dy (int):        y-coordinate in arome domain
        verbose (bool):  print details

    Returns:
        pandas series: arome height (asl) level of the grid point

    """
    if verbose:
        print(f"Calculating arome levels hegihts above the ({dx},{dy}) grid point")

    # file containing arome heights data (could be any file)
    height_data = nc.Dataset(
        "/scratch/adandoy/AROME/20211118T1200P/P.arome-forecast.payerne+0000_00.nc",
        "r",
    )

    # open altitudes above sea level
    nc_alti = height_data.groups["P"].variables["Altitude"][:]  # alt above ground level
    nc_physio = height_data.groups["PHYSIO"].variables["zsol"][
        dy, dx
    ]  # ground alt above sea level

    df_height = pd.Series(nc_physio + nc_alti)

    return df_height


def get_arome_profiles(
    folder,
    date,
    leadtime,
    lat,
    lon,
    variables_list,
    alt_bot,
    alt_top,
    verbose,
):
    """Retrieve vertical profile of variable from arome simulation.

    Args:
        folder (str):           here are the icon simulation output files
        date (datetime object): init date of simulation
        leadtime (list of int): simulation leadtime(s)
        lat (float):            latitude of location
        lon (float):            longitude of location
        variables_list (str):   variable shortname
        alt_bot (int):          lower boundary of plot
        alt_top (int):          upper boundary of plot
        verbose (bool):         print details

    Returns:
        pandas dataframe:       arome simulation values

    """
    if verbose:
        print("--- retrieving & filtering arome data")

    # create the dict that will contain altitude and arome values
    data_dict = {}

    # profile location in arome coords
    dy, dx = coord_2_arome_pts(lat, lon, verbose)

    # folder containing the arome files
    nc_path = folder + datetime.strftime(date, "%Y%m%dT%H%MP")
    if verbose:
        print(f"Looking for files in {str(nc_path)}")

    ## Create height Data Frame and select altitude

    # calculate arome heights above sea level
    df_height = calc_arome_height(dx, dy, verbose)

    # select the index where altitudes are between requested bottom and top
    crit = slice_top_bottom_V2(
        df_height=df_height, alt_top=alt_top, alt_bot=alt_bot, verbose=verbose
    )

    data_dict["height"] = df_height[crit]

    # if var is string transform it to a 1 element list
    if isinstance(variables_list, str):
        variables_list = [
            variables_list,
        ]

    ## Create values Data Frame

    for var in variables_list:

        # is var availible in our Arome files ?
        if vdf.loc["arome_name"][var] == None:
            print(f"--- ! No {var} in arome files")
            sys.exit(1)

        else:
            var_aro = vdf.loc["arome_name"][var]  # name of variables in arome
            if verbose:
                print(f"Searching for {var} (called {var_aro}) in Arome.")

        # load nc files as xarray dataset
        if verbose:
            print("Loading files into xarray dataset.")

        # looking for nc files
        files = []
        for lt in leadtime:
            if lt < 10:
                lt = "0" + str(lt)
            else:
                lt = str(lt)
            files.append(
                Path(nc_path, f"{var_aro}.arome-forecast.payerne+00{lt}_00.nc")
            )

        if verbose:
            print("files:")
            for f in files:
                print(f"  {f}")

        nc_data = nc.Dataset(files[0], "r")
        ncgrp = nc_data.groups[var_aro]  # selecting the right group (ensembles)
        xr_data = xr.open_dataset(
            xr.backends.NetCDF4DataStore(ncgrp)
        )  # nc to xarray dataset

        for i in files[1:]:  # all the files except the first wich is already openend
            nc_data = nc.Dataset(i, "r")  # open DS with netDCF4 modules
            ncgrp = nc_data.groups[var_aro]  # selecting the group we need
            xr_data_tmp = xr.open_dataset(
                xr.backends.NetCDF4DataStore(ncgrp)
            )  # converting it to xarray Dataset

            xr_data = xr.concat(
                [xr_data, xr_data_tmp], dim="time"
            )  # adding our new DS to the big old one

        if verbose:
            print("Finished loading files into xarray dataset.")

        # subselect values at the right grid point and do conversions
        values = (
            xr_data.variables[var_aro][:, :, dy, dx] * vdf.loc["mult_arome"][var]
            + vdf.loc["plus_arome"][var]
        )

        # fill into dataframe
        df_values = pd.DataFrame(columns=leadtime, data=values.transpose())

        # only extract the relevant altitude levels (encoded in the crit series; True --> relevant)
        df_values = df_values[crit]

        # add to dictionary
        data_dict[var] = df_values

    return data_dict


def get_arome_timeseries(
    lat, lon, vars, init, levels, start_lt, end_lt, folder, verbose
):
    """Retrieve timeseries from AROME outputs.

    Args:
        lat (float):                         latitude
        lon (float):                         longitude
        vars (list of strings or string):    arome variables
        init (datetime object):              init date of simulation
        levels (list of int):                model levels ("1" = lowest model level)
        start_lt (int):                      start leadtime
        end_lt (int):                        end leadtime
        folder (str):                        folder containing subfolders with arome runs
        verbose (bool):                      print details

    """
    df = pd.DataFrame()

    # open timeseries location in arome coords
    dy, dx = coord_2_arome_pts(lat, lon, verbose)

    # folder containing the arome files
    nc_path = folder + datetime.strftime(init, "%Y%m%dT%H%MP")
    if verbose:
        print(f"Looking for files in {str(nc_path)}")

    # if string, transform it to a 1 element list
    if isinstance(vars, str):
        vars = [
            vars,
        ]

    if isinstance(levels, int):
        levels = [
            levels,
        ]

    print(levels, vars)
    for var in vars:

        # is var availible in our Arome files ?
        if vdf.loc["arome_name"][var] == None:
            print(f"--- ! No {var} in arome files")
            sys.exit(1)
        else:
            var_aro = vdf.loc["arome_name"][var]  # name of variables in arome
            if verbose:
                print(f"Searching for {var} (called {var_aro}) in Arome.")

        # looking for nc files
        files = sorted(glob.glob(f"{nc_path}/{var_aro}.arome-forecast.payerne+00*.nc"))[
            start_lt : end_lt + 1
        ]

        if verbose:
            print("files:")
            for f in files:
                print(f"  {f}")

        # load nc files as xarray dataset
        if verbose:
            print("Loading files into xarray dataset.")

        nc_data = nc.Dataset(files[0], "r")
        ncgrp = nc_data.groups[var_aro]  # selecting the right group (ensembles)
        xr_data = xr.open_dataset(
            xr.backends.NetCDF4DataStore(ncgrp)
        )  # nc to xarray dataset

        for i in files[1:]:  # all the files except the first wich is already openend
            nc_data = nc.Dataset(i, "r")  # open DS with netDCF4 modules
            ncgrp = nc_data.groups[var_aro]  # selecting the group we need
            xr_data_tmp = xr.open_dataset(
                xr.backends.NetCDF4DataStore(ncgrp)
            )  # converting it to xarray Dataset

            xr_data = xr.concat(
                [xr_data, xr_data_tmp], dim="time"
            )  # adding our new DS to the big old one

        if verbose:
            print("Finished loading files into xarray dataset.")

        ## timestamp column
        if "timestamp" not in df.columns:  # only the first loop time
            date_list = []
            for date in xr_data["Time"]:
                # from POSIX to string format
                date_list.append(
                    (
                        datetime.utcfromtimestamp(int(date)) + timedelta(hours=1)
                    ).strftime("%Y-%m-%d %H:%M:%S")
                )
            df["timestamp"] = date_list

        ## var column
        # one column for each requested levels
        for level in levels:

            # 2D var or level = 0
            if level == 0 and xr_data["z"].size < 2:  # and len(levels) == 1:
                if xr_data["z"].size < 2:
                    column_label = var
                    values = xr_data.variables[var_aro][:, 0, dy, dx]
                else:
                    print(
                        f"--- ! No level 0 for 3D vars in arome (for first level input '1')"
                    )
                    sys.exit(1)

            # 3D var -> add level to column name
            else:
                column_label = f"{var}~{level}"
                # ask for level -1 so level indent in arome and in icon are equivalent.
                values = xr_data.variables[var_aro][:, level - 1, dy, dx]

            # decumulating vars
            if vdf.loc["acc"][var] == True:
                if verbose:
                    print("Decumalating arome vars")

                values = decumulate(values)

            # add factor or values
            mult, plus = vdf.loc["mult_arome"][var], vdf.loc["plus_arome"][var]

            df[column_label] = values * mult + plus

    return df


def get_arome_hm(lat, lon, var, init, height_list, start_lt, end_lt, folder, verbose):
    """Retrieve timeseries of an interpolated var for Arome output.

    Args:
        lat (float):                  latitude in degrees
        lon (float):                  longitude in degrees
        var (str):                    variable name
        init (datetime object):       init date of simulation
        height_list (list of floats):  list of heights on where to do the interpolation
        start_lt (int):               start leadtime
        end_lt (int):                 end leadtime
        folder (str):                 folder containing subfolders with arome runs
        verbose (bool):               print details

    Returns:
        pandas dataframe:             arome simulation values

    """
    df = pd.DataFrame()

    # open timeseries location in arome coords
    dy, dx = coord_2_arome_pts(lat, lon)

    # folder containing the arome files
    nc_path = folder + datetime.strftime(init, "%Y%m%dT%H%MP")
    if verbose:
        print(f"Looking for files in {str(nc_path)}")

    # oepening arome level heights
    height_arome = calc_arome_height(dx, dy)

    # is var availible in our Arome files ?
    if vdf.loc["arome_name"][var] == None:
        print(f"--- ! No {var} in arome files")
        sys.exit(1)
    else:
        var_aro = vdf.loc["arome_name"][var]  # name of variables in arome
        if verbose:
            print(f"Searching for {var} (called {var_aro}) in Arome.")

    # looking for nc files
    files = sorted(glob.glob(f"{nc_path}/{var_aro}.arome-forecast.payerne+00*.nc"))[
        start_lt:end_lt
    ]

    if verbose:
        print("files:")
        for f in files:
            print(f"  {f}")

    # load nc files as xarray dataset
    nc_data = nc.Dataset(files[0], "r")
    ncgrp = nc_data.groups[var_aro]  # selecting the right group (ensembles)
    xr_data = xr.open_dataset(
        xr.backends.NetCDF4DataStore(ncgrp)
    )  # nc to xarray dataset

    for i in files[1:-1]:  # all the files except the first wich is already openend
        nc_data = nc.Dataset(i, "r")  # open DS with netDCF4 modules
        ncgrp = nc_data.groups[var_aro]  # selecting the group we need
        xr_data_tmp = xr.open_dataset(
            xr.backends.NetCDF4DataStore(ncgrp)
        )  # converting it to xarray Dataset
        xr_data = xr.concat(
            [xr_data, xr_data_tmp], dim="time"
        )  # adding our new DS to the big old one

    ## timestamp column
    date_list = []
    for date in xr_data["Time"]:
        # from POSIX to string format
        date_list.append(
            (datetime.utcfromtimestamp(int(date)) + timedelta(hours=1)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    df["timestamp"] = date_list

    ## variables columns
    values = xr_data.variables[var_aro][:, :, dy, dx]

    if verbose:
        print(f"Interpolating arome {var} and heights on: {height_list}...")
    # creating f_interpolate_aro function thanks to scipy
    f_interpolate_aro = scipy.interpolate.interp1d(
        height_arome, values, axis=1, fill_value="extrapolate"
    )

    # interoplating arome over requested height levels
    values = f_interpolate_aro(height_list)
    if verbose:
        print(f"Finished interpolating.")

    # add factor or values
    mult, plus = vdf.loc["mult_arome"][var], vdf.loc["plus_arome"][var]

    for k in range(len(height_list)):
        col_name = f"{var}~{str(height_list[k])}"
        df[col_name] = values[:, k] * mult + plus

    return df
