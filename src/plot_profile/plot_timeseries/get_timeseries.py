"""Retrieve available data into dict for timeseries plots."""
# Standard library
from pprint import pprint

# Third-party
import netCDF4 as nc
import pandas as pd 
import xarray as xr
from datetime import datetime 
import glob 
import sys

# First-party
from plot_profile.plot_icon.get_icon import get_icon_timeseries
from plot_profile.utils.dwh_retrieve import dwh_retrieve
from plot_profile.utils.stations import sdf
from plot_profile.plot_arome.variables_tmp import vdf
from plot_profile.utils.arome_tools import coord_2_arome_pts

# from ipdb import set_trace

def get_arome_timeseries(lat, lon, vars, init, level, start_lt, end_lt, folder, verbose):
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
    df = pd.DataFrame()
    dy, dx = coord_2_arome_pts(lat, lon) # timeseries location in arome coords
    
    # folder containing the arome files
    nc_path = folder + datetime.strftime(init,"%Y%m%dT%H%MP")
    if verbose:
        print(f"Looking for files in {str(nc_path)}")

    # if string, transform it to a 1 element list 
    if isinstance(vars, str):
        lst_tmp = []
        vars = lst_tmp.append(vars)
        vars = lst_tmp
    print(vars)

    for var in vars: 
        # is var availible in our Arome files ?
        if vdf.loc["arome_name"][var] == None:
            print(f"--- ! No {var} in arome files")
            sys.exit(1)
        else: 
            var_aro = vdf.loc["arome_name"][var]    # name of variables in arome
            if verbose:
                print(f"Searching for {var} (called {var_aro}) in Arome.")

        # looking for nc files       
        files = sorted(glob.glob(f"{nc_path}/{var_aro}.arome-forecast.payerne+00*.nc"))[start_lt:end_lt]
        
        if verbose:
            print("files:")
        for f in files:
            print(f"  {f}")

        # load nc files as xarray dataset
        if verbose:
            print("Loading files into xarray dataset.")

        nc_data = nc.Dataset(files[0],"r")
        ncgrp = nc_data.groups[var_aro]   # selecting the right group (ensembles)
        xr_data = xr.open_dataset(xr.backends.NetCDF4DataStore(ncgrp))  #nc to xarray dataset
        
        for i in files[1:-1]:     # all the files except the first wich is already openend
            nc_data =  nc.Dataset(i,"r")     # open DS with netDCF4 modules
            ncgrp = nc_data.groups[var_aro]   # selecting the group we need
            xr_data_tmp = xr.open_dataset(xr.backends.NetCDF4DataStore(ncgrp))  # converting it to xarray Dataset
            
            xr_data = xr.concat([xr_data, xr_data_tmp], dim='time')             # adding our new DS to the big old one 

        if verbose:
            print("Finished loading files into xarray dataset.")

        # timestamp column
        if 'timestamp' not in df.columns:  # only the first loop time
            date_list = []
            for date in xr_data['Time']:
                # from POSIX to string format
                date_list.append(datetime.utcfromtimestamp(int(date)).strftime("%Y-%m-%d %H:%M:%S"))
            df['timestamp'] = date_list

        # var column
        # 2D var or level = 0
        if (level == 0) or (xr_data['z'].size < 2):
            column_label = var
            values = xr_data.variables[var_aro][:, 0, dy, dx]
        # 3D var -> add level to column name
        else:
            column_label = f"{var}~{level}"
            values = xr_data.variables[var_aro][:, level, dy, dx]
        
        # add deaveraging here for some arome vars ? here :)
        # ...

        mult , plus = vdf.loc["mult_arome"][var] , vdf.loc["plus_arome"][var]
        df[column_label] = values * mult + plus 
    
    return(df)


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

            level = element[2]
            id = element[3]
            folder = element[4]
            init = element[5]

            if f"arome~{id}" in timeseries_dict:
                df = get_arome_timeseries(
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
                timeseries_dict[f"arome~{id}"] = get_arome_timeseries(
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
