"""Purpose: define command line inputs.

Author: Michel Zeller

Date: 05/10/2021.
"""
# Local
from .functions import *


@click.command()
@click.option("--station_id", default="06610", help="station ID: XXXXX - def: 00610")
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
    help="altitude bottom value: int - def: 0 [m] (ground level)",
)
@click.option(
    "--alt_top",
    default=40000,
    type=int,
    help="altitude top value: int - def: 40000 [m]",
)
@click.option(
    "--params",
    type=click.Choice(
        [
            "742",
            "gph",
            "743",
            "winddir",
            "744",
            "press",
            "745",
            "temp",
            "746",
            "relhum",
            "747",
            "dewp",
            "748",
            "windvel",
        ],
        case_sensitive=False,
    ),
    multiple=True,
    default=("742", "745", "747", "744"),
    help="Default: '742','745','747', '744'",
)
@click.option(
    "--out_path",
    default="plots/",
    type=str,
    help="path to folder where the plots should be saved - def: plots/",
)
def main(
    *, station_id: str, start: str, end: str, params: tuple, alt_bot: int, alt_top: int
) -> None:

    print_steps = False
    station_type = "profile"

    start, end, params, params_tuple = reformat_inputs(
        start=start,
        end=end,
        params=params,
        station_id=station_id,
        station_type=station_type,
        print_steps=print_steps,
    )

    # create dataframes
    df = dwh2pandas(
        params=params,
        start=start,
        end=end,
        station_id=station_id,
        station_type=station_type,
        print_steps=print_steps,
    )
    params_df = extract_columns(
        params_tuple=params_tuple,
        data=df,
        print_steps=print_steps,
        alt_bot=alt_bot,
        alt_top=alt_top,
    )

    # create plots (& add further optional arguments for the plot functions as cli)
    create_plots(params_df=params_df, start=start, station_id=station_id)
