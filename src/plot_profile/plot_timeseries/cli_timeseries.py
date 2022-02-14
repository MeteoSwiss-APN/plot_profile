"""Purpose: Plot time-height-crosssection of MWR observational data.

Author: Michel Zeller

Date: 21/01/2022.
"""
# Standard library
from pprint import pprint

# Third-party
import click

# Local
from .get_timeseries import get_timeseries_dict
from .plot_timeseries import create_plot


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
@click.option("--folder", type=str, help="Path to ICON simulations.")
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
    type=(str, str, int),
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
    var: str,
    loc: str,
    device: str,
    # Optional
    ymin: tuple,
    ymax: tuple,
    appendix: str,
    datatypes: tuple,
    folder: str,
    grid: bool,
    grid_file: str,
    init: str,
    outpath: str,
    verbose: bool,
    add_model: tuple,
    add_obs: tuple,
):
    """Plot timeseries of variables retrieved from various differend measurement devices.

    Example commands:
    plot_timeseries --start 21111900 --end 21111902 --loc gla --device 5cm --device 2m --var temp
    plot_timeseries --outpath plots --start 21111900 --end 21111902 --loc pay --device 5cm --device 2m --device 2m_tower --device 10m_tower --device 30m_tower --var temp
    # incl ICON
    plot_timeseries --start 21111900 --end 21111912 --loc pay --folder /scratch/swester/output_icon/ICON-1/ --init 21111812 --outpath plots --add_obs 2m temp --add_obs 10m_tower temp --add_obs 2m rad_sw_down --add_obs 2m rad_sw_up --add_model icon temp 1 --add_model icon temp 2
    """
    # add is a tuple of tuples; which gets converted to a list of lists with the following
    # the following line. afterwards two lists w/ all unique devices and variables are created
    elements = None
    add = list(add_obs) + list(add_model)
    if add_model or add_obs:
        elements = [
            list(item) for item in list(add)
        ]  # convert tuple of tuples to list of lists
        devs = list([list[0] for list in add])  # list(set([list[0] for list in add]))
        vars = list([list[1] for list in add])  # list(set([list[1] for list in add]))

    # if plots for only one device w/ a number of different vars should be created,
    # using the --var and --device flags could me more user friendly
    if device and var:
        devs = list(device)
        vars = list(var)

    timeseries_dict, multi_axes = get_timeseries_dict(
        start=start,
        end=end,
        elements=elements,  # all elements of the plot are in the add-list
        variable=vars,
        loc=loc,
        device=devs,
        init=init,
        folder=folder,
        grid_file=grid_file,
        verbose=verbose,
    )

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
