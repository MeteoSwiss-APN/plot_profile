"""Purpose: Plot process diagrams.

Author: Arthur Dandoy

Date: 08/04/2022.
"""

# Standard library
import sys
from pprint import pprint

# Third-party
import click

# First-party
from plot_profile.plot_timeseries.get_timeseries import get_timeseries_dict
from plot_profile.plot_timeseries.parse_timeseries_inputs import parse_inputs
from plot_profile.plot_timeseries.plot_timeseries import create_plot

# from ipdb import set_trace


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
@click.option("--dummy", type=str, help="this is a test")
def main(*, dummy: str):
    print(f"{dummy}")
    print("This is a process diagram !")
