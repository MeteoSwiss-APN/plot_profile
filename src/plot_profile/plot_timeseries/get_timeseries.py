"""Retrieve available data into dict for timeseries plots."""
# Local
from ..plot_icon.get_icon import get_icon_timeseries
from ..utils.dwh_retrieve import dwh_retrieve
from ..utils.stations import sdf

# from ipdb import set_trace


def get_arome():
    # TODO: implement function to retrieve data from AROME model (.csv, .nc, whatever)
    # and parse into pandas dataframe
    return print("should return AROME dataframe at this point")


def get_timeseries_dict(
    start, end, elements, loc, device, init, folder, grid_file, verbose
):
    if "icon" in device:  # ICON STUFF
        # > icon_columns is a list, of column names for the icon-dataframe
        # > icon_vars is a list of variables to retrieve for the icon model
        # > icon_levels is a corresponding list of levels, for which these variables should be retrieved
        icon_columns, icon_vars, icon_levels = [], [], []
        sep = "~"
        for element in elements:
            if element[0] == "icon":
                icon_vars.append(element[1])
                icon_levels.append(element[2])
                if element[2] != 0:
                    icon_columns.append(element[1] + sep + str(element[2]))
                else:
                    icon_columns.append(element[1])

    # if "arome" in device:
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~AROME STUFF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # maybe some preliminary definitions and variables are necesary for the AROME model;
    # define them here. TODO.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    # retrieve for each device one dataframe, containing all corresponding variables at all specified levels
    timeseries_dict = {}
    # fill the timeseries_dict
    for dev in list(set(device)):
        if dev == "icon":
            timeseries_dict["icon"] = get_icon_timeseries(
                lat=sdf[loc].lat,
                lon=sdf[loc].lon,
                cols=icon_columns,
                vars=icon_vars,
                init=init,
                level=icon_levels,
                start_lt=int((start - init).total_seconds() / 3600),  # full hours!
                end_lt=int((end - init).total_seconds() / 3600),  # full hours!
                folder=folder,
                grid_file=grid_file,
                verbose=verbose,
            )
            continue  # go to next variable

        if dev == "arome":
            # call function, which returns a nice dataframe, containing the data from the arome model
            timeseries_dict["arome"] = get_arome()
            continue  # go to next variable

        # collect variables that belong to current device
        vars = []
        for element in elements:
            if element[0] == dev:
                vars.append(element[1])

        # all other devices apart from ICON which are retrievable from DWH
        data = dwh_retrieve(
            device=dev,
            station=loc,
            vars=vars,
            timestamps=[start, end],
            verbose=verbose,
        )

        if not data.empty:
            timeseries_dict[dev] = data

    return timeseries_dict
