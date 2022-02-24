"""Purpose: Plot time-height-crosssection of MWR observational data.

Author: Michel Zeller

Date: 21/01/2022.
"""

# Standard library
import sys
from pprint import pprint

# Third-party
import click

# First-party
from plot_profile.plot_timeseries.get_timeseries import get_timeseries_dict
from plot_profile.plot_timeseries.parse_timeseries_inputs import parse_inputs
from plot_profile.plot_timeseries.plot_timeseries import create_plot

# from ipdb import set_trace


@click.command()
# mandatory click options
@click.option(
    "--start",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Start timestamp: yymmddHH",
)
@click.option(
    "--end",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: End timestamp: yymmddHH",
)
@click.option(
    "--var",
    type=str,
    multiple=True,  # TODO: implement later, s.t. several variables with the same unit can be selected
    help="MANDATORY: Variable name.",
)
@click.option(
    "--loc", default="pay", type=str, help="MANDATORY: Name of location. Def: pay"
)
@click.option(
    "--device",
    type=click.Choice(
        [
            "5cm",
            "2m",
            "2m_tower",
            "10m_tower",
            "30m_tower",
        ],
        case_sensitive=True,
    ),
    multiple=True,
    help="MANDATORY: Choose type of device.",
)
# optional options
@click.option(
    "--ymin",
    type=float,
    multiple=True,
    help="Minimum value of y-axis/axes. Def: Fits values.",
)
@click.option(
    "--ymax",
    type=float,
    multiple=True,
    help="Maximum value of x-axis/axes. Def: Fits values.",
)
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
@click.option("--folder", type=str, help="Path to model simulations.", multiple=True)
@click.option(
    "--grid",
    is_flag=True,
    default=False,
    help="Add grid to plot.",
)
@click.option(
    "--grid_file",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
@click.option(
    "--init",
    type=click.DateTime(formats=["%y%m%d%H"]),
    multiple=True,
    help="Init timestamp of model simulation: yymmddHH",
)
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
    "--add_model",
    type=(str, str, int, str),
    multiple=True,
    help="Specify which model/variable/level should be added to plot. If no level should be retrieved, enter 0.",
)
@click.option(
    "--add_obs",
    type=(str, str),
    multiple=True,
    help="Specify which device/variable should be added to plot.",
)
def main(
    *,
    # Mandatory
    start: str,
    end: str,
    loc: str,
    # Models, Devices and Variables
    var: str,
    device: str,
    add_model: tuple,
    add_obs: tuple,
    # Mandatory for ICON
    grid_file: str,
    init: str,
    folder: str,
    # Optional
    ymin: tuple,
    ymax: tuple,
    appendix: str,
    grid: bool,
    datatypes: tuple,
    outpath: str,
    verbose: bool,
):
    """Plot timeseries of variables retrieved from various differend measurement devices.

    Example commands:
    plot_timeseries --start 21111900 --end 21111902 --loc gla --device 5cm --device 2m --var temp
    plot_timeseries --outpath plots --start 21111900 --end 21111902 --loc pay --device 5cm --device 2m --device 2m_tower --device 10m_tower --device 30m_tower --var temp
    # incl ICON
    plot_timeseries --start 21111900 --end 21111912 --loc pay --folder /scratch/swester/output_icon/ICON-1/ --init 21111812 --outpath plots --add_obs 2m temp --add_obs 10m_tower temp --add_obs 2m rad_sw_down --add_obs 2m rad_sw_up --add_model icon temp 1 --add_model icon temp 2

    # incl several different ICON instances:
    plot_timeseries --outpath plots --loc pay --start 21111900 --end 21111906 --add_model icon temp 1 ref --folder /scratch/swester/output_icon/ICON-1/  --init 21111812

    plot_timeseries --outpath plots --loc pay --start 21111900 --end 21111906 --add_model icon temp 1 ref --add_model icon temp 10 exp --add_model icon temp 2 ref --add_model icon temp 20 exp --folder /scratch/swester/output_icon/ICON-1/  --folder /scratch/swester/output_icon/ICON-1/ --folder /scratch/swester/output_icon/exp1/ --folder /scratch/swester/output_icon/exp1/ --init 21111812

    """
    elements, multi_axes = parse_inputs(
        loc, var, device, add_model, add_obs, folder, init, verbose
    )

    timeseries_dict = get_timeseries_dict(
        start=start,
        end=end,
        elements=elements,
        loc=loc,
        grid_file=grid_file,
        verbose=verbose,
    )

    # pprint(timeseries_dict)
    # sys.exit(1)

    create_plot(
        data=timeseries_dict,
        multi_axes=multi_axes,
        location=loc,
        start=start,
        end=end,
        ymin=ymin,
        ymax=ymax,
        grid=grid,
        datatypes=datatypes,
        outpath=outpath,
        appendix=appendix,
        verbose=verbose,
    )

    print("--- done")
