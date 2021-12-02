"""Purpose: define command line inputs.

Author: Stephanie Westerhuis

Date: 10/11/2021.
"""
# test
# Standard library
# import ipdb
import pickle
from typing import NamedTuple

# Third-party
import click

# Local
from .get_icon import get_icon
from .plot_icon import create_plot


@click.command()
# options without default value
@click.option(
    "--date",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="init date of icon simulation: YYMMDDHH",
)
@click.option("--folder", type=str, help="path to folder with icon output")
@click.option(
    "--var",
    type=click.Choice(
        [
            "temp",
            "qc",
            "qv",
        ],
        case_sensitive=True,
    ),
    multiple=False,
    help="variable name",
)
# options with default value
@click.option("--alt_bot", default=490, type=int, help="altitude bottom:  int")
@click.option("--alt_top", default=2000, type=int, help="altitude top value: int")
@click.option("--appendix", type=str, help="append to output filename")
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
        case_sensitive=False,
    ),
    multiple=True,
    default=["png"],
    help="Choose data type(s) of final result. Default: png",
)
@click.option("--ind", type=int, default=-1, help="index of location")
@click.option(
    "--grid",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="icon file containing HEIGHT field",
)
@click.option(
    "--leadtime", type=int, multiple=True, default=(0,), help="simulation lead time"
)
@click.option("--lat", default=46.81281, type=float, help="latitude of location")
@click.option("--lon", default=6.94363, type=float, help="longitude of location")
@click.option("--loc", default="pay", type=str, help="location name")
@click.option("--model", default="icon-1", type=str, help="nwp model name")
@click.option(
    "--outpath",
    type=str,
    help="path to folder where the plots should be saved - def: None",
)
@click.option(
    "--show_grid",
    is_flag=True,
    help="Show grid on plot - def: False",
)
@click.option("--xmin", type=float, help="Minimum value of xaxis")
@click.option("--xmax", type=float, help="Maximum value of xaxis")
def main(
    *,
    date: str,
    folder: str,
    var: str,
    alt_bot: int,
    alt_top: int,
    appendix: str,
    grid: str,
    ind: int,
    leadtime: int,
    lat: float,
    lon: float,
    loc: str,
    model: str,
    outpath: str,
    show_grid: bool,
    xmin: float,
    xmax: float,
    datatypes: tuple,
) -> None:

    if True:
        height, values = get_icon(
            folder=folder,
            date=date,
            leadtime=leadtime,
            lat=lat,
            lon=lon,
            ind=ind,
            grid=grid,
            var_shortname=var,
            alt_bot=alt_bot,
            alt_top=alt_top,
        )

        ## for faster debugging of plotting function
        # f = open('/scratch/swester/tmp/height.pckl', 'wb')
        # pickle.dump(height, f)
        # f.close()
        # f = open('/scratch/swester/tmp/values.pckl', 'wb')
        # pickle.dump(values, f)
        # f.close()
        # f1 = open("/scratch/swester/tmp/height.pckl", "rb")
        # height = pickle.load(f1)
        # f1.close()
        # f2 = open("/scratch/swester/tmp/values.pckl", "rb")
        # values = pickle.load(f2)
        # f2.close()

        create_plot(
            var_shortname=var,
            df_height=height,
            df_values=values,
            outpath=outpath,
            date=date,
            alt_bot=alt_bot,
            alt_top=alt_top,
            loc=loc,
            model=model,
            appendix=appendix,
            xmin=xmin,
            xmax=xmax,
            datatypes=datatypes,
        )

    print("--- Done.")
