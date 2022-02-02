"""Purpose: define command line inputs.

Author: Stephanie Westerhuis

Date: 10/11/2021.
"""
# Standard library
import sys

# Third-party
import click

# Local
from ..utils.dwh_retrieve import dwh_retrieve
from ..utils.stations import sdf
from ..utils.utils import slice_top_bottom
from ..utils.utils import validtime_from_leadtime
from .get_icon import get_icon
from .plot_icon import create_plot

# import ipdb


@click.command()
# options without default value (mandatory to specify by user)
@click.option(
    "--date",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Init date of icon simulation: YYMMDDHH.",
)
@click.option(
    "--folder",
    type=str,
    help="MANDATORY: Path to main folder with icon output. Here should be a subfolder named after the date containing nc-files.",
)
@click.option(
    "--var",
    type=click.Choice(
        [
            "temp",
            "qc",
            "qv",
            "clc",
            "ddt_t_rad_lw",
            "ddt_t_rad_sw",
            "qc_dia",
            "qv_dia",
            "qi_dia",
        ],
        case_sensitive=True,
    ),
    multiple=True,
    help="MANDATORY: Variable name(s).",
)
# options with default value
@click.option(
    "--add_clouds",
    is_flag=True,
    help="Show clouds on plot. Def: False",
)
@click.option(
    "--relhum_thresh",
    default=98,
    type=float,
    help="Relative humidity threshold for clouds. Def: 98",
)
@click.option(
    "--add_rs",
    type=int,
    multiple=True,
    help="Add radiosounding for specified leadtime. Def: None",
)
@click.option("--alt_bot", type=int, help="Altitude bottom. Def: surface.")
@click.option("--alt_top", default=2000, type=int, help="Altitude top. Def: 2000")
@click.option(
    "--appendix", type=str, help="String to append to output filename. Def: None"
)
@click.option(
    "--datatypes",
    type=click.Choice(
        [
            "eps",
            "jpeg",
            "jpg",
            "pdf",
            "pgf",
            "png",
            "ps",
            "raw",
            "rgba",
            "svg",
            "svgz",
            "tif",
            "tiff",
        ],
        case_sensitive=True,
    ),
    multiple=True,
    default=[
        "png",
    ],
    help="Choose data type(s) of final result. Def: png",
)
@click.option("--ind", type=int, help="Index of location (known from previous runs).")
@click.option(
    "--grid",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
@click.option(
    "--leadtime",
    type=int,
    multiple=True,
    default=(0,),
    help="Leadtime(s) to be shown in one plot. Def: 0.",
)
@click.option("--lat", type=float, help="Latitude of location.")
@click.option("--lon", type=float, help="Longitude of location.")
@click.option("--loc", type=str, help="Name of location.")
@click.option("--model", default="icon-1", type=str, help="NWP model name. Def: icon-1")
@click.option(
    "--outpath",
    type=str,
    help="Path to folder where the plots should be saved. Def: /scratch/USER/tmp",
)
@click.option(
    "--show_grid",
    is_flag=True,
    help="Show grid on plot. Flag, def: False",
)
@click.option(
    "--show_marker",
    is_flag=True,
    help="Add markers (o). Flag, def: False",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Output details on what is happening.",
)
@click.option(
    "--xmin",
    type=float,
    multiple=True,
    help="Minimum value of xaxis. Def: Fits values.",
)
@click.option(
    "--xmax",
    type=float,
    multiple=True,
    help="Maximum value of xaxis. Def: Fits values.",
)
@click.option(
    "--xrange_fix",
    is_flag=True,
    help="Use fix xrange from variable dataframe. Overwrites specified xmin and xmax. Flag, def: False",
)
@click.option(
    "--single_xaxis",
    is_flag=True,
    help="Plot two variables w/ the same unit only on one x-axis, not two. Flag, def: False",
)
@click.option(
    "--zeroline",
    is_flag=True,
    help="Show grid on plot. Flag, def: False",
)
def main(
    *,
    date: str,
    folder: str,
    var: str,
    add_clouds: bool,
    relhum_thresh: float,
    add_rs: int,
    alt_bot: int,
    alt_top: int,
    appendix: str,
    datatypes: tuple,
    grid: str,
    ind: int,
    leadtime: int,
    lat: float,
    lon: float,
    loc: str,
    model: str,
    outpath: str,
    show_grid: bool,
    show_marker: bool,
    zeroline: bool,
    verbose: bool,
    xmin: tuple,
    xmax: tuple,
    xrange_fix: bool,
    single_xaxis: bool,
):
    """Plot vertical profiles of variables from ICON simulation.

    If 1, 3, or more variables are specified, each will be plotted individually.
    If 2 variables are given, they will be shown in the same figure.

    Example command:
    plot_icon_profiles --date 21111812 --outpath plots --folder /scratch/swester/output_icon/ICON-1/ --var temp --leadtime 11 --leadtime 12 --loc pay

    Model output is expected to be in netcdf-format in a sub-folder named after the given date.

    """
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

    # A) retrieve data from ICON forecasts
    ######################################
    data_dict = get_icon(
        folder=folder,
        date=date,
        leadtime=leadtime,
        lat=lat,
        lon=lon,
        ind=ind,
        grid=grid,
        variables_list=var,
        alt_bot=alt_bot,
        alt_top=alt_top,
        verbose=verbose,
    )

    # B) retrieve observational data
    ################################
    if add_rs or add_clouds:
        if verbose:
            print("Retrieving radiosounding from DWH.")

        # list of timestamps for which radiosounding is retrieved
        rs_timestamps = [validtime_from_leadtime(date, lt) for lt in add_rs]

        # create obs_dict (like data_dict)
        obs_dict = {"rs": {tt: None for tt in rs_timestamps}}

        # determine variables which should be retrieved
        if var[0] in ["temp", "dewp_temp", "wind_dir", "wind_vel"] and add_clouds:
            rs_var = (var[0], "rel_hum")
        elif var[0] == "rel_hum" or add_clouds:
            rs_var = ("rel_hum",)
        elif var[0] in ["temp", "dewp_temp", "wind_dir", "wind_vel"]:
            rs_var = (var[0],)
        else:
            print(f"--add_rs specified but no matching 1st variable: {var[0]}")
            sys.exit(1)

        # loop over timestamps and fill data_dict
        for timestamp in rs_timestamps:
            unsliced_timestamp_df = dwh_retrieve(
                device="rs",
                station="pay",
                vars=rs_var,
                timestamps=timestamp.strftime("%Y%m%d%H"),
                verbose=verbose,
            )
            crit = slice_top_bottom(
                df_height=unsliced_timestamp_df["altitude"],
                alt_top=alt_top,
                alt_bot=alt_bot,
                verbose=verbose,
            )
            sliced_timestamp_df = unsliced_timestamp_df[crit]
            obs_dict["rs"][timestamp] = sliced_timestamp_df
    else:
        obs_dict = None

    # C) create plot
    ################
    create_plot(
        variables_list=var,
        data_dict=data_dict,
        obs_dict=obs_dict,
        outpath=outpath,
        date=date,
        add_clouds=add_clouds,
        relhum_thresh=relhum_thresh,
        alt_bot=alt_bot,
        alt_top=alt_top,
        loc=loc,
        model=model,
        appendix=appendix,
        xmin=xmin,
        xmax=xmax,
        xrange_fix=xrange_fix,
        datatypes=datatypes,
        verbose=verbose,
        show_grid=show_grid,
        show_marker=show_marker,
        zeroline=zeroline,
        single_xaxis=single_xaxis,
    )

    print("--- done")
