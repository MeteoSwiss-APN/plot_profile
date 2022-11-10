"""Purpose: define command line inputs.

Author: Michel Zeller

Date: 05/10/2021.
"""
# Standard library
import sys

# Third-party
import click

# Local
from ..utils.stations import sdf
from .get_rs import get_rs
from .plot_rs import create_plot


@click.command()
@click.option("--loc", default="pay", help="Name station. Def: pay")
@click.option(
    "--date", default="202108310000", help="start date: YYYYMMDDHH00. Def: 2021083100"
)
@click.option(
    "--params",
    type=click.Choice(
        [
            "wind_dir",
            "temp",
            "dewp_temp",
            "wind_vel",
            "pot_temp",
        ],
        case_sensitive=False,
    ),
    multiple=True,
    default=("temp", "dewp_temp", "wind_vel", "wind_dir"),
    help="Def: all",
)
@click.option(
    "--outpath",
    type=str,
    help="Path to folder for plots. Def: /scratch/<user>/tmp/",
)
@click.option(
    "--print_steps",
    is_flag=True,
    help="Add this flag to display intermediate steps.",
)
# command line inputs for
@click.option(
    "--grid",
    is_flag=True,
    help="Show grid on plot. Def: False",
)
@click.option(
    "--clouds",
    is_flag=True,
    help="Show clouds on plot. Def: False",
)
@click.option(
    "--relhum_thresh",
    default=98,
    type=float,
    help="Relative humidity threshold for clouds. Def: 98",
)
# command line inputs for axes limit settings
@click.option(
    "--alt_bot",
    type=int,
    help="altitude bottom value: int",
)
@click.option(
    "--alt_top",
    default=5000,
    type=int,
    help="Altitude top value: int. Def: 5000",
)
@click.option(
    "--standard_settings",
    is_flag=True,
    help="Flag: temp_range: -100-30 [°C], windvel_range: 0-50 [km/h]",
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
@click.option(
    "--pot_temp_min",
    type=float,
    help="Define the minimum potential temperature. Disclaimer: Add --personal_settings flag!",
)
@click.option(
    "--pot_temp_max",
    type=float,
    help="Define the maximum potential temperature. Disclaimer: Add --personal_settings flag!",
)

def main(
    *,
    loc: str,
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
    pot_temp_min: float,
    pot_temp_max: float,
) -> None:
    """Plot vertical profiles of balloon radiosounding data.

    Available variables are: wind_vel/wind_dir/temp/dewp_temp.

    If (wind_dir or wind_vel) AND (temp or dewp_temp) are plottet, two plots side by side will be created.
    Otherwise one plot containing up to two variables.

    Personal axis limits can be specified by using the '--personal_settings' flag in conjunction with the
    axis limits one wants to define.

    Standard (pre-defined) axis limits can be used by applying the '--standard_settings' flag. Check out
    the standard settings by executing: plot_rs --help

    Otherwise the axes limits will be fitted to the data.

    Example command:
    plot_rs --date 2021111912 --params temp --params dewp_temp --alt_top 2500
    plot_rs --date 2022011112 --params temp --clouds --relhum_thresh 95 --grid
    plot_rs --date 2022041912 --params temp --params dewp_temp --params wind_vel --params wind_dir

    """
    # Preparations:

    # get station dataframe
    if loc in ["pay", "inn"]:
        print(f"--- Specified station: {loc}.")
        station = sdf[loc]
    else:
        print(f"{station} not yet defined!")
        sys.exit(1)

    # define lower altitude if None is specified by user
    if not alt_bot:
        alt_bot = station.elevation

    df = get_rs(
        date=date,
        params=params,
        clouds=clouds,
        station=station,
        print_steps=print_steps,
        alt_bot=alt_bot,
        alt_top=alt_top,
    )

    create_plot(
        df=df,
        relhum_thresh=relhum_thresh,
        grid=grid,
        clouds=clouds,
        outpath=outpath,
        station=station,
        date=date,
        alt_top=alt_top,
        alt_bot=alt_bot,
        params=params,
        print_steps=print_steps,
        standard_settings=standard_settings,
        personal_settings=personal_settings,
        temp_min=temp_min,
        temp_max=temp_max,
        windvel_min=windvel_min,
        windvel_max=windvel_max,
        pot_temp_min=pot_temp_min,
        pot_temp_max=pot_temp_max,
    )

    print("--- Done.")
