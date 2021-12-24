"""Command line interface of plot_profile."""

# Third-party
import click

# Local
from . import __version__


# pylint: disable=W0613  # unused-argument (param)
def print_version(ctx, param, value: bool) -> None:
    """Print the version number and exit."""
    if value:
        click.echo(__version__)
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
def main() -> None:
    """Plot observations and ICON variabels from NWP forecasts.

    Available entry points:

     - plot_rs: Radiosoundings

     - plot_icon_profilse: ICON profiles

     - plot_rs_icon: Compare ICON profiles to radiosoundings

     - plot_icon_heatmap: Heatmap of ICON vertical variables

     - plot_mwr_heatmap: Heatmap of microwave radiometers


    """
    pass
