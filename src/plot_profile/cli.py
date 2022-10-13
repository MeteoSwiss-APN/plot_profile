"""Command line interface of plot_profile."""

# Third-party
import click

# First-party
from plot_profile.utils.stations import sdf
from plot_profile.utils.variables import vdf

# Local
from . import __version__

# from ipdb import set_trace


def print_version(ctx, param, value: bool) -> None:
    """Print the version number and exit."""
    if value:
        click.echo(__version__)
        ctx.exit(0)


def print_variables(ctx, param, value: bool) -> None:
    """Print the available variable names and exit."""
    if value:
        print("The following variables are available:")
        # loop over variables (columns)
        for var in vdf:
            print(f"{vdf[var].long_name} -> {vdf[var].short_name}")
        ctx.exit(0)


def print_stations(ctx, param, value: bool) -> None:
    """Print the available variable names and exit."""
    if value:
        print("The following stations are available:")
        # loop over stations (columns)
        for station in sdf:
            print(f"{sdf[station].long_name} -> {sdf[station].short_name}")
        ctx.exit(0)


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.option(
    "--version",
    "-V",
    help="Print version and exit.",
    is_flag=True,
    expose_value=False,
    callback=print_version,
)
@click.option(
    "--stations",
    "-S",
    help="Print available stations and exit.",
    is_flag=True,
    expose_value=False,
    callback=print_stations,
)
@click.option(
    "--variables",
    "-N",
    help="Print available variable names and exit.",
    is_flag=True,
    expose_value=False,
    callback=print_variables,
)
def main() -> None:
    """Plot observations and ICON variabels from NWP forecasts.

    Available entry points:

     - plot_rs: Radiosoundings

     - plot_profiles: Vertical profiles from ICON and observations for 1 specific time.

     - plot_icon_profiles: Vertical profiles from ICON only for multiple leadtimes.

     - plot_timeseries: Timeseries  from ICON and observations from start to end.

     - plot_icon_heatmap: Heatmap of ICON vertical variables

     - plot_mwr_heatmap: Heatmap of microwave radiometers


    """
    pass
