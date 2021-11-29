"""Purpose: define command line inputs.

Author: Stephanie Westerhuis

Date: 10/11/2021.
"""
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
@click.option("--alt_bot", default=0, type=int, help="altitude bottom:  int")
@click.option("--alt_top", default=2000, type=int, help="altitude top value: int")
@click.option(
    "--date",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="init date of icon simulation: YYMMDDHH",
)
@click.option("--folder", type=str, help="path to folder with icon output")
@click.option("--ind", type=int, default=-1, help="index of location")
@click.option(
    "--grid",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="icon file containing HEIGHT field",
)
@click.option("--lat", default=46.81281, type=float, help="latitude of location")
@click.option("--lon", default=6.94363, type=float, help="longitude of location")
@click.option(
    "--leadtime", type=int, multiple=True, default=(0,), help="simulation lead time"
)
@click.option("--loc", default="pay", type=str, help="location name")
@click.option("--model", default="icon-1", type=str, help="nwp model name")
@click.option(
    "--outpath",
    default="/scratch/swester/tmp",
    type=str,
    help="path to folder where the plots should be saved - def: /scratch/user/tmp",
)
@click.option(
    "--personal_settings",
    is_flag=True,
    help="If this flag is added, personal 'standard' settings can be defined using the temp_min/max and windvel_min/max flags",
)
@click.option(
    "--print_steps",
    is_flag=True,
    help="Add this flag to display intermediate steps.",
)
@click.option(
    "--show_grid",
    is_flag=True,
    help="Show grid on plot - def: False",
)
@click.option(
    "--standard_settings",
    is_flag=True,
    help="temp_range: -100-30 [°C], windvel_range: 0-50 [km/h]",
)
@click.option(
    "--temp_min",
    type=float,
    help="Define the minimum temperature. Disclaimer: Add --personal_settings flag!",
)
@click.option(
    "--temp_max",
    type=float,
    help="Define the maximum temperature. Disclaimer: Add --personal_settings flag!",
)
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
    default=("temp"),
    help="variable name",
)
@click.option(
    "--windvel_min",
    type=float,
    help="Define the minimum windvelocity. Disclaimer: Add --personal_settings flag!",
)
@click.option(
    "--windvel_max",
    type=float,
    help="Define the maximum windvelocity. Disclaimer: Add --personal_settings flag!",
)
def main(
    *,
    alt_bot: int,
    alt_top: int,
    date: str,
    folder: str,
    grid: str,
    ind: int,
    leadtime: int,
    lat: float,
    lon: float,
    loc: str,
    model: str,
    outpath: str,
    personal_settings: bool,
    print_steps: bool,
    standard_settings: bool,
    show_grid: bool,
    temp_min: float,
    temp_max: float,
    var: str,
    windvel_min: float,
    windvel_max: float,
) -> None:

    # height, values = get_icon(
    #    folder=folder,
    #    date=date,
    #    leadtime=leadtime,
    #    lat=lat,
    #    lon=lon,
    #    ind=ind,
    #    grid=grid,
    #    var_shortname=var,
    #    alt_bot=alt_bot,
    #    alt_top=alt_top,
    # )

    #
    #    # for faster debugging of plotting function
    #    f = open('/scratch/swester/tmp/height.pckl', 'wb')
    #    pickle.dump(height, f)
    #    f.close()
    #    f = open('/scratch/swester/tmp/values.pckl', 'wb')
    #    pickle.dump(values, f)
    #    f.close()
    f1 = open("/scratch/swester/tmp/height.pckl", "rb")
    height = pickle.load(f1)
    f1.close()
    f2 = open("/scratch/swester/tmp/values.pckl", "rb")
    values = pickle.load(f2)
    f2.close()

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
    )

    print("--- Done.")
