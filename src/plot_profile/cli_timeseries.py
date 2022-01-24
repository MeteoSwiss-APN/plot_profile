"""Purpose: Plot time-height-crosssection of MWR observational data.

Author: Michel Zeller

Date: 21/01/2022.
"""

# Third-party
import click

# Local
from .dwh_retrieve import dwh_retrieve
from .plot_timeseries import create_plot
from .utils import check_inputs


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
    # multiple=True, # TODO: implement later, s.t. several variables with the same unit can be selected
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
            # TODO: add all possible devices here
        ],
        case_sensitive=True,
    ),
    multiple=True,
    default=[
        "5cm",
    ],
    help="MANDATORY: Choose type of device. Def: 5cm",
)
# optional options
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
def main(
    *,
    # Mandatory
    start: str,
    end: str,
    var: str,
    loc: str,
    device: str,
    # Optional
    appendix: str,
    datatypes: tuple,
    outpath: str,
    verbose: bool,
    grid: bool,
):
    """Plot timeseries of variables retrieved from various differend measurement devices.

    Currently, only temperature is supported.

    Example command:
    plot_timeseries --start 21111900 --end 21111902 --loc gla --device 5cm --device 2m --var temp

    """
    check_inputs(var, loc, verbose)

    data_dict = {}
    for dev in device:
        data_dict[dev] = dwh_retrieve(
            device=dev,
            station=loc,
            vars=var,
            timestamps=[start, end],
            verbose=False,  # TODO: change False to verbose
        )

    create_plot(
        data=data_dict,
        devices=device,
        start=start,
        end=end,
        datatypes=datatypes,
        outpath=outpath,
        appendix=appendix,
        verbose=verbose,
        grid=grid,
        var=var,
        loc=loc,
    )

    print("--- done")
