"""Purpose: Get data from icon simulation.

Author: Stephanie Westerhuis

Date: 11/11/2021
"""

# Standard library
import subprocess  # use: run command line commands from python
from io import StringIO
from pathlib import Path

# Third-party
# import ipdb
import numpy as np
import pandas as pd
import xarray as xr
from click.decorators import option


def lfff_name(lt):
    """Create mch-filename for icon ctrl run for given leadtime.

    Args:
        lt (int): leadtime

    Returns:
        str: lfff_filename (mch-convention)

    """
    hour = int(lt) % 24
    day = (int(lt) - hour) // 24
    remaining_s = round((lt - int(lt)) * 3600)
    sec = int(remaining_s % 60)
    mm = int((remaining_s - sec) / 60)

    return f"lfff{day:02}{hour:02}{mm:02}{sec:02}.nc"


def get_icon(folder, leadtime, lat, lon, ind, grid, var, alt_bot, alt_top):
    """Retrieve vertical profile of variable from icon simulation.

    Args:
        folder (str):           here are the icon simulation output files
        leadtime (list of int): simulation leadtime(s)
        lat (float):            latitude of location
        lon (float):            longitude of location
        ind (int):              index of location
        grid (str):             icon grid file containing HEIGHT field
        var (str):              variable name in icon file
        alt_bot (int):          lower boundary of plot
        alt_top (int):          upper boundary of plot

    Returns:
        pandas dataframe:       icon simulation values

    """
    df = pd.DataFrame()
    print(folder)

    files = [Path(folder, lfff_name(lt)) for lt in leadtime]
    ds = xr.open_mfdataset(files).squeeze()
    lats = np.rad2deg(ds.clat_1.values)
    lons = np.rad2deg(ds.clon_1.values)
    # ipdb.set_trace()
    return df
