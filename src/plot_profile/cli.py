"""Purpose: define command line inputs.

Author: Michel Zeller

Date: 05/10/2021.
"""
# Standard library
from typing import NamedTuple

# Local
from .functions import *


@click.command()
# @click.argument("station_id") # make the station ID non-optional
@click.option("--station_id", default="06610", help="station ID: XXXXX - def: 06610")
@click.option(
    "--start", default="2021083100", help="start date: YYYYMMDDHH - def: 2021083100"
)
@click.option(
    "--end", default="2021083100", help="end date: YYYYMMDDHH - def: 2021083100"
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
            "744",
            "press",
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
    default=("743", "745", "748", "747", "744"),
    help="Default: all",
)
@click.option(
    "--out_path",
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
    help="Show clouds on plot - def: True",
)
@click.option(
    "--relhum_thresh",
    default=80,
    type=float,
    help="Define the relative humidity threshold for clouds - def: 80",
)
def main(
    *,
    station_id: str,
    start: str,
    end: str,
    params: tuple,
    alt_bot: int,
    alt_top: int,
    out_path: str,
    grid: bool,
    clouds: bool,
    relhum_thresh: float,
) -> None:
    # choose if intermediate steps should be printed (for mere debugging purposes)
    print_steps = False

    # this is the standard station_type we try to consider
    station_type = "profile"

    # station_id and parameter_id dicts
    params_dict = {
        "743": "743",
        "winddir": "743",
        "744": "744",
        "press": "744",
        "745": "745",
        "temp": "745",
        "746": "746",
        "relhum": "746",
        "747": "747",
        "dewp": "747",
        "748": "748",
        "windvel": "748",
    }
    stations_dict = {"06610": "PAYERNE"}

    start, end, params, params_tuple, station_name = reformat_inputs(
        start=start,
        end=end,
        params=params,
        station_id=station_id,
        params_dict=params_dict,
        stations_dict=stations_dict,
        print_steps=print_steps,
    )

    # create dataframes
    df = dwh2pandas(
        params=params,
        start=start,
        end=end,
        station_id=station_id,
        print_steps=print_steps,
    )

    station_height = df["elev"].iloc[0]
    if station_height > alt_bot:
        alt_bot = station_height

    if alt_top == 40000:
        alt_top = df["742"].max() * 1.05

    params_df = extract_columns(
        params_tuple=params_tuple,
        data=df,
        print_steps=print_steps,
        alt_bot=alt_bot,
        alt_top=alt_top,
    )

    # # saving the dataframe as csv
    # params_df.to_csv('params_df.csv')
    # df.to_csv('df.csv')

    create_plot(
        df=params_df,
        relhum_thresh=relhum_thresh,
        grid=grid,
        clouds=clouds,
        outpath=out_path,
        station_name=station_name,
        start=start,
        alt_top=alt_top,
        alt_bot=alt_bot,
        params=params,
    )
