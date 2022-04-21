"""Purpose: Plot time-height-crosssection of ICON simulation.

Author: Michel Zeller

Date: 08/12/2021.
"""

# Standard library
from datetime import timedelta

# Third-party
import click

# Local
from ..utils.dwh_retrieve import dwh_retrieve
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
    multiple=True,
    help="MANDATORY: Variable name(s).",
)
@click.option(
    "--var_min", type=float, help="Lower Limit for Colorbar/Variable. No default."
)
@click.option(
    "--var_max", type=float, help="Upper Limit for Colorbar/Variable. No default."
)

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
    "--verbose",
    is_flag=True,
    default=False,
    help="Output details on what is happening.",
)
@click.option(
    "--add_cbh",
    is_flag=True,
    default=False,
    help="Add cloud base height & vertical visibility scatter plots to heat map.",
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
    verbose: bool,
    var_min: float,
    var_max: float,
    add_cbh: bool,
):
    """Plot heatmap (time-height crosssection) of variable from ICON simulation.

    Example command:
    plot_icon_heatmap --date 21111812 --folder /scratch/swester/output_icon/ICON-1/ --var temp --alt_top 2000 --start_leadtime 0 --end_leadtime 12

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

    if add_cbh:
        t1 = date + timedelta(hours=start_leadtime)
        t2 = date + timedelta(hours=end_leadtime)
        surface_data = dwh_retrieve(
            device="2m",  # hardcoded
            station=loc,  # "pay",
            vars=("cbh", "ver_vis"),
            timestamps=[t1, t2],
            verbose=verbose,
        )
        # if the retrieved dataframe for the cloud base height is empty because no data for the given
        # timeframe or location exists; assign None to surface_data
        if surface_data.empty:
            surface_data = None
    else:
        surface_data = None

    if True:
        create_heatmap(
            variables_list=var,
            data_dict=data_dict,
            outpath=outpath,
            date=date,
            loc=loc,
            model=model,
            appendix=appendix,
            datatypes=datatypes,
            leadtime=leadtimes,
            verbose=verbose,
            var_min=var_min,
            var_max=var_max,
            surface_data=surface_data,
        )

    print("--- done")
