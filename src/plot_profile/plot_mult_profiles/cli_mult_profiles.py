"""Purpose: define command line inputs for plot_mult_profiles.

Author: Arthur Dandoy

Date: 03/05/2022.
"""
# Standard library
from datetime import timedelta

# Third-party
import click

# First-party
from plot_profile.plot_mult_profiles.get_mult_profiles import get_mult_data
from plot_profile.plot_mult_profiles.plot_mult_profiles import create_mult_plot
from plot_profile.plot_profiles.get_profiles import parse_inputs


@click.command()
# options without default value (mandatory to specify by user)
@click.option(
    "--date_ref",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Reference date from which leadtimes are determined. (ex: 21111812)",
)

# ADD MODELS AND OBSERVATIONS TO PLOT W/: add_model, model_src, add_obs
@click.option(
    "--add_model",
    type=(str, str, str),
    multiple=True,
    help="Specify which model/variable/model_id should be added to plot.",
)
@click.option(
    "--model_src",
    type=(str, click.Path(exists=True), click.DateTime(formats=["%y%m%d%H"])),
    multiple=True,
    help="Specify for each model ID, one source flag. I.e. <model_id> <folder> <init>",
)
@click.option(
    "--add_obs",
    type=(str, str),
    multiple=True,
    help="Specify which device/variable should be added to plot.",
)
@click.option(
    "--leadtime",
    type=int,
    multiple=True,
    default=(0,),
    help="Leadtime(s) to be shown in one plot. Def: 0.",
)

# options with default value
@click.option(
    "--grid_file",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
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
@click.option("--ymin", type=int, help="Altitude bottom. Def: surface.")
@click.option("--ymax", default=2000, type=int, help="Altitude top. Def: 2000")
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
@click.option("--lat", type=float, help="Latitude of location.")
@click.option("--lon", type=float, help="Longitude of location.")
@click.option("--loc", type=str, help="Name of location.")
@click.option(
    "--outpath",
    type=str,
    help="Path to folder where the plots should be saved. Def: /scratch/USER/tmp",
)
@click.option(
    "--grid",
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
    date_ref: click.DateTime,
    add_model: tuple,
    add_obs: tuple,
    model_src: tuple,
    leadtime: tuple,
    grid_file: str,
    add_clouds: bool,
    relhum_thresh: float,
    ymin: int,
    ymax: int,
    appendix: str,
    datatypes: tuple,
    ind: int,
    lat: float,
    lon: float,
    loc: str,
    outpath: str,
    grid: bool,
    show_marker: bool,
    zeroline: bool,
    verbose: bool,
    xmin: tuple,
    xmax: tuple,
    xrange_fix: bool,
    single_xaxis: bool,
):
    """Plot vertical profiles of variables from icon, arome simulations or observations.

    If 1, 3, or more variables are specified, each will be plotted individually.
    If 2 variables are given, they will be shown in the same figure.

    Example command:
    plot_mult_profiles --loc pay --add_model arome temp aro --add_model icon temp ico --add_obs rs temp --leadtime 12 --leadtime 15
      --model_src aro /scratch/adandoy/AROME/ 21111812 --model_src ico /scratch/swester/output_icon/ICON-1/ 21111812

    Model output is expected to be in netcdf-format in a sub-folder named after the given date.

    """
    elements, multi_axes = parse_inputs(loc, add_model, add_obs, model_src, verbose)

    if verbose and multi_axes:
        print("Employing two different axes: Bottom and Top.")

    # dates_lt = [date_ref + timedelta(hours = i) for i in leadtime]

    data_dict = get_mult_data(
        date_ref=date_ref,
        leadtimes=leadtime,
        loc=loc,
        grid=grid_file,
        ylims=(ymin, ymax),
        elements=elements,
        verbose=verbose,
    )

    create_mult_plot(
        data_dict=data_dict,
        date_ref=date_ref,
        multi_axes=multi_axes,
        location=loc,
        xlims=(xmin, xmax),
        ylims=(ymin, ymax),
        grid=grid,
        show_marker=show_marker,
        datatypes=datatypes,
        outpath=outpath,
        appendix=appendix,
        verbose=verbose,
    )

    print("--- done")
