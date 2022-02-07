"""Purpose: Plot time-height-crosssection of MWR observational data.

Author: Michel Zeller

Date: 21/01/2022.
"""
# Third-party
import click

# Local
from .get_timeseries import get_data_dict
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
        ["5cm", "2m", "2m_tower", "10m_tower", "30m_tower", "icon"],
        case_sensitive=True,
    ),
    multiple=True,
    default=[
        "2m",
    ],
    help="MANDATORY: Choose type of device. Def: 2m",
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
    "--grid",
    is_flag=True,
    default=False,
    help="Add grid to plot.",
)
@click.option(
    "--init",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Init timestamp of model simulation: yymmddHH",
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
    grid: bool,
    init: str,
    outpath: str,
    verbose: bool,
):
    """Plot timeseries of variables retrieved from various differend measurement devices.

    Example commands:
    plot_timeseries --start 21111900 --end 21111902 --loc gla --device 5cm --device 2m --var temp
    plot_timeseries --outpath plots --start 21111900 --end 21111902 --loc pay --device 5cm --device 2m --device 2m_tower --device 10m_tower --device 30m_tower --var temp
    """
    data_dict, multi_axes = get_data_dict(
        start=start,
        end=end,
        variable=var,
        loc=loc,
        device=device,
        init=init,
        verbose=verbose,
    )

    create_plot(
        ymin=ymin,
        ymax=ymax,
        multi_axes=multi_axes,
        data=data_dict,
        devices=list(set(device)),  # from the device-list, extract all unique devices
        start=start,
        end=end,
        datatypes=datatypes,
        outpath=outpath,
        appendix=appendix,
        verbose=verbose,
        grid=grid,
        var=list(set(var)),  # form the var-list, extract all unique variables
        loc=loc,
    )

    print("--- done")
