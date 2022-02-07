"""Purpose: Plot time-height-crosssection of MWR observational data.

Author: Stephanie Westerhuis

Date: 05/01/2022.
"""

# Standard library
import sys
from pprint import pprint as pp

# Third-party
import click
import pandas as pd

# Local
from ..utils.dwh_retrieve import dwh_retrieve
from ..utils.stations import sdf
from ..utils.utils import slice_top_bottom
from ..utils.variables import vdf
from .plot_mwr import mwr_heatmap


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
    help="MANDATORY: Variable name.",
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
    default="png",
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
    plot_mwr_heatmap --start 21111812 --end 21111912 --var temp --alt_top 2000 --outpath plots

    """
    # retrieve station dataframe
    try:
        station = sdf[loc]
        if verbose:
            print(f"Retrieving MWR data for {station.long_name}.")
    except KeyError:
        print(f"! {loc} is not listed as an available station.")
        sys.exit(1)

    # retrieve variable dataframe
    try:
        var_frame = vdf[var]
        if verbose:
            print(f"Selected variable: {var_frame.long_name}.")
    except KeyError:
        print(f"! {var} is not available as variable.")
        sys.exit(1)

    ## retrieve obs from DWH
    mwr_data = dwh_retrieve(
        device="mwr",
        station=loc,
        vars=var,
        timestamps=[start, end],
        verbose=verbose,
    )

    # slice top and bottom
    if not alt_bot:
        alt_bot = mwr_data.index.min()
    crit = slice_top_bottom(mwr_data.index, alt_top, alt_bot)
    # make same index
    crit.index = mwr_data.index
    mwr_data = mwr_data[crit]

    pp(mwr_data.head())
    mwr_data = mwr_data.subtract(273.15)  # K --> °C
    pp(mwr_data.head())

    mwr_heatmap(
        start=start,
        end=end,
        mwr_data=mwr_data,
        station=station,
        var=var_frame,
        min_value=min,
        max_value=max,
        appendix=appendix,
        datatypes=datatypes,
        outpath=outpath,
    )

    print("--- done")
