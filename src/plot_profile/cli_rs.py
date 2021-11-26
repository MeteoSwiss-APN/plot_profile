"""Purpose: define command line inputs.

Author: Michel Zeller

Date: 05/10/2021.
"""
# Standard library
from typing import NamedTuple

# Third-party
import click

# Local
from .get_data import get_data
from .plot_data import create_plot


@click.command()
@click.option("--station_id", default="06610", help="station ID: XXXXX - def: 06610")
@click.option(
    "--date", default="2021083100", help="start date: YYYYMMDDHH - def: 2021083100"
)
@click.option(
    "--alt_bot",
    default=0,
    type=int,
    help="altitude bottom value: int - def: elevation of radiosounding station",
)
@click.option(
    "--alt_top",
    default=40000,
    type=int,
    help="altitude top value: int - def: 10% over max altitude of radiosounding retrieval",
)
@click.option(
    "--params",
    type=click.Choice(
        [
            "743",
            "winddir",
            "745",
            "temp",
            "747",
            "dewp",
            "748",
            "windvel",
        ],
        case_sensitive=False,
    ),
    multiple=True,
    default=("743", "745", "748", "747"),
    help="Default: all",
)
@click.option(
    "--outpath",
    default="plots/",
    type=str,
    help="path to folder where the plots should be saved - def: plots/",
)
@click.option(
    "--grid",
    is_flag=True,
    help="Show grid on plot - def: False",
)
@click.option(
    "--clouds",
    is_flag=True,
    # default=True,
    help="Show clouds on plot - def: True",
)
@click.option(
    "--relhum_thresh",
    default=80,
    type=float,
    help="Define the relative humidity threshold for clouds - def: 80",
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
    station_id: str,
    date: str,
    params: tuple,
    alt_bot: int,
    alt_top: int,
    outpath: str,
    grid: bool,
    clouds: bool,
    relhum_thresh: float,
    print_steps: bool,
    standard_settings: bool,
    personal_settings: bool,
    temp_min: float,
    temp_max: float,
    windvel_min: float,
    windvel_max: float,
) -> None:

    df, station_name, relevant_params = get_data(
        date=date,
        params=params,
        station_id=station_id,
        print_steps=print_steps,
        alt_bot=alt_bot,
        alt_top=alt_top,
    )

    if False:
        create_plot(
            df=df,
            relhum_thresh=relhum_thresh,
            grid=grid,
            clouds=clouds,
            outpath=outpath,
            station_name=station_name,
            date=date,
            alt_top=alt_top,
            alt_bot=alt_bot,
            params=relevant_params,
            print_steps=print_steps,
            standard_settings=standard_settings,
            personal_settings=personal_settings,
            temp_min=temp_min,
            temp_max=temp_max,
            windvel_min=windvel_min,
            windvel_max=windvel_max,
        )

    print("--- Done.")
