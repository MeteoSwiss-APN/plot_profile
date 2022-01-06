"""Purpose: Plot time-height-crosssection of MWR observational data.

Author: Michel Zeller

Date: 05/01/2022.
"""

# Standard library
import sys

# Third-party
import click

# Local
from .dwh_retrieve import dwh_retrieve
from .plot_mwr import mwr_heatmap
from .stations import sdf

# import ipdb


@click.command()
# mandatory click options
@click.option(
    "--start",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Start timestamp: yymmddHHMM",
)
@click.option(
    "--end",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: End timestamp: yymmddHHMM",
)
@click.option(
    "--var",
    type=click.Choice(
        [
            "temp",
        ],
        case_sensitive=True,
    ),
    multiple=True,
    help="MANDATORY: Variable name(s).",
)
# optional options
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
    multiple=False,
    default=["png"],
    help="Choose data type(s) of final result. Def: png",
)
@click.option("--loc", default="pay", type=str, help="Name of location. Def: pay")
@click.option(
    "--min", type=float, help="Lower limit for colorbar/variable. No default."
)
@click.option(
    "--max", type=float, help="Upper limit for colorbar/variable. No default."
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
def main(
    *,
    start: str,
    end: str,
    var: str,
    alt_bot: int,
    alt_top: int,
    appendix: str,
    datatypes: tuple,
    loc: str,
    min: float,
    max: float,
    outpath: str,
    verbose: bool,
):
    """Plot heatmap of variables retrieved from microwave radiometer.

    Currently, only temperature is supported.

    Example command:
    plot_mwr_heatmap --start 21111812 --end 21111912 --var temp --alt_top 2000

    """
    # check whether station exists
    try:
        station = sdf[loc]
        if verbose:
            print(f"Retrieving MWR data for {station.long_name}.")
    except KeyError:
        print("! {loc} is not listed as an available station.")
        sys.exit(1)

    # retrieve obs from DWH
    mwr_data = dwh_retrieve(
        device="mwr", station=loc, vars=var, timestamps=[start, end], verbose=verbose
    )

    mwr_heatmap(
        mwr_data=mwr_data, datatypes=datatypes, outpath=outpath, station=station
    )

    print("--- done")
