"""Purpose: define command line inputs.

Author: Stephanie Westerhuis

Date: 10/11/2021.
"""
# Standard library
from typing import NamedTuple

# Third-party
import click

# Local
from .get_icon import *
from .plot_data import *


@click.command()
@click.option("--folder", type=str, help="path to folder with icon output")
@click.option(
    "--leadtime", type=int, multiple=True, default=(0,), help="simulation lead time"
)
@click.option("--lat", type=float, help="latitude of location")
@click.option("--lon", type=float, help="longitude of location")
@click.option("--ind", type=int, default=-1, help="index of location")
@click.option(
    "--grid",
    type=str,
    default="/store/mch/msopr/tsm/fieldextra/static/share/grid_descriptions/ICON-1E_DOM01_R19B08.nc",
    help="icon file with HEIGHT field",
)
@click.option("--alt_bot", default=0, type=int, help="altitude bottom:  int")
@click.option("--alt_top", default=2000, type=int, help="altitude top value: int")
@click.option(
    "--var",
    type=click.Choice(
        [
            "T",
            "QC",
            "QV",
        ],
        case_sensitive=True,
    ),
    multiple=False,
    default=("T"),
    help="variable name",
)
@click.option(
    "--outpath",
    default="tmp/",
    type=str,
    help="path to folder where the plots should be saved - def: plots/",
)
@click.option(
    "--show_grid",
    is_flag=True,
    help="Show grid on plot - def: False",
)
@click.option(
    "--print_steps",
    is_flag=True,
    help="Add this flag to display intermediate steps.",
)
@click.option(
    "--standard_settings",
    is_flag=True,
    help="temp_range: -100-30 [°C], windvel_range: 0-50 [km/h]",
)
@click.option(
    "--personal_settings",
    is_flag=True,
    help="If this flag is added, personal 'standard' settings can be defined using the temp_min/max and windvel_min/max flags",
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
    folder: str,
    leadtime: int,
    lat: float,
    lon: float,
    ind: int,
    grid: str,
    alt_bot: int,
    alt_top: int,
    var: str,
    outpath: str,
    show_grid: bool,
    print_steps: bool,
    standard_settings: bool,
    personal_settings: bool,
    temp_min: float,
    temp_max: float,
    windvel_min: float,
    windvel_max: float,
) -> None:

    df = get_icon(
        folder=folder,
        leadtime=leadtime,
        lat=lat,
        lon=lon,
        ind=ind,
        grid=grid,
        var=var,
        alt_bot=alt_bot,
        alt_top=alt_top,
    )
    # df, station_name, relevant_params = get_data(
    #    date=date,
    #    params=params,
    #    station_id=station_id,
    #    print_steps=print_steps,
    #    alt_bot=alt_bot,
    #    alt_top=alt_top,
    # )

    # create_plot(
    #    df=df,
    #    relhum_thresh=relhum_thresh,
    #    grid=grid,
    #    clouds=clouds,
    #    outpath=outpath,
    #    station_name=station_name,
    #    date=date,
    #    alt_top=alt_top,
    #    alt_bot=alt_bot,
    #    params=relevant_params,
    #    print_steps=print_steps,
    #    standard_settings=standard_settings,
    #    personal_settings=personal_settings,
    #    temp_min=temp_min,
    #    temp_max=temp_max,
    #    windvel_min=windvel_min,
    #    windvel_max=windvel_max,
    # )

    print("--- Done.")
