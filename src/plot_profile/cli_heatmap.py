"""Purpose: Plot time-height-crosssection of ICON simulation.

Author: Michel Zeller

Date: 08/12/2021.
"""

# Third-party
import click

# Local
from .get_icon import get_icon
from .plot_icon import create_heatmap

# import ipdb


@click.command()
# options without default value (mandatory to specify by user)
@click.option(
    "--date",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Init date of icon simulation: YYMMDDHH.",
)
@click.option("--folder", type=str, help="MANDATORY: Path to folder with icon output.")
@click.option(
    "--var",
    type=click.Choice(
        ["temp", "qc", "qv", "clc", "ddt_t_rad_lw", "ddt_t_rad_sw"],
        case_sensitive=True,
    ),
    multiple=True,  # TODO: change to true later, s.t. several 'heatmaps' can be created at once!
    help="MANDATORY: Variable name(s).",
)  # for the
# options with default value
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
    default=["png"],
    help="Choose data type(s) of final result. Def: png",
)
@click.option("--ind", type=int, help="Index of location (known from previous runs).")
@click.option(
    "--grid",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
# ~~~~~~~~~NEW~~~~~~~~~ #
@click.option(
    "--start_leadtime",
    type=int,
    multiple=False,
    default=0,
    help="Leadtime(s) to be shown in one plot. Def: 0.",
)
@click.option(
    "--end_leadtime",
    type=int,
    multiple=False,
    default=10,
    help="Leadtime(s) to be shown in one plot. Def: 10.",
)
@click.option(
    "--step",
    type=int,
    default=1,
    help="Leadtime(s) to be shown in one plot. Def: 1.",
)

# ~~~~~~~~~NEW~~~~~~~~~ #
@click.option(
    "--lat", default=46.81281, type=float, help="Latitude of location. Def: 46.81 (PAY)"
)
@click.option(
    "--lon", default=6.94363, type=float, help="Longitude of location. Def: 6.94 (PAY)"
)
@click.option("--loc", default="pay", type=str, help="Name of location. Def: pay")
@click.option("--model", default="icon-1", type=str, help="NWP model name. Def: icon-1")
@click.option(
    "--outpath",
    type=str,
    help="Path to folder where the plots should be saved. Def: /scratch/USER/tmp",
)
@click.option(
    "--show_grid",
    is_flag=True,
    help="Show grid on plot. Def: False",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Output details on what is happening.",
)
@click.option("--xmin", type=float, help="Minimum value of xaxis. Def: Fits values.")
@click.option("--xmax", type=float, help="Maximum value of xaxis. Def: Fits values.")
@click.option(
    "--xrange_fix",
    is_flag=True,
    default=False,
    help="Use fix xrange from variable dataframe. Overwrites specified xmin and xmax.",
)
@click.option(
    "--zeroline",
    is_flag=True,
    help="Show zero line on plot. Def: False",
)
def main(
    *,
    date: str,
    folder: str,
    var: str,
    alt_bot: int,
    alt_top: int,
    appendix: str,
    datatypes: tuple,
    grid: str,
    ind: int,
    start_leadtime: int,
    end_leadtime: int,
    step: int,
    lat: float,
    lon: float,
    loc: str,
    model: str,
    outpath: str,
    show_grid: bool,
    zeroline: bool,
    verbose: bool,
    xmin: float,
    xmax: float,
    xrange_fix: bool,
):
    """Plot heatmap (time-height crosssection) of variable from ICON simulation.

    Example command:
    TODO

    """
    leadtimes = list(range(start_leadtime, end_leadtime + 1, step))
    data_dict = get_icon(
        folder=folder,
        date=date,
        leadtime=leadtimes,
        lat=lat,
        lon=lon,
        ind=ind,
        grid=grid,
        variables_list=var,
        alt_bot=alt_bot,
        alt_top=alt_top,
        verbose=verbose,
    )

    create_heatmap(
        variables_list=var,
        data_dict=data_dict,
        outpath=outpath,
        date=date,
        alt_bot=alt_bot,
        alt_top=alt_top,
        loc=loc,
        model=model,
        appendix=appendix,
        datatypes=datatypes,
        leadtime=leadtimes,
        verbose=verbose,
    )

    print("--- done")
